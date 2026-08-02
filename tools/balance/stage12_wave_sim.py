#!/usr/bin/env python3
"""Deterministic Stage 12 snow-region finale benchmark for Tower RNG."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.02
MAX_SIMULATION_SECONDS = 180.0
STAGE_SCALE = 10 ** ((12 - 1) / 3)
STAGE_REWARD_SCALE = STAGE_SCALE * (1.08 ** 11)
BOSS_REWARD_MODIFIER = 1.15

ENTRY_SLOTS = 9
ENTRY_ROLE_CAP = 3
ENTRY_MIN_ROLES = 5
ENTRY_OUTPUT_MULTIPLIER = 480.0

FARM_SLOTS = 10
FARM_ROLE_CAP = 4
FARM_MIN_ROLES = 5
FARM_OUTPUT_MULTIPLIER = 540.0


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


TOWER_IDS = (
    "archer",
    "slinger",
    "frost",
    "rogue",
    "drummer",
    "hunter",
)

SNOW_HARE = MonsterSpec(
    monster_id="MON_SNOW_HARE",
    hp=0.60 * STAGE_SCALE,
    time_to_base=18.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm"}),
)

FROST_WOLF = MonsterSpec(
    monster_id="MON_FROST_WOLF",
    hp=3.20 * STAGE_SCALE,
    time_to_base=25.0,
    spawn_cost=10,
    base_damage=1,
    tags=frozenset({"fast"}),
    frenzy_at_fraction=0.40,
    frenzy_speed_multiplier=1.25,
)

RIME_GUARDIAN = MonsterSpec(
    monster_id="MON_RIME_GUARDIAN",
    hp=7.20 * STAGE_SCALE,
    time_to_base=40.0,
    spawn_cost=30,
    base_damage=4,
    tags=frozenset({"thick", "armored", "ice_shell"}),
    shield_fraction=0.25,
    shell_speed_while_shielded=0.85,
    shell_speed_after_break=1.15,
)

GLACIER_COLOSSUS = MonsterSpec(
    monster_id="BOSS_GLACIER_COLOSSUS",
    hp=23.50 * STAGE_SCALE,
    time_to_base=68.0,
    spawn_cost=100,
    base_damage=15,
    tags=frozenset({"boss", "elite", "large", "armored", "ice_shell"}),
    shield_fraction=0.15,
    phase_shield_at_fraction=0.60,
    phase_shield_fraction=0.15,
    shell_speed_while_shielded=0.90,
    shell_speed_after_break=1.08,
    freeze_at_fraction=0.30,
    freeze_duration=0.80,
    freeze_progress=0.03,
    reward_modifier=BOSS_REWARD_MODIFIER,
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.60, SNOW_HARE) for index in range(12)],
    2: [SpawnEntry(index * 0.95, FROST_WOLF) for index in range(6)],
    3: [
        SpawnEntry(0.00, RIME_GUARDIAN),
        SpawnEntry(1.00, SNOW_HARE),
        SpawnEntry(2.00, FROST_WOLF),
        SpawnEntry(3.00, SNOW_HARE),
        SpawnEntry(4.00, FROST_WOLF),
        SpawnEntry(5.00, SNOW_HARE),
    ],
    4: [
        SpawnEntry(0.00, RIME_GUARDIAN),
        SpawnEntry(1.20, RIME_GUARDIAN),
        SpawnEntry(2.40, FROST_WOLF),
        SpawnEntry(3.60, SNOW_HARE),
    ],
    5: [SpawnEntry(0.00, GLACIER_COLOSSUS)]
    + [SpawnEntry(1.80 + index * 1.60, SNOW_HARE) for index in range(5)],
}


def formation_lineups(
    slots: int,
    role_cap: int,
    minimum_distinct_roles: int,
) -> list[tuple[str, ...]]:
    lineups: list[tuple[str, ...]] = []
    for counts in product(range(role_cap + 1), repeat=len(TOWER_IDS)):
        if sum(counts) != slots:
            continue
        if sum(count > 0 for count in counts) < minimum_distinct_roles:
            continue
        lineups.append(
            tuple(
                tower_id
                for tower_id, count in zip(TOWER_IDS, counts)
                for _ in range(count)
            )
        )
    return lineups


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
    pending = list(WAVES[wave_number])
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


def wave_budget(wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in WAVES[wave_number])


def wave_reward_units(wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in WAVES[wave_number]
    )


def effective_hp(spec: MonsterSpec) -> float:
    return spec.hp * (
        1.0 + spec.shield_fraction + spec.phase_shield_fraction
    )


def wave_effective_hp(wave_number: int) -> float:
    return sum(
        effective_hp(entry.spec) for entry in WAVES[wave_number]
    )


def profile_results(
    slots: int,
    role_cap: int,
    minimum_distinct_roles: int,
    multiplier: float,
):
    lineups = formation_lineups(
        slots,
        role_cap,
        minimum_distinct_roles,
    )
    rows = {
        wave_number: [
            (lineup, simulate(lineup, wave_number, multiplier))
            for lineup in lineups
        ]
        for wave_number in range(1, 6)
    }
    result_maps = {
        wave_number: dict(rows[wave_number]) for wave_number in rows
    }
    cycles = [
        sum(
            result_maps[wave_number][lineup].clear_time
            for wave_number in range(1, 6)
        )
        for lineup in lineups
    ]
    return lineups, rows, cycles


def validate() -> None:
    assert [wave_budget(wave) for wave in range(1, 6)] == [
        60,
        60,
        65,
        75,
        125,
    ]
    assert abs(
        sum(wave_reward_units(wave) for wave in range(1, 6)) - 400.0
    ) < 1e-9

    entry_lineups, entry_rows, entry_cycles = profile_results(
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        4,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(entry_lineups) == 560
    assert all(
        result.leaks == 0
        for wave in entry_rows.values()
        for _, result in wave
    )
    assert 108.0 <= mean(entry_cycles) <= 118.0
    assert max(entry_cycles) <= 145.0

    healthy_lineups, healthy_rows, healthy_cycles = profile_results(
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        ENTRY_MIN_ROLES,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(healthy_lineups) == 320
    assert all(
        result.leaks == 0
        for wave in healthy_rows.values()
        for _, result in wave
    )
    assert mean(healthy_cycles) <= 116.0
    assert max(healthy_cycles) <= 140.0

    farm_lineups, farm_rows, farm_cycles = profile_results(
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )
    assert len(farm_lineups) == 726
    assert all(
        result.leaks == 0
        for wave in farm_rows.values()
        for _, result in wave
    )
    normal_averages = [
        mean(result.clear_time for _, result in farm_rows[wave])
        for wave in range(1, 5)
    ]
    boss_average = mean(
        result.clear_time for _, result in farm_rows[5]
    )
    assert all(7.0 <= value <= 21.0 for value in normal_averages)
    assert 28.0 <= boss_average <= 33.0
    assert 88.0 <= mean(farm_cycles) <= 92.0
    assert max(farm_cycles) <= 115.0
    boss_share = boss_average / mean(farm_cycles)
    assert 0.31 <= boss_share <= 0.35


def print_profile(
    name: str,
    slots: int,
    role_cap: int,
    minimum_distinct_roles: int,
    multiplier: float,
) -> None:
    lineups, rows, cycles = profile_results(
        slots,
        role_cap,
        minimum_distinct_roles,
        multiplier,
    )
    print(
        f"{name}: slots={slots} role_cap={role_cap} "
        f"minimum_roles={minimum_distinct_roles} "
        f"multiplier=x{multiplier:.2f} lineups={len(lineups)}"
    )
    for wave_number in range(1, 6):
        results = [result for _, result in rows[wave_number]]
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(wave_number):>3} "
            f"reward={wave_reward_units(wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(wave_number):>10.2f} "
            f"avg={mean(times):>5.2f}s "
            f"median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s "
            f"worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(
        result.clear_time for _, result in rows[5]
    )
    print(
        f"  Cycle: avg={mean(cycles):.2f}s "
        f"median={median(cycles):.2f}s "
        f"best={min(cycles):.2f}s "
        f"worst={max(cycles):.2f}s "
        f"boss_share={boss_average / mean(cycles) * 100:.1f}%"
    )


if __name__ == "__main__":
    validate()
    print_profile(
        "entry_all",
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        4,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    print_profile(
        "entry_healthy",
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        ENTRY_MIN_ROLES,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    print_profile(
        "farm",
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )
    print("All Stage 12 benchmark assertions passed.")
