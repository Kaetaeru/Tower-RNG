#!/usr/bin/env python3
"""Benchmark manual fusion materials, power compression, and unlock timing."""
from __future__ import annotations

import bisect
import math
from collections import Counter

import numpy as np

try:
    from numba import njit, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

    def njit(*args, **kwargs):
        if args and callable(args[0]) and len(args) == 1 and not kwargs:
            return args[0]
        return lambda fn: fn

    prange = range


ACCOUNT_COUNT = 20_000 if HAS_NUMBA else 2_000
RANDOM_SEED = 20260811
MILESTONES = [2.5, 5.0, 15.0, 30.0]

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
    ],
    dtype=np.int64,
)

POWER = (DENOMINATORS / 10.0) ** 0.20
TIER1_MULTIPLIER = 1.45
TIER2_MULTIPLIER = TIER1_MULTIPLIER ** 2

FUSION_NODES = [
    ("Fusion Core", 250_000),
    ("Advanced Fusion", 750_000_000),
    ("Rare Lineages", 2_000_000_000),
]

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

FARM_CYCLES = [
    56.28, 60.0, 65.0, 62.0, 68.0,
    75.0, 68.0, 75.0, 82.0, 76.0,
    84.0, 90.0, 86.0, 93.0, 100.0,
]

ROLL_STAGE_TIMELINE = [
    (0.15, 1), (0.30, 2), (0.50, 3), (1.0, 4), (1.5, 5),
    (2.0, 6), (3.0, 7), (4.0, 8), (5.0, 9), (6.5, 10),
    (8.0, 11), (9.5, 12), (10.5, 13), (12.0, 14),
    (float("inf"), 15),
]

XP_STAGE_TIMELINE = [
    (3.5 / 60.0, 1), (10.0 / 60.0, 2), (0.50, 3), (1.0, 4),
    (1.5, 5), (2.0, 6), (3.0, 7), (4.0, 8), (5.0, 9),
    (6.5, 10), (8.0, 11), (9.5, 12), (10.5, 13), (12.0, 14),
    (float("inf"), 15),
]


def stage_reward_scale(stage: int) -> float:
    return 10.0 ** ((stage - 1) / 3.0) * 1.08 ** (stage - 1)


def xp_per_minute(stage: int) -> float:
    return 400.0 * stage_reward_scale(stage) * 60.0 / FARM_CYCLES[stage - 1]


def target_rebirth_minutes(number: int) -> float:
    if number == 2:
        return 20.0
    if number == 3:
        return 35.0
    if number <= 50:
        return 50.0
    return min(70.0, 50.0 + 5.0 * ((number - 1) // 50))


def round_three_significant(value: float) -> float:
    return float(round(value, 2 - math.floor(math.log10(value))))


def required_xp(number: int, stage: int) -> float:
    if number == 1:
        return 7_000.0
    return round_three_significant(
        xp_per_minute(stage) * target_rebirth_minutes(number)
    )


def performance_multiplier(points: int) -> float:
    return min(
        2.5,
        1.0 + 0.025 * min(points, 25) + 0.005 * max(points - 25, 0),
    )


def xp_stage_at(hours: float) -> int:
    for end, stage in XP_STAGE_TIMELINE:
        if hours < end:
            return stage
    raise AssertionError("unreachable")


def build_rebirth_events(end_hours: float = 30.0) -> list[float]:
    seconds = 0.0
    xp = 0.0
    rebirths = 0
    performance_points = 0
    anchor = 1
    requirement = required_xp(1, 1)
    events = []
    tick = 0.25

    while seconds < end_hours * 3_600.0:
        stage = xp_stage_at(seconds / 3_600.0)
        if stage > anchor:
            old_requirement = requirement
            anchor = stage
            if rebirths >= 1:
                requirement = required_xp(rebirths + 1, anchor)
                xp = xp / old_requirement * requirement

        xp += (
            xp_per_minute(stage)
            / 60.0
            * performance_multiplier(performance_points) ** 0.60
            * tick
        )
        seconds += tick

        if xp + 1e-9 >= requirement:
            rebirths += 1
            events.append(seconds / 3_600.0)
            xp = 0.0
            performance_points += 1
            requirement = required_xp(rebirths + 1, anchor)

    return events


REBIRTH_EVENTS = build_rebirth_events()


def rebirth_count(hours: float) -> int:
    return bisect.bisect_right(REBIRTH_EVENTS, hours)


def luck_bonus(points: int) -> float:
    return 0.034 * min(points, 25) + 0.004 * max(points - 25, 0)


def roll_stage_at(hours: float) -> int:
    for end, stage in ROLL_STAGE_TIMELINE:
        if hours < end:
            return stage
    raise AssertionError("unreachable")


def roll_interval(base: float, points: int) -> float:
    rate = 1.0 + 0.01 * min(points, 25) + 0.0025 * max(points - 25, 0)
    return max(2.0, base / rate)


def compression_for_roll(hours: float, roll_number: int) -> float:
    base = (
        1.0
        + 0.245 * (roll_stage_at(hours) - 1)
        + luck_bonus(rebirth_count(hours))
    )
    if roll_number % 100 == 0:
        return min(base + 0.65, 6.05)
    if roll_number % 10 == 0:
        return min(base + 0.25, 5.65)
    return min(base, 5.40)


def final_weights(compression: float) -> np.ndarray:
    logs = np.log10(DENOMINATORS)
    raw = 10.0 ** (-(1.0 + (logs - 1.0) / compression))
    return raw / raw.sum()


def grouped_rolls() -> list[Counter]:
    milestone_seconds = [hours * 3_600.0 for hours in MILESTONES]
    groups = [Counter() for _ in MILESTONES]

    def add_roll(seconds: float, number: int) -> None:
        index = bisect.bisect_left(milestone_seconds, seconds)
        if index < len(groups):
            compression = compression_for_roll(seconds / 3_600.0, number)
            groups[index][round(compression, 12)] += 1

    add_roll(0.0, 1)
    roll_number = 1
    next_roll = 12.0
    while next_roll <= milestone_seconds[-1]:
        roll_number += 1
        add_roll(next_roll, roll_number)
        hours = next_roll / 3_600.0
        base = 4.0 if next_roll < 79.0 else 3.6
        next_roll += roll_interval(base, rebirth_count(hours))
    return groups


def time_for_flex_budget(target: float) -> float:
    if target <= FLEX_BUDGET_POINTS[0][1]:
        hour, budget = FLEX_BUDGET_POINTS[0]
        return hour * target / budget
    for (h0, b0), (h1, b1) in zip(
        FLEX_BUDGET_POINTS, FLEX_BUDGET_POINTS[1:]
    ):
        if target <= b1:
            return h0 + (target - b0) / (b1 - b0) * (h1 - h0)
    h0, b0 = FLEX_BUDGET_POINTS[-2]
    h1, b1 = FLEX_BUDGET_POINTS[-1]
    return h1 + (target - b1) / (b1 - b0) * (h1 - h0)


def fusion_schedule():
    cumulative = 0.0
    rows = []
    for name, cost in FUSION_NODES:
        cumulative += cost
        rows.append((name, cost, cumulative, time_for_flex_budget(cumulative)))
    return rows


@njit
def lineage_curve(
    count: int,
    power: float,
    role_cap: int,
    tier1: float,
    tier2: float,
    max_tier: int,
):
    best = np.full(role_cap + 1, -1e300)
    best[0] = 0.0
    for selected in range(1, role_cap + 1):
        max_tier2 = selected if max_tier >= 2 else 0
        for tier2_count in range(max_tier2 + 1):
            max_tier1 = selected - tier2_count if max_tier >= 1 else 0
            for tier1_count in range(max_tier1 + 1):
                base_count = selected - tier2_count - tier1_count
                material_cost = 9 * tier2_count + 3 * tier1_count + base_count
                if material_cost <= count:
                    value = power * (
                        tier2 * tier2_count
                        + tier1 * tier1_count
                        + base_count
                    )
                    if value > best[selected]:
                        best[selected] = value
    return best


@njit
def formation_one(
    counts,
    slots: int,
    role_cap: int,
    max_rank: int,
    max_tier: int,
) -> float:
    role_curves = np.full((6, role_cap + 1), -1e300)
    role_curves[:, 0] = 0.0

    for tower_index in range(50):
        role = ROLE_CODES[tower_index]
        eligible = tower_index < max_rank
        curve = lineage_curve(
            counts[tower_index],
            POWER[tower_index],
            role_cap,
            TIER1_MULTIPLIER if eligible else 1.0,
            TIER2_MULTIPLIER if eligible else 1.0,
            max_tier if eligible else 0,
        )
        old = role_curves[role].copy()
        new = np.full(role_cap + 1, -1e300)
        for left in range(role_cap + 1):
            if old[left] < -1e200:
                continue
            for right in range(role_cap - left + 1):
                if curve[right] < -1e200:
                    continue
                value = old[left] + curve[right]
                if value > new[left + right]:
                    new[left + right] = value
        role_curves[role] = new

    total = np.full(slots + 1, -1e300)
    total[0] = 0.0
    for role in range(6):
        old = total.copy()
        new = np.full(slots + 1, -1e300)
        for left in range(slots + 1):
            if old[left] < -1e200:
                continue
            for right in range(min(role_cap, slots - left) + 1):
                if role_curves[role, right] < -1e200:
                    continue
                value = old[left] + role_curves[role, right]
                if value > new[left + right]:
                    new[left + right] = value
        total = new

    answer = 0.0
    for value in total:
        if value > answer:
            answer = value
    return answer


@njit(parallel=True)
def formation_batch(owned, slots, role_cap, max_rank, max_tier):
    result = np.empty(owned.shape[0])
    for account in prange(owned.shape[0]):
        result[account] = formation_one(
            owned[account], slots, role_cap, max_rank, max_tier
        )
    return result


def quantiles(values: np.ndarray) -> list[float]:
    return [float(value) for value in np.quantile(values, [0.10, 0.50, 0.90, 0.99])]


def variant_duplicate_rates() -> dict[float, float]:
    families = [5_000, 10_000, 20_000, 50_000]
    variant_nodes = [
        (0, 12, 3_500_000), (1, 12, 15_000_000),
        (2, 12, 50_000_000), (3, 12, 150_000_000),
        (0, 31, 100_000_000), (1, 31, 200_000_000),
        (2, 31, 500_000_000), (3, 31, 1_000_000_000),
        (0, 50, 1_000_000_000), (1, 50, 2_000_000_000),
        (2, 50, 5_000_000_000), (3, 50, 15_000_000_000),
    ]
    cumulative = 0.0
    schedule = []
    for family, rank, cost in variant_nodes:
        cumulative += cost
        schedule.append((time_for_flex_budget(cumulative), family, rank))

    def eligibility(hours: float) -> list[int]:
        result = [0, 0, 0, 0]
        for unlock, family, rank in schedule:
            if unlock <= hours:
                result[family] = max(result[family], rank)
        return result

    results = {}
    for end_hours in [15.0, 30.0]:
        lambdas = np.zeros((4, 50))
        roll_number = 1
        seconds = 0.0
        while seconds / 3_600.0 <= end_hours + 1e-12:
            hours = seconds / 3_600.0
            weights = final_weights(compression_for_roll(hours, roll_number))
            eligible = eligibility(hours)
            for family, denominator in enumerate(families):
                rank = eligible[family]
                if rank:
                    lambdas[family, :rank] += weights[:rank] / denominator
            if seconds == 0.0:
                seconds = 12.0
            else:
                base = 4.0 if seconds < 79.0 else 3.6
                seconds += roll_interval(base, rebirth_count(hours))
            roll_number += 1

        rng = np.random.default_rng(RANDOM_SEED + int(end_hours))
        counts = rng.poisson(lambdas, size=(ACCOUNT_COUNT, 4, 50))
        results[end_hours] = float((counts >= 3).any(axis=(1, 2)).mean())
    return results


def run():
    rng = np.random.default_rng(RANDOM_SEED)
    owned = np.zeros((ACCOUNT_COUNT, 50), dtype=np.int32)
    rows = {}
    cumulative_rolls = 0
    configs = {
        2.5: (7, 3, 31, 1),
        5.0: (8, 3, 31, 1),
        15.0: (12, 4, 31, 2),
        30.0: (12, 4, 50, 2),
    }

    formation_batch(np.zeros((1, 50), dtype=np.int32), 4, 2, 31, 1)

    for hours, group in zip(MILESTONES, grouped_rolls()):
        for compression, count in sorted(group.items()):
            owned += rng.multinomial(
                count,
                final_weights(compression),
                size=ACCOUNT_COUNT,
            ).astype(np.int32)
        cumulative_rolls += sum(group.values())

        slots, role_cap, max_rank, max_tier = configs[hours]
        base = formation_batch(owned, slots, role_cap, 0, 0)
        fused = formation_batch(owned, slots, role_cap, max_rank, max_tier)
        rows[hours] = {
            "rolls": cumulative_rolls,
            "base_quantiles": quantiles(base),
            "fused_quantiles": quantiles(fused),
            "ratio_quantiles": quantiles(fused / base),
            "fusionable_rate": float((owned[:, :max_rank] >= 3).any(axis=1).mean()),
        }

    duplicate_rates = variant_duplicate_rates()

    assert 2.0 <= fusion_schedule()[0][3] <= 4.0
    assert rows[2.5]["fusionable_rate"] >= 0.999
    assert rows[2.5]["ratio_quantiles"][1] <= 1.15
    assert rows[15.0]["ratio_quantiles"][1] <= 1.05
    assert rows[30.0]["ratio_quantiles"][1] <= 1.05
    assert duplicate_rates[30.0] < 0.05
    return fusion_schedule(), rows, duplicate_rates


def main() -> None:
    schedule, rows, duplicate_rates = run()
    print("FUSION SCHEDULE")
    for row in schedule:
        print(row)
    print(
        "POWER",
        TIER1_MULTIPLIER,
        TIER2_MULTIPLIER,
        "equivalent denominator multipliers",
        TIER1_MULTIPLIER ** 5,
        TIER2_MULTIPLIER ** 5,
    )
    for hours, row in rows.items():
        print(hours, row)
    print("variant duplicate probability", duplicate_rates)
    print("All fusion benchmark assertions passed.")


if __name__ == "__main__":
    main()
