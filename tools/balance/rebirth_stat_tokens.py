#!/usr/bin/env python3
"""Reproduce the provisional V1 rebirth-stat token benchmark.

The model combines:
- four stat tokens per rebirth,
- the provisional rebirth schedule used only for milestone balancing,
- stage luck, luck-stat compression, golden/diamond rolls,
- roll-speed stat effects,
- simple performance and currency multipliers.

It does not replace the future Defense XP curve simulation.
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

TOKENS_PER_REBIRTH = 4
FIRST_REBIRTH_HOURS = 1.0 / 6.0
SECOND_REBIRTH_HOURS = 0.5
LATER_REBIRTH_INTERVAL_HOURS = 2.0 / 3.0

STAGE_COEFFICIENT = 0.245
NORMAL_COMPRESSION_CAP = 5.40
GOLDEN_COMPRESSION_BONUS = 0.25
GOLDEN_COMPRESSION_CAP = 5.65
DIAMOND_COMPRESSION_BONUS = 0.65
DIAMOND_COMPRESSION_CAP = 6.05

BASE_AUTO_ROLL_INTERVAL = 4.0
COIN_SPEED_NODE_INTERVAL = 3.6
ROLL_SPEED_INTERVAL_FLOOR = 2.0

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
    luck_per_rebirth: int
    performance_per_rebirth: int
    currency_per_rebirth: int
    roll_speed_per_rebirth: int

    def validate(self) -> None:
        total = (
            self.luck_per_rebirth
            + self.performance_per_rebirth
            + self.currency_per_rebirth
            + self.roll_speed_per_rebirth
        )
        if total > TOKENS_PER_REBIRTH:
            raise ValueError(f"{self.name}: allocation exceeds token reward")


SCENARIOS = [
    AllocationScenario("unallocated", 0, 0, 0, 0),
    AllocationScenario("balanced", 1, 1, 1, 1),
    AllocationScenario("luck_heavy", 2, 1, 0, 1),
    AllocationScenario("luck_focused", 4, 0, 0, 0),
    AllocationScenario("speed_focused", 0, 0, 0, 4),
]


def rebirth_count(active_hours: float) -> int:
    if active_hours < FIRST_REBIRTH_HOURS:
        return 0
    if active_hours < SECOND_REBIRTH_HOURS:
        return 1
    return 2 + int(
        (active_hours - SECOND_REBIRTH_HOURS) / LATER_REBIRTH_INTERVAL_HOURS
        + 1e-9
    )


def points(active_hours: float, scenario: AllocationScenario, stat: str) -> int:
    count = rebirth_count(active_hours)
    per_rebirth = {
        "luck": scenario.luck_per_rebirth,
        "performance": scenario.performance_per_rebirth,
        "currency": scenario.currency_per_rebirth,
        "roll_speed": scenario.roll_speed_per_rebirth,
    }[stat]
    return count * per_rebirth


def luck_compression_bonus(level: int) -> float:
    return 0.0315 * min(level, 25) + 0.0090 * max(level - 25, 0)


def performance_multiplier(level: int) -> float:
    value = 1.0 + 0.025 * min(level, 25) + 0.005 * max(level - 25, 0)
    return min(value, 2.50)


def currency_multiplier(level: int) -> float:
    value = 1.0 + 0.040 * min(level, 25) + 0.010 * max(level - 25, 0)
    return min(value, 4.00)


def roll_rate_multiplier(level: int) -> float:
    return 1.0 + 0.010 * min(level, 25) + 0.0025 * max(level - 25, 0)


def final_roll_interval(base_interval: float, level: int) -> float:
    return max(
        ROLL_SPEED_INTERVAL_FLOOR,
        base_interval / roll_rate_multiplier(level),
    )


def stage_at(active_hours: float) -> int:
    for end_hour, stage in STAGE_TIMELINE:
        if active_hours < end_hour:
            return stage
    raise AssertionError("unreachable")


def final_weights(compression: float) -> list[float]:
    raw_weights = []
    for denominator in DENOMINATORS:
        base_log_odds = math.log10(denominator)
        adjusted_log_odds = 1.0 + (base_log_odds - 1.0) / compression
        raw_weights.append(10.0 ** (-adjusted_log_odds))
    total = sum(raw_weights)
    return [weight / total for weight in raw_weights]


def top_tower_probability(compression: float) -> float:
    return final_weights(compression)[-1]


def compression_for_roll(
    active_hours: float,
    total_roll_number: int,
    scenario: AllocationScenario,
) -> float:
    stage = stage_at(active_hours)
    luck_level = points(active_hours, scenario, "luck")
    base = (
        1.0
        + STAGE_COEFFICIENT * (stage - 1)
        + luck_compression_bonus(luck_level)
    )

    if total_roll_number % 100 == 0:
        return min(
            base + DIAMOND_COMPRESSION_BONUS,
            DIAMOND_COMPRESSION_CAP,
        )
    if total_roll_number % 10 == 0:
        return min(
            base + GOLDEN_COMPRESSION_BONUS,
            GOLDEN_COMPRESSION_CAP,
        )
    return min(base, NORMAL_COMPRESSION_CAP)


def simulate_scenario(
    scenario: AllocationScenario,
    end_hours: float = 30.0,
) -> tuple[dict[float, int], dict[float, float]]:
    scenario.validate()

    roll_counts: dict[float, int] = {}
    cumulative_chances: dict[float, float] = {}
    milestone_index = 0

    roll_number = 1
    survival = 1.0 - top_tower_probability(
        compression_for_roll(0.0, roll_number, scenario)
    )

    next_roll_seconds = 12.0
    while next_roll_seconds <= end_hours * 3_600.0:
        roll_number += 1
        active_hours = next_roll_seconds / 3_600.0
        compression = compression_for_roll(active_hours, roll_number, scenario)
        survival *= 1.0 - top_tower_probability(compression)

        while (
            milestone_index < len(MILESTONES_HOURS)
            and next_roll_seconds >= MILESTONES_HOURS[milestone_index] * 3_600.0
        ):
            milestone = MILESTONES_HOURS[milestone_index]
            roll_counts[milestone] = roll_number
            cumulative_chances[milestone] = 1.0 - survival
            milestone_index += 1

        base_interval = (
            BASE_AUTO_ROLL_INTERVAL
            if next_roll_seconds < 79.0
            else COIN_SPEED_NODE_INTERVAL
        )
        speed_level = points(active_hours, scenario, "roll_speed")
        next_roll_seconds += final_roll_interval(base_interval, speed_level)

    while milestone_index < len(MILESTONES_HOURS):
        milestone = MILESTONES_HOURS[milestone_index]
        roll_counts[milestone] = roll_number
        cumulative_chances[milestone] = 1.0 - survival
        milestone_index += 1

    return roll_counts, cumulative_chances


def print_report() -> None:
    print("REBIRTH AND TOKEN MILESTONES")
    for hours in MILESTONES_HOURS:
        count = rebirth_count(hours)
        print(
            f"{hours:>5.2f} h: rebirths={count:>2}, "
            f"earned_tokens={count * TOKENS_PER_REBIRTH:>3}"
        )

    print("\nBALANCED BRANCH EFFECTS")
    balanced = SCENARIOS[1]
    for hours in [0.25, 2.0, 5.0, 13.5, 15.0, 30.0]:
        level = points(hours, balanced, "luck")
        interval = final_roll_interval(
            COIN_SPEED_NODE_INTERVAL,
            points(hours, balanced, "roll_speed"),
        )
        print(
            f"{hours:>5.2f} h: level={level:>2}, "
            f"luck_bonus={luck_compression_bonus(level):.4f}, "
            f"performance=x{performance_multiplier(level):.3f}, "
            f"currency=x{currency_multiplier(level):.3f}, "
            f"roll_interval={interval:.3f}s"
        )

    print("\nTOP-TOWER ACQUISITION CHANCE")
    scenario_results = {}
    for scenario in SCENARIOS:
        roll_counts, chances = simulate_scenario(scenario)
        scenario_results[scenario.name] = (roll_counts, chances)
        rendered = ", ".join(
            f"{hours:g}h={chances[hours] * 100:.3f}%/{roll_counts[hours]:,}rolls"
            for hours in [5.0, 13.5, 15.0, 25.0, 30.0]
        )
        print(f"{scenario.name:>13}: {rendered}")

    balanced_chances = scenario_results["balanced"][1]
    assert 0.03 <= balanced_chances[13.5] <= 0.05
    assert 0.03 <= balanced_chances[15.0] <= 0.05
    assert 0.15 <= balanced_chances[25.0] <= 0.25
    assert 0.15 <= balanced_chances[30.0] <= 0.25

    assert performance_multiplier(10_000) == 2.50
    assert currency_multiplier(10_000) == 4.00
    assert final_roll_interval(COIN_SPEED_NODE_INTERVAL, 10_000) == 2.00
    assert final_weights(NORMAL_COMPRESSION_CAP)[0] > 0.0
    assert final_weights(NORMAL_COMPRESSION_CAP)[-1] < final_weights(NORMAL_COMPRESSION_CAP)[-2]

    print("\nAll benchmark assertions passed.")


if __name__ == "__main__":
    print_report()
