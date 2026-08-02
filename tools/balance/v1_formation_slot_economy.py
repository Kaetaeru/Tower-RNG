#!/usr/bin/env python3
"""Simulate V1 formation-slot economy and role-limited formation power.

The model uses the established stage, rebirth, luck, currency, roll-speed, and
50-tower probability benchmarks. Slot prices are tested with a planning
allocation in which 30% of collected coins after 8.5 active minutes is reserved
for sequential formation-slot nodes. This is a benchmark assumption, not an
enforced player spending rule.
"""

from __future__ import annotations

import bisect
import math
from collections import Counter
from dataclasses import dataclass

import numpy as np

TOKENS_PER_REBIRTH = 4
FIRST_REBIRTH_XP = 7_000
PERFORMANCE_CLEAR_SPEED_ELASTICITY = 0.60

PLANNED_FARM_CYCLE_SECONDS = [
    56.28,
    60.0,
    65.0,
    62.0,
    68.0,
    75.0,
    68.0,
    75.0,
    82.0,
    76.0,
    84.0,
    90.0,
    86.0,
    93.0,
    100.0,
]

STABLE_FARM_STAGE_TIMELINE: list[tuple[float, int]] = [
    (3.5 / 60.0, 1),
    (10.0 / 60.0, 2),
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

ROLL_STAGE_TIMELINE: list[tuple[float, int]] = [
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

ROLES = [
    "single", "aoe", "control", "finisher", "support", "large",
    "single", "aoe", "control", "finisher", "support", "large",
    "single", "aoe", "control", "finisher", "support", "large",
    "single", "aoe", "control", "finisher", "support", "large",
    "aoe",
    "single", "aoe", "control", "finisher", "support", "large",
    "single", "control", "finisher", "support", "large", "aoe",
    "single", "control", "finisher", "support", "large", "aoe",
    "single", "control", "finisher", "support", "large", "aoe",
    "single",
]

POWER = np.array([(denominator / 10.0) ** 0.20 for denominator in DENOMINATORS])

STAGE_COEFFICIENT = 0.245
NORMAL_COMPRESSION_CAP = 5.40
GOLDEN_COMPRESSION_BONUS = 0.25
GOLDEN_COMPRESSION_CAP = 5.65
DIAMOND_COMPRESSION_BONUS = 0.65
DIAMOND_COMPRESSION_CAP = 6.05

BASE_AUTO_ROLL_INTERVAL = 4.0
COIN_SPEED_NODE_INTERVAL = 3.6
ROLL_SPEED_INTERVAL_FLOOR = 2.0

ACCOUNT_COUNT = 20_000
RANDOM_SEED = 20260802
MILESTONES_HOURS = [0.25, 0.50, 2.0, 5.0, 12.0, 13.5, 15.0, 30.0]

SLOT_PRICES = [
    1_200,
    15_000,
    170_000,
    1_500_000,
    9_000_000,
    80_000_000,
    400_000_000,
    2_300_000_000,
]
SLOT_BUDGET_START_MINUTES = 8.5
SLOT_COIN_SHARE = 0.30


@dataclass(frozen=True)
class Scenario:
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
    Scenario("unallocated", 0, 0, 0, 0),
    Scenario("balanced", 1, 1, 1, 1),
    Scenario("collector_hybrid", 2, 1, 0, 1),
    Scenario("currency_focused", 0, 0, 4, 0),
    Scenario("performance_focused", 0, 4, 0, 0),
]


def stage_scale(stage: int) -> float:
    return 10.0 ** ((stage - 1) / 3.0)


def stage_reward_scale(stage: int) -> float:
    return stage_scale(stage) * 1.08 ** (stage - 1)


def planned_defense_xp_per_minute(stage: int) -> float:
    cycle_xp = 400.0 * stage_reward_scale(stage)
    return cycle_xp * 60.0 / PLANNED_FARM_CYCLE_SECONDS[stage - 1]


def stage_at(active_hours: float, timeline: list[tuple[float, int]]) -> int:
    for end_hour, stage in timeline:
        if active_hours < end_hour:
            return stage
    raise AssertionError("unreachable")


def target_rebirth_minutes(next_rebirth_number: int) -> float:
    if next_rebirth_number == 2:
        return 20.0
    if next_rebirth_number == 3:
        return 35.0
    if next_rebirth_number <= 50:
        return 50.0
    tier = (next_rebirth_number - 1) // 50
    return min(70.0, 50.0 + 5.0 * tier)


def round_three_significant(value: float) -> float:
    decimal_places = 2 - math.floor(math.log10(value))
    return float(round(value, decimal_places))


def required_defense_xp(next_rebirth_number: int, anchor_stage: int) -> float:
    if next_rebirth_number == 1:
        return float(FIRST_REBIRTH_XP)
    raw = (
        planned_defense_xp_per_minute(anchor_stage)
        * target_rebirth_minutes(next_rebirth_number)
    )
    return round_three_significant(raw)


def performance_multiplier(points: int) -> float:
    raw = 1.0 + 0.025 * min(points, 25) + 0.005 * max(points - 25, 0)
    return min(2.50, raw)


def defense_xp_rate_multiplier(performance_points: int) -> float:
    return performance_multiplier(performance_points) ** PERFORMANCE_CLEAR_SPEED_ELASTICITY


def simulate_rebirths(
    performance_points_per_rebirth: int,
    end_hours: float = 30.0,
    tick_seconds: float = 0.25,
) -> list[float]:
    active_seconds = 0.0
    defense_xp = 0.0
    rebirth_count = 0
    performance_points = 0
    anchor_stage = 1
    requirement = required_defense_xp(1, anchor_stage)
    events: list[float] = []

    while active_seconds < end_hours * 3_600.0:
        active_hours = active_seconds / 3_600.0
        stage = stage_at(active_hours, STABLE_FARM_STAGE_TIMELINE)

        if stage > anchor_stage:
            old_requirement = requirement
            anchor_stage = stage
            if rebirth_count >= 1:
                requirement = required_defense_xp(
                    rebirth_count + 1,
                    anchor_stage,
                )
                defense_xp = defense_xp / old_requirement * requirement

        xp_per_second = (
            planned_defense_xp_per_minute(stage)
            / 60.0
            * defense_xp_rate_multiplier(performance_points)
        )
        defense_xp += xp_per_second * tick_seconds
        active_seconds += tick_seconds

        if defense_xp + 1e-9 < requirement:
            continue

        rebirth_count += 1
        events.append(active_seconds / 3_600.0)
        defense_xp = 0.0
        performance_points += performance_points_per_rebirth
        requirement = required_defense_xp(rebirth_count + 1, anchor_stage)

    return events


def rebirth_count_at(events: list[float], active_hours: float) -> int:
    return sum(event <= active_hours for event in events)


def points(
    events: list[float],
    active_hours: float,
    scenario: Scenario,
    stat_name: str,
) -> int:
    per_rebirth = {
        "luck": scenario.luck_per_rebirth,
        "performance": scenario.performance_per_rebirth,
        "currency": scenario.currency_per_rebirth,
        "roll_speed": scenario.roll_speed_per_rebirth,
    }[stat_name]
    return rebirth_count_at(events, active_hours) * per_rebirth


def luck_compression_bonus(level: int) -> float:
    return 0.0340 * min(level, 25) + 0.0040 * max(level - 25, 0)


def currency_multiplier(level: int) -> float:
    raw = 1.0 + 0.040 * min(level, 25) + 0.010 * max(level - 25, 0)
    return min(4.00, raw)


def roll_rate_multiplier(level: int) -> float:
    return 1.0 + 0.010 * min(level, 25) + 0.0025 * max(level - 25, 0)


def final_roll_interval(base_interval: float, level: int) -> float:
    return max(
        ROLL_SPEED_INTERVAL_FLOOR,
        base_interval / roll_rate_multiplier(level),
    )


def final_weights(compression: float) -> np.ndarray:
    raw_weights = []
    for denominator in DENOMINATORS:
        adjusted_log_odds = (
            1.0
            + (math.log10(denominator) - 1.0) / compression
        )
        raw_weights.append(10.0 ** (-adjusted_log_odds))
    total = sum(raw_weights)
    return np.array([weight / total for weight in raw_weights])


def compression_for_roll(
    active_hours: float,
    total_roll_number: int,
    scenario: Scenario,
    events: list[float],
) -> float:
    stage = stage_at(active_hours, ROLL_STAGE_TIMELINE)
    luck_level = points(events, active_hours, scenario, "luck")
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


def grouped_rolls(
    scenario: Scenario,
    events: list[float],
) -> list[Counter[float]]:
    milestone_seconds = [hours * 3_600.0 for hours in MILESTONES_HOURS]
    groups: list[Counter[float]] = [Counter() for _ in milestone_seconds]

    def add_roll(active_seconds: float, roll_number: int) -> None:
        interval_index = bisect.bisect_left(milestone_seconds, active_seconds)
        if interval_index >= len(groups):
            return
        compression = compression_for_roll(
            active_seconds / 3_600.0,
            roll_number,
            scenario,
            events,
        )
        groups[interval_index][round(compression, 12)] += 1

    add_roll(0.0, 1)
    roll_number = 1
    next_roll_seconds = 12.0
    while next_roll_seconds <= milestone_seconds[-1]:
        roll_number += 1
        add_roll(next_roll_seconds, roll_number)
        active_hours = next_roll_seconds / 3_600.0
        base_interval = (
            BASE_AUTO_ROLL_INTERVAL
            if next_roll_seconds < 79.0
            else COIN_SPEED_NODE_INTERVAL
        )
        speed_points = points(
            events,
            active_hours,
            scenario,
            "roll_speed",
        )
        next_roll_seconds += final_roll_interval(
            base_interval,
            speed_points,
        )

    return groups


def planned_coin_per_minute(
    active_hours: float,
    scenario: Scenario,
    events: list[float],
) -> float:
    stage = stage_at(active_hours, STABLE_FARM_STAGE_TIMELINE)
    active_minutes = active_hours * 60.0

    if active_minutes < 0.67:
        collection_efficiency = 0.75
    elif active_minutes < 3.55:
        collection_efficiency = 0.85
    else:
        collection_efficiency = 0.92

    coin_tree_multiplier = 1.0 if active_minutes < 8.35 else 1.15
    currency_points = points(events, active_hours, scenario, "currency")

    return (
        planned_defense_xp_per_minute(stage)
        * collection_efficiency
        * coin_tree_multiplier
        * currency_multiplier(currency_points)
    )


def slot_purchase_times(
    scenario: Scenario,
    events: list[float],
    end_hours: float = 30.0,
    tick_minutes: float = 0.025,
) -> list[float]:
    slot_budget = 0.0
    price_index = 0
    purchase_times: list[float] = []

    total_steps = int(end_hours * 60.0 / tick_minutes)
    for step in range(total_steps + 1):
        active_minutes = step * tick_minutes
        active_hours = active_minutes / 60.0

        if active_minutes >= SLOT_BUDGET_START_MINUTES:
            slot_budget += (
                planned_coin_per_minute(active_hours, scenario, events)
                * tick_minutes
                * SLOT_COIN_SHARE
            )

        while (
            price_index < len(SLOT_PRICES)
            and slot_budget + 1e-9 >= SLOT_PRICES[price_index]
        ):
            slot_budget -= SLOT_PRICES[price_index]
            purchase_times.append(active_hours)
            price_index += 1

    return purchase_times


def total_slots_at(purchase_times: list[float], active_hours: float) -> int:
    return 4 + sum(time <= active_hours for time in purchase_times)


def role_cap(total_slots: int) -> int:
    return max(2, math.ceil(total_slots / 3.0))


def unconstrained_top_k(counts: np.ndarray, total_slots: int) -> np.ndarray:
    remaining = np.full(counts.shape[0], total_slots, dtype=np.int16)
    total = np.zeros(counts.shape[0])

    for tower_index in range(len(DENOMINATORS) - 1, -1, -1):
        take = np.minimum(counts[:, tower_index], remaining)
        total += take * POWER[tower_index]
        remaining -= take

    return total


def role_constrained_top_k(counts: np.ndarray, total_slots: int) -> np.ndarray:
    per_role_cap = role_cap(total_slots)
    remaining = np.full(counts.shape[0], total_slots, dtype=np.int16)
    total = np.zeros(counts.shape[0])
    used_by_role = {
        role: np.zeros(counts.shape[0], dtype=np.int16)
        for role in set(ROLES)
    }

    for tower_index in range(len(DENOMINATORS) - 1, -1, -1):
        role = ROLES[tower_index]
        role_remaining = np.maximum(
            0,
            per_role_cap - used_by_role[role],
        )
        take = np.minimum(
            np.minimum(counts[:, tower_index], remaining),
            role_remaining,
        )
        total += take * POWER[tower_index]
        remaining -= take
        used_by_role[role] += take

    return total


def quantiles(values: np.ndarray) -> list[float]:
    return [
        float(value)
        for value in np.quantile(values, [0.10, 0.50, 0.90, 0.99])
    ]


def run() -> dict[str, dict[str, object]]:
    if len(DENOMINATORS) != 50 or len(ROLES) != 50:
        raise AssertionError("V1 ladder must contain 50 towers")

    expected_roles = Counter({
        "single": 9,
        "aoe": 9,
        "control": 8,
        "finisher": 8,
        "support": 8,
        "large": 8,
    })
    if Counter(ROLES) != expected_roles:
        raise AssertionError("unexpected role distribution")

    results: dict[str, dict[str, object]] = {}

    for scenario_index, scenario in enumerate(SCENARIOS):
        scenario.validate()
        events = simulate_rebirths(scenario.performance_per_rebirth)
        purchase_times = slot_purchase_times(scenario, events)
        roll_groups = grouped_rolls(scenario, events)
        rng = np.random.default_rng(RANDOM_SEED + scenario_index)
        owned = np.zeros(
            (ACCOUNT_COUNT, len(DENOMINATORS)),
            dtype=np.int32,
        )
        cumulative_rolls = 0
        rows: dict[float, dict[str, object]] = {}

        for milestone_index, group in enumerate(roll_groups):
            for compression, roll_count in sorted(group.items()):
                owned += rng.multinomial(
                    roll_count,
                    final_weights(compression),
                    size=ACCOUNT_COUNT,
                ).astype(np.int32)

            cumulative_rolls += sum(group.values())
            active_hours = MILESTONES_HOURS[milestone_index]
            total_slots = total_slots_at(purchase_times, active_hours)
            performance_points = points(
                events,
                active_hours,
                scenario,
                "performance",
            )
            performance = performance_multiplier(performance_points)
            raw_power = unconstrained_top_k(owned, total_slots) * performance
            constrained_power = (
                role_constrained_top_k(owned, total_slots)
                * performance
            )

            rows[active_hours] = {
                "slots": total_slots,
                "role_cap": role_cap(total_slots),
                "rolls": cumulative_rolls,
                "rebirths": rebirth_count_at(events, active_hours),
                "performance": performance,
                "unconstrained_quantiles": quantiles(raw_power),
                "role_constrained_quantiles": quantiles(constrained_power),
                "retention_quantiles": quantiles(
                    constrained_power / raw_power
                ),
            }

        results[scenario.name] = {
            "slot_purchase_times": purchase_times,
            "rows": rows,
        }

    balanced = results["balanced"]
    balanced_times = balanced["slot_purchase_times"]
    if not isinstance(balanced_times, list):
        raise AssertionError("unexpected purchase-time type")
    if not 12.5 <= balanced_times[-1] <= 14.5:
        raise AssertionError("balanced slot 12 must unlock near completion")

    balanced_rows = balanced["rows"]
    if not isinstance(balanced_rows, dict):
        raise AssertionError("unexpected row type")
    if balanced_rows[15.0]["slots"] != 12:
        raise AssertionError("balanced account must have 12 slots by 15h")
    if balanced_rows[30.0]["slots"] != 12:
        raise AssertionError("slot cap must remain 12")

    return results


def render(value: float) -> str:
    if value >= 1_000:
        return f"{value:,.0f}"
    if value >= 100:
        return f"{value:,.1f}"
    return f"{value:,.2f}"


def print_report(results: dict[str, dict[str, object]]) -> None:
    print(f"ACCOUNTS PER SCENARIO: {ACCOUNT_COUNT:,}")
    print(
        "SLOT MODEL: reserve 30% of collected coins after "
        "8.5 active minutes"
    )

    for scenario in SCENARIOS:
        result = results[scenario.name]
        purchase_times = result["slot_purchase_times"]
        if not isinstance(purchase_times, list):
            raise AssertionError("unexpected purchase-time type")
        rendered_times = ", ".join(
            f"S{slot}={hours * 60.0:.1f}m"
            for slot, hours in enumerate(purchase_times, start=5)
        )
        print(f"\n{scenario.name}: {rendered_times}")

        rows = result["rows"]
        if not isinstance(rows, dict):
            raise AssertionError("unexpected row type")
        for active_hours in MILESTONES_HOURS:
            row = rows[active_hours]
            power = row["role_constrained_quantiles"]
            retention = row["retention_quantiles"]
            print(
                f"  {active_hours:>5.2f}h "
                f"slots={row['slots']} cap={row['role_cap']} "
                f"R={row['rebirths']} rolls={row['rolls']:,} "
                f"EC={render(power[0])}/{render(power[1])}/"
                f"{render(power[2])} "
                f"median-retention={retention[1] * 100.0:.1f}%"
            )

    print("\nAll formation-slot benchmark assertions passed.")


if __name__ == "__main__":
    print_report(run())
