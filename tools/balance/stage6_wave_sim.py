#!/usr/bin/env python3
"""Deterministic Stage 6 regional-finale benchmark for Tower RNG.

Stage 6 is the desert regional finale and a full-validation anchor. It tests
all six-slot entry formations with at least four roles and all seven-slot farm
formations with at least five roles while respecting the current role caps.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.02
MAX_SIMULATION_SECONDS = 120.0
STAGE_SCALE = 10 ** ((6 - 1) / 3)
STAGE_REWARD_SCALE = STAGE_SCALE * (1.08**5)
BOSS_REWARD_MODIFIER = 1.15

ENTRY_SLOTS = 6
ENTRY_ROLE_CAP = 2
ENTRY_MIN_ROLES = 4
ENTRY_OUTPUT_MULTIPLIER = 8.00

FARM_SLOTS = 7
FARM_ROLE_CAP = 3
FARM_MIN_ROLES = 5
FARM_OUTPUT_MULTIPLIER = 9.50


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
    burrow_at_fraction: float = 0.0
    burrow_duration: float = 0.0
    burrow_progress: float = 0.0
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
    burrow_triggered: bool = False
    untargetable_until: float = 0.0


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

DUST_SCARAB = MonsterSpec(
    monster_id="MON_DUST_SCARAB",
    hp=0.95 * STAGE_SCALE,
    time_to_base=15.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm", "fast"}),
)

DUNE_JACKAL = MonsterSpec(
    monster_id="MON_DUNE_JACKAL",
    hp=3.20 * STAGE_SCALE,
    time_to_base=20.0,
    spawn_cost=10,
    base_damage=1,
    tags=frozenset({"fast"}),
)

SANDSTONE_SENTINEL = MonsterSpec(
    monster_id="MON_SANDSTONE_SENTINEL",
    hp=6.70 * STAGE_SCALE,
    time_to_base=28.0,
    spawn_cost=30,
    base_damage=3,
    tags=frozenset({"armored", "thick"}),
    shield_fraction=0.20,
)

GLASS_SCORPION = MonsterSpec(
    monster_id="BOSS_GLASS_SCORPION",
    hp=21.80 * STAGE_SCALE,
    time_to_base=50.0,
    spawn_cost=100,
    base_damage=10,
    tags=frozenset({"boss", "elite", "large", "armored"}),
    shield_fraction=0.12,
    phase_shield_fraction=0.18,
    burrow_at_fraction=0.35,
    burrow_duration=1.25,
    burrow_progress=0.06,
    reward_modifier=BOSS_REWARD_MODIFIER,
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.50, DUST_SCARAB) for index in range(12)],
    2: [SpawnEntry(index * 0.85, DUNE_JACKAL) for index in range(6)],
    3: [
        SpawnEntry(0.00, SANDSTONE_SENTINEL),
        SpawnEntry(0.90, DUST_SCARAB),
        SpawnEntry(1.80, DUNE_JACKAL),
        SpawnEntry(2.70, DUST_SCARAB),
        SpawnEntry(3.60, DUNE_JACKAL),
        SpawnEntry(4.50, DUST_SCARAB),
    ],
    4: [
        SpawnEntry(0.00, SANDSTONE_SENTINEL),
        SpawnEntry(1.00, SANDSTONE_SENTINEL),
        SpawnEntry(2.00, DUNE_JACKAL),
        SpawnEntry(3.00, DUST_SCARAB),
    ],
    5: [SpawnEntry(0.00, GLASS_SCORPION)]
    + [SpawnEntry(1.50 + index * 1.50, DUST_SCARAB) for index in range(5)],
}


def formation_lineups(
    slots: int, role_cap: int, minimum_distinct_roles: int
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


def deal_damage(monster: MonsterState, damage: float, current_time: float) -> None:
    if current_time < monster.untargetable_until:
        return

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

    if (
        not monster.burrow_triggered
        and monster.spec.burrow_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.burrow_at_fraction
    ):
        monster.burrow_triggered = True
        monster.untargetable_until = current_time + monster.spec.burrow_duration
        monster.progress = min(
            0.98, monster.progress + monster.spec.burrow_progress
        )


def simulate(
    lineup: tuple[str, ...], wave_number: int, account_multiplier: float
) -> SimulationResult:
    has_drummer = "drummer" in lineup
    ally_output_multiplier = 1.15 if has_drummer else 1.0

    towers: list[TowerState] = []
    for tower_id in lineup:
        first_attack = {"rogue": 0.75, "hunter": 0.50}.get(tower_id, 0.25)
        towers.append(TowerState(tower_id, first_attack))

    pending = list(WAVES[wave_number])
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
                if monster.alive
                and not monster.leaked
                and current_time >= monster.untargetable_until
            ]
            if not active:
                tower.next_attack += 0.05
                continue

            interval = 2.0 if tower.tower_id == "hunter" else 1.0
            multiplier = ally_output_multiplier * account_multiplier

            if tower.tower_id == "archer":
                deal_damage(choose_front(active), 1.0 * multiplier, current_time)

            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    deal_damage(target, 0.60 * multiplier, current_time)

            elif tower.tower_id == "frost":
                target = choose_front(active)
                deal_damage(target, 0.55 * multiplier, current_time)
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
                deal_damage(target, damage, current_time)

            elif tower.tower_id == "drummer":
                deal_damage(
                    choose_front(active), 0.55 * account_multiplier, current_time
                )

            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                deal_damage(target, damage, current_time)

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


def wave_budget(wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in WAVES[wave_number])


def wave_reward_units(wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in WAVES[wave_number]
    )


def wave_effective_hp(wave_number: int) -> float:
    total = 0.0
    for entry in WAVES[wave_number]:
        spec = entry.spec
        total += spec.hp * (
            1.0 + spec.shield_fraction + spec.phase_shield_fraction
        )
    return total


def profile_results(
    slots: int,
    role_cap: int,
    minimum_distinct_roles: int,
    multiplier: float,
):
    lineups = formation_lineups(slots, role_cap, minimum_distinct_roles)
    rows: dict[int, list[tuple[tuple[str, ...], SimulationResult]]] = {}
    for wave_number in range(1, 6):
        rows[wave_number] = [
            (lineup, simulate(lineup, wave_number, multiplier))
            for lineup in lineups
        ]
    cycles = [
        sum(
            dict(rows[wave_number])[lineup].clear_time
            for wave_number in range(1, 6)
        )
        for lineup in lineups
    ]
    return lineups, rows, cycles


def validate() -> None:
    assert [wave_budget(wave) for wave in range(1, 6)] == [60, 60, 65, 75, 125]
    assert abs(sum(wave_reward_units(wave) for wave in range(1, 6)) - 400.0) < 1e-9

    entry_lineups, entry_rows, entry_cycles = profile_results(
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        ENTRY_MIN_ROLES,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(entry_lineups) == 121
    entry_leaks = {
        wave: sum(result.leaks for _, result in entry_rows[wave])
        for wave in range(1, 6)
    }
    assert entry_leaks[1] == 0
    assert entry_leaks[5] == 0
    assert sum(entry_leaks.values()) <= 4
    assert 98.0 <= mean(entry_cycles) <= 110.0
    assert max(entry_cycles) <= 130.0

    healthy_entry_lineups, healthy_entry_rows, healthy_entry_cycles = profile_results(
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        5,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(healthy_entry_lineups) == 31
    assert all(
        result.leaks == 0
        for wave in healthy_entry_rows.values()
        for _, result in wave
    )
    assert max(healthy_entry_cycles) <= 118.0

    farm_lineups, farm_rows, farm_cycles = profile_results(
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )
    assert len(farm_lineups) == 96
    assert all(
        result.leaks == 0
        for wave in farm_rows.values()
        for _, result in wave
    )
    normal_averages = [
        mean(result.clear_time for _, result in farm_rows[wave])
        for wave in range(1, 5)
    ]
    boss_average = mean(result.clear_time for _, result in farm_rows[5])
    assert all(8.0 <= value <= 16.0 for value in normal_averages)
    assert 22.0 <= boss_average <= 26.0
    assert 72.0 <= mean(farm_cycles) <= 78.0
    assert max(farm_cycles) <= 92.0
    boss_share = boss_average / mean(farm_cycles)
    assert 0.30 <= boss_share <= 0.35


def print_profile(
    name: str,
    slots: int,
    role_cap: int,
    minimum_distinct_roles: int,
    multiplier: float,
) -> None:
    lineups, rows, cycles = profile_results(
        slots, role_cap, minimum_distinct_roles, multiplier
    )
    print(
        f"{name}: slots={slots} role_cap={role_cap} "
        f"minimum_roles={minimum_distinct_roles} multiplier=x{multiplier:.2f} "
        f"lineups={len(lineups)}"
    )
    for wave_number in range(1, 6):
        results = [result for _, result in rows[wave_number]]
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(wave_number):>3} "
            f"reward={wave_reward_units(wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(wave_number):>8.2f} "
            f"avg={mean(times):>5.2f}s median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(result.clear_time for _, result in rows[5])
    print(
        f"  Cycle: avg={mean(cycles):.2f}s median={median(cycles):.2f}s "
        f"best={min(cycles):.2f}s worst={max(cycles):.2f}s "
        f"boss_share={boss_average / mean(cycles) * 100:.1f}%"
    )


def main() -> None:
    validate()
    print("Stage 6 regional-finale benchmark")
    print(f"StageScale: {STAGE_SCALE:.8f}")
    print(f"StageRewardScale: {STAGE_REWARD_SCALE:.8f}")
    print_profile(
        "ENTRY",
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        ENTRY_MIN_ROLES,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    print_profile(
        "ENTRY_5_ROLE_SUBSET",
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        5,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    print_profile(
        "FARM",
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )

    farm_cycles = profile_results(
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )[2]
    xp_per_minute = (
        sum(wave_reward_units(wave) for wave in range(1, 6))
        * STAGE_REWARD_SCALE
        / mean(farm_cycles)
        * 60.0
    )
    print(f"Farm Defense XP per minute: {xp_per_minute:.2f}")
    print("All Stage 6 assertions passed.")


if __name__ == "__main__":
    main()
