#!/usr/bin/env python3
"""Reproduce the provisional V1 post-first-rebirth Defense XP curve.

The model keeps coins, doors, stage position, and combat state through rebirth.
Only Defense XP resets. Later requirements are anchored to the highest stage in
which the account has earned Defense XP. When that anchor rises, current XP is
rescaled so the completion percentage is preserved.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

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

MILESTONES_HOURS = [0.25, 0.50, 2.0, 5.0, 12.0, 13.5, 15.0, 25.0, 30.0]


@dataclass(frozen=True)
class RebirthScenario:
    name: str
    performance_points_per_rebirth: int


SCENARIOS = [
    RebirthScenario("no_performance", 0),
    RebirthScenario("balanced", 1),
    RebirthScenario("performance_half", 2),
    RebirthScenario("performance_focused", 4),
]


def stage_scale(stage: int) -> float:
    return 10.0 ** ((stage - 1) / 3.0)


def stage_reward_scale(stage: int) -> float:
    return stage_scale(stage) * 1.08 ** (stage - 1)


def planned_defense_xp_per_minute(stage: int) -> float:
    cycle_xp = 400.0 * stage_reward_scale(stage)
    return cycle_xp * 60.0 / PLANNED_FARM_CYCLE_SECONDS[stage - 1]


def stable_farm_stage_at(active_hours: float) -> int:
    for end_hour, stage in STABLE_FARM_STAGE_TIMELINE:
        if active_hours < end_hour:
            return stage
    raise AssertionError("unreachable")


def target_rebirth_minutes(next_rebirth_number: int) -> float:
    if next_rebirth_number <= 1:
        raise ValueError("the first rebirth uses the fixed 7,000 XP benchmark")
    if next_rebirth_number == 2:
        return 20.0
    if next_rebirth_number == 3:
        return 35.0
    if next_rebirth_number <= 50:
        return 50.0

    tier = (next_rebirth_number - 1) // 50
    return min(70.0, 50.0 + 5.0 * tier)


def round_three_significant(value: float) -> float:
    if value <= 0.0:
        raise ValueError("value must be positive")
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


def rescale_progress(
    current_xp: float,
    old_requirement: float,
    new_requirement: float,
) -> float:
    if old_requirement <= 0.0 or new_requirement <= 0.0:
        raise ValueError("requirements must be positive")
    return current_xp / old_requirement * new_requirement


def simulate_rebirths(
    scenario: RebirthScenario,
    end_hours: float = 30.0,
    tick_seconds: float = 0.25,
) -> list[dict[str, float | int]]:
    active_seconds = 0.0
    defense_xp = 0.0
    rebirth_count = 0
    performance_points = 0
    anchor_stage = 1
    requirement = required_defense_xp(1, anchor_stage)
    events: list[dict[str, float | int]] = []

    while active_seconds < end_hours * 3_600.0:
        stage = stable_farm_stage_at(active_seconds / 3_600.0)

        if stage > anchor_stage:
            old_requirement = requirement
            anchor_stage = stage
            if rebirth_count >= 1:
                requirement = required_defense_xp(
                    rebirth_count + 1,
                    anchor_stage,
                )
                defense_xp = rescale_progress(
                    defense_xp,
                    old_requirement,
                    requirement,
                )

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
        events.append(
            {
                "rebirth": rebirth_count,
                "active_minutes": active_seconds / 60.0,
                "stage": stage,
                "anchor_stage": anchor_stage,
                "requirement": requirement,
                "performance_points_before": performance_points,
                "performance_multiplier_before": performance_multiplier(
                    performance_points
                ),
            }
        )

        defense_xp = 0.0
        performance_points += scenario.performance_points_per_rebirth
        requirement = required_defense_xp(
            rebirth_count + 1,
            anchor_stage,
        )

    return events


def count_by(events: list[dict[str, float | int]], hours: float) -> int:
    return sum(float(event["active_minutes"]) <= hours * 60.0 for event in events)


def print_report() -> None:
    print("PLANNED DEFENSE XP RATE")
    print("stage | xp/min | R2 20m | R3 35m | R4-50 50m")
    for stage in range(1, 16):
        print(
            f"{stage:>5} | "
            f"{planned_defense_xp_per_minute(stage):>12,.1f} | "
            f"{required_defense_xp(2, stage):>12,.0f} | "
            f"{required_defense_xp(3, stage):>12,.0f} | "
            f"{required_defense_xp(4, stage):>14,.0f}"
        )

    print("\nREBIRTH MILESTONES")
    results: dict[str, list[dict[str, float | int]]] = {}
    for scenario in SCENARIOS:
        events = simulate_rebirths(scenario)
        results[scenario.name] = events
        rendered = ", ".join(
            f"{hours:g}h={count_by(events, hours)}"
            for hours in MILESTONES_HOURS
        )
        print(f"{scenario.name:>20}: {rendered}")

    balanced = results["balanced"]
    focused = results["performance_focused"]
    no_performance = results["no_performance"]

    print("\nBALANCED FIRST EVENTS")
    for event in balanced[:10]:
        print(
            f"R{int(event['rebirth']):>2}: "
            f"{float(event['active_minutes']):>7.2f} min, "
            f"stage={int(event['stage']):>2}, "
            f"requirement={float(event['requirement']):,.0f}"
        )

    assert 7.0 <= float(balanced[0]["active_minutes"]) <= 15.0
    assert 25.0 <= float(balanced[1]["active_minutes"]) <= 35.0
    assert count_by(balanced, 2.0) == 4
    assert 7 <= count_by(balanced, 5.0) <= 9
    assert 20 <= count_by(balanced, 15.0) <= 24
    assert 44 <= count_by(balanced, 30.0) <= 48
    assert count_by(no_performance, 30.0) < count_by(balanced, 30.0)
    assert count_by(focused, 30.0) <= 60

    old_requirement = required_defense_xp(4, 3)
    new_requirement = required_defense_xp(4, 4)
    current_xp = old_requirement * 0.3725
    rescaled_xp = rescale_progress(current_xp, old_requirement, new_requirement)
    assert math.isclose(rescaled_xp / new_requirement, 0.3725, rel_tol=1e-12)

    print("\nAll benchmark assertions passed.")


if __name__ == "__main__":
    print_report()
