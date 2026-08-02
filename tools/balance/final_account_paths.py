#!/usr/bin/env python3
"""Re-run fast, central, and slow V1 completion paths.

The required-clear benchmark intentionally excludes variant and fusion power, so
neither optional system becomes mandatory for Stage 15 completion.
"""
from __future__ import annotations

import bisect
import math
from collections import Counter

import numpy as np

from v1_gate_economy import (
    Strategy,
    simulate,
    unlocked_slots_at as slots_at,
    combat_multiplier_at as combat_at,
    performance_multiplier,
    BUDGET_SPLIT_START_MINUTES,
    early_stage,
)


def stage_at_state(state, hour: float) -> int:
    if hour < BUDGET_SPLIT_START_MINUTES / 60.0:
        return early_stage(hour * 60.0)
    stage = 3
    for gate, unlocked_at in state.gate_times.items():
        if unlocked_at <= hour:
            stage = max(stage, gate)
    return stage


ACCOUNT_COUNT = 10_000
RANDOM_SEED = 20260812

# The ideal action benchmark needs about 9,550 EC for a 120-second clear.
# Support-budget correction and the residual runtime budget raise the rounded
# input requirement to about 10,020. A small safety margin produces 10,050.
FIRST_CLEAR_EC = 10_050.0
STABLE_FARM_EC = 12_200.0
MILESTONES = [step / 2.0 for step in range(16, 45)]  # 8h through 22h

DENOMINATORS = np.array(
    [10] * 6
    + [20] * 6
    + [100] * 6
    + [200] * 6
    + [256]
    + [1_000] * 6
    + [
        12_500,
        78_125,
        1_250_000,
        7_812_500,
        48_828_125,
        781_250_000,
        4_882_812_500,
        30_517_578_125,
        488_281_250_000,
        3_051_757_812_500,
        19_073_486_328_125,
        305_175_781_250_000,
        1_953_125_000_000_000,
        10_000_000_000_000_000,
        500_000_000_000_000_000,
        3_125_000_000_000_000_000,
        20_000_000_000_000_000_000,
        50_000_000_000_000_000_000,
        100_000_000_000_000_000_000,
    ],
    dtype=np.float64,
)
POWER = (DENOMINATORS / 10.0) ** 0.20
ROLE_CODES = np.array(
    [
        0, 1, 2, 3, 4, 5,
        0, 1, 2, 3, 4, 5,
        0, 1, 2, 3, 4, 5,
        0, 1, 2, 3, 4, 5,
        1,
        0, 1, 2, 3, 4, 5,
        0, 2, 3, 4, 5, 1,
        0, 2, 3, 4, 5, 1,
        0, 2, 3, 4, 5, 1,
        0,
    ]
)

SCENARIOS = [
    Strategy("fast_gate", 0.50, 0.20, 0.20, 0.10, 1.00),
    Strategy("balanced", 0.35, 0.30, 0.25, 0.10, 1.00),
    Strategy("slow_60pct", 0.35, 0.30, 0.25, 0.10, 0.60),
    Strategy("slow_50pct", 0.35, 0.30, 0.25, 0.10, 0.50),
]
QUANTILES = [0.10, 0.25, 0.50, 0.75, 0.90]


def luck_bonus(points: int) -> float:
    return 0.034 * min(points, 25) + 0.004 * max(points - 25, 0)


def roll_rate(points: int) -> float:
    return 1.0 + 0.01 * min(points, 25) + 0.0025 * max(points - 25, 0)


def roll_interval(base: float, points: int) -> float:
    return max(2.0, base / roll_rate(points))


def rebirth_count(state, hour: float) -> int:
    return bisect.bisect_right(state.rebirth_times, hour)


def compression_for_roll(state, hour: float, roll_number: int) -> float:
    base = (
        1.0
        + 0.245 * (stage_at_state(state, hour) - 1)
        + luck_bonus(rebirth_count(state, hour))
    )
    if roll_number % 100 == 0:
        return min(base + 0.65, 6.05)
    if roll_number % 10 == 0:
        return min(base + 0.25, 5.65)
    return min(base, 5.40)


def final_weights(compression: float) -> np.ndarray:
    raw = 10.0 ** (
        -(1.0 + (np.log10(DENOMINATORS) - 1.0) / compression)
    )
    return raw / raw.sum()


def grouped_rolls(state) -> list[Counter]:
    milestone_seconds = [hour * 3_600.0 for hour in MILESTONES]
    groups = [Counter() for _ in MILESTONES]

    def add_roll(seconds: float, number: int) -> None:
        index = bisect.bisect_left(milestone_seconds, seconds)
        if index < len(groups):
            compression = compression_for_roll(state, seconds / 3_600.0, number)
            groups[index][round(compression, 12)] += 1

    add_roll(0.0, 1)
    roll_number = 1
    next_roll = 12.0
    while next_roll <= milestone_seconds[-1]:
        roll_number += 1
        add_roll(next_roll, roll_number)
        hour = next_roll / 3_600.0
        base = 4.0 if next_roll < 79.0 else 3.6
        next_roll += roll_interval(base, rebirth_count(state, hour))
    return groups


def formation_power(owned, slots: int, role_cap: int) -> np.ndarray:
    account_count = owned.shape[0]
    remaining_slots = np.full(account_count, slots, dtype=np.int16)
    role_remaining = np.full((account_count, 6), role_cap, dtype=np.int16)
    total = np.zeros(account_count)

    for tower_index in range(49, -1, -1):
        role = ROLE_CODES[tower_index]
        take = np.minimum(
            owned[:, tower_index],
            np.minimum(remaining_slots, role_remaining[:, role]),
        )
        total += take * POWER[tower_index]
        remaining_slots -= take
        role_remaining[:, role] -= take
    return total


def crossing(rows, quantile_index: int, threshold: float, gate_time: float):
    for row in rows:
        if (
            row["hour"] + 1e-9 >= gate_time
            and row["quantiles"][quantile_index] >= threshold
        ):
            return row["hour"]
    return None


def simulate_path(strategy: Strategy, seed: int):
    state = simulate(strategy)
    rng = np.random.default_rng(seed)
    owned = np.zeros((ACCOUNT_COUNT, 50), dtype=np.int32)
    rows = []

    for hour, group in zip(MILESTONES, grouped_rolls(state)):
        for compression, count in sorted(group.items()):
            owned += rng.multinomial(
                count,
                final_weights(compression),
                size=ACCOUNT_COUNT,
            ).astype(np.int32)

        slots = slots_at(state, hour)
        role_cap = max(2, math.ceil(slots / 3))
        base = formation_power(owned, slots, role_cap)
        final = (
            base
            * performance_multiplier(rebirth_count(state, hour))
            * combat_at(state, hour)
        )
        rows.append(
            {
                "hour": hour,
                "stage": stage_at_state(state, hour),
                "slots": slots,
                "rebirths": rebirth_count(state, hour),
                "combat_multiplier": combat_at(state, hour),
                "quantiles": [
                    float(value) for value in np.quantile(final, QUANTILES)
                ],
            }
        )

    gate_time = state.gate_times[15]
    return {
        "gate15": gate_time,
        "rows": rows,
        "first_clear": {
            str(quantile): crossing(rows, index, FIRST_CLEAR_EC, gate_time)
            for index, quantile in enumerate(QUANTILES)
        },
        "stable_farm": {
            str(quantile): crossing(rows, index, STABLE_FARM_EC, gate_time)
            for index, quantile in enumerate(QUANTILES)
        },
    }


def run():
    results = {
        scenario.name: simulate_path(scenario, RANDOM_SEED + index)
        for index, scenario in enumerate(SCENARIOS)
    }

    assert 8.0 <= results["fast_gate"]["first_clear"]["0.9"] <= 10.0
    assert 12.0 <= results["balanced"]["first_clear"]["0.5"] <= 15.0
    assert 14.0 <= results["balanced"]["first_clear"]["0.25"] <= 16.0
    assert 18.0 <= results["slow_60pct"]["first_clear"]["0.1"] <= 22.0
    assert 18.0 <= results["slow_50pct"]["first_clear"]["0.5"] <= 22.0
    return results


def main() -> None:
    results = run()
    for name, row in results.items():
        print(
            "\n",
            name,
            "gate", row["gate15"],
            "first", row["first_clear"],
            "stable", row["stable_farm"],
        )
    print(
        "All final path assertions passed. "
        "Variants and fusion are excluded from required-clear power."
    )


if __name__ == "__main__":
    main()
