#!/usr/bin/env python3
"""Deterministic Stage 9 regional-finale benchmark for Tower RNG.

Stage 9 is the jungle regional finale and a full-validation anchor. It checks
all eight-slot entry formations with at least four roles, a healthy entry subset
with at least five roles, and all nine-slot farm formations with at least five
roles while respecting the current role cap.

The benchmark introduces three jungle behaviors that later Stage 7 and 8
lightweight checks may reuse:
- split-on-defeat swarm bodies,
- a one-time route dash,
- one-time regeneration that can be skipped by lethal burst damage.
The boss also has a short one-time untargetable close-up phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.02
MAX_SIMULATION_SECONDS = 150.0
STAGE_SCALE = 10 ** ((9 - 1) / 3)
STAGE_REWARD_SCALE = STAGE_SCALE * (1.08**8)
BOSS_REWARD_MODIFIER = 1.15

ENTRY_SLOTS = 8
ENTRY_ROLE_CAP = 3
ENTRY_MIN_ROLES = 4
ENTRY_OUTPUT_MULTIPLIER = 58.0

FARM_SLOTS = 9
FARM_ROLE_CAP = 3
FARM_MIN_ROLES = 5
FARM_OUTPUT_MULTIPLIER = 65.4


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
    tags: frozenset[str] = frozenset()
    shield_fraction: float = 0.0
    phase_heal_fraction: float = 0.0
    phase_heal_at_fraction: float = 0.0
    untargetable_at_fraction: float = 0.0
    untargetable_duration: float = 0.0
    untargetable_progress: float = 0.0
    dash_at_progress: float = 0.0
    dash_progress: float = 0.0
    split_count: int = 0
    split_child: Optional["MonsterSpec"] = None
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
    heal_triggered: bool = False
    untargetable_triggered: bool = False
    dash_triggered: bool = False
    split_triggered: bool = False
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

SPORELING = MonsterSpec(
    monster_id="MON_JUNGLE_SPORELING",
    hp=0.20 * STAGE_SCALE,
    time_to_base=14.0,
    spawn_cost=0,
    base_damage=1,
    tags=frozenset({"swarm", "child"}),
    reward_modifier=0.0,
)

SPORE_POD = MonsterSpec(
    monster_id="MON_SPORE_POD",
    hp=0.55 * STAGE_SCALE,
    time_to_base=17.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm"}),
    split_count=2,
    split_child=SPORELING,
)

VINE_STALKER = MonsterSpec(
    monster_id="MON_VINE_STALKER",
    hp=3.00 * STAGE_SCALE,
    time_to_base=22.0,
    spawn_cost=10,
    base_damage=1,
    tags=frozenset({"fast"}),
    dash_at_progress=0.55,
    dash_progress=0.08,
)

REGROWTH_GUARDIAN = MonsterSpec(
    monster_id="MON_REGROWTH_GUARDIAN",
    hp=6.50 * STAGE_SCALE,
    time_to_base=34.0,
    spawn_cost=30,
    base_damage=3,
    tags=frozenset({"thick", "regenerating"}),
    phase_heal_at_fraction=0.45,
    phase_heal_fraction=0.15,
)

ANCIENT_MAWFLOWER = MonsterSpec(
    monster_id="BOSS_ANCIENT_MAWFLOWER",
    hp=22.0 * STAGE_SCALE,
    time_to_base=58.0,
    spawn_cost=100,
    base_damage=12,
    tags=frozenset({"boss", "elite", "large", "regenerating"}),
    shield_fraction=0.10,
    phase_heal_at_fraction=0.55,
    phase_heal_fraction=0.15,
    untargetable_at_fraction=0.30,
    untargetable_duration=1.20,
    untargetable_progress=0.04,
    reward_modifier=BOSS_REWARD_MODIFIER,
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.55, SPORE_POD) for index in range(12)],
    2: [SpawnEntry(index * 0.85, VINE_STALKER) for index in range(6)],
    3: [
        SpawnEntry(0.00, REGROWTH_GUARDIAN),
        SpawnEntry(0.90, SPORE_POD),
        SpawnEntry(1.80, VINE_STALKER),
        SpawnEntry(2.70, SPORE_POD),
        SpawnEntry(3.60, VINE_STALKER),
        SpawnEntry(4.50, SPORE_POD),
    ],
    4: [
        SpawnEntry(0.00, REGROWTH_GUARDIAN),
        SpawnEntry(1.10, REGROWTH_GUARDIAN),
        SpawnEntry(2.20, VINE_STALKER),
        SpawnEntry(3.30, SPORE_POD),
    ],
    5: [SpawnEntry(0.00, ANCIENT_MAWFLOWER)]
    + [SpawnEntry(1.60 + index * 1.40, SPORE_POD) for index in range(5)],
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


def deal_damage(monster: MonsterState, damage: float, current_time: float) -> None:
    if current_time < monster.untargetable_until:
        return

    if monster.shield > 0.0:
        absorbed = min(monster.shield, damage)
        monster.shield -= absorbed
        damage -= absorbed
    monster.hp -= damage

    if (
        not monster.heal_triggered
        and monster.spec.phase_heal_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.phase_heal_at_fraction
    ):
        monster.heal_triggered = True
        monster.hp = min(
            monster.spec.hp,
            monster.hp + monster.spec.hp * monster.spec.phase_heal_fraction,
        )

    if (
        not monster.untargetable_triggered
        and monster.spec.untargetable_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.untargetable_at_fraction
    ):
        monster.untargetable_triggered = True
        monster.untargetable_until = (
            current_time + monster.spec.untargetable_duration
        )
        monster.progress = min(
            0.98,
            monster.progress + monster.spec.untargetable_progress,
        )


def create_monster(
    uid: int,
    spec: MonsterSpec,
    progress: float = 0.0,
) -> MonsterState:
    return MonsterState(
        uid=uid,
        spec=spec,
        hp=spec.hp,
        shield=spec.hp * spec.shield_fraction,
        progress=progress,
    )


def simulate(
    lineup: tuple[str, ...],
    wave_number: int,
    account_multiplier: float,
) -> SimulationResult:
    has_drummer = "drummer" in lineup
    ally_output_multiplier = 1.15 if has_drummer else 1.0

    towers: list[TowerState] = []
    for tower_id in lineup:
        first_attack = {"rogue": 0.75, "hunter": 0.50}.get(
            tower_id,
            0.25,
        )
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
            monsters.append(create_monster(next_uid, spawn.spec))
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
                deal_damage(
                    choose_front(active),
                    1.0 * multiplier,
                    current_time,
                )

            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    deal_damage(target, 0.60 * multiplier, current_time)

            elif tower.tower_id == "frost":
                target = choose_front(active)
                deal_damage(target, 0.55 * multiplier, current_time)
                slow_fraction = 0.15 * (1.15 if has_drummer else 1.0)
                target.slow_fraction = max(
                    target.slow_fraction,
                    slow_fraction,
                )
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
                deal_damage(target, damage, current_time)

            elif tower.tower_id == "drummer":
                deal_damage(
                    choose_front(active),
                    0.55 * account_multiplier,
                    current_time,
                )

            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                deal_damage(target, damage, current_time)

            tower.next_attack += interval

            for monster in list(active):
                if not monster.alive or monster.hp > 1e-9:
                    continue

                monster.alive = False
                if monster.spec.split_count and not monster.split_triggered:
                    monster.split_triggered = True
                    child = monster.spec.split_child
                    if child is None:
                        raise AssertionError("split child is missing")
                    for child_index in range(monster.spec.split_count):
                        offset = (
                            child_index - (monster.spec.split_count - 1) / 2
                        ) * 0.008
                        child_progress = max(
                            0.0,
                            min(0.97, monster.progress + offset),
                        )
                        monsters.append(
                            create_monster(next_uid, child, child_progress)
                        )
                        next_uid += 1

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

            if (
                not monster.dash_triggered
                and monster.spec.dash_at_progress > 0.0
                and monster.progress >= monster.spec.dash_at_progress
            ):
                monster.dash_triggered = True
                monster.progress = min(
                    0.98,
                    monster.progress + monster.spec.dash_progress,
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


def spec_effective_hp(spec: MonsterSpec) -> float:
    total = spec.hp * (
        1.0 + spec.shield_fraction + spec.phase_heal_fraction
    )
    if spec.split_count and spec.split_child is not None:
        total += spec.split_count * spec_effective_hp(spec.split_child)
    return total


def wave_effective_hp(wave_number: int) -> float:
    return sum(
        spec_effective_hp(entry.spec)
        for entry in WAVES[wave_number]
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
    rows: dict[int, list[tuple[tuple[str, ...], SimulationResult]]] = {}
    for wave_number in range(1, 6):
        rows[wave_number] = [
            (lineup, simulate(lineup, wave_number, multiplier))
            for lineup in lineups
        ]

    result_maps = {
        wave_number: dict(rows[wave_number])
        for wave_number in rows
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
        ENTRY_MIN_ROLES,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(entry_lineups) == 486
    entry_leaks = {
        wave: sum(result.leaks for _, result in entry_rows[wave])
        for wave in range(1, 6)
    }
    assert entry_leaks[1] == 0
    assert entry_leaks[5] == 0
    assert sum(entry_leaks.values()) <= 4
    assert 100.0 <= mean(entry_cycles) <= 112.0
    assert max(entry_cycles) <= 140.0

    healthy_lineups, healthy_rows, healthy_cycles = profile_results(
        ENTRY_SLOTS,
        ENTRY_ROLE_CAP,
        5,
        ENTRY_OUTPUT_MULTIPLIER,
    )
    assert len(healthy_lineups) == 201
    assert all(
        result.leaks == 0
        for wave in healthy_rows.values()
        for _, result in wave
    )
    assert mean(healthy_cycles) <= 108.0
    assert max(healthy_cycles) <= 128.0

    farm_lineups, farm_rows, farm_cycles = profile_results(
        FARM_SLOTS,
        FARM_ROLE_CAP,
        FARM_MIN_ROLES,
        FARM_OUTPUT_MULTIPLIER,
    )
    assert len(farm_lineups) == 320
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
    assert all(10.0 <= value <= 16.5 for value in normal_averages)
    assert 25.0 <= boss_average <= 29.0
    assert 80.0 <= mean(farm_cycles) <= 84.0
    assert max(farm_cycles) <= 104.0

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
            f"effective_hp={wave_effective_hp(wave_number):>9.2f} "
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


def main() -> None:
    validate()
    print("Stage 9 regional-finale benchmark")
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
    print("All Stage 9 assertions passed.")


if __name__ == "__main__":
    main()
