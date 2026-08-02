#!/usr/bin/env python3
"""Deterministic aggregate Stage 15 wave benchmark for Tower RNG.

This benchmark converts account-level EquivalentContribution into a continuous
lane damage model. It validates the provisional Stage 15 wave envelope before
individual Stage 15 towers and runtime combat behaviors exist.
"""

from __future__ import annotations

from dataclasses import dataclass

TICK_SECONDS = 0.01
MAX_SECONDS = 180.0
STANDARD_STAGE15_HP = 232_080.0
STAGE15_REWARD_SCALE = 136_332.45128513008


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
    tags: frozenset[str] = frozenset()
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
    progress: float = 0.0
    leaked: bool = False
    dead: bool = False


@dataclass(frozen=True)
class Result:
    clear_time: float
    leaks: int
    base_damage: int


CINDERLING = MonsterSpec(
    monster_id="MON_CINDERLING",
    hp=STANDARD_STAGE15_HP * (0.16 / 3.0),
    time_to_base=16.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm", "fast"}),
)

LAVA_HOUND = MonsterSpec(
    monster_id="MON_LAVA_HOUND",
    hp=STANDARD_STAGE15_HP * 0.15,
    time_to_base=20.0,
    spawn_cost=15,
    base_damage=2,
    tags=frozenset({"fast"}),
)

MAGMA_GUARD = MonsterSpec(
    monster_id="MON_MAGMA_GUARD",
    hp=STANDARD_STAGE15_HP * 0.82,
    time_to_base=30.0,
    spawn_cost=50,
    base_damage=5,
    tags=frozenset({"shield", "thick"}),
)

OBSIDIAN_COLOSSUS = MonsterSpec(
    monster_id="MON_OBSIDIAN_COLOSSUS",
    hp=STANDARD_STAGE15_HP * 0.85,
    time_to_base=36.0,
    spawn_cost=75,
    base_damage=8,
    tags=frozenset({"elite", "thick", "large"}),
)

CALDERA_HEART = MonsterSpec(
    monster_id="BOSS_CALDERA_HEART",
    hp=STANDARD_STAGE15_HP * 1.50,
    time_to_base=45.0,
    spawn_cost=100,
    base_damage=15,
    tags=frozenset({"boss", "elite", "large"}),
    reward_modifier=1.15,
)


WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.45, CINDERLING) for index in range(12)],
    2: [SpawnEntry(index * 1.50, LAVA_HOUND) for index in range(4)],
    3: [
        SpawnEntry(0.0, MAGMA_GUARD),
        *[
            SpawnEntry(1.50 + index * 1.50, CINDERLING)
            for index in range(4)
        ],
    ],
    4: [
        SpawnEntry(0.0, OBSIDIAN_COLOSSUS),
        SpawnEntry(3.0, LAVA_HOUND),
        SpawnEntry(6.0, LAVA_HOUND),
    ],
    5: [
        SpawnEntry(0.0, CALDERA_HEART),
        *[
            SpawnEntry(2.0 + index * 2.0, CINDERLING)
            for index in range(6)
        ],
    ],
}


PROFILES = {
    "15h_P10": 10_188.0,
    "15h_P50": 19_665.0,
    "30h_P10": 60_575.0,
}


def active_monsters(states: list[MonsterState]) -> list[MonsterState]:
    return [state for state in states if not state.dead and not state.leaked]


def simulate(equivalent_contribution: float, wave_number: int) -> Result:
    pending = list(WAVES[wave_number])
    states: list[MonsterState] = []
    current_time = 0.0
    next_uid = 0
    leaks = 0
    base_damage = 0

    while current_time < MAX_SECONDS:
        while pending and pending[0].spawn_time <= current_time + 1e-9:
            spawn = pending.pop(0)
            states.append(
                MonsterState(
                    uid=next_uid,
                    spec=spawn.spec,
                    hp=spawn.spec.hp,
                )
            )
            next_uid += 1

        living = active_monsters(states)
        if living:
            count = len(living)
            density_multiplier = (
                0.90 if count == 1 else 1.03 if count <= 3 else 1.10
            )
            front = max(living, key=lambda state: (state.progress, -state.uid))

            target_multiplier = 1.0
            if "boss" in front.spec.tags:
                target_multiplier *= 1.18
            elif "elite" in front.spec.tags:
                target_multiplier *= 1.10
            if "shield" in front.spec.tags and front.hp / front.spec.hp > 0.60:
                target_multiplier *= 0.92
            if front.hp / front.spec.hp <= 0.30:
                target_multiplier *= 1.08

            total_damage = (
                equivalent_contribution
                * density_multiplier
                * target_multiplier
                * TICK_SECONDS
            )

            if count == 1:
                front.hp -= total_damage
            else:
                primary_damage = total_damage * 0.70
                splash_damage = total_damage - primary_damage
                front.hp -= primary_damage

                splash_targets = [
                    state
                    for state in sorted(
                        living,
                        key=lambda state: (-state.progress, state.uid),
                    )
                    if state.uid != front.uid
                ][:4]
                if splash_targets:
                    damage_each = splash_damage / len(splash_targets)
                    for target in splash_targets:
                        target.hp -= damage_each
                else:
                    front.hp -= splash_damage

            for state in living:
                if state.hp <= 1e-9:
                    state.dead = True

        for state in states:
            if state.dead or state.leaked:
                continue
            control_time_multiplier = 1.05 if "boss" in state.spec.tags else 1.10
            state.progress += (
                TICK_SECONDS
                / (state.spec.time_to_base * control_time_multiplier)
            )
            if state.progress >= 1.0:
                state.leaked = True
                leaks += 1
                base_damage += state.spec.base_damage

        if not pending and all(state.dead or state.leaked for state in states):
            return Result(current_time, leaks, base_damage)

        current_time += TICK_SECONDS

    raise RuntimeError(f"Wave {wave_number} did not resolve")


def wave_hp(wave_number: int) -> float:
    return sum(entry.spec.hp for entry in WAVES[wave_number])


def wave_budget(wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in WAVES[wave_number])


def wave_reward_units(wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in WAVES[wave_number]
    )


def profile_results(equivalent_contribution: float) -> list[Result]:
    return [simulate(equivalent_contribution, wave) for wave in range(1, 6)]


def cycle_time(equivalent_contribution: float) -> float:
    return sum(result.clear_time for result in profile_results(equivalent_contribution))


def minimum_ec_for_120_second_cycle() -> float:
    low = 8_000.0
    high = 11_000.0
    for _ in range(50):
        midpoint = (low + high) / 2.0
        if cycle_time(midpoint) > 120.0:
            low = midpoint
        else:
            high = midpoint
    return high


def main() -> None:
    all_profile_results: dict[str, list[Result]] = {}

    print("Stage 15 aggregate full-cycle benchmark")
    print("profile | W1 | W2 | W3 | W4 | W5 | cycle | boss share | leaks")

    for name, equivalent_contribution in PROFILES.items():
        results = profile_results(equivalent_contribution)
        all_profile_results[name] = results
        times = [result.clear_time for result in results]
        leaks = sum(result.leaks for result in results)
        print(
            f"{name:>8} | "
            + " | ".join(f"{value:>5.2f}" for value in times)
            + f" | {sum(times):>6.2f} | {times[-1] / sum(times):>10.3f} | {leaks}"
        )

    print("\nWave data")
    print("wave | count | hp | budget | reward units")
    for wave in range(1, 6):
        print(
            f"{wave:>4} | {len(WAVES[wave]):>5} | {wave_hp(wave):>10,.1f} | "
            f"{wave_budget(wave):>6} | {wave_reward_units(wave):>12.1f}"
        )

    total_reward_units = sum(wave_reward_units(wave) for wave in range(1, 6))
    print(
        f"Total spawn budget={sum(wave_budget(wave) for wave in range(1, 6))}, "
        f"reward units={total_reward_units:.1f}, "
        f"planned DefenseXP={total_reward_units * STAGE15_REWARD_SCALE:,.0f}"
    )

    minimum_ec = minimum_ec_for_120_second_cycle()
    print(
        f"Minimum EC for <=120s cycle: {minimum_ec:,.2f} "
        f"({minimum_ec / PROFILES['15h_P10'] * 100:.2f}% of 15h P10)"
    )

    entry = all_profile_results["15h_P10"]
    entry_times = [result.clear_time for result in entry]
    assert sum(result.leaks for result in entry) == 0
    assert entry_times[0] <= 18.0
    assert entry_times[1] <= 18.0
    assert entry_times[2] <= 25.0
    assert entry_times[3] <= 25.0
    assert 28.0 <= entry_times[4] <= 40.0
    assert 100.0 <= sum(entry_times) <= 120.0
    assert 0.25 <= entry_times[4] / sum(entry_times) <= 0.35

    median = all_profile_results["15h_P50"]
    assert sum(result.leaks for result in median) == 0
    assert sum(result.clear_time for result in median) <= 70.0

    farm = all_profile_results["30h_P10"]
    assert sum(result.leaks for result in farm) == 0
    assert sum(result.clear_time for result in farm) <= 40.0

    assert [wave_budget(wave) for wave in range(1, 6)] == [60, 60, 70, 105, 130]
    assert abs(total_reward_units - 440.0) < 1e-9

    print("All Stage 15 benchmark assertions passed.")


if __name__ == "__main__":
    main()
