"""Deterministic Stage 1 wave benchmark for Tower RNG.

The model validates provisional catalog values before the runtime combat system
exists. It simulates all 15 four-slot lineups made from the six baseline tower
roles, one tower per role, against the canonical Stage 1 wave schedules.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.01
MAX_SIMULATION_SECONDS = 30.0
AVERAGE_MIN_SECONDS = 9.0
AVERAGE_MAX_SECONDS = 11.0
WORST_MAX_SECONDS = 12.5


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
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


PRAIRIE_SLIME = MonsterSpec(
    monster_id="MON_PRAIRIE_SLIME",
    hp=5.0,
    time_to_base=10.0,
    spawn_cost=10,
    base_damage=1,
)

FIELD_RAT = MonsterSpec(
    monster_id="MON_FIELD_RAT",
    hp=2.0,
    time_to_base=8.5,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm"}),
)

YOUNG_BOAR = MonsterSpec(
    monster_id="MON_YOUNG_BOAR",
    hp=12.0,
    time_to_base=12.0,
    spawn_cost=20,
    base_damage=2,
    tags=frozenset({"thick"}),
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
    1: [SpawnEntry(index * 0.75, PRAIRIE_SLIME) for index in range(6)],
    2: [SpawnEntry(index * 0.40, FIELD_RAT) for index in range(15)],
    3: [
        SpawnEntry(0.00, YOUNG_BOAR),
        SpawnEntry(0.50, FIELD_RAT),
        SpawnEntry(1.00, PRAIRIE_SLIME),
        SpawnEntry(1.50, FIELD_RAT),
        SpawnEntry(2.00, PRAIRIE_SLIME),
        SpawnEntry(2.50, FIELD_RAT),
        SpawnEntry(3.00, PRAIRIE_SLIME),
        SpawnEntry(3.50, FIELD_RAT),
    ],
    4: [
        SpawnEntry(0.00, YOUNG_BOAR),
        SpawnEntry(0.75, PRAIRIE_SLIME),
        SpawnEntry(1.50, FIELD_RAT),
        SpawnEntry(2.25, YOUNG_BOAR),
        SpawnEntry(3.00, PRAIRIE_SLIME),
        SpawnEntry(3.75, FIELD_RAT),
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


def simulate(lineup: tuple[str, ...], wave_number: int) -> SimulationResult:
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

            if tower.tower_id == "archer":
                choose_front(active).hp -= 1.0 * ally_output_multiplier

            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    target.hp -= 0.60 * ally_output_multiplier

            elif tower.tower_id == "frost":
                target = choose_front(active)
                target.hp -= 0.55 * ally_output_multiplier
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
                damage = 0.80 * ally_output_multiplier
                if target.hp / target.spec.hp <= 0.30:
                    damage *= 2.0
                target.hp -= damage

            elif tower.tower_id == "drummer":
                choose_front(active).hp -= 0.55

            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * ally_output_multiplier
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
                TICK_SECONDS / monster.spec.time_to_base * speed_multiplier
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
        f"Wave {wave_number} did not resolve within {MAX_SIMULATION_SECONDS}s"
    )


def wave_budget(wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in WAVES[wave_number])


def wave_hp(wave_number: int) -> float:
    return sum(entry.spec.hp for entry in WAVES[wave_number])


def main() -> None:
    lineups = list(combinations(TOWER_IDS, 4))
    all_results: dict[int, list[tuple[tuple[str, ...], SimulationResult]]] = {}

    print("Stage 1 deterministic wave benchmark")
    print(f"Lineups: {len(lineups)} unique four-role combinations")

    for wave_number in range(1, 5):
        results = [
            (lineup, simulate(lineup, wave_number)) for lineup in lineups
        ]
        all_results[wave_number] = results
        times = sorted(result.clear_time for _, result in results)
        total_leaks = sum(result.leaks for _, result in results)

        print(
            f"W{wave_number}: budget={wave_budget(wave_number):>3} "
            f"hp={wave_hp(wave_number):>4.1f} "
            f"count={len(WAVES[wave_number]):>2} "
            f"avg={mean(times):>5.2f}s "
            f"median={median(times):>5.2f}s "
            f"best={times[0]:>5.2f}s "
            f"worst={times[-1]:>5.2f}s "
            f"leaks={total_leaks}"
        )

        if total_leaks:
            raise SystemExit(f"Wave {wave_number} leaked in benchmark")
        if not AVERAGE_MIN_SECONDS <= mean(times) <= AVERAGE_MAX_SECONDS:
            raise SystemExit(
                f"Wave {wave_number} average clear time is outside target band"
            )
        if times[-1] > WORST_MAX_SECONDS:
            raise SystemExit(
                f"Wave {wave_number} worst clear time exceeds safety limit"
            )

    cycle_rows: list[tuple[tuple[str, ...], list[float]]] = []
    for lineup in lineups:
        times = [
            dict(all_results[wave_number])[lineup].clear_time
            for wave_number in range(1, 5)
        ]
        cycle_rows.append((lineup, times))

    cycle_rows.sort(key=lambda row: mean(row[1]))
    cycle_means = [mean(times) for _, times in cycle_rows]

    print(
        f"Cycle: avg={mean(cycle_means):.2f}s "
        f"median_lineup={median(cycle_means):.2f}s "
        f"best_lineup={cycle_means[0]:.2f}s "
        f"worst_lineup={cycle_means[-1]:.2f}s"
    )
    print(f"Best lineup: {', '.join(cycle_rows[0][0])}")
    print(f"Worst lineup: {', '.join(cycle_rows[-1][0])}")


if __name__ == "__main__":
    main()
