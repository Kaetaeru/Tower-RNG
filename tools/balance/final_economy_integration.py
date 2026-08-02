#!/usr/bin/env python3
"""Integrate variant, fusion, and offline branches with the core coin model."""
from __future__ import annotations

from dataclasses import dataclass

from v1_gate_economy import (
    STRATEGIES,
    State,
    TICK_MINUTES,
    BUDGET_SPLIT_START_MINUTES,
    early_stage,
    process_rebirths,
    base_reward_per_minute,
    collection_efficiency,
    coin_tree_multiplier,
    currency_multiplier,
    process_purchases,
)


def simulate_with_history(strategy, end_hours: float = 30.0):
    state = State()
    history = []
    next_history_minute = 0.0
    steps = int(end_hours * 60.0 / TICK_MINUTES) + 1

    for _ in range(steps):
        state.current_stage = (
            early_stage(state.minute)
            if state.minute < BUDGET_SPLIT_START_MINUTES
            else state.highest_open_stage
        )
        process_rebirths(state)

        coin_per_minute = (
            base_reward_per_minute(state.current_stage)
            * collection_efficiency(state.minute)
            * coin_tree_multiplier(state.minute)
            * currency_multiplier(state.currency_points)
            * strategy.coin_efficiency
        )
        collected = coin_per_minute * TICK_MINUTES
        state.total_collected_coin += collected
        process_purchases(state, strategy, collected)

        if state.minute + 1e-9 >= next_history_minute:
            history.append(
                (
                    state.minute / 60.0,
                    state.current_stage,
                    state.utility_reserve,
                    state.total_collected_coin,
                    state.rebirth_count,
                    state.currency_points,
                )
            )
            next_history_minute += 1.0
        state.minute += TICK_MINUTES

    return state, history


VARIANT_NODES = [
    3_500_000,
    15_000_000,
    50_000_000,
    150_000_000,
    100_000_000,
    200_000_000,
    500_000_000,
    1_000_000_000,
    1_000_000_000,
    2_000_000_000,
    5_000_000_000,
    15_000_000_000,
]
FUSION_NODES = [250_000, 750_000_000, 2_000_000_000]
OFFLINE_NODES = [
    100_000,
    5_000_000,
    15_000_000,
    100_000_000,
    500_000_000,
    2_500_000_000,
]
BRANCHES = {
    "variant": VARIANT_NODES,
    "fusion": FUSION_NODES,
    "offline": OFFLINE_NODES,
}


@dataclass(frozen=True)
class OptionalStrategy:
    name: str
    variant: float
    fusion: float
    offline: float


OPTIONAL_STRATEGIES = [
    OptionalStrategy("balanced_mastery", 0.55, 0.20, 0.25),
    OptionalStrategy("collector", 0.75, 0.15, 0.10),
    OptionalStrategy("comfort", 0.35, 0.20, 0.45),
]


def allocate(state, history, strategy: OptionalStrategy):
    budgets = {key: 0.0 for key in BRANCHES}
    indices = {key: 0 for key in BRANCHES}
    times = {key: [] for key in BRANCHES}
    previous_utility = 0.0

    # Core feature unlocks are bought before optional specialization. This keeps
    # offline coins in the 1-2h window and manual fusion in the 2-4h window.
    bootstrap = [("offline", 0), ("fusion", 0)]
    bootstrap_index = 0
    bootstrap_budget = 0.0
    base_weights = {
        "variant": strategy.variant,
        "fusion": strategy.fusion,
        "offline": strategy.offline,
    }

    for hour, _, utility, _, _, _ in history:
        delta = max(0.0, utility - previous_utility)
        previous_utility = utility

        if bootstrap_index < len(bootstrap):
            bootstrap_budget += delta
            while bootstrap_index < len(bootstrap):
                branch, node_index = bootstrap[bootstrap_index]
                cost = BRANCHES[branch][node_index]
                if bootstrap_budget + 1e-9 < cost:
                    break
                bootstrap_budget -= cost
                times[branch].append(hour)
                indices[branch] = 1
                bootstrap_index += 1
            if bootstrap_index < len(bootstrap):
                continue
            delta = bootstrap_budget
            bootstrap_budget = 0.0

        active = {
            key: weight
            for key, weight in base_weights.items()
            if indices[key] < len(BRANCHES[key])
        }
        if active:
            total_weight = sum(active.values())
            for key, weight in active.items():
                budgets[key] += delta * weight / total_weight

        for key, costs in BRANCHES.items():
            while (
                indices[key] < len(costs)
                and budgets[key] + 1e-9 >= costs[indices[key]]
            ):
                budgets[key] -= costs[indices[key]]
                times[key].append(hour)
                indices[key] += 1

    spent = sum(sum(costs[: indices[key]]) for key, costs in BRANCHES.items())
    return {
        "times": times,
        "indices": indices,
        "spent": spent,
        "utility": state.utility_reserve,
        "leftover": state.utility_reserve - spent,
    }


def run():
    core_states = {
        strategy.name: simulate_with_history(strategy)
        for strategy in [STRATEGIES[0], STRATEGIES[1], STRATEGIES[4]]
    }
    results = {}
    for core_name, (state, history) in core_states.items():
        results[core_name] = {
            strategy.name: allocate(state, history, strategy)
            for strategy in OPTIONAL_STRATEGIES
        }

    optional_total = sum(sum(costs) for costs in BRANCHES.values())
    balanced = results["balanced"]["balanced_mastery"]
    additional_sink_for_five_billion_reserve = max(
        0.0,
        balanced["leftover"] - 5_000_000_000,
    )

    assert optional_total == 30_888_850_000
    assert balanced["spent"] == optional_total
    assert 19_000_000_000 <= balanced["leftover"] <= 21_000_000_000
    assert 15_000_000_000 <= additional_sink_for_five_billion_reserve <= 16_000_000_000
    return results, optional_total, additional_sink_for_five_billion_reserve


def main() -> None:
    results, optional_total, required_sink = run()
    print("optional total", optional_total)
    print("additional sink for <=5B reserve", required_sink)
    for core_name, strategies in results.items():
        print("\n", core_name)
        for strategy_name, row in strategies.items():
            print(
                strategy_name,
                "utility", row["utility"],
                "spent", row["spent"],
                "leftover", row["leftover"],
                "complete", {
                    key: (values[-1] if values else None)
                    for key, values in row["times"].items()
                },
                "counts", row["indices"],
            )
    print(
        "All integrated economy assertions passed; "
        "additional mastery sink remains a content decision."
    )


if __name__ == "__main__":
    main()
