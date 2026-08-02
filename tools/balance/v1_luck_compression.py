#!/usr/bin/env python3
"""Reproduce the provisional V1 luck-compression benchmark.

The script uses exact catalog denominators but floating-point log weights for the
runtime luck model. It deterministically calculates the probability of owning
at least one copy of the V1 top normal-roll tower by each time milestone.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


DENOMINATORS: list[int] = (
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
    ]
)

STAGE_COEFFICIENT = 0.245
LUCK_TOKEN_COEFFICIENT = 0.040
NORMAL_CAP = 5.40
GOLDEN_BONUS = 0.25
GOLDEN_CAP = 5.65
DIAMOND_BONUS = 0.65
DIAMOND_CAP = 6.05

# Central V1 stage-entry plan in active-play hours.
STAGE_TIMELINE: list[tuple[float, int]] = [
    (0.15, 1),
    (0.30, 2),
    (0.50, 3),
    (1.00, 4),
    (1.50, 5),
    (2.00, 6),
    (3.00, 7),
    (4.00, 8),
    (5.00, 9),
    (6.50, 10),
    (8.00, 11),
    (9.50, 12),
    (10.50, 13),
    (12.00, 14),
    (float("inf"), 15),
]

MILESTONES_HOURS = [0.25, 0.50, 2.0, 5.0, 12.0, 13.5, 15.0, 20.0, 25.0, 30.0]


@dataclass(frozen=True)
class AllocationScenario:
    name: str
    luck_tokens_per_hour_after_30m: float


SCENARIOS = [
    AllocationScenario("none", 0.00),
    AllocationScenario("light", 0.75),
    AllocationScenario("balanced", 1.50),
    AllocationScenario("focused", 2.25),
]


def stage_at(active_hours: float) -> int:
    for end_hour, stage in STAGE_TIMELINE:
        if active_hours < end_hour:
            return stage
    raise AssertionError("unreachable")


def roll_times_seconds(end_hours: float = 30.0) -> list[float]:
    """First manual roll, then 4.0 s auto rolls, then 3.6 s after 1:19."""
    times = [0.0]

    next_roll = 12.0  # Auto-roll is bought at 0:08; first auto result at 0:12.
    while next_roll <= 79.0:
        times.append(next_roll)
        next_roll += 4.0

    next_roll = 82.6  # Speed I is bought at 1:19; next full 3.6 s cycle.
    while next_roll < end_hours * 3_600.0:
        times.append(next_roll)
        next_roll += 3.6

    return times


def final_weights(compression: float) -> list[float]:
    raw = []
    for denominator in DENOMINATORS:
        base_log_odds = math.log10(denominator)
        adjusted_log_odds = 1.0 + (base_log_odds - 1.0) / compression
        raw.append(10.0 ** (-adjusted_log_odds))
    total = sum(raw)
    return [weight / total for weight in raw]


def top_tower_probability(compression: float) -> float:
    return final_weights(compression)[-1]


def compression_for_roll(
    active_hours: float,
    total_roll_number: int,
    luck_token_rate: float,
) -> float:
    stage = stage_at(active_hours)
    allocated_luck_tokens = max(0.0, active_hours - 0.5) * luck_token_rate
    base = (
        1.0
        + STAGE_COEFFICIENT * (stage - 1)
        + LUCK_TOKEN_COEFFICIENT * allocated_luck_tokens
    )

    if total_roll_number % 100 == 0:
        return min(base + DIAMOND_BONUS, DIAMOND_CAP)
    if total_roll_number % 10 == 0:
        return min(base + GOLDEN_BONUS, GOLDEN_CAP)
    return min(base, NORMAL_CAP)


def cumulative_top_chance(scenario: AllocationScenario) -> dict[float, float]:
    survival = 1.0
    results: dict[float, float] = {}
    milestone_index = 0

    for roll_number, seconds in enumerate(roll_times_seconds(), start=1):
        active_hours = seconds / 3_600.0
        compression = compression_for_roll(
            active_hours,
            roll_number,
            scenario.luck_tokens_per_hour_after_30m,
        )
        survival *= 1.0 - top_tower_probability(compression)

        while (
            milestone_index < len(MILESTONES_HOURS)
            and seconds >= MILESTONES_HOURS[milestone_index] * 3_600.0
        ):
            milestone = MILESTONES_HOURS[milestone_index]
            results[milestone] = 1.0 - survival
            milestone_index += 1

    while milestone_index < len(MILESTONES_HOURS):
        milestone = MILESTONES_HOURS[milestone_index]
        results[milestone] = 1.0 - survival
        milestone_index += 1

    return results


def print_report() -> None:
    times = roll_times_seconds()

    print("ROLL COUNTS")
    for hours in MILESTONES_HOURS:
        count = sum(seconds <= hours * 3_600.0 for seconds in times)
        print(f"{hours:>5.2f} h: {count:>6,d}")

    print("\nBASE COMPRESSION BY STAGE")
    for stage in [1, 3, 6, 9, 12, 15]:
        value = 1.0 + STAGE_COEFFICIENT * (stage - 1)
        print(f"Stage {stage:>2}: {value:.3f}")

    print("\nCUMULATIVE TOP-TOWER ACQUISITION CHANCE")
    for scenario in SCENARIOS:
        results = cumulative_top_chance(scenario)
        rendered = ", ".join(
            f"{hours:g}h={results[hours] * 100:.3f}%"
            for hours in MILESTONES_HOURS
        )
        print(f"{scenario.name:>8}: {rendered}")

    balanced = cumulative_top_chance(SCENARIOS[2])
    focused = cumulative_top_chance(SCENARIOS[3])

    assert 0.03 <= balanced[13.5] <= 0.05
    assert 0.03 <= balanced[15.0] <= 0.05
    assert 0.15 <= balanced[25.0] <= 0.25
    assert 0.15 <= balanced[30.0] <= 0.25
    assert focused[30.0] <= 0.25

    max_normal = final_weights(NORMAL_CAP)
    assert max_normal[0] > 0.0
    assert max_normal[-1] < max_normal[-2]

    print("\nAll benchmark assertions passed.")


if __name__ == "__main__":
    print_report()
