#!/usr/bin/env python3
"""Reproduce the provisional V1 coin-tree combat progression curve."""

from __future__ import annotations

from v1_formation_slot_economy import (
    MILESTONES_HOURS,
    SCENARIOS,
    SLOT_BUDGET_START_MINUTES,
    Scenario,
    planned_coin_per_minute,
    run as run_formation_benchmark,
    simulate_rebirths,
)

COMBAT_BUDGET_START_MINUTES = 4.75
COMBAT_COIN_SHARE = 0.25

# Core Output I and II already exist in the first-session benchmark.
INITIAL_CORE_TIMELINE = [
    (0.93 / 60.0, 1.25),
    (4.75 / 60.0, 1.50),
]

FUTURE_NODE_PRICES = [
    12_000,
    42_000,
    290_000,
    3_300_000,
    25_000_000,
    45_000_000,
    280_000_000,
    1_950_000_000,
    6_600_000_000,
]

FUTURE_CUMULATIVE_MULTIPLIERS = [
    1.75,
    2.00,
    2.30,
    2.65,
    3.05,
    3.50,
    4.00,
    4.50,
    5.00,
]

STAGE15_STANDARD_HP = 232_080.0


def combat_purchase_times(
    scenario: Scenario,
    end_hours: float = 30.0,
    tick_minutes: float = 0.025,
) -> list[float]:
    events = simulate_rebirths(scenario.performance_per_rebirth)
    combat_budget = 0.0
    price_index = 0
    purchase_times: list[float] = []

    total_steps = int(end_hours * 60.0 / tick_minutes)
    for step in range(total_steps + 1):
        active_minutes = step * tick_minutes
        active_hours = active_minutes / 60.0

        if active_minutes >= COMBAT_BUDGET_START_MINUTES:
            combat_budget += (
                planned_coin_per_minute(active_hours, scenario, events)
                * tick_minutes
                * COMBAT_COIN_SHARE
            )

        while (
            price_index < len(FUTURE_NODE_PRICES)
            and combat_budget + 1e-9 >= FUTURE_NODE_PRICES[price_index]
        ):
            combat_budget -= FUTURE_NODE_PRICES[price_index]
            purchase_times.append(active_hours)
            price_index += 1

    return purchase_times


def coin_combat_multiplier_at(
    purchase_times: list[float],
    active_hours: float,
) -> float:
    multiplier = 1.0
    for unlock_time, value in INITIAL_CORE_TIMELINE:
        if unlock_time <= active_hours:
            multiplier = value

    for unlock_time, value in zip(
        purchase_times,
        FUTURE_CUMULATIVE_MULTIPLIERS,
        strict=True,
    ):
        if unlock_time <= active_hours:
            multiplier = value

    return multiplier


def run() -> dict[str, dict[str, object]]:
    formation_results = run_formation_benchmark()
    results: dict[str, dict[str, object]] = {}

    for scenario in SCENARIOS:
        purchase_times = combat_purchase_times(scenario)
        formation_rows = formation_results[scenario.name]["rows"]
        if not isinstance(formation_rows, dict):
            raise AssertionError("unexpected formation row type")

        rows: dict[float, dict[str, object]] = {}
        for active_hours in MILESTONES_HOURS:
            formation_row = formation_rows[active_hours]
            formation_quantiles = formation_row[
                "role_constrained_quantiles"
            ]
            multiplier = coin_combat_multiplier_at(
                purchase_times,
                active_hours,
            )
            final_quantiles = [
                value * multiplier
                for value in formation_quantiles
            ]
            rows[active_hours] = {
                "coin_combat_multiplier": multiplier,
                "formation_quantiles": formation_quantiles,
                "final_quantiles": final_quantiles,
                "stage15_standard_ttk": [
                    STAGE15_STANDARD_HP / value
                    for value in final_quantiles
                ],
            }

        results[scenario.name] = {
            "purchase_times": purchase_times,
            "rows": rows,
        }

    balanced = results["balanced"]
    balanced_times = balanced["purchase_times"]
    if not isinstance(balanced_times, list):
        raise AssertionError("unexpected purchase-time type")
    if not 19.5 <= balanced_times[-1] <= 20.5:
        raise AssertionError("balanced x5.0 must unlock near 20h")

    balanced_rows = balanced["rows"]
    if not isinstance(balanced_rows, dict):
        raise AssertionError("unexpected row type")
    if balanced_rows[15.0]["coin_combat_multiplier"] != 4.50:
        raise AssertionError("balanced 15h multiplier must be x4.50")
    if balanced_rows[30.0]["coin_combat_multiplier"] != 5.00:
        raise AssertionError("balanced 30h multiplier must be x5.00")

    return results


def render(value: float) -> str:
    if value >= 1_000:
        return f"{value:,.0f}"
    if value >= 100:
        return f"{value:,.1f}"
    return f"{value:,.2f}"


def print_report(results: dict[str, dict[str, object]]) -> None:
    print(
        "COMBAT MODEL: reserve 25% of collected coins after "
        "Core Output II at 4.75 active minutes"
    )

    for scenario in SCENARIOS:
        result = results[scenario.name]
        purchase_times = result["purchase_times"]
        if not isinstance(purchase_times, list):
            raise AssertionError("unexpected purchase-time type")
        rendered_times = ", ".join(
            f"L{level}={hours * 60.0:.1f}m"
            for level, hours in enumerate(purchase_times, start=3)
        )
        print(f"\n{scenario.name}: {rendered_times}")

        rows = result["rows"]
        if not isinstance(rows, dict):
            raise AssertionError("unexpected row type")
        for active_hours in MILESTONES_HOURS:
            row = rows[active_hours]
            values = row["final_quantiles"]
            print(
                f"  {active_hours:>5.2f}h "
                f"coin=x{row['coin_combat_multiplier']:.2f} "
                f"EC={render(values[0])}/{render(values[1])}/"
                f"{render(values[2])}"
            )

    print("\nAll coin-combat benchmark assertions passed.")


if __name__ == "__main__":
    print_report(run())
