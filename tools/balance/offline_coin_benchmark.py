#!/usr/bin/env python3
"""Benchmark V1 offline coin efficiency, storage caps, and abuse guards."""
from __future__ import annotations

FARM_CYCLE_SECONDS = {
    1: 56.28, 2: 65.90, 3: 78.00, 4: 61.23, 5: 67.71,
    6: 75.00, 7: 68.00, 8: 75.00, 9: 82.00, 10: 76.00,
    11: 84.00, 12: 90.00, 13: 86.00, 14: 93.00, 15: 100.00,
}
REWARD_UNITS = {stage: 400.0 for stage in range(1, 16)}
REWARD_UNITS[15] = 440.0

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

OFFLINE_NODES = [
    ("Offline Unlock", 100_000, "efficiency", 0.25),
    ("Offline Efficiency II", 5_000_000, "efficiency", 0.30),
    ("Offline Storage II", 15_000_000, "cap_hours", 12.0),
    ("Offline Efficiency III", 100_000_000, "efficiency", 0.35),
    ("Offline Storage III", 500_000_000, "cap_hours", 24.0),
    ("Offline Efficiency IV", 2_500_000_000, "efficiency", 0.40),
]

# active hours, highest completed stage, balanced currency points
MILESTONES = [
    (2.0, 6, 4),
    (5.0, 9, 8),
    (15.0, 15, 22),
    (30.0, 15, 46),
]


def stage_reward_scale(stage: int) -> float:
    return 10.0 ** ((stage - 1) / 3.0) * 1.08 ** (stage - 1)


def base_coin_per_hour(stage: int) -> float:
    return (
        REWARD_UNITS[stage]
        * stage_reward_scale(stage)
        * 3_600.0
        / FARM_CYCLE_SECONDS[stage]
    )


def currency_multiplier(points: int) -> float:
    value = 1.0 + 0.040 * min(points, 25) + 0.010 * max(points - 25, 0)
    return min(4.0, value)


def offline_anchor_stage(highest_completed_stage: int) -> int:
    """Use the previous regional finale instead of the current frontier."""
    return max(1, 3 * ((highest_completed_stage - 1) // 3))


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


def purchase_schedule() -> list[dict[str, float | str]]:
    cumulative = 0.0
    rows = []
    for name, cost, kind, value in OFFLINE_NODES:
        cumulative += cost
        rows.append(
            {
                "name": name,
                "cost": float(cost),
                "cumulative": cumulative,
                "active_hours": time_for_flex_budget(cumulative),
                "kind": kind,
                "value": float(value),
            }
        )
    return rows


def offline_state_at(
    active_hours: float,
    schedule: list[dict[str, float | str]],
) -> tuple[float, float]:
    efficiency = 0.0
    cap_hours = 0.0
    for node in schedule:
        if float(node["active_hours"]) <= active_hours:
            if node["kind"] == "efficiency":
                efficiency = float(node["value"])
                cap_hours = max(cap_hours, 8.0)
            else:
                cap_hours = float(node["value"])
    return efficiency, cap_hours


def offline_reward(
    highest_completed_stage: int,
    currency_points: int,
    efficiency: float,
    cap_hours: float,
    absence_hours: float,
) -> tuple[float, int, float]:
    anchor = offline_anchor_stage(highest_completed_stage)
    verified_online_rate = (
        base_coin_per_hour(anchor)
        * 0.92
        * 1.15
        * currency_multiplier(currency_points)
    )
    applied_hours = min(absence_hours, cap_hours)
    return (
        verified_online_rate * efficiency * applied_hours,
        anchor,
        verified_online_rate,
    )


def run():
    schedule = purchase_schedule()
    rows = []
    for active_hours, highest_stage, currency_points in MILESTONES:
        efficiency, cap_hours = offline_state_at(active_hours, schedule)
        one_day, anchor, online_rate = offline_reward(
            highest_stage,
            currency_points,
            efficiency,
            cap_hours,
            24.0,
        )
        rows.append(
            {
                "active_hours": active_hours,
                "highest_stage": highest_stage,
                "anchor_stage": anchor,
                "currency_multiplier": currency_multiplier(currency_points),
                "efficiency": efficiency,
                "cap_hours": cap_hours,
                "verified_online_per_hour": online_rate,
                "one_day_reward": one_day,
                "three_day_reward": offline_reward(
                    highest_stage, currency_points, efficiency, cap_hours, 72.0
                )[0],
                "seven_day_reward": offline_reward(
                    highest_stage, currency_points, efficiency, cap_hours, 168.0
                )[0],
            }
        )

    assert 1.0 <= float(schedule[0]["active_hours"]) <= 2.0
    assert schedule[-1]["cumulative"] == 3_120_100_000
    assert 17.0 <= float(schedule[-1]["active_hours"]) <= 20.0
    assert rows[-1]["one_day_reward"] < 5_000_000_000
    assert rows[-1]["efficiency"] <= 0.40
    return schedule, rows


def main() -> None:
    schedule, rows = run()
    print("OFFLINE PURCHASE SCHEDULE")
    for row in schedule:
        print(row)
    print("\nOFFLINE MILESTONES")
    for row in rows:
        print(row)
    print("\nAll offline coin assertions passed.")


if __name__ == "__main__":
    main()
