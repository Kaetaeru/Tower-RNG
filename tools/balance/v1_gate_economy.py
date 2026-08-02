#!/usr/bin/env python3
"""Integrated V1 gate, formation-slot, and coin-combat economy benchmark.

This benchmark starts from the confirmed first-session path and, after 8.5
active minutes, partitions collected coins among permanent gates, formation
slots, combat nodes, and a flexible utility reserve. Gate prices are tuned so
the balanced allocation reaches the current region timeline. When a progression
branch is complete, its share is redistributed across unfinished branches. The
final combat node is priced as a mastery sink so this rational reallocation does
not collapse the 20-hour target.

The model is a balance recommendation only. Catalog adoption is separate.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

TICK_MINUTES = 0.01
BUDGET_SPLIT_START_MINUTES = 8.5
END_HOURS = 30.0

# Actual measured farm cycles for 1-6. Planning cycles for 7-15.
FARM_CYCLE_SECONDS = {
    1: 56.28,
    2: 65.90,
    3: 78.00,
    4: 61.23,
    5: 67.71,
    6: 75.00,
    7: 68.00,
    8: 75.00,
    9: 82.00,
    10: 76.00,
    11: 84.00,
    12: 90.00,
    13: 86.00,
    14: 93.00,
    15: 100.00,
}

REWARD_UNITS = {stage: 400.0 for stage in range(1, 16)}
REWARD_UNITS[15] = 440.0

# Gate 2 and 3 remain fixed by the first-session economy.
EARLY_GATE_TIMES_MINUTES = {2: 3.05, 3: 7.83}
GATE_TARGET_HOURS = {
    4: 0.50,
    5: 1.00,
    6: 1.50,
    7: 2.00,
    8: 3.00,
    9: 4.00,
    10: 5.00,
    11: 6.50,
    12: 8.00,
    13: 9.50,
    14: 10.50,
    15: 12.00,
}

# Provisional balance recommendation. Not yet catalog-adopted.
GATE_PRICES = {
    2: 750,
    3: 3_200,
    4: 15_000,
    5: 60_000,
    6: 120_000,
    7: 300_000,
    8: 1_500_000,
    9: 3_000_000,
    10: 7_500_000,
    11: 30_000_000,
    12: 60_000_000,
    13: 150_000_000,
    14: 250_000_000,
    15: 800_000_000,
}

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

COMBAT_NODE_PRICES = [
    12_000,
    42_000,
    290_000,
    3_300_000,
    25_000_000,
    45_000_000,
    280_000_000,
    1_950_000_000,
    30_000_000_000,
]

COMBAT_MULTIPLIERS = [1.75, 2.00, 2.30, 2.65, 3.05, 3.50, 4.00, 4.50, 5.00]


@dataclass(frozen=True)
class Strategy:
    name: str
    gate_share: float
    slot_share: float
    combat_share: float
    utility_share: float
    coin_efficiency: float = 1.0

    def validate(self) -> None:
        total = self.gate_share + self.slot_share + self.combat_share + self.utility_share
        assert abs(total - 1.0) < 1e-9, (self.name, total)
        assert 0.0 < self.coin_efficiency <= 1.0


STRATEGIES = [
    Strategy("balanced", 0.35, 0.30, 0.25, 0.10),
    Strategy("gate_priority", 0.50, 0.20, 0.20, 0.10),
    Strategy("combat_priority", 0.25, 0.20, 0.45, 0.10),
    Strategy("slot_priority", 0.25, 0.45, 0.20, 0.10),
    Strategy("slow_balanced_70pct", 0.35, 0.30, 0.25, 0.10, 0.70),
]


@dataclass
class State:
    minute: float = 0.0
    current_stage: int = 1
    highest_open_stage: int = 3

    gate_budget: float = 0.0
    slot_budget: float = 0.0
    combat_budget: float = 0.0
    utility_reserve: float = 0.0
    total_collected_coin: float = 0.0

    next_gate: int = 4
    next_slot_index: int = 0
    next_combat_index: int = 0

    gate_times: dict[int, float] = field(default_factory=dict)
    slot_times: list[float] = field(default_factory=list)
    combat_times: list[float] = field(default_factory=list)

    rebirth_count: int = 0
    performance_points: int = 0
    currency_points: int = 0
    defense_xp: float = 0.0
    anchor_stage: int = 1
    requirement: float = 7_000.0
    rebirth_times: list[float] = field(default_factory=list)


def stage_scale(stage: int) -> float:
    return 10.0 ** ((stage - 1) / 3.0)


def stage_reward_scale(stage: int) -> float:
    return stage_scale(stage) * 1.08 ** (stage - 1)


def base_reward_per_minute(stage: int) -> float:
    return (
        REWARD_UNITS[stage]
        * stage_reward_scale(stage)
        * 60.0
        / FARM_CYCLE_SECONDS[stage]
    )


def collection_efficiency(minute: float) -> float:
    if minute < 0.67:
        return 0.75
    if minute < 3.55:
        return 0.85
    return 0.92


def coin_tree_multiplier(minute: float) -> float:
    return 1.0 if minute < 8.35 else 1.15


def performance_multiplier(points: int) -> float:
    raw = 1.0 + 0.025 * min(points, 25) + 0.005 * max(points - 25, 0)
    return min(2.50, raw)


def defense_xp_rate_multiplier(points: int) -> float:
    return performance_multiplier(points) ** 0.60


def currency_multiplier(points: int) -> float:
    raw = 1.0 + 0.040 * min(points, 25) + 0.010 * max(points - 25, 0)
    return min(4.00, raw)


def round_three_significant(value: float) -> float:
    decimal_places = 2 - math.floor(math.log10(value))
    return float(round(value, decimal_places))


def target_rebirth_minutes(next_rebirth_number: int) -> float:
    if next_rebirth_number == 2:
        return 20.0
    if next_rebirth_number == 3:
        return 35.0
    if next_rebirth_number <= 50:
        return 50.0
    tier = (next_rebirth_number - 1) // 50
    return min(70.0, 50.0 + 5.0 * tier)


def required_defense_xp(next_rebirth_number: int, anchor_stage: int) -> float:
    if next_rebirth_number == 1:
        return 7_000.0
    return round_three_significant(
        base_reward_per_minute(anchor_stage)
        * target_rebirth_minutes(next_rebirth_number)
    )


def early_stage(minute: float) -> int:
    if minute < EARLY_GATE_TIMES_MINUTES[2]:
        return 1
    if minute < EARLY_GATE_TIMES_MINUTES[3]:
        return 2
    return 3


def process_rebirths(state: State) -> None:
    if state.current_stage > state.anchor_stage:
        old_requirement = state.requirement
        state.anchor_stage = state.current_stage
        if state.rebirth_count >= 1:
            state.requirement = required_defense_xp(
                state.rebirth_count + 1,
                state.anchor_stage,
            )
            state.defense_xp = (
                state.defense_xp / old_requirement * state.requirement
            )

    state.defense_xp += (
        base_reward_per_minute(state.current_stage)
        * defense_xp_rate_multiplier(state.performance_points)
        * TICK_MINUTES
    )

    while state.defense_xp + 1e-9 >= state.requirement:
        state.defense_xp -= state.requirement
        state.rebirth_count += 1
        # Balanced rebirth allocation is fixed to isolate coin-spending strategy.
        state.performance_points += 1
        state.currency_points += 1
        state.rebirth_times.append(state.minute / 60.0)
        state.requirement = required_defense_xp(
            state.rebirth_count + 1,
            state.anchor_stage,
        )


def process_purchases(state: State, strategy: Strategy, collected_coin: float) -> None:
    if state.minute < BUDGET_SPLIT_START_MINUTES:
        if state.minute >= 4.75:
            state.combat_budget += collected_coin * 0.25
    else:
        # Keep 10% for utility. Reallocate completed progression-branch shares
        # across unfinished branches, so money never remains trapped.
        weights = {}
        if state.next_gate <= 15:
            weights["gate"] = strategy.gate_share
        if state.next_slot_index < len(SLOT_PRICES):
            weights["slot"] = strategy.slot_share
        if state.next_combat_index < len(COMBAT_NODE_PRICES):
            weights["combat"] = strategy.combat_share
        state.utility_reserve += collected_coin * strategy.utility_share
        progression_pool = collected_coin * (1.0 - strategy.utility_share)
        if weights:
            total_weight = sum(weights.values())
            state.gate_budget += progression_pool * weights.get("gate", 0.0) / total_weight
            state.slot_budget += progression_pool * weights.get("slot", 0.0) / total_weight
            state.combat_budget += progression_pool * weights.get("combat", 0.0) / total_weight
        else:
            state.utility_reserve += progression_pool

    while (
        state.next_combat_index < len(COMBAT_NODE_PRICES)
        and state.combat_budget + 1e-9
        >= COMBAT_NODE_PRICES[state.next_combat_index]
    ):
        state.combat_budget -= COMBAT_NODE_PRICES[state.next_combat_index]
        state.combat_times.append(state.minute / 60.0)
        state.next_combat_index += 1

    while (
        state.next_slot_index < len(SLOT_PRICES)
        and state.slot_budget + 1e-9 >= SLOT_PRICES[state.next_slot_index]
    ):
        state.slot_budget -= SLOT_PRICES[state.next_slot_index]
        state.slot_times.append(state.minute / 60.0)
        state.next_slot_index += 1

    while state.next_gate <= 15 and state.gate_budget + 1e-9 >= GATE_PRICES[state.next_gate]:
        state.gate_budget -= GATE_PRICES[state.next_gate]
        state.highest_open_stage = state.next_gate
        state.gate_times[state.next_gate] = state.minute / 60.0
        state.next_gate += 1


def simulate(strategy: Strategy, end_hours: float = END_HOURS) -> State:
    strategy.validate()
    state = State()
    total_steps = int(end_hours * 60.0 / TICK_MINUTES) + 1

    for _ in range(total_steps):
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
        collected_coin = coin_per_minute * TICK_MINUTES
        state.total_collected_coin += collected_coin
        process_purchases(state, strategy, collected_coin)
        state.minute += TICK_MINUTES

    return state


def unlocked_slots_at(state: State, hour: float) -> int:
    return 4 + sum(unlock <= hour for unlock in state.slot_times)


def combat_multiplier_at(state: State, hour: float) -> float:
    multiplier = 1.0
    if hour >= 0.93 / 60.0:
        multiplier = 1.25
    if hour >= 4.75 / 60.0:
        multiplier = 1.50
    for unlock, value in zip(state.combat_times, COMBAT_MULTIPLIERS):
        if unlock <= hour:
            multiplier = value
    return multiplier


def time_for_slots(state: State, total_slots: int) -> float:
    if total_slots <= 4:
        return 0.0
    return state.slot_times[total_slots - 5]


def time_for_combat_multiplier(state: State, target: float) -> float:
    if target <= 1.25:
        return 0.93 / 60.0
    if target <= 1.50:
        return 4.75 / 60.0
    index = COMBAT_MULTIPLIERS.index(target)
    return state.combat_times[index]


def entry_ready_time(state: State) -> float:
    # Fast/first-entry deterministic floor used by the 12h planning path.
    return max(
        state.gate_times[15],
        time_for_slots(state, 11),
        time_for_combat_multiplier(state, 4.00),
    )


def stable_ready_time(state: State) -> float:
    # Balanced 13.5h deterministic package, before stochastic roster checks.
    return max(
        state.gate_times[15],
        time_for_slots(state, 12),
        time_for_combat_multiplier(state, 4.50),
    )


def validate(results: dict[str, State]) -> None:
    assert sum(GATE_PRICES[stage] for stage in range(4, 16)) == 1_302_495_000

    balanced = results["balanced"]
    for stage, target in GATE_TARGET_HOURS.items():
        actual = balanced.gate_times[stage]
        assert abs(actual - target) <= 0.16, (stage, actual, target)

    assert 12.5 <= time_for_slots(balanced, 12) <= 13.5
    assert 12.5 <= time_for_combat_multiplier(balanced, 4.50) <= 13.5
    assert 19.5 <= time_for_combat_multiplier(balanced, 5.00) <= 21.0

    gate_priority = results["gate_priority"]
    assert 8.0 <= gate_priority.gate_times[15] <= 10.0
    assert 8.0 <= entry_ready_time(gate_priority) <= 10.5
    assert stable_ready_time(gate_priority) <= 11.0

    combat_priority = results["combat_priority"]
    slot_priority = results["slot_priority"]
    for state in (combat_priority, slot_priority):
        assert 15.0 <= state.gate_times[15] <= 16.5
        assert stable_ready_time(state) <= 18.0

    slow = results["slow_balanced_70pct"]
    assert 15.0 <= slow.gate_times[15] <= 17.0
    assert 16.0 <= stable_ready_time(slow) <= 18.0
    assert time_for_combat_multiplier(slow, 5.00) >= 25.0

    for state in results.values():
        assert len(state.slot_times) == len(SLOT_PRICES)
        assert len(state.combat_times) == len(COMBAT_NODE_PRICES)
        assert state.utility_reserve > 0.0


def utility_reserve_at(strategy: Strategy, hour: float) -> float:
    return simulate(strategy, end_hours=hour).utility_reserve


def main() -> None:
    results = {strategy.name: simulate(strategy) for strategy in STRATEGIES}
    validate(results)

    print("V1 integrated gate economy benchmark")
    print("Gate price total S4-S15:", f"{sum(GATE_PRICES[s] for s in range(4,16)):,.0f}")
    print()
    for strategy in STRATEGIES:
        state = results[strategy.name]
        print(strategy.name)
        print(
            "  gate15=", f"{state.gate_times[15]:.2f}h",
            "entry_ready=", f"{entry_ready_time(state):.2f}h",
            "stable_ready=", f"{stable_ready_time(state):.2f}h",
        )
        print(
            "  slot12=", f"{time_for_slots(state,12):.2f}h",
            "combat4.5=", f"{time_for_combat_multiplier(state,4.50):.2f}h",
            "combat5.0=", f"{time_for_combat_multiplier(state,5.00):.2f}h",
        )
        print(
            "  rebirths30h=", state.rebirth_count,
            "utility_reserve15h=", f"{utility_reserve_at(strategy, 15.0):,.0f}",
        )
        print()

    print("Balanced gates")
    for stage in range(4, 16):
        print(
            f"  S{stage}: price={GATE_PRICES[stage]:>13,} "
            f"time={results['balanced'].gate_times[stage]:5.2f}h"
        )
    print("All integrated gate economy assertions passed.")


if __name__ == "__main__":
    main()
