#!/usr/bin/env python3
"""Simulate V1 tower ownership and formation-power distributions.

Rolls with an identical final probability vector are sampled as one exact
multinomial group. The formation frontier uses owned copies, total slot count,
and tower EquivalentContribution only. It intentionally excludes unresolved
role caps, support/control overlap, variants, fusion, and coin-tree combat
bonuses.
"""

from __future__ import annotations

import bisect
from collections import Counter

import numpy as np

from rebirth_stat_tokens import (
    AllocationScenario,
    BASE_AUTO_ROLL_INTERVAL,
    COIN_SPEED_NODE_INTERVAL,
    DENOMINATORS,
    compression_for_roll,
    final_roll_interval,
    final_weights,
    points,
    rebirth_count_at,
    rebirth_events,
)
from v1_rebirth_xp_curve import TOKENS_PER_REBIRTH, performance_multiplier

ACCOUNT_COUNT = 20_000
RANDOM_SEED = 20260802
MILESTONES_HOURS = [0.25, 0.50, 2.0, 5.0, 15.0, 30.0]
FORMATION_SLOTS = [4, 6, 8, 10, 12]

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
POWER = np.array([(n / 10.0) ** 0.20 for n in DENOMINATORS])

SCENARIOS = [
    AllocationScenario("unallocated", 0, 0, 0, 0),
    AllocationScenario("balanced", 1, 1, 1, 1),
    AllocationScenario("collector_hybrid", 2, 1, 0, 1),
    AllocationScenario("luck_focused", 4, 0, 0, 0),
    AllocationScenario("performance_focused", 0, 4, 0, 0),
]


def grouped_rolls(scenario, events):
    milestone_seconds = [hours * 3600.0 for hours in MILESTONES_HOURS]
    groups = [Counter() for _ in MILESTONES_HOURS]

    def add_roll(active_seconds, roll_number):
        interval_index = bisect.bisect_left(milestone_seconds, active_seconds)
        if interval_index >= len(groups):
            return
        compression = compression_for_roll(
            active_seconds / 3600.0, roll_number, scenario, events
        )
        groups[interval_index][round(compression, 12)] += 1

    add_roll(0.0, 1)
    roll_number = 1
    next_roll_seconds = 12.0
    while next_roll_seconds <= milestone_seconds[-1]:
        roll_number += 1
        add_roll(next_roll_seconds, roll_number)
        active_hours = next_roll_seconds / 3600.0
        base_interval = (
            BASE_AUTO_ROLL_INTERVAL
            if next_roll_seconds < 79.0
            else COIN_SPEED_NODE_INTERVAL
        )
        speed_points = points(events, active_hours, scenario, "roll_speed")
        next_roll_seconds += final_roll_interval(base_interval, speed_points)
    return groups


def integer_quantiles(values):
    return [
        int(value)
        for value in np.quantile(
            values, [0.10, 0.50, 0.90, 0.99], method="nearest"
        )
    ]


def numeric_quantiles(values):
    return [float(value) for value in np.quantile(values, [0.10, 0.50, 0.90, 0.99])]


def formation_frontier(counts):
    totals = np.zeros((counts.shape[0], len(FORMATION_SLOTS)))
    remaining = np.tile(np.array(FORMATION_SLOTS), (counts.shape[0], 1))
    for tower_index in range(len(DENOMINATORS) - 1, -1, -1):
        take = np.minimum(counts[:, tower_index, None], remaining)
        totals += take * POWER[tower_index]
        remaining -= take
    return totals


def six_role_core(counts):
    has_tower = counts > 0
    total = np.zeros(counts.shape[0])
    for role in sorted(set(ROLES)):
        role_indices = np.array([i for i, value in enumerate(ROLES) if value == role])
        role_owned = has_tower[:, role_indices]
        reversed_position = np.argmax(role_owned[:, ::-1], axis=1)
        best_index = role_indices[len(role_indices) - 1 - reversed_position]
        total += np.where(role_owned.any(axis=1), POWER[best_index], 0.0)
    return total


def summarize(counts, performance):
    has_tower = counts > 0
    reverse_position = np.argmax(has_tower[:, ::-1], axis=1)
    highest_index = len(DENOMINATORS) - 1 - reverse_position
    highest_power = POWER[highest_index]
    frontier_base = formation_frontier(counts)
    frontier_final = frontier_base * performance
    core_final = six_role_core(counts) * performance

    rank_q = integer_quantiles(highest_index + 1)
    return {
        "highest_rank_q": rank_q,
        "highest_denominator_q": [DENOMINATORS[rank - 1] for rank in rank_q],
        "highest_power_q": numeric_quantiles(highest_power),
        "distinct_q": integer_quantiles(has_tower.sum(axis=1)),
        "frontier_base_q": [
            numeric_quantiles(frontier_base[:, i])
            for i in range(len(FORMATION_SLOTS))
        ],
        "frontier_final_q": [
            numeric_quantiles(frontier_final[:, i])
            for i in range(len(FORMATION_SLOTS))
        ],
        "six_role_core_final_q": numeric_quantiles(core_final),
        "top12_best_share_q": numeric_quantiles(
            highest_power / frontier_base[:, -1]
        ),
        "top_tower_rate": float(
            (highest_index == len(DENOMINATORS) - 1).mean()
        ),
    }


def run():
    if len(DENOMINATORS) != 50 or len(ROLES) != 50:
        raise AssertionError("V1 ladder must contain 50 towers")
    if Counter(ROLES) != Counter({
        "single": 9,
        "aoe": 9,
        "control": 8,
        "finisher": 8,
        "support": 8,
        "large": 8,
    }):
        raise AssertionError("unexpected role distribution")

    all_results = {}
    for scenario_index, scenario in enumerate(SCENARIOS):
        scenario.validate()
        events = rebirth_events(scenario)
        groups = grouped_rolls(scenario, events)
        rng = np.random.default_rng(RANDOM_SEED + scenario_index)
        owned = np.zeros(
            (ACCOUNT_COUNT, len(DENOMINATORS)), dtype=np.int32
        )
        cumulative_rolls = 0
        scenario_results = {}

        for milestone_index, group in enumerate(groups):
            for compression, roll_count in sorted(group.items()):
                owned += rng.multinomial(
                    roll_count,
                    final_weights(compression),
                    size=ACCOUNT_COUNT,
                ).astype(np.int32)
            cumulative_rolls += sum(group.values())
            if not np.all(owned.sum(axis=1) == cumulative_rolls):
                raise AssertionError("owned counts must equal exact roll count")

            hours = MILESTONES_HOURS[milestone_index]
            rebirths = rebirth_count_at(events, hours)
            performance_points = (
                rebirths * scenario.performance_per_rebirth
            )
            summary = summarize(
                owned, performance_multiplier(performance_points)
            )
            summary.update({
                "rolls": cumulative_rolls,
                "rebirths": rebirths,
                "tokens": rebirths * TOKENS_PER_REBIRTH,
                "luck_points": rebirths * scenario.luck_per_rebirth,
                "performance_points": performance_points,
                "performance_multiplier": performance_multiplier(
                    performance_points
                ),
                "roll_speed_points": (
                    rebirths * scenario.roll_speed_per_rebirth
                ),
            })
            scenario_results[hours] = summary
        all_results[scenario.name] = scenario_results

    balanced = all_results["balanced"]
    assert 0.03 <= balanced[15.0]["top_tower_rate"] <= 0.06
    assert 0.20 <= balanced[30.0]["top_tower_rate"] <= 0.30
    for hours in MILESTONES_HOURS:
        medians = [
            row[1] for row in balanced[hours]["frontier_final_q"]
        ]
        assert medians == sorted(medians)
    return all_results


def fmt(value):
    if value >= 1000:
        return f"{value:,.0f}"
    if value >= 100:
        return f"{value:,.1f}"
    return f"{value:,.2f}"


def print_report(results):
    print(f"ACCOUNTS PER SCENARIO: {ACCOUNT_COUNT:,}")
    print("QUANTILES: P10 / P50 / P90 / P99")
    balanced = results["balanced"]

    print("\nBALANCED MILESTONES")
    for hours in MILESTONES_HOURS:
        row = balanced[hours]
        den = row["highest_denominator_q"]
        top12 = row["frontier_final_q"][-1]
        print(
            f"{hours:>5.2f}h rolls={row['rolls']:>6,} "
            f"R={row['rebirths']:>2} "
            f"perf=x{row['performance_multiplier']:.3f} "
            f"bestN={den[0]:,}/{den[1]:,}/{den[2]:,}/{den[3]:,} "
            f"top12={fmt(top12[0])}/{fmt(top12[1])}/"
            f"{fmt(top12[2])}/{fmt(top12[3])} "
            f"top50={row['top_tower_rate'] * 100:.3f}%"
        )

    print("\nBALANCED SLOT FRONTIER AT 15H AND 30H")
    for hours in [15.0, 30.0]:
        print(f"{hours:g}h")
        for index, slots in enumerate(FORMATION_SLOTS):
            q = balanced[hours]["frontier_final_q"][index]
            print(
                f"  top{slots:>2}: {fmt(q[0])}/{fmt(q[1])}/"
                f"{fmt(q[2])}/{fmt(q[3])}"
            )

    print("\nSCENARIO COMPARISON")
    for hours in [15.0, 30.0]:
        print(f"{hours:g}h")
        for scenario in SCENARIOS:
            row = results[scenario.name][hours]
            top12 = row["frontier_final_q"][-1]
            print(
                f"  {scenario.name:>19}: R={row['rebirths']:>2} "
                f"rolls={row['rolls']:>6,} "
                f"perf=x{row['performance_multiplier']:.3f} "
                f"medianBestN={row['highest_denominator_q'][1]:,} "
                f"top12={fmt(top12[0])}/{fmt(top12[1])}/"
                f"{fmt(top12[2])} "
                f"top50={row['top_tower_rate'] * 100:.3f}%"
            )
    print("\nAll roster benchmark assertions passed.")


if __name__ == "__main__":
    print_report(run())
