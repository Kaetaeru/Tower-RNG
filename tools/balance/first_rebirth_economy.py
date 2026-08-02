"""Deterministic first-rebirth economy benchmark for Tower RNG.

This planning model connects Stage 1 combat output to early permanent purchases,
Stage 2/3 gate prices, and the first Defense XP requirement. It intentionally
uses scenario-based stage readiness because the launch probability table and
full tower roster are not complete yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

TICK_SECONDS = 0.10
MAX_SECONDS = 15 * 60
STAGE_BUDGET_PER_CYCLE = 385.0
FIRST_REBIRTH_XP = 6_500.0

STAGE_REWARD_SCALE = {
    1: 1.0,
    2: 2.15443469 * 1.08,
    3: 4.64158883 * (1.08**2),
}

# Stage 1 is measured. Stage 2 and 3 are economy-planning targets only.
BASE_CYCLE_SECONDS = {
    1: 56.28,
    2: 66.0,
    3: 78.0,
}


@dataclass(frozen=True)
class Purchase:
    purchase_id: str
    name: str
    cost: int
    effect: str = "none"
    value: float = 0.0


@dataclass(frozen=True)
class Event:
    second: float
    name: str
    stage: int
    defense_xp: float
    remaining_coin: float


@dataclass(frozen=True)
class ScenarioResult:
    strategy: str
    readiness: str
    rebirth_second: float
    final_stage: int
    remaining_coin: float
    events: tuple[Event, ...]


PURCHASES = {
    "AUTO_ROLL": Purchase("AUTO_ROLL", "자동 굴리기", 10),
    "AUTO_FORMATION": Purchase("AUTO_FORMATION", "자동 편성", 30),
    "MAGNET_RANGE_1": Purchase(
        "MAGNET_RANGE_1", "자석 범위 I", 50, "collection", 0.85
    ),
    "CORE_OUTPUT_1": Purchase(
        "CORE_OUTPUT_1", "핵심 성능 I", 100, "output", 0.25
    ),
    "ROLL_SPEED_1": Purchase("ROLL_SPEED_1", "굴리기 속도 I", 160),
    "STAGE_2_GATE": Purchase(
        "STAGE_2_GATE", "스테이지 2 문", 750, "gate", 2
    ),
    "MAGNET_SPEED_1": Purchase(
        "MAGNET_SPEED_1", "자석 속도 I", 220, "collection", 0.92
    ),
    "COMBAT_BRANCH": Purchase("COMBAT_BRANCH", "전투 분야 해금", 450),
    "CORE_OUTPUT_2": Purchase(
        "CORE_OUTPUT_2", "핵심 성능 II", 650, "output", 0.25
    ),
    "STAGE_3_GATE": Purchase(
        "STAGE_3_GATE", "스테이지 3 문", 3_200, "gate", 3
    ),
    "COIN_YIELD_1": Purchase(
        "COIN_YIELD_1", "코인 획득 I", 550, "coin", 0.15
    ),
    "FORMATION_SLOT_5": Purchase(
        "FORMATION_SLOT_5", "편성 슬롯 5", 1_200, "output", 0.25
    ),
}

STRATEGIES = {
    "balanced": (
        "AUTO_ROLL",
        "AUTO_FORMATION",
        "MAGNET_RANGE_1",
        "CORE_OUTPUT_1",
        "ROLL_SPEED_1",
        "STAGE_2_GATE",
        "MAGNET_SPEED_1",
        "COMBAT_BRANCH",
        "CORE_OUTPUT_2",
        "STAGE_3_GATE",
        "COIN_YIELD_1",
        "FORMATION_SLOT_5",
    ),
    "door_rush": (
        "AUTO_ROLL",
        "AUTO_FORMATION",
        "MAGNET_RANGE_1",
        "CORE_OUTPUT_1",
        "STAGE_2_GATE",
        "ROLL_SPEED_1",
        "STAGE_3_GATE",
        "MAGNET_SPEED_1",
        "COMBAT_BRANCH",
        "CORE_OUTPUT_2",
        "COIN_YIELD_1",
        "FORMATION_SLOT_5",
    ),
    "tree_first": (
        "AUTO_ROLL",
        "AUTO_FORMATION",
        "MAGNET_RANGE_1",
        "CORE_OUTPUT_1",
        "ROLL_SPEED_1",
        "MAGNET_SPEED_1",
        "COMBAT_BRANCH",
        "CORE_OUTPUT_2",
        "COIN_YIELD_1",
        "STAGE_2_GATE",
        "FORMATION_SLOT_5",
        "STAGE_3_GATE",
    ),
}

# These are not player percentiles. They represent future tower-roster outcomes.
READINESS_SCENARIOS = {
    "stage1_only": {2: 9_999.0, 3: 9_999.0},
    "slow_stage2": {2: 5 * 60.0, 3: 9_999.0},
    "median_stage2": {2: 3.5 * 60.0, 3: 10 * 60.0},
    "fast_stage2": {2: 2.5 * 60.0, 3: 7 * 60.0},
}


def onboarding_efficiency(second: float) -> float:
    """Approximate the first rolls filling four formation slots."""
    if second < 10:
        return 0.25
    if second < 25:
        return 0.55
    if second < 40:
        return 0.80
    return 1.0


def cycle_seconds(stage: int, output_multiplier: float) -> float:
    """Planning-only output elasticity with a spawn/animation floor."""
    nominal = BASE_CYCLE_SECONDS[stage]
    return max(nominal * 0.58, nominal / (output_multiplier**0.72))


def simulate(strategy: str, readiness: str) -> ScenarioResult:
    order = STRATEGIES[strategy]
    ready_at = READINESS_SCENARIOS[readiness]

    second = 0.0
    coin = 0.0
    defense_xp = 0.0
    collection_efficiency = 0.75
    output_multiplier = 1.0
    coin_multiplier = 1.0
    current_stage = 1
    opened_stages = {1}
    next_purchase_index = 0
    events: list[Event] = []

    while second < MAX_SECONDS and defense_xp < FIRST_REBIRTH_XP:
        if next_purchase_index < len(order):
            purchase = PURCHASES[order[next_purchase_index]]
            if coin >= purchase.cost:
                coin -= purchase.cost
                next_purchase_index += 1

                if purchase.effect == "collection":
                    collection_efficiency = purchase.value
                elif purchase.effect == "output":
                    output_multiplier += purchase.value
                elif purchase.effect == "coin":
                    coin_multiplier += purchase.value
                elif purchase.effect == "gate":
                    opened_stages.add(int(purchase.value))

                events.append(
                    Event(
                        second=second,
                        name=purchase.name,
                        stage=current_stage,
                        defense_xp=defense_xp,
                        remaining_coin=coin,
                    )
                )

        for stage in (3, 2):
            if stage in opened_stages and second >= ready_at[stage]:
                current_stage = stage
                break

        efficiency = onboarding_efficiency(second)
        gross_rate = (
            STAGE_BUDGET_PER_CYCLE
            * STAGE_REWARD_SCALE[current_stage]
            / cycle_seconds(current_stage, output_multiplier)
        )

        defense_xp += gross_rate * efficiency * TICK_SECONDS
        coin += (
            gross_rate
            * collection_efficiency
            * coin_multiplier
            * efficiency
            * TICK_SECONDS
        )
        second += TICK_SECONDS

    return ScenarioResult(
        strategy=strategy,
        readiness=readiness,
        rebirth_second=second,
        final_stage=current_stage,
        remaining_coin=coin,
        events=tuple(events),
    )


def event_time(result: ScenarioResult, name: str) -> float | None:
    for event in result.events:
        if event.name == name:
            return event.second
    return None


def validate(results: list[ScenarioResult]) -> None:
    for result in results:
        assert 7 * 60 <= result.rebirth_second <= 15 * 60, result

    balanced_median = next(
        result
        for result in results
        if result.strategy == "balanced" and result.readiness == "median_stage2"
    )

    assert (event_time(balanced_median, "자동 굴리기") or 999) <= 15
    assert (event_time(balanced_median, "자동 편성") or 999) <= 30
    assert (event_time(balanced_median, "자석 범위 I") or 999) <= 45

    stage_2_time = event_time(balanced_median, "스테이지 2 문")
    stage_3_time = event_time(balanced_median, "스테이지 3 문")
    assert stage_2_time is not None and 2 * 60 <= stage_2_time <= 5 * 60
    assert stage_3_time is not None and 5 * 60 <= stage_3_time <= 10 * 60


def main() -> None:
    results = [
        simulate(strategy, readiness)
        for strategy in STRATEGIES
        for readiness in READINESS_SCENARIOS
    ]
    validate(results)

    print("First rebirth economy benchmark")
    print("StageCoinUnit: 1")
    print(f"FirstRebirthXP: {FIRST_REBIRTH_XP:,.0f}")
    print()

    for strategy in STRATEGIES:
        rows = [result for result in results if result.strategy == strategy]
        print(strategy)
        for result in rows:
            print(
                f"  {result.readiness:14} "
                f"rebirth={result.rebirth_second / 60:5.2f}m "
                f"stage={result.final_stage} "
                f"purchases={len(result.events):2} "
                f"coin={result.remaining_coin:7.0f}"
            )
        print(
            "  average rebirth: "
            f"{mean(result.rebirth_second for result in rows) / 60:.2f}m"
        )
        print()

    median = next(
        result
        for result in results
        if result.strategy == "balanced" and result.readiness == "median_stage2"
    )
    print("Balanced / median purchase timeline")
    for event in median.events:
        print(
            f"  {event.second / 60:5.2f}m  {event.name:16} "
            f"stage={event.stage} xp={event.defense_xp:7.0f}"
        )


if __name__ == "__main__":
    main()
