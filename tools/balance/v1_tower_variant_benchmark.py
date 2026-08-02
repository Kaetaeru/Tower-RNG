#!/usr/bin/env python3
"""Benchmark V1 tower-variant unlocks, acquisition, power, and coin sink.

The base tower is rolled first with the existing compression model. A separate
fixed variant ticket can replace that result with one unlocked compatible
variant. Family ticket probabilities are not directly compressed by Luck.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from rebirth_stat_tokens import (
    BASE_AUTO_ROLL_INTERVAL,
    COIN_SPEED_NODE_INTERVAL,
    DENOMINATORS,
    SCENARIOS,
    compression_for_roll,
    final_roll_interval,
    final_weights,
    points,
    rebirth_events,
)

ACCOUNT_COUNT = 20_000
RANDOM_SEED = 20260803
MILESTONES = [5.0, 8.0, 10.0, 12.0, 13.5, 15.0, 20.0, 25.0, 30.0]
POWER = np.array([(denominator / 10.0) ** 0.20 for denominator in DENOMINATORS])

FLEX_BUDGET_POINTS = [
    (2.0, 134_000.0),
    (5.0, 3_460_000.0),
    (8.0, 28_579_000.0),
    (10.0, 99_986_000.0),
    (12.0, 364_629_000.0),
    (13.0, 750_032_000.0),
    (15.0, 1_581_906_000.0),
    (20.0, 3_859_756_000.0),
    (30.0, 50_921_671_000.0),
]

# Raw role-capped median formation frontier before performance and coin growth.
BASE_FORMATION_MEDIAN = {
    5.0: 149.76 / 1.20,
    15.0: 4_370.0 / 1.55,
    30.0: 23_067.0 / 1.73,
}
FORMATION_SLOTS = {5.0: 8, 15.0: 12, 30.0: 12}


@dataclass(frozen=True)
class Family:
    family_id: str
    label: str
    denominator: int

    @property
    def chance(self) -> float:
        return 1.0 / self.denominator

    @property
    def power_multiplier(self) -> float:
        return self.denominator ** 0.20


FAMILIES = (
    Family("fire", "인화성", 5_000),
    Family("toxic", "독성", 10_000),
    Family("void", "공허", 20_000),
    Family("giant", "거대", 50_000),
)

# Balanced optional-branch purchase order. Each expansion replaces the prior
# eligibility rank for that family: 12 common slots, 31 repeated slots, all 50.
VARIANT_NODES = (
    ("fire", 12, 3_500_000, "인화성 해금"),
    ("toxic", 12, 15_000_000, "독성 해금"),
    ("void", 12, 50_000_000, "공허 해금"),
    ("giant", 12, 150_000_000, "거대 해금"),
    ("fire", 31, 100_000_000, "인화성 확장 I"),
    ("toxic", 31, 200_000_000, "독성 확장 I"),
    ("void", 31, 500_000_000, "공허 확장 I"),
    ("giant", 31, 1_000_000_000, "거대 확장 I"),
    ("fire", 50, 1_000_000_000, "인화성 확장 II"),
    ("toxic", 50, 2_000_000_000, "독성 확장 II"),
    ("void", 50, 5_000_000_000, "공허 확장 II"),
    ("giant", 50, 15_000_000_000, "거대 확장 II"),
)


def time_for_flex_budget(target: float) -> float:
    if target <= FLEX_BUDGET_POINTS[0][1]:
        hour, budget = FLEX_BUDGET_POINTS[0]
        return hour * target / budget
    for (h0, b0), (h1, b1) in zip(FLEX_BUDGET_POINTS, FLEX_BUDGET_POINTS[1:]):
        if target <= b1:
            return h0 + (target - b0) / (b1 - b0) * (h1 - h0)
    h0, b0 = FLEX_BUDGET_POINTS[-2]
    h1, b1 = FLEX_BUDGET_POINTS[-1]
    return h1 + (target - b1) / (b1 - b0) * (h1 - h0)


def purchase_schedule() -> list[dict[str, float | int | str]]:
    cumulative = 0.0
    rows = []
    for family_id, max_rank, cost, name in VARIANT_NODES:
        cumulative += cost
        rows.append(
            {
                "family_id": family_id,
                "max_rank": max_rank,
                "cost": cost,
                "cumulative": cumulative,
                "active_hours": time_for_flex_budget(cumulative),
                "name": name,
            }
        )
    return rows


def eligibility_at(hours: float, schedule) -> dict[str, int]:
    result = {family.family_id: 0 for family in FAMILIES}
    for node in schedule:
        if float(node["active_hours"]) <= hours + 1e-12:
            family_id = str(node["family_id"])
            result[family_id] = max(result[family_id], int(node["max_rank"]))
    return result


def build_rolls(end_hours: float = 30.0):
    scenario = next(row for row in SCENARIOS if row.name == "balanced")
    events = rebirth_events(scenario)
    rolls = [(0.0, 1, compression_for_roll(0.0, 1, scenario, events))]
    roll_number = 1
    next_roll_seconds = 12.0
    while next_roll_seconds <= end_hours * 3_600.0:
        roll_number += 1
        active_hours = next_roll_seconds / 3_600.0
        rolls.append(
            (
                active_hours,
                roll_number,
                compression_for_roll(active_hours, roll_number, scenario, events),
            )
        )
        base_interval = (
            BASE_AUTO_ROLL_INTERVAL
            if next_roll_seconds < 79.0
            else COIN_SPEED_NODE_INTERVAL
        )
        speed_points = points(events, active_hours, scenario, "roll_speed")
        next_roll_seconds += final_roll_interval(base_interval, speed_points)
    return rolls


def integer_quantiles(values: np.ndarray) -> list[int]:
    return [
        int(value)
        for value in np.quantile(values, [0.10, 0.50, 0.90, 0.99], method="nearest")
    ]


def numeric_quantiles(values: np.ndarray) -> list[float]:
    return [float(value) for value in np.quantile(values, [0.10, 0.50, 0.90, 0.99])]


def milestone_stats(rolls, schedule, milestone: float, rng):
    lambdas = {family.family_id: 0.0 for family in FAMILIES}
    base_mixture = {
        family.family_id: np.zeros(len(DENOMINATORS), dtype=np.float64)
        for family in FAMILIES
    }
    log_no_variant = 0.0
    roll_count = 0

    for active_hours, _, compression in rolls:
        if active_hours > milestone + 1e-12:
            break
        roll_count += 1
        tower_weights = np.asarray(final_weights(compression))
        eligibility = eligibility_at(active_hours, schedule)
        total_variant_probability = 0.0
        for family in FAMILIES:
            max_rank = eligibility[family.family_id]
            if max_rank <= 0:
                continue
            eligible_mass = float(tower_weights[:max_rank].sum())
            probability = family.chance * eligible_mass
            lambdas[family.family_id] += probability
            base_mixture[family.family_id][:max_rank] += (
                family.chance * tower_weights[:max_rank]
            )
            total_variant_probability += probability
        log_no_variant += math.log1p(-total_variant_probability)

    family_counts = {}
    variant_powers = [[] for _ in range(ACCOUNT_COUNT)]
    variant_increments = [[] for _ in range(ACCOUNT_COUNT)]

    # Variant events are rare, so Poisson superposition is used for the 20k
    # account distribution. P(any) below is still calculated exactly per roll.
    for family in FAMILIES:
        counts = rng.poisson(lambdas[family.family_id], size=ACCOUNT_COUNT)
        family_counts[family.family_id] = counts
        event_count = int(counts.sum())
        mixture = base_mixture[family.family_id]
        if event_count == 0 or mixture.sum() <= 0.0:
            continue
        mixture /= mixture.sum()
        base_indices = rng.choice(len(DENOMINATORS), size=event_count, p=mixture)
        cursor = 0
        for account_index, count in enumerate(counts):
            if count == 0:
                continue
            indices = base_indices[cursor : cursor + count]
            cursor += count
            variant_powers[account_index].extend(
                (POWER[indices] * family.power_multiplier).tolist()
            )
            variant_increments[account_index].extend(
                (POWER[indices] * (family.power_multiplier - 1.0)).tolist()
            )

    total_counts = sum(family_counts.values())
    best_variant_power = np.array(
        [max(values) if values else 0.0 for values in variant_powers]
    )
    slots = FORMATION_SLOTS.get(milestone, 12)
    uplift_frontier = np.array(
        [
            sum(sorted(values, reverse=True)[:slots]) if values else 0.0
            for values in variant_increments
        ]
    )

    result = {
        "rolls": roll_count,
        "eligibility": eligibility_at(milestone, schedule),
        "expected_count": sum(lambdas.values()),
        "any_probability": 1.0 - math.exp(log_no_variant),
        "count_quantiles": integer_quantiles(total_counts),
        "best_power_quantiles": numeric_quantiles(best_variant_power),
        "uplift_quantiles": numeric_quantiles(uplift_frontier),
        "family_expected": lambdas,
    }
    if milestone in BASE_FORMATION_MEDIAN:
        result["median_uplift_share"] = (
            result["uplift_quantiles"][1] / BASE_FORMATION_MEDIAN[milestone]
        )
    return result


def run():
    schedule = purchase_schedule()
    rolls = build_rolls()
    rng = np.random.default_rng(RANDOM_SEED)
    results = {
        milestone: milestone_stats(rolls, schedule, milestone, rng)
        for milestone in MILESTONES
    }

    assert abs(sum(family.chance for family in FAMILIES) - 0.00037) < 1e-12
    assert schedule[-1]["cumulative"] == 25_018_500_000
    assert 24.0 <= float(schedule[-1]["active_hours"]) <= 25.0
    assert 2.0 <= results[15.0]["expected_count"] <= 5.0
    assert 0.85 <= results[15.0]["any_probability"] <= 0.99
    assert 8.0 <= results[30.0]["expected_count"] <= 15.0
    assert results[30.0]["any_probability"] >= 0.999
    assert results[15.0]["median_uplift_share"] <= 0.10
    assert results[30.0]["median_uplift_share"] <= 0.15
    return schedule, results


def main() -> None:
    schedule, results = run()
    print("VARIANT PURCHASE SCHEDULE")
    for node in schedule:
        print(
            f"{node['name']:>14} cost={node['cost']:>13,.0f} "
            f"cumulative={node['cumulative']:>14,.0f} "
            f"time={node['active_hours']:>5.2f}h rank<={node['max_rank']}"
        )

    print("\nFAMILY RATES AND POWER")
    for family in FAMILIES:
        print(
            f"{family.label:>4}: 1/{family.denominator:,}, "
            f"multiplier=x{family.power_multiplier:.4f}"
        )

    print("\nMILESTONES")
    for milestone in MILESTONES:
        row = results[milestone]
        eligibility = "/".join(
            str(row["eligibility"][family.family_id]) for family in FAMILIES
        )
        suffix = ""
        if "median_uplift_share" in row:
            suffix = f" uplift_share={row['median_uplift_share'] * 100:.2f}%"
        print(
            f"{milestone:>4.1f}h rolls={row['rolls']:>6,} eligibility={eligibility} "
            f"E[count]={row['expected_count']:.3f} "
            f"P(any)={row['any_probability'] * 100:5.1f}% "
            f"countQ={row['count_quantiles']} "
            f"bestPowerQ={[round(v, 2) for v in row['best_power_quantiles']]} "
            f"upliftQ={[round(v, 2) for v in row['uplift_quantiles']]}{suffix}"
        )

    print("\nAll variant benchmark assertions passed.")


if __name__ == "__main__":
    main()
