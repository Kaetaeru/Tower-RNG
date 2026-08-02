#!/usr/bin/env python3
"""Lightweight Stage 13 and 14 lava-region benchmarks for Tower RNG."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Optional

TICK = 0.05
MAX_SECONDS = 180.0
BOSS_REWARD = 1.15

LINEUPS_10 = {
    "balanced": ("archer", "archer", "slinger", "slinger", "frost", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "aoe_missing": ("archer", "archer", "archer", "frost", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "single_missing": ("slinger", "slinger", "slinger", "frost", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "control_missing": ("archer", "archer", "slinger", "slinger", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "support_missing": ("archer", "archer", "slinger", "slinger", "frost", "frost", "rogue", "rogue", "hunter", "hunter"),
    "boss_missing": ("archer", "archer", "archer", "slinger", "slinger", "frost", "frost", "rogue", "drummer", "drummer"),
}

LINEUPS_11 = {
    "balanced": ("archer", "archer", "slinger", "slinger", "frost", "frost", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "aoe_missing": ("archer", "archer", "archer", "archer", "frost", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "single_missing": ("slinger", "slinger", "slinger", "frost", "frost", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "control_missing": ("archer", "archer", "archer", "slinger", "slinger", "rogue", "rogue", "drummer", "drummer", "hunter", "hunter"),
    "support_missing": ("archer", "archer", "archer", "slinger", "slinger", "frost", "frost", "rogue", "rogue", "hunter", "hunter"),
    "boss_missing": ("archer", "archer", "archer", "slinger", "slinger", "slinger", "frost", "frost", "rogue", "drummer", "drummer"),
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
    phase_shield_at_fraction: float = 0.0
    phase_shield_fraction: float = 0.0
    frenzy_at_fraction: float = 0.0
    frenzy_speed_multiplier: float = 1.0
    death_remnant_count: int = 0
    death_remnant: Optional["MonsterSpec"] = None
    shell_break_delay: float = 0.0
    exposed_at_fraction: float = 0.0
    exposed_damage_taken_multiplier: float = 1.0
    exposed_speed_multiplier: float = 1.0
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
    alive: bool = True
    leaked: bool = False
    slow_until: float = 0.0
    slow_fraction: float = 0.0
    phase_shield_triggered: bool = False
    frenzy_triggered: bool = False
    shell_broken: bool = False
    shell_delay_pending: bool = False
    exposed: bool = False
    remnant_triggered: bool = False


@dataclass
class TowerState:
    tower_id: str
    next_attack: float
    current_target: Optional[int] = None


@dataclass(frozen=True)
class StageDefinition:
    stage: int
    planned_cycle_seconds: float
    entry_multiplier: float
    farm_multiplier: float
    entry_lineups: dict[str, tuple[str, ...]]
    farm_lineups: dict[str, tuple[str, ...]]
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
    return min(monsters, key=lambda monster: (monster.hp / max(monster.spec.hp, 1e-9), -monster.progress, monster.uid))


def choose_high_hp(monsters: list[MonsterState]) -> MonsterState:
    return max(monsters, key=lambda monster: (monster.spec.hp + monster.shield, monster.progress, -monster.uid))


def choose_splash_group(monsters: list[MonsterState]) -> list[MonsterState]:
    best_group: list[MonsterState] = []
    for center in monsters:
        group = sorted(
            (monster for monster in monsters if abs(monster.progress - center.progress) <= 0.075),
            key=lambda monster: abs(monster.progress - center.progress),
        )[:3]
        if len(group) > len(best_group):
            best_group = group
    return best_group


def create_monster(uid: int, spec: MonsterSpec, progress: float = 0.0) -> MonsterState:
    return MonsterState(uid, spec, spec.hp, spec.hp * spec.shield_fraction, progress)


def deal_damage(monster: MonsterState, damage: float) -> None:
    if monster.exposed:
        damage *= monster.spec.exposed_damage_taken_multiplier

    shield_before = monster.shield
    absorbed = min(monster.shield, damage)
    monster.shield -= absorbed
    damage -= absorbed

    if shield_before > 0.0 and monster.shield <= 1e-9 and not monster.shell_broken:
        monster.shell_broken = True
        if monster.spec.shell_break_delay > 0.0:
            monster.shell_delay_pending = True

    monster.hp -= damage

    if (
        not monster.phase_shield_triggered
        and monster.spec.phase_shield_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.phase_shield_at_fraction
    ):
        monster.phase_shield_triggered = True
        monster.shield += monster.spec.hp * monster.spec.phase_shield_fraction

    if (
        not monster.frenzy_triggered
        and monster.spec.frenzy_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.frenzy_at_fraction
    ):
        monster.frenzy_triggered = True

    if (
        not monster.exposed
        and monster.spec.exposed_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.exposed_at_fraction
    ):
        monster.exposed = True


def simulate(lineup: tuple[str, ...], waves: dict[int, list[SpawnEntry]], wave_number: int, account_multiplier: float) -> tuple[float, int]:
    has_drummer = "drummer" in lineup
    ally_multiplier = 1.15 if has_drummer else 1.0
    towers = [
        TowerState(tower_id, {"rogue": 0.75, "hunter": 0.50}.get(tower_id, 0.25))
        for tower_id in lineup
    ]
    pending = list(waves[wave_number])
    monsters: list[MonsterState] = []
    next_uid = 0
    current_time = 0.0
    leaks = 0

    while current_time < MAX_SECONDS:
        while pending and pending[0].spawn_time <= current_time + 1e-9:
            spawn = pending.pop(0)
            monsters.append(create_monster(next_uid, spawn.spec))
            next_uid += 1

        pending_delay = 0.0
        spawned: list[MonsterState] = []

        for tower in towers:
            if current_time + 1e-9 < tower.next_attack:
                continue
            active = [monster for monster in monsters if monster.alive and not monster.leaked]
            if not active:
                tower.next_attack += 0.05
                continue

            interval = 2.0 if tower.tower_id == "hunter" else 1.0
            multiplier = ally_multiplier * account_multiplier

            if tower.tower_id == "archer":
                deal_damage(choose_front(active), 1.0 * multiplier)
            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    deal_damage(target, 0.60 * multiplier)
            elif tower.tower_id == "frost":
                target = choose_front(active)
                deal_damage(target, 0.55 * multiplier)
                target.slow_fraction = max(target.slow_fraction, 0.15 * (1.15 if has_drummer else 1.0))
                target.slow_until = max(target.slow_until, current_time + 1.25)
            elif tower.tower_id == "rogue":
                target = choose_low_health(active)
                if tower.current_target is not None and tower.current_target != target.uid:
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
                if monster.shell_delay_pending:
                    pending_delay = max(pending_delay, monster.spec.shell_break_delay)
                    monster.shell_delay_pending = False

            for monster in list(active):
                if not monster.alive or monster.hp > 1e-9:
                    continue
                monster.alive = False
                if monster.spec.death_remnant is not None and not monster.remnant_triggered:
                    monster.remnant_triggered = True
                    for _ in range(monster.spec.death_remnant_count):
                        spawned.append(create_monster(next_uid, monster.spec.death_remnant, monster.progress))
                        next_uid += 1
                for rogue in towers:
                    if rogue.tower_id == "rogue" and rogue.current_target == monster.uid:
                        rogue.current_target = None

            monsters.extend(spawned)
            spawned.clear()

            if pending_delay > 0.0:
                for other_tower in towers:
                    other_tower.next_attack = max(other_tower.next_attack, current_time + pending_delay)
                pending_delay = 0.0

        for monster in monsters:
            if not monster.alive or monster.leaked:
                continue
            speed_multiplier = 1.0
            if monster.frenzy_triggered:
                speed_multiplier *= monster.spec.frenzy_speed_multiplier
            if monster.exposed:
                speed_multiplier *= monster.spec.exposed_speed_multiplier
            if current_time < monster.slow_until:
                speed_multiplier *= 1.0 - monster.slow_fraction
            else:
                monster.slow_fraction = 0.0
            monster.progress += TICK / monster.spec.time_to_base * speed_multiplier
            if monster.progress >= 1.0:
                monster.leaked = True
                leaks += 1

        if not pending and all(not monster.alive or monster.leaked for monster in monsters):
            return current_time, leaks
        current_time += TICK

    raise RuntimeError(f"Wave {wave_number} did not resolve")


def make_stage(stage: int, planned: float, entry_multiplier: float, farm_multiplier: float) -> StageDefinition:
    scale = 10 ** ((stage - 1) / 3)
    ember = MonsterSpec("MON_LAVA_EMBER", 0.12 * scale, 13.0, 0, 1, frozenset({"swarm", "remnant"}), reward_modifier=0.0)
    cinderling = MonsterSpec("MON_CINDERLING", 0.60 * scale, 17.0, 5, 1, frozenset({"swarm"}), death_remnant_count=1, death_remnant=ember)
    hound = MonsterSpec("MON_LAVA_HOUND", 3.80 * scale, 24.0, 15, 2, frozenset({"fast"}), frenzy_at_fraction=0.45, frenzy_speed_multiplier=1.30)

    if stage == 13:
        guard = MonsterSpec("MON_MAGMA_GUARD", 10.80 * scale, 42.0, 50, 5, frozenset({"thick", "armored"}), shield_fraction=0.16)
        boss = MonsterSpec("BOSS_LAVA_PACK_ALPHA", 18.0 * scale, 70.0, 100, 14, frozenset({"boss", "elite", "large"}), shield_fraction=0.08, frenzy_at_fraction=0.40, frenzy_speed_multiplier=1.18, reward_modifier=BOSS_REWARD)
        waves = {
            1: [SpawnEntry(index * 0.55, cinderling) for index in range(12)],
            2: [SpawnEntry(index * 1.50, hound) for index in range(4)],
            3: [SpawnEntry(0.0, guard)] + [SpawnEntry(1.5 + index * 1.5, cinderling) for index in range(4)],
            4: [SpawnEntry(0.0, guard), SpawnEntry(2.5, hound), SpawnEntry(5.0, cinderling), SpawnEntry(7.5, cinderling)],
            5: [SpawnEntry(0.0, boss)] + [SpawnEntry(2.0 + index * 2.0, cinderling) for index in range(4)],
        }
        return StageDefinition(stage, planned, entry_multiplier, farm_multiplier, LINEUPS_10, LINEUPS_10, waves)

    guard = MonsterSpec("MON_MAGMA_GUARD", 11.30 * scale, 42.0, 50, 5, frozenset({"thick", "armored"}), shield_fraction=0.20, shell_break_delay=0.25)
    colossus = MonsterSpec("MON_OBSIDIAN_COLOSSUS", 11.60 * scale, 52.0, 75, 8, frozenset({"elite", "thick", "large"}), shield_fraction=0.15, exposed_at_fraction=0.50, exposed_damage_taken_multiplier=1.12, exposed_speed_multiplier=1.15)
    boss = MonsterSpec("BOSS_OBSIDIAN_TITAN", 19.50 * scale, 74.0, 100, 16, frozenset({"boss", "elite", "large", "armored"}), shield_fraction=0.10, phase_shield_at_fraction=0.58, phase_shield_fraction=0.10, shell_break_delay=0.30, exposed_at_fraction=0.45, exposed_damage_taken_multiplier=1.10, exposed_speed_multiplier=1.12, reward_modifier=BOSS_REWARD)
    waves = {
        1: [SpawnEntry(index * 0.55, cinderling) for index in range(12)],
        2: [SpawnEntry(index * 1.50, hound) for index in range(4)],
        3: [SpawnEntry(0.0, guard)] + [SpawnEntry(1.5 + index * 1.5, cinderling) for index in range(4)],
        4: [SpawnEntry(0.0, colossus)],
        5: [SpawnEntry(0.0, boss)] + [SpawnEntry(2.0 + index * 2.0, cinderling) for index in range(4)],
    }
    return StageDefinition(stage, planned, entry_multiplier, farm_multiplier, LINEUPS_10, LINEUPS_11, waves)


def profile(stage: StageDefinition, lineups: dict[str, tuple[str, ...]], multiplier: float):
    rows = {
        wave: {name: simulate(lineup, stage.waves, wave, multiplier) for name, lineup in lineups.items()}
        for wave in range(1, 6)
    }
    cycles = {name: sum(rows[wave][name][0] for wave in range(1, 6)) for name in lineups}
    return rows, cycles


def effective_hp(spec: MonsterSpec) -> float:
    total = spec.hp * (1.0 + spec.shield_fraction + spec.phase_shield_fraction)
    if spec.death_remnant is not None:
        total += spec.death_remnant_count * effective_hp(spec.death_remnant)
    return total


def wave_effective_hp(stage: StageDefinition, wave: int) -> float:
    return sum(effective_hp(entry.spec) for entry in stage.waves[wave])


def validate_stage(stage: StageDefinition) -> None:
    entry_rows, _ = profile(stage, stage.entry_lineups, stage.entry_multiplier)
    farm_rows, farm_cycles = profile(stage, stage.farm_lineups, stage.farm_multiplier)
    assert all(result[1] == 0 for rows in entry_rows.values() for result in rows.values())
    assert all(result[1] == 0 for rows in farm_rows.values() for result in rows.values())
    farm_average = mean(farm_cycles.values())
    assert abs(farm_average - stage.planned_cycle_seconds) / stage.planned_cycle_seconds <= 0.05
    assert max(farm_cycles.values()) <= stage.planned_cycle_seconds * 1.20
    assert max(farm_cycles.values()) / farm_cycles["balanced"] <= 1.25
    boss_average = mean(result[0] for result in farm_rows[5].values())
    assert 0.25 <= boss_average / farm_average <= 0.35
    reward_units = sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for wave in range(1, 6)
        for entry in stage.waves[wave]
    )
    assert abs(reward_units - 400.0) < 1e-9


def print_stage(stage: StageDefinition) -> None:
    validate_stage(stage)
    print(f"Stage {stage.stage} lightweight lava benchmark")
    print(f"StageScale={stage.stage_scale:,.8f}, RewardScale={stage.reward_scale:,.8f}")
    for label, lineups, multiplier in (
        ("entry", stage.entry_lineups, stage.entry_multiplier),
        ("farm", stage.farm_lineups, stage.farm_multiplier),
    ):
        rows, cycles = profile(stage, lineups, multiplier)
        print(f"{label}: multiplier=x{multiplier:,.2f}, lineups={len(lineups)}")
        for wave in range(1, 6):
            times = [result[0] for result in rows[wave].values()]
            leaks = sum(result[1] for result in rows[wave].values())
            budget = sum(entry.spec.spawn_cost for entry in stage.waves[wave])
            reward = sum(entry.spec.spawn_cost * entry.spec.reward_modifier for entry in stage.waves[wave])
            print(
                f"  W{wave}: budget={budget}, reward={reward:.1f}, "
                f"effective_hp={wave_effective_hp(stage, wave):,.2f}, "
                f"avg={mean(times):.2f}s, best={min(times):.2f}s, "
                f"worst={max(times):.2f}s, leaks={leaks}"
            )
        boss_average = mean(result[0] for result in rows[5].values())
        print(
            f"  cycle: avg={mean(cycles.values()):.2f}s, "
            f"median={median(cycles.values()):.2f}s, "
            f"best={min(cycles.values()):.2f}s, "
            f"worst={max(cycles.values()):.2f}s, "
            f"boss_share={boss_average / mean(cycles.values()) * 100:.1f}%"
        )
        print(f"  lineup cycles={cycles}")


def main() -> None:
    stages = (
        make_stage(13, 86.0, 850.0, 975.0),
        make_stage(14, 93.0, 1450.0, 1740.0),
    )
    for stage in stages:
        print_stage(stage)
    print("All Stage 13-14 lightweight benchmark assertions passed.")


if __name__ == "__main__":
    main()
