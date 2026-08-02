#!/usr/bin/env python3
"""Benchmark the optional late-game mastery utility sink.

The branch only opens after the existing variant, fusion, and offline optional
branches are fully funded. It reuses already-confirmed navigation, formation,
targeting, collection-display, and presentation conveniences. It does not add
combat power, roll luck, variant chance, or recurring fees.
"""
from __future__ import annotations

from dataclasses import dataclass

from final_economy_integration import (
    BRANCHES,
    OPTIONAL_STRATEGIES,
    allocate,
    simulate_with_history,
)
from v1_gate_economy import STRATEGIES


@dataclass(frozen=True)
class MasteryNode:
    node_id: str
    label: str
    price: int
    category: str


MASTERY_NODES = (
    MasteryNode("MST_TELEPORT_CORE", "텔레포터 코어", 250_000_000, "navigation"),
    MasteryNode("MST_STAGE_FAVORITES", "스테이지 즐겨찾기", 500_000_000, "navigation"),
    MasteryNode("MST_ROLE_TARGETING", "역할별 타겟 명령", 750_000_000, "targeting"),
    MasteryNode("MST_FORMATION_PRESET_II", "편성 프리셋 II", 1_000_000_000, "formation"),
    MasteryNode("MST_TOWER_TARGETING", "개별 타워 타겟 명령", 1_500_000_000, "targeting"),
    MasteryNode("MST_FORMATION_PRESET_III", "편성 프리셋 III", 2_000_000_000, "formation"),
    MasteryNode("MST_TARGET_PROFILE", "타겟 프로필 저장", 2_500_000_000, "targeting"),
    MasteryNode("MST_QUICK_HUD", "퀵 HUD 확장", 3_000_000_000, "formation"),
    MasteryNode("MST_COIN_DISPLAY_CONTROL", "코인 표시·병합 제어", 4_000_000_000, "collection"),
    MasteryNode("MST_COLLECTION_PRESENTATION", "도감·획득 연출 프리셋", 4_500_000_000, "presentation"),
    MasteryNode("MST_CONTROL_ROOM", "숙련 제어실 완성", 5_200_000_000, "mastery"),
)

EXISTING_OPTIONAL_TOTAL = sum(sum(costs) for costs in BRANCHES.values())
MASTERY_TOTAL = sum(node.price for node in MASTERY_NODES)


def utility_time(history, target: float) -> float | None:
    previous_hour, previous_value = history[0][0], history[0][2]
    for row in history[1:]:
        hour, value = row[0], row[2]
        if value + 1e-9 >= target:
            if value <= previous_value:
                return hour
            fraction = (target - previous_value) / (value - previous_value)
            return previous_hour + fraction * (hour - previous_hour)
        previous_hour, previous_value = hour, value
    return None


def node_times(history) -> list[float | None]:
    cumulative = EXISTING_OPTIONAL_TOTAL
    times: list[float | None] = []
    for node in MASTERY_NODES:
        cumulative += node.price
        times.append(utility_time(history, cumulative))
    return times


def purchased_at(utility: float) -> tuple[int, int, float]:
    available = max(0.0, utility - EXISTING_OPTIONAL_TOTAL)
    spent = 0
    count = 0
    for node in MASTERY_NODES:
        if available + 1e-9 < node.price:
            break
        available -= node.price
        spent += node.price
        count += 1
    return count, spent, available


def run():
    results = {}
    balanced_optional = next(
        strategy for strategy in OPTIONAL_STRATEGIES
        if strategy.name == "balanced_mastery"
    )

    for strategy in STRATEGIES:
        state_30, history_30 = simulate_with_history(strategy, end_hours=30.0)
        optional_30 = allocate(state_30, history_30, balanced_optional)
        state_45, history_45 = simulate_with_history(strategy, end_hours=45.0)
        optional_45 = allocate(state_45, history_45, balanced_optional)

        existing_complete = all(
            optional_45["indices"][key] == len(BRANCHES[key])
            for key in BRANCHES
        )
        times = node_times(history_45) if existing_complete else [None] * len(MASTERY_NODES)

        if all(optional_30["indices"][key] == len(BRANCHES[key]) for key in BRANCHES):
            count, spent, leftover = purchased_at(state_30.utility_reserve)
        else:
            count, spent, leftover = 0, 0, optional_30["leftover"]

        results[strategy.name] = {
            "utility_30": state_30.utility_reserve,
            "optional_spent_30": optional_30["spent"],
            "optional_leftover_30": optional_30["leftover"],
            "mastery_count_30": count,
            "mastery_spent_30": spent,
            "final_leftover_30": leftover,
            "node_times": times,
        }

    assert EXISTING_OPTIONAL_TOTAL == 30_888_850_000
    assert sum(node.price for node in MASTERY_NODES[:10]) == 20_000_000_000
    assert MASTERY_TOTAL == 25_200_000_000

    balanced = results["balanced"]
    assert balanced["mastery_count_30"] == 10
    assert balanced["mastery_spent_30"] == 20_000_000_000
    assert balanced["final_leftover_30"] <= 100_000_000
    assert 29.8 <= balanced["node_times"][9] <= 30.2
    assert 30.8 <= balanced["node_times"][10] <= 31.3

    gate = results["gate_priority"]
    assert gate["mastery_count_30"] == 11
    assert 4_000_000_000 <= gate["final_leftover_30"] <= 5_000_000_000

    for name in ("combat_priority", "slot_priority"):
        row = results[name]
        assert row["mastery_count_30"] == 6
        assert row["final_leftover_30"] <= 1_000_000_000

    slow = results["slow_balanced_70pct"]
    assert slow["mastery_count_30"] == 0
    assert slow["final_leftover_30"] <= 5_000_000_000

    return results


def main() -> None:
    results = run()
    print("existing optional total", f"{EXISTING_OPTIONAL_TOTAL:,}")
    print("mastery total", f"{MASTERY_TOTAL:,}")
    cumulative = 0
    for index, node in enumerate(MASTERY_NODES, start=1):
        cumulative += node.price
        print(index, node.node_id, f"{node.price:,}", f"{cumulative:,}")
    print()
    for name, row in results.items():
        print(name)
        print("  mastery count 30h", row["mastery_count_30"])
        print("  mastery spent 30h", f"{row['mastery_spent_30']:,.0f}")
        print("  final leftover 30h", f"{row['final_leftover_30']:,.0f}")
        print("  node times", [None if value is None else round(value, 2) for value in row["node_times"]])
    print("All mastery utility sink assertions passed.")


if __name__ == "__main__":
    main()
