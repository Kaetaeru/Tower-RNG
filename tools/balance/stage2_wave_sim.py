"""Deterministic Stage 2 full-cycle benchmark for Tower RNG.

The model reuses the six provisional baseline tower roles and tests every
four-role lineup against the canonical Stage 2 waves. Two account profiles are
validated:

- entry: Core Output I+II level power, where a few weak role combinations may
  take limited base damage in the hardest normal waves;
- farm: the same core growth plus a modest roster-quality gain, where every
  lineup must clear all five waves without leaks.

The Stage 2 farm cycle intentionally validates the earlier 66-second economy
proxy rather than changing the long-term progression model.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.01
MAX_SIMULATION_SECONDS = 60.0
STAGE_SCALE = 2.15443469
STAGE_REWARD_SCALE = STAGE_SCALE * 1.08
BOSS_REWARD_MODIFIER = 1.15

ENTRY_OUTPUT_MULTIPLIER = 1.50
FARM_OUTPUT_MULTIPLIER = 1.65


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
    reward_modifier: float = 1.0
    tags: frozenset[str] = frozenset()


@dataclass(frozen=True)
class SpawnEntry:
    spawn_time: float
    spec: MonsterSpec


@dataclass
class MonsterState:
    uid: int
    spec: MonsterSpec
    hp: float
    progress: float = 0.0
    slow_until: float = 0.0
    slow_fraction: float = 0.0
    alive: bool = True
    leaked: bool = False


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
    kills: int
    monster_count: int


MOSS_SPRITE = MonsterSpec(
    monster_id="MON_MOSS_SPRITE",
    hp=10.8,
    time_to_base=11.0,
    spawn_cost=10,
    base_damage=1,
)

BRAMBLE_HARE = MonsterSpec(
    monster_id="MON_BRAMBLE_HARE",
    hp=4.3,
    time_to_base=9.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm", "fast"}),
)

BARK_BEETLE = MonsterSpec(
    monster_id="MON_BARK_BEETLE",
    hp=24.0,
    time_to_base=15.5,
    spawn_cost=20,
    base_damage=2,
    tags=frozenset({"thick", "armored"}),
)

THORNHORN_STAG = MonsterSpec(
    monster_id="BOSS_THORNHORN_STAG",
    hp=100.0,
    time_to_base=25.0,
    spawn_cost=100,
    base_damage=6,
    reward_modifier=BOSS_REWARD_MODIFIER,
    tags=frozenset({"boss", "elite", "large", "thick"}),
)

TOWER_IDS = (
    "archer",
    "slinger",
    "frost",
    "rogue",
    "drummer",
    "hunter",
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [
        SpawnEntry(index * 0.45, BRAMBLE_HARE)
        for index in range(12)
    ],
    2: [
        SpawnEntry(index * 0.70, MOSS_SPRITE)
        for index in range(6)
    ],
    3: [
        SpawnEntry(0.00, BARK_BEETLE),
        SpawnEntry(0.75, BRAMBLE_HARE),
        SpawnEntry(1.50, MOSS_SPRITE),
        SpawnEntry(2.25, BRAMBLE_HARE),
        SpawnEntry(3.00, MOSS_SPRITE),
        SpawnEntry(3.75, BRAMBLE_HARE),
        SpawnEntry(4.50, BRAMBLE_HARE),
        SpawnEntry(5.25, BRAMBLE_HARE),
    ],
    4: [
        SpawnEntry(0.00, BARK_BEETLE),
        SpawnEntry(0.75, MOSS_SPRITE),
        SpawnEntry(1.50, BRAMBLE_HARE),
        SpawnEntry(2.25, MOSS_SPRITE),
        SpawnEntry(3.00, BRAMBLE_HARE),
        SpawnEntry(3.75, MOSS_SPRITE),
        SpawnEntry(4.50, BRAMBLE_HARE),
        SpawnEntry(5.25, BRAMBLE_HARE),
    ],
    5: [
        SpawnEntry(0.00, THORNHORN_STAG),
        *[
            SpawnEntry(1.50 + index * 1.50, BRAMBLE_HARE)
            for index in range(6)
        ],
    ],
}


def choose_front(monsters: list[MonsterState]) -> MonsterState:
    return max(monsters, key=lambda monster: (monster.progress, -monster.uid))


def choose_low_health(monsters: list[MonsterState]) -> MonsterState:
    return min(
        monsters,
        key=lambda monster: (
            monster.hp / monster.spec.hp,
            -monster.progress,
            monster.uid,
        ),
    )


def choose_high_hp(monsters: list[MonsterState]) -> MonsterState:
    return max(
        monsters,
        key=lambda monster: (monster.spec.hp, monster.progress, -monster.uid),
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


def simulate(
    lineup: tuple[str, ...],
    wave_number: int,
    account_output_multiplier: float,
) -> SimulationResult:
    has_drummer = "drummer" in lineup
    ally_output_multiplier = 1.15 if has_drummer else 1.0

    towers: list[TowerState] = []
    for tower_id in lineup:
        first_attack = {
            "rogue": 0.75,
            "hunter": 0.50,
        }.get(tower_id, 0.25)
        towers.append(TowerState(tower_id, first_attack))

    pending = list(WAVES[wave_number])
    monsters: list[MonsterState] = []
    next_uid = 0
    current_time = 0.0
    leaks = 0
    base_damage = 0
    kills = 0

    while current_time < MAX_SIMULATION_SECONDS:
        while pending and pending[0].spawn_time <= current_time + 1e-9:
            spawn = pending.pop(0)
            monsters.append(
                MonsterState(
                    uid=next_uid,
                    spec=spawn.spec,
                    hp=spawn.spec.hp,
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
            output_multiplier = (
                ally_output_multiplier * account_output_multiplier
            )

            if tower.tower_id == "archer":
                choose_front(active).hp -= 1.0 * output_multiplier

            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    target.hp -= 0.60 * output_multiplier

            elif tower.tower_id == "frost":
                target = choose_front(active)
                target.hp -= 0.55 * output_multiplier
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
                damage = 0.80 * output_multiplier
                if target.hp / target.spec.hp <= 0.30:
                    damage *= 2.0
                target.hp -= damage

            elif tower.tower_id == "drummer":
                choose_front(active).hp -= 0.55 * account_output_multiplier

            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * output_multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                target.hp -= damage

            tower.next_attack += interval

            for monster in active:
                if monster.alive and monster.hp <= 1e-9:
                    monster.alive = False
                    kills += 1
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
            return SimulationResult(
                clear_time=current_time,
                leaks=leaks,
                base_damage=base_damage,
                kills=kills,
                monster_count=len(monsters),
            )

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


def wave_hp(wave_number: int) -> float:
    return sum(entry.spec.hp for entry in WAVES[wave_number])


def run_profile(
    name: str,
    output_multiplier: float,
) -> dict[int, list[tuple[tuple[str, ...], SimulationResult]]]:
    lineups = list(combinations(TOWER_IDS, 4))
    results_by_wave: dict[
        int,
        list[tuple[tuple[str, ...], SimulationResult]],
    ] = {}

    print(f"\n{name} profile: output x{output_multiplier:.2f}")
    for wave_number in range(1, 6):
        rows = [
            (
                lineup,
                simulate(lineup, wave_number, output_multiplier),
            )
            for lineup in lineups
        ]
        results_by_wave[wave_number] = rows
        times = sorted(result.clear_time for _, result in rows)
        total_leaks = sum(result.leaks for _, result in rows)
        total_base_damage = sum(
            result.base_damage for _, result in rows
        )

        print(
            f"W{wave_number}: "
            f"budget={wave_budget(wave_number):>3} "
            f"reward={wave_reward_units(wave_number):>6.1f} "
            f"hp={wave_hp(wave_number):>6.1f} "
            f"avg={mean(times):>5.2f}s "
            f"median={median(times):>5.2f}s "
            f"best={times[0]:>5.2f}s "
            f"worst={times[-1]:>5.2f}s "
            f"leaks={total_leaks:>2} "
            f"base_damage={total_base_damage:>2}"
        )

    cycle_totals = []
    for lineup_index in range(len(lineups)):
        cycle_totals.append(
            sum(
                results_by_wave[wave][lineup_index][1].clear_time
                for wave in range(1, 6)
            )
        )

    print(
        f"Cycle: avg={mean(cycle_totals):.2f}s "
        f"median={median(cycle_totals):.2f}s "
        f"best={min(cycle_totals):.2f}s "
        f"worst={max(cycle_totals):.2f}s"
    )
    return results_by_wave


def validate(
    entry: dict[int, list[tuple[tuple[str, ...], SimulationResult]]],
    farm: dict[int, list[tuple[tuple[str, ...], SimulationResult]]],
) -> None:
    farm_times = {
        wave: [result.clear_time for _, result in rows]
        for wave, rows in farm.items()
    }

    entry_cycle = [
        sum(entry[wave][index][1].clear_time for wave in range(1, 6))
        for index in range(15)
    ]
    farm_cycle = [
        sum(farm[wave][index][1].clear_time for wave in range(1, 6))
        for index in range(15)
    ]

    assert [wave_budget(wave) for wave in range(1, 6)] == [
        60,
        60,
        65,
        70,
        130,
    ]
    assert abs(sum(wave_reward_units(w) for w in range(1, 6)) - 400.0) < 1e-9

    assert sum(result.leaks for _, result in entry[1]) == 0
    assert sum(result.leaks for _, result in entry[2]) == 0
    assert sum(result.leaks for _, result in entry[5]) == 0
    assert sum(result.leaks for rows in entry.values() for _, result in rows) <= 10
    assert 65.0 <= mean(entry_cycle) <= 75.0

    assert sum(result.leaks for rows in farm.values() for _, result in rows) == 0
    assert all(8.0 <= mean(farm_times[wave]) <= 13.0 for wave in range(1, 5))
    assert 18.0 <= mean(farm_times[5]) <= 23.0
    assert 60.0 <= mean(farm_cycle) <= 66.0
    assert max(farm_cycle) <= 76.0


def main() -> None:
    print("Stage 2 deterministic full-cycle benchmark")
    print("Lineups: 15 unique four-role combinations")
    print(f"StageScale: {STAGE_SCALE:.6f}")
    print(f"StageRewardScale: {STAGE_REWARD_SCALE:.6f}")

    entry = run_profile("entry", ENTRY_OUTPUT_MULTIPLIER)
    farm = run_profile("farm", FARM_OUTPUT_MULTIPLIER)
    validate(entry, farm)

    total_reward_units = sum(
        wave_reward_units(wave) for wave in range(1, 6)
    )
    farm_cycle_average = mean(
        sum(farm[wave][index][1].clear_time for wave in range(1, 6))
        for index in range(15)
    )
    defense_xp_per_minute = (
        total_reward_units
        * STAGE_REWARD_SCALE
        / farm_cycle_average
        * 60.0
    )

    print("\nEconomy")
    print(f"SpawnBudget total: {sum(wave_budget(w) for w in range(1, 6))}")
    print(f"Reward units total: {total_reward_units:.0f}")
    print(f"Farm cycle average: {farm_cycle_average:.2f}s")
    print(f"Defense XP per minute: {defense_xp_per_minute:.2f}")
    print("All Stage 2 benchmark assertions passed.")


if __name__ == "__main__":
    main()
