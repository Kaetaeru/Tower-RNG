#!/usr/bin/env python3
"""Deterministic Stage 3 regional-finale benchmark for Tower RNG.

Stage 3 is the first regional finale and a full-validation anchor. It tests all
four-role entry lineups and all five-role farm lineups made from the six
provisional baseline roles. The farm profile is tuned to preserve the existing
78-second economy proxy.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.01
MAX_SIMULATION_SECONDS = 90.0
STAGE_SCALE = 4.64158883
STAGE_REWARD_SCALE = STAGE_SCALE * (1.08**2)
BOSS_REWARD_MODIFIER = 1.15

ENTRY_SLOTS = 4
FARM_SLOTS = 5
ENTRY_OUTPUT_MULTIPLIER = 1.80
FARM_OUTPUT_MULTIPLIER = 1.80


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


TOWER_IDS = (
    "archer",
    "slinger",
    "frost",
    "rogue",
    "drummer",
    "hunter",
)

GLOW_MOTH = MonsterSpec(
    monster_id="MON_GLOW_MOTH",
    hp=1.30 * STAGE_SCALE,
    time_to_base=12.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm", "fast"}),
)

ROOT_SPRITE = MonsterSpec(
    monster_id="MON_ROOT_SPRITE",
    hp=4.50 * STAGE_SCALE,
    time_to_base=15.5,
    spawn_cost=10,
    base_damage=1,
)

BARK_GUARD = MonsterSpec(
    monster_id="MON_BARK_GUARD",
    hp=8.30 * STAGE_SCALE,
    time_to_base=21.0,
    spawn_cost=30,
    base_damage=3,
    tags=frozenset({"armored", "thick"}),
    shield_fraction=0.25,
)

ANCIENT_TREANT = MonsterSpec(
    monster_id="BOSS_ANCIENT_TREANT",
    hp=32.00 * STAGE_SCALE,
    time_to_base=42.0,
    spawn_cost=100,
    base_damage=8,
    tags=frozenset({"boss", "elite", "large", "armored"}),
    shield_fraction=0.15,
    phase_shield_fraction=0.20,
    reward_modifier=BOSS_REWARD_MODIFIER,
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.55, GLOW_MOTH) for index in range(12)],
    2: [SpawnEntry(index * 0.85, ROOT_SPRITE) for index in range(6)],
    3: [
        SpawnEntry(0.00, BARK_GUARD),
        SpawnEntry(0.90, GLOW_MOTH),
        SpawnEntry(1.80, ROOT_SPRITE),
        SpawnEntry(2.70, GLOW_MOTH),
        SpawnEntry(3.60, ROOT_SPRITE),
        SpawnEntry(4.50, GLOW_MOTH),
    ],
    4: [
        SpawnEntry(0.00, BARK_GUARD),
        SpawnEntry(1.20, BARK_GUARD),
        SpawnEntry(2.40, ROOT_SPRITE),
        SpawnEntry(3.60, GLOW_MOTH),
    ],
    5: [SpawnEntry(0.00, ANCIENT_TREANT)]
    + [SpawnEntry(1.50 + index * 1.50, GLOW_MOTH) for index in range(5)],
}


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
        total += spec.hp * (1.0 + spec.shield_fraction)
        total += spec.hp * spec.phase_shield_fraction
    return total


def profile_results(slots: int, multiplier: float):
    lineups = list(combinations(TOWER_IDS, slots))
    rows: dict[int, list[tuple[tuple[str, ...], SimulationResult]]] = {}
    for wave_number in range(1, 6):
        rows[wave_number] = [
            (lineup, simulate(lineup, wave_number, multiplier))
            for lineup in lineups
        ]
    cycles = [
        sum(dict(rows[wave_number])[lineup].clear_time for wave_number in range(1, 6))
        for lineup in lineups
    ]
    return lineups, rows, cycles


def validate() -> None:
    assert [wave_budget(wave) for wave in range(1, 6)] == [60, 60, 65, 75, 125]
    assert abs(sum(wave_reward_units(wave) for wave in range(1, 6)) - 400.0) < 1e-9

    _, entry_rows, entry_cycles = profile_results(
        ENTRY_SLOTS, ENTRY_OUTPUT_MULTIPLIER
    )
    entry_leaks = {
        wave: sum(result.leaks for _, result in entry_rows[wave])
        for wave in range(1, 6)
    }
    assert entry_leaks[1] == 0
    assert entry_leaks[5] == 0
    assert sum(entry_leaks.values()) <= 6
    assert 90.0 <= mean(entry_cycles) <= 110.0
    assert max(entry_cycles) <= 118.0

    _, farm_rows, farm_cycles = profile_results(FARM_SLOTS, FARM_OUTPUT_MULTIPLIER)
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
    assert all(8.0 <= value <= 15.0 for value in normal_averages)
    assert 26.0 <= boss_average <= 33.0
    assert 75.0 <= mean(farm_cycles) <= 81.0
    assert max(farm_cycles) <= 86.0
    boss_share = boss_average / mean(farm_cycles)
    assert 0.30 <= boss_share <= 0.36


def print_profile(name: str, slots: int, multiplier: float) -> None:
    lineups, rows, cycles = profile_results(slots, multiplier)
    print(f"{name}: slots={slots} multiplier=x{multiplier:.2f}")
    for wave_number in range(1, 6):
        results = [result for _, result in rows[wave_number]]
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(wave_number):>3} "
            f"reward={wave_reward_units(wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(wave_number):>7.2f} "
            f"avg={mean(times):>5.2f}s median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(result.clear_time for _, result in rows[5])
    print(
        f"  Cycle: avg={mean(cycles):.2f}s median={median(cycles):.2f}s "
        f"best={min(cycles):.2f}s worst={max(cycles):.2f}s "
        f"boss_share={boss_average / mean(cycles) * 100:.1f}% "
        f"lineups={len(lineups)}"
    )


def main() -> None:
    validate()
    print("Stage 3 regional-finale benchmark")
    print(f"StageScale: {STAGE_SCALE:.8f}")
    print(f"StageRewardScale: {STAGE_REWARD_SCALE:.8f}")
    print_profile("ENTRY", ENTRY_SLOTS, ENTRY_OUTPUT_MULTIPLIER)
    print_profile("FARM", FARM_SLOTS, FARM_OUTPUT_MULTIPLIER)

    farm_cycle = profile_results(FARM_SLOTS, FARM_OUTPUT_MULTIPLIER)[2]
    xp_per_minute = (
        sum(wave_reward_units(wave) for wave in range(1, 6))
        * STAGE_REWARD_SCALE
        / mean(farm_cycle)
        * 60.0
    )
    print(f"Farm Defense XP per minute: {xp_per_minute:.2f}")
    print("All Stage 3 assertions passed.")


if __name__ == "__main__":
    main()
