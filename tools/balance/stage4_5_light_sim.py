#!/usr/bin/env python3
"""Lightweight Stage 4 and Stage 5 desert benchmarks for Tower RNG.

The model reuses the Stage 6 desert combat grammar and validates six
representative formations instead of exhaustively enumerating all role-count
combinations. It must be promoted to full validation if the acceptance checks
fail or a new monster behavior is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.02
MAX_SIMULATION_SECONDS = 120.0
BOSS_REWARD_MODIFIER = 1.15

TOWER_IDS = (
    "archer",
    "slinger",
    "frost",
    "rogue",
    "drummer",
    "hunter",
)

FIVE_SLOT_LINEUPS: dict[str, tuple[str, ...]] = {
    "balanced": ("archer", "slinger", "frost", "drummer", "hunter"),
    "aoe_missing": ("archer", "archer", "frost", "drummer", "hunter"),
    "single_missing": ("slinger", "slinger", "frost", "rogue", "drummer"),
    "control_missing": ("archer", "slinger", "rogue", "drummer", "hunter"),
    "support_missing": ("archer", "slinger", "frost", "rogue", "hunter"),
    "boss_missing": ("archer", "slinger", "frost", "rogue", "drummer"),
}

SIX_SLOT_LINEUPS: dict[str, tuple[str, ...]] = {
    "balanced": TOWER_IDS,
    "aoe_missing": ("archer", "archer", "frost", "rogue", "drummer", "hunter"),
    "single_missing": ("slinger", "slinger", "frost", "rogue", "drummer", "hunter"),
    "control_missing": ("archer", "archer", "slinger", "rogue", "drummer", "hunter"),
    "support_missing": ("archer", "archer", "slinger", "frost", "rogue", "hunter"),
    "boss_missing": ("archer", "archer", "slinger", "frost", "rogue", "drummer"),
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
    phase_triggered: bool = False


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
    entry_lineups: dict[str, tuple[str, ...]]
    farm_lineups: dict[str, tuple[str, ...]]
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
    if monster.shield > 0.0:
        absorbed = min(monster.shield, damage)
        monster.shield -= absorbed
        damage -= absorbed
    monster.hp -= damage

    if (
        not monster.phase_triggered
        and monster.spec.phase_shield_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * 0.60
    ):
        monster.phase_triggered = True
        monster.shield += monster.spec.hp * monster.spec.phase_shield_fraction


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
            monsters.append(
                MonsterState(
                    uid=next_uid,
                    spec=spawn.spec,
                    hp=spawn.spec.hp,
                    shield=spawn.spec.hp * spawn.spec.shield_fraction,
                )
            )
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
                target.slow_until = max(target.slow_until, current_time + 1.25)

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
                deal_damage(choose_front(active), 0.55 * account_multiplier)

            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                deal_damage(target, damage)

            tower.next_attack += interval

            for monster in active:
                if monster.alive and monster.hp <= 1e-9:
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
            if current_time < monster.slow_until:
                speed_multiplier -= monster.slow_fraction
            else:
                monster.slow_fraction = 0.0

            monster.progress += (
                TICK_SECONDS / monster.spec.time_to_base * speed_multiplier
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
        f"Wave {wave_number} did not resolve within {MAX_SIMULATION_SECONDS}s"
    )


def make_stage_4() -> StageDefinition:
    scale = 10 ** ((4 - 1) / 3)
    scarab = MonsterSpec(
        "MON_DUST_SCARAB",
        0.75 * scale,
        14.0,
        5,
        1,
        frozenset({"swarm", "fast"}),
    )
    jackal = MonsterSpec(
        "MON_DUNE_JACKAL",
        2.60 * scale,
        19.0,
        10,
        1,
        frozenset({"fast"}),
    )
    sentinel = MonsterSpec(
        "MON_SANDSTONE_SENTINEL",
        5.20 * scale,
        27.0,
        30,
        3,
        frozenset({"armored", "thick"}),
        shield_fraction=0.10,
    )
    boss = MonsterSpec(
        "BOSS_DUNE_JACKAL_ALPHA",
        14.00 * scale,
        38.0,
        100,
        8,
        frozenset({"boss", "elite", "large"}),
        shield_fraction=0.05,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )

    waves = {
        1: [SpawnEntry(index * 0.45, scarab) for index in range(12)],
        2: [SpawnEntry(index * 0.75, jackal) for index in range(6)],
        3: [
            SpawnEntry(0.00, sentinel),
            SpawnEntry(0.90, scarab),
            SpawnEntry(1.80, jackal),
            SpawnEntry(2.70, scarab),
            SpawnEntry(3.60, jackal),
            SpawnEntry(4.50, scarab),
        ],
        4: [
            SpawnEntry(0.00, sentinel),
            SpawnEntry(1.00, sentinel),
            SpawnEntry(2.00, jackal),
        ],
        5: [SpawnEntry(0.00, boss)]
        + [SpawnEntry(1.50 + index * 1.50, scarab) for index in range(6)],
    }

    return StageDefinition(
        stage=4,
        planned_cycle_seconds=62.0,
        entry_lineups=FIVE_SLOT_LINEUPS,
        farm_lineups=SIX_SLOT_LINEUPS,
        entry_multiplier=1.95,
        farm_multiplier=1.95,
        waves=waves,
    )


def make_stage_5() -> StageDefinition:
    scale = 10 ** ((5 - 1) / 3)
    scarab = MonsterSpec(
        "MON_DUST_SCARAB",
        0.85 * scale,
        14.5,
        5,
        1,
        frozenset({"swarm", "fast"}),
    )
    jackal = MonsterSpec(
        "MON_DUNE_JACKAL",
        2.90 * scale,
        19.5,
        10,
        1,
        frozenset({"fast"}),
    )
    sentinel = MonsterSpec(
        "MON_SANDSTONE_SENTINEL",
        6.00 * scale,
        27.5,
        30,
        3,
        frozenset({"armored", "thick"}),
        shield_fraction=0.15,
    )
    boss = MonsterSpec(
        "BOSS_SANDSTONE_BEHEMOTH",
        17.50 * scale,
        44.0,
        100,
        9,
        frozenset({"boss", "elite", "large", "armored"}),
        shield_fraction=0.12,
        phase_shield_fraction=0.10,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )

    waves = {
        1: [SpawnEntry(index * 0.48, scarab) for index in range(12)],
        2: [SpawnEntry(index * 0.80, jackal) for index in range(6)],
        3: [
            SpawnEntry(0.00, sentinel),
            SpawnEntry(0.90, scarab),
            SpawnEntry(1.80, jackal),
            SpawnEntry(2.70, scarab),
            SpawnEntry(3.60, jackal),
            SpawnEntry(4.50, scarab),
        ],
        4: [
            SpawnEntry(0.00, sentinel),
            SpawnEntry(1.00, sentinel),
            SpawnEntry(2.00, jackal),
            SpawnEntry(3.00, scarab),
        ],
        5: [SpawnEntry(0.00, boss)]
        + [SpawnEntry(1.50 + index * 1.50, scarab) for index in range(5)],
    }

    return StageDefinition(
        stage=5,
        planned_cycle_seconds=68.0,
        entry_lineups=SIX_SLOT_LINEUPS,
        farm_lineups=SIX_SLOT_LINEUPS,
        entry_multiplier=4.00,
        farm_multiplier=4.65,
        waves=waves,
    )


def wave_budget(stage: StageDefinition, wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in stage.waves[wave_number])


def wave_reward_units(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in stage.waves[wave_number]
    )


def wave_effective_hp(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        entry.spec.hp
        * (1.0 + entry.spec.shield_fraction + entry.spec.phase_shield_fraction)
        for entry in stage.waves[wave_number]
    )


def profile_results(
    stage: StageDefinition,
    lineups: dict[str, tuple[str, ...]],
    multiplier: float,
):
    rows: dict[int, dict[str, SimulationResult]] = {}
    for wave_number in range(1, 6):
        rows[wave_number] = {
            name: simulate(lineup, stage.waves, wave_number, multiplier)
            for name, lineup in lineups.items()
        }

    cycles = {
        name: sum(rows[wave][name].clear_time for wave in range(1, 6))
        for name in lineups
    }
    return rows, cycles


def validate_stage(stage: StageDefinition) -> None:
    expected_budgets = {
        4: [60, 60, 65, 70, 130],
        5: [60, 60, 65, 75, 125],
    }[stage.stage]
    assert [wave_budget(stage, wave) for wave in range(1, 6)] == expected_budgets
    assert abs(
        sum(wave_reward_units(stage, wave) for wave in range(1, 6)) - 400.0
    ) < 1e-9

    entry_rows, entry_cycles = profile_results(
        stage, stage.entry_lineups, stage.entry_multiplier
    )
    farm_rows, farm_cycles = profile_results(
        stage, stage.farm_lineups, stage.farm_multiplier
    )

    assert all(
        result.leaks == 0
        for rows in (entry_rows, farm_rows)
        for wave in rows.values()
        for result in wave.values()
    )

    farm_average = mean(farm_cycles.values())
    difference = abs(farm_average - stage.planned_cycle_seconds) / stage.planned_cycle_seconds
    assert difference <= 0.05

    balanced_cycle = farm_cycles["balanced"]
    assert max(farm_cycles.values()) <= balanced_cycle * 1.25

    boss_average = mean(farm_rows[5][name].clear_time for name in stage.farm_lineups)
    boss_share = boss_average / farm_average
    assert 0.24 <= boss_share <= 0.34

    if stage.stage == 4:
        assert 70.0 <= mean(entry_cycles.values()) <= 82.0
        assert 59.0 <= farm_average <= 65.0
        assert max(farm_cycles.values()) <= 68.0
    else:
        assert 74.0 <= mean(entry_cycles.values()) <= 82.0
        assert 65.0 <= farm_average <= 71.0
        assert max(farm_cycles.values()) <= 74.0


def print_profile(
    stage: StageDefinition,
    name: str,
    lineups: dict[str, tuple[str, ...]],
    multiplier: float,
) -> None:
    rows, cycles = profile_results(stage, lineups, multiplier)
    print(
        f"{name}: slots={len(next(iter(lineups.values())))} "
        f"multiplier=x{multiplier:.2f} profiles={len(lineups)}"
    )
    for wave_number in range(1, 6):
        results = list(rows[wave_number].values())
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(stage, wave_number):>3} "
            f"reward={wave_reward_units(stage, wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(stage, wave_number):>8.2f} "
            f"avg={mean(times):>5.2f}s median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(rows[5][name].clear_time for name in lineups)
    print(
        f"  Cycle: avg={mean(cycles.values()):.2f}s "
        f"median={median(cycles.values()):.2f}s "
        f"best={min(cycles.values()):.2f}s "
        f"worst={max(cycles.values()):.2f}s "
        f"boss_share={boss_average / mean(cycles.values()) * 100:.1f}%"
    )
    for profile_name, cycle in cycles.items():
        print(f"    {profile_name:16} {cycle:6.2f}s")


def main() -> None:
    stages = (make_stage_4(), make_stage_5())
    for stage in stages:
        validate_stage(stage)
        print(f"Stage {stage.stage} lightweight desert benchmark")
        print(f"StageScale: {stage.stage_scale:.8f}")
        print(f"StageRewardScale: {stage.reward_scale:.8f}")
        print_profile(
            stage,
            "ENTRY",
            stage.entry_lineups,
            stage.entry_multiplier,
        )
        print_profile(
            stage,
            "FARM",
            stage.farm_lineups,
            stage.farm_multiplier,
        )
        farm_cycles = profile_results(
            stage, stage.farm_lineups, stage.farm_multiplier
        )[1]
        xp_per_minute = (
            400.0 * stage.reward_scale / mean(farm_cycles.values()) * 60.0
        )
        difference_percent = (
            (mean(farm_cycles.values()) - stage.planned_cycle_seconds)
            / stage.planned_cycle_seconds
            * 100.0
        )
        print(f"Farm Defense XP per minute: {xp_per_minute:.2f}")
        print(f"Planned cycle difference: {difference_percent:+.2f}%")
        print()

    print("All Stage 4 and Stage 5 lightweight assertions passed.")


if __name__ == "__main__":
    main()
