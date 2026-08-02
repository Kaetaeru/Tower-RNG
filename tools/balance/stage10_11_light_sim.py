#!/usr/bin/env python3
"""Lightweight Stage 10 and Stage 11 snow-region benchmarks for Tower RNG.

The benchmark reuses the Stage 12 snow combat grammar and checks six
representative nine-slot formations instead of exhaustively enumerating all
role-count combinations. It must be promoted to full validation if an
acceptance check fails or a new monster behavior is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.02
MAX_SIMULATION_SECONDS = 180.0
BOSS_REWARD_MODIFIER = 1.15

LINEUPS: dict[str, tuple[str, ...]] = {
    "balanced": (
        "archer", "archer", "slinger", "slinger", "frost",
        "rogue", "drummer", "hunter", "hunter",
    ),
    "aoe_missing": (
        "archer", "archer", "archer", "frost", "rogue",
        "drummer", "hunter", "hunter", "hunter",
    ),
    "single_missing": (
        "slinger", "slinger", "slinger", "frost", "rogue",
        "rogue", "drummer", "hunter", "hunter",
    ),
    "control_missing": (
        "archer", "archer", "slinger", "slinger", "rogue",
        "rogue", "drummer", "hunter", "hunter",
    ),
    "support_missing": (
        "archer", "archer", "slinger", "slinger", "frost",
        "rogue", "rogue", "hunter", "hunter",
    ),
    "boss_missing": (
        "archer", "archer", "archer", "slinger", "slinger",
        "frost", "rogue", "rogue", "drummer",
    ),
}


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
    tags: frozenset[str] = frozenset()
    shield_fraction: float = 0.0
    phase_shield_fraction: float = 0.0
    phase_shield_at_fraction: float = 0.0
    frenzy_at_fraction: float = 0.0
    frenzy_speed_multiplier: float = 1.0
    shell_speed_while_shielded: float = 1.0
    shell_speed_after_break: float = 1.0
    freeze_at_fraction: float = 0.0
    freeze_duration: float = 0.0
    freeze_progress: float = 0.0
    reward_modifier: float = 1.0


@dataclass(frozen=True)
class SpawnEntry:
    spawn_time: float
    spec: MonsterSpec


@dataclass
class MonsterState:
    uid: int
    spec: MonsterSpec
    hp: float
    shield: float
    progress: float = 0.0
    slow_until: float = 0.0
    slow_fraction: float = 0.0
    alive: bool = True
    leaked: bool = False
    phase_shield_triggered: bool = False
    frenzy_triggered: bool = False
    shell_broken: bool = False
    freeze_triggered: bool = False
    freeze_pending: bool = False


@dataclass
class TowerState:
    tower_id: str
    next_attack: float
    current_target: Optional[int] = None


@dataclass(frozen=True)
class SimulationResult:
    clear_time: float
    leaks: int
    base_damage: int


@dataclass(frozen=True)
class StageDefinition:
    stage: int
    planned_cycle_seconds: float
    entry_multiplier: float
    farm_multiplier: float
    waves: dict[int, list[SpawnEntry]]

    @property
    def stage_scale(self) -> float:
        return 10 ** ((self.stage - 1) / 3)

    @property
    def reward_scale(self) -> float:
        return self.stage_scale * (1.08 ** (self.stage - 1))


def choose_front(monsters: list[MonsterState]) -> MonsterState:
    return max(monsters, key=lambda monster: (monster.progress, -monster.uid))


def choose_low_health(monsters: list[MonsterState]) -> MonsterState:
    return min(
        monsters,
        key=lambda monster: (
            monster.hp / max(monster.spec.hp, 1e-9),
            -monster.progress,
            monster.uid,
        ),
    )


def choose_high_hp(monsters: list[MonsterState]) -> MonsterState:
    return max(
        monsters,
        key=lambda monster: (
            monster.spec.hp + monster.shield,
            monster.progress,
            -monster.uid,
        ),
    )


def choose_splash_group(monsters: list[MonsterState]) -> list[MonsterState]:
    best_group: list[MonsterState] = []
    for center in monsters:
        group = sorted(
            (
                monster
                for monster in monsters
                if abs(monster.progress - center.progress) <= 0.075
            ),
            key=lambda monster: abs(monster.progress - center.progress),
        )[:3]
        if len(group) > len(best_group):
            best_group = group
    return best_group


def deal_damage(monster: MonsterState, damage: float) -> None:
    shield_before = monster.shield
    if monster.shield > 0.0:
        absorbed = min(monster.shield, damage)
        monster.shield -= absorbed
        damage -= absorbed
    if shield_before > 0.0 and monster.shield <= 1e-9:
        monster.shell_broken = True

    monster.hp -= damage

    if (
        not monster.phase_shield_triggered
        and monster.spec.phase_shield_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.phase_shield_at_fraction
    ):
        monster.phase_shield_triggered = True
        monster.shield += monster.spec.hp * monster.spec.phase_shield_fraction
        monster.shell_broken = False

    if (
        not monster.frenzy_triggered
        and monster.spec.frenzy_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.frenzy_at_fraction
    ):
        monster.frenzy_triggered = True

    if (
        not monster.freeze_triggered
        and monster.spec.freeze_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.freeze_at_fraction
    ):
        monster.freeze_triggered = True
        monster.freeze_pending = True
        monster.progress = min(
            0.98,
            monster.progress + monster.spec.freeze_progress,
        )


def create_monster(uid: int, spec: MonsterSpec) -> MonsterState:
    return MonsterState(
        uid=uid,
        spec=spec,
        hp=spec.hp,
        shield=spec.hp * spec.shield_fraction,
    )


def simulate(
    lineup: tuple[str, ...],
    waves: dict[int, list[SpawnEntry]],
    wave_number: int,
    account_multiplier: float,
) -> SimulationResult:
    has_drummer = "drummer" in lineup
    ally_output_multiplier = 1.15 if has_drummer else 1.0

    towers = [
        TowerState(
            tower_id,
            {"rogue": 0.75, "hunter": 0.50}.get(tower_id, 0.25),
        )
        for tower_id in lineup
    ]
    pending = list(waves[wave_number])
    monsters: list[MonsterState] = []
    next_uid = 0
    current_time = 0.0
    leaks = 0
    base_damage = 0

    while current_time < MAX_SIMULATION_SECONDS:
        while pending and pending[0].spawn_time <= current_time + 1e-9:
            spawn = pending.pop(0)
            monsters.append(create_monster(next_uid, spawn.spec))
            next_uid += 1

        for tower in towers:
            if current_time + 1e-9 < tower.next_attack:
                continue

            active = [
                monster
                for monster in monsters
                if monster.alive and not monster.leaked
            ]
            if not active:
                tower.next_attack += 0.05
                continue

            interval = 2.0 if tower.tower_id == "hunter" else 1.0
            multiplier = ally_output_multiplier * account_multiplier

            if tower.tower_id == "archer":
                deal_damage(choose_front(active), 1.0 * multiplier)
            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    deal_damage(target, 0.60 * multiplier)
            elif tower.tower_id == "frost":
                target = choose_front(active)
                deal_damage(target, 0.55 * multiplier)
                slow_fraction = 0.15 * (1.15 if has_drummer else 1.0)
                target.slow_fraction = max(target.slow_fraction, slow_fraction)
                target.slow_until = max(
                    target.slow_until,
                    current_time + 1.25,
                )
            elif tower.tower_id == "rogue":
                target = choose_low_health(active)
                if (
                    tower.current_target is not None
                    and tower.current_target != target.uid
                ):
                    tower.current_target = target.uid
                    tower.next_attack = current_time + 0.25
                    continue
                tower.current_target = target.uid
                damage = 0.80 * multiplier
                if target.hp / target.spec.hp <= 0.30:
                    damage *= 2.0
                deal_damage(target, damage)
            elif tower.tower_id == "drummer":
                deal_damage(
                    choose_front(active),
                    0.55 * account_multiplier,
                )
            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                deal_damage(target, damage)

            tower.next_attack += interval

            freeze_events = [
                monster for monster in monsters if monster.freeze_pending
            ]
            if freeze_events:
                duration = max(
                    monster.spec.freeze_duration for monster in freeze_events
                )
                for monster in freeze_events:
                    monster.freeze_pending = False
                for other in towers:
                    other.next_attack = max(
                        other.next_attack,
                        current_time + duration,
                    )

            for monster in active:
                if not monster.alive or monster.hp > 1e-9:
                    continue
                monster.alive = False
                for rogue in towers:
                    if (
                        rogue.tower_id == "rogue"
                        and rogue.current_target == monster.uid
                    ):
                        rogue.current_target = None

        for monster in monsters:
            if not monster.alive or monster.leaked:
                continue

            speed_multiplier = 1.0
            if (
                monster.spec.shell_speed_while_shielded != 1.0
                or monster.spec.shell_speed_after_break != 1.0
            ):
                speed_multiplier *= (
                    monster.spec.shell_speed_while_shielded
                    if monster.shield > 1e-9
                    else monster.spec.shell_speed_after_break
                )
            if monster.frenzy_triggered:
                speed_multiplier *= monster.spec.frenzy_speed_multiplier
            if current_time < monster.slow_until:
                speed_multiplier *= 1.0 - monster.slow_fraction
            else:
                monster.slow_fraction = 0.0

            monster.progress += (
                TICK_SECONDS
                / monster.spec.time_to_base
                * speed_multiplier
            )
            if monster.progress >= 1.0:
                monster.leaked = True
                leaks += 1
                base_damage += monster.spec.base_damage

        if not pending and all(
            not monster.alive or monster.leaked for monster in monsters
        ):
            return SimulationResult(current_time, leaks, base_damage)

        current_time += TICK_SECONDS

    raise RuntimeError(
        f"Wave {wave_number} did not resolve within "
        f"{MAX_SIMULATION_SECONDS}s"
    )


def build_stage_10() -> StageDefinition:
    scale = 10 ** ((10 - 1) / 3)
    hare = MonsterSpec(
        "MON_SNOW_HARE", 0.60 * scale, 18.0, 5, 1,
        frozenset({"swarm"}),
    )
    wolf = MonsterSpec(
        "MON_FROST_WOLF", 3.20 * scale, 25.0, 10, 1,
        frozenset({"fast"}),
        frenzy_at_fraction=0.40,
        frenzy_speed_multiplier=1.25,
    )
    guardian = MonsterSpec(
        "MON_RIME_GUARDIAN", 7.20 * scale, 40.0, 30, 4,
        frozenset({"thick", "armored", "ice_shell"}),
        shield_fraction=0.25,
        shell_speed_while_shielded=0.85,
        shell_speed_after_break=1.15,
    )
    boss = MonsterSpec(
        "BOSS_FROSTFANG_ALPHA", 21.50 * scale, 66.0, 100, 12,
        frozenset({"boss", "elite", "large", "ice_shell"}),
        shield_fraction=0.08,
        shell_speed_while_shielded=0.92,
        shell_speed_after_break=1.06,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )
    waves = {
        1: [SpawnEntry(index * 0.60, hare) for index in range(12)],
        2: [SpawnEntry(index * 0.95, wolf) for index in range(6)],
        3: [
            SpawnEntry(0.00, guardian),
            SpawnEntry(1.00, hare),
            SpawnEntry(2.00, wolf),
            SpawnEntry(3.00, hare),
            SpawnEntry(4.00, wolf),
            SpawnEntry(5.00, hare),
        ],
        4: [
            SpawnEntry(0.00, guardian),
            SpawnEntry(1.20, guardian),
            SpawnEntry(2.40, wolf),
            SpawnEntry(3.60, hare),
        ],
        5: [SpawnEntry(0.00, boss)]
        + [SpawnEntry(1.80 + index * 1.60, hare) for index in range(5)],
    }
    return StageDefinition(10, 76.0, 110.0, 130.0, waves)


def build_stage_11() -> StageDefinition:
    scale = 10 ** ((11 - 1) / 3)
    hare = MonsterSpec(
        "MON_SNOW_HARE", 0.60 * scale, 18.0, 5, 1,
        frozenset({"swarm"}),
    )
    wolf = MonsterSpec(
        "MON_FROST_WOLF", 3.20 * scale, 25.0, 10, 1,
        frozenset({"fast"}),
        frenzy_at_fraction=0.40,
        frenzy_speed_multiplier=1.25,
    )
    guardian = MonsterSpec(
        "MON_RIME_GUARDIAN", 7.20 * scale, 40.0, 30, 4,
        frozenset({"thick", "armored", "ice_shell"}),
        shield_fraction=0.25,
        shell_speed_while_shielded=0.85,
        shell_speed_after_break=1.15,
    )
    boss = MonsterSpec(
        "BOSS_RIME_BEHEMOTH", 20.50 * scale, 67.0, 100, 14,
        frozenset({"boss", "elite", "large", "armored", "ice_shell"}),
        shield_fraction=0.12,
        phase_shield_at_fraction=0.60,
        phase_shield_fraction=0.10,
        shell_speed_while_shielded=0.90,
        shell_speed_after_break=1.08,
        freeze_at_fraction=0.30,
        freeze_duration=0.45,
        freeze_progress=0.02,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )
    waves = {
        1: [SpawnEntry(index * 0.60, hare) for index in range(12)],
        2: [SpawnEntry(index * 0.95, wolf) for index in range(6)],
        3: [
            SpawnEntry(0.00, guardian),
            SpawnEntry(1.00, hare),
            SpawnEntry(2.00, wolf),
            SpawnEntry(3.00, hare),
            SpawnEntry(4.00, wolf),
            SpawnEntry(5.00, hare),
        ],
        4: [
            SpawnEntry(0.00, guardian),
            SpawnEntry(1.20, guardian),
            SpawnEntry(2.40, wolf),
            SpawnEntry(3.60, hare),
        ],
        5: [SpawnEntry(0.00, boss)]
        + [SpawnEntry(1.80 + index * 1.60, hare) for index in range(5)],
    }
    return StageDefinition(11, 84.0, 230.0, 258.0, waves)


def wave_budget(stage: StageDefinition, wave_number: int) -> int:
    return sum(
        entry.spec.spawn_cost for entry in stage.waves[wave_number]
    )


def wave_reward_units(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in stage.waves[wave_number]
    )


def effective_hp(spec: MonsterSpec) -> float:
    return spec.hp * (
        1.0 + spec.shield_fraction + spec.phase_shield_fraction
    )


def wave_effective_hp(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        effective_hp(entry.spec)
        for entry in stage.waves[wave_number]
    )


def profile_results(
    stage: StageDefinition,
    account_multiplier: float,
):
    rows = {
        wave_number: {
            name: simulate(
                lineup,
                stage.waves,
                wave_number,
                account_multiplier,
            )
            for name, lineup in LINEUPS.items()
        }
        for wave_number in range(1, 6)
    }
    cycles = {
        name: sum(
            rows[wave_number][name].clear_time
            for wave_number in range(1, 6)
        )
        for name in LINEUPS
    }
    return rows, cycles


def validate_stage(stage: StageDefinition) -> None:
    assert [wave_budget(stage, wave) for wave in range(1, 6)] == [
        60, 60, 65, 75, 125,
    ]
    assert abs(
        sum(wave_reward_units(stage, wave) for wave in range(1, 6))
        - 400.0
    ) < 1e-9

    entry_rows, _ = profile_results(stage, stage.entry_multiplier)
    farm_rows, farm_cycles = profile_results(stage, stage.farm_multiplier)

    assert all(
        result.leaks == 0
        for rows in (entry_rows, farm_rows)
        for wave in rows.values()
        for result in wave.values()
    )

    farm_average = mean(farm_cycles.values())
    assert abs(farm_average - stage.planned_cycle_seconds) <= (
        stage.planned_cycle_seconds * 0.05
    )
    assert max(farm_cycles.values()) <= stage.planned_cycle_seconds * 1.20

    balanced_time = farm_cycles["balanced"]
    assert max(farm_cycles.values()) <= balanced_time * 1.25

    boss_average = mean(
        farm_rows[5][name].clear_time for name in LINEUPS
    )
    boss_share = boss_average / farm_average
    assert 0.25 <= boss_share <= 0.35


def print_profile(
    stage: StageDefinition,
    profile_name: str,
    account_multiplier: float,
) -> None:
    rows, cycles = profile_results(stage, account_multiplier)
    print(
        f"Stage {stage.stage} {profile_name}: slots=9 role_cap=3 "
        f"multiplier=x{account_multiplier:.2f} lineups={len(LINEUPS)}"
    )
    for wave_number in range(1, 6):
        results = list(rows[wave_number].values())
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(stage, wave_number):>3} "
            f"reward={wave_reward_units(stage, wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(stage, wave_number):>12.2f} "
            f"avg={mean(times):>5.2f}s median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(rows[5][name].clear_time for name in LINEUPS)
    print(
        f"  Cycle: avg={mean(cycles.values()):.2f}s "
        f"median={median(cycles.values()):.2f}s "
        f"best={min(cycles.values()):.2f}s "
        f"worst={max(cycles.values()):.2f}s "
        f"boss_share={boss_average / mean(cycles.values()) * 100:.1f}%"
    )
    for name, cycle in cycles.items():
        print(f"    {name}: {cycle:.2f}s")


def main() -> None:
    for stage in (build_stage_10(), build_stage_11()):
        validate_stage(stage)
        print(
            f"\nStage {stage.stage}: scale={stage.stage_scale:.8f} "
            f"reward_scale={stage.reward_scale:.8f} "
            f"planned={stage.planned_cycle_seconds:.2f}s"
        )
        print_profile(stage, "entry", stage.entry_multiplier)
        print_profile(stage, "farm", stage.farm_multiplier)
        _, farm_cycles = profile_results(stage, stage.farm_multiplier)
        xp_per_minute = (
            400.0 * stage.reward_scale * 60.0 / mean(farm_cycles.values())
        )
        print(f"  DefenseXP/min={xp_per_minute:.2f}")

    print("\nAll Stage 10 and Stage 11 lightweight assertions passed.")


if __name__ == "__main__":
    main()
