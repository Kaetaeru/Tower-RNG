#!/usr/bin/env python3
"""Generate the V1 stage validation plan and planning-rate table.

Only anchor stages receive full combinatorial combat validation. Intermediate
stages use representative lineups unless a new mechanic or a failed acceptance
check promotes them to full validation.
"""

from __future__ import annotations

from dataclasses import dataclass

FULL_VALIDATION_STAGES = {1, 3, 6, 9, 12, 15}
EXTRA_FULL_BENCHMARKS = {2}
PLANNED_CYCLE_SECONDS = {
    1: 56.28,
    2: 66.0,
    3: 78.0,
    4: 62.0,
    5: 68.0,
    6: 75.0,
    7: 68.0,
    8: 75.0,
    9: 82.0,
    10: 76.0,
    11: 84.0,
    12: 90.0,
    13: 86.0,
    14: 93.0,
    15: 100.0,
}
REWARD_UNITS = {stage: 400.0 for stage in range(1, 16)}
REWARD_UNITS[15] = 440.0

MEASURED_CYCLES = {
    1: 56.28,
    2: 65.90,
    3: 78.00,
}

CURRENT_ANCHOR_BUDGETS = {
    1: [60, 75, 70, 70, 110],
    2: [60, 60, 65, 70, 130],
    3: [60, 60, 65, 75, 125],
    15: [60, 60, 70, 105, 130],
}
WAVE_BUDGET_ENVELOPES = {
    1: (50, 70),
    2: (55, 80),
    3: (60, 80),
    4: (65, 110),
    5: (110, 150),
}


@dataclass(frozen=True)
class StagePlan:
    stage: int
    region: int
    position: str
    validation: str
    stage_scale: float
    reward_scale: float
    standard_hp: float
    cycle_seconds: float
    reward_units: float
    defense_xp_per_minute: float


def stage_scale(stage: int) -> float:
    return 10 ** ((stage - 1) / 3)


def reward_scale(stage: int) -> float:
    return stage_scale(stage) * (1.08 ** (stage - 1))


def region_position(stage: int) -> tuple[int, str]:
    region = (stage - 1) // 3 + 1
    position_index = (stage - 1) % 3
    position = ("intro", "middle", "finale")[position_index]
    return region, position


def validation_mode(stage: int) -> str:
    if stage in FULL_VALIDATION_STAGES:
        return "full-anchor"
    if stage in EXTRA_FULL_BENCHMARKS:
        return "full-extra"
    return "light"


def build_plan(stage: int) -> StagePlan:
    region, position = region_position(stage)
    cycle = PLANNED_CYCLE_SECONDS[stage]
    units = REWARD_UNITS[stage]
    scale = stage_scale(stage)
    rewards = reward_scale(stage)
    return StagePlan(
        stage=stage,
        region=region,
        position=position,
        validation=validation_mode(stage),
        stage_scale=scale,
        reward_scale=rewards,
        standard_hp=5.0 * scale,
        cycle_seconds=cycle,
        reward_units=units,
        defense_xp_per_minute=units * rewards / cycle * 60.0,
    )


def validate() -> list[StagePlan]:
    plans = [build_plan(stage) for stage in range(1, 16)]

    assert FULL_VALIDATION_STAGES == {1, 3, 6, 9, 12, 15}
    assert [p.stage for p in plans if p.validation == "light"] == [
        4, 5, 7, 8, 10, 11, 13, 14
    ]
    assert EXTRA_FULL_BENCHMARKS == {2}

    for stage, measured in MEASURED_CYCLES.items():
        planned = PLANNED_CYCLE_SECONDS[stage]
        relative_error = abs(measured - planned) / planned
        assert relative_error <= 0.01, (stage, measured, planned)

    for stage, budgets in CURRENT_ANCHOR_BUDGETS.items():
        assert len(budgets) == 5
        for wave, budget in enumerate(budgets, start=1):
            low, high = WAVE_BUDGET_ENVELOPES[wave]
            assert low <= budget <= high, (stage, wave, budget)
        assert 360 <= sum(budgets) <= 440

    assert all(
        plans[index].standard_hp < plans[index + 1].standard_hp
        for index in range(len(plans) - 1)
    )
    assert all(
        plans[index].defense_xp_per_minute
        < plans[index + 1].defense_xp_per_minute
        for index in range(len(plans) - 1)
    )
    return plans


def main() -> None:
    plans = validate()
    print("V1 stage generation and validation plan")
    print(
        "stage region position validation stage_scale standard_hp "
        "cycle reward_units xp_per_min"
    )
    for plan in plans:
        print(
            f"{plan.stage:>2} {plan.region:>2} {plan.position:>7} "
            f"{plan.validation:>11} {plan.stage_scale:>11.3f} "
            f"{plan.standard_hp:>12.2f} {plan.cycle_seconds:>6.2f} "
            f"{plan.reward_units:>6.0f} {plan.defense_xp_per_minute:>14.2f}"
        )
    print("All stage validation-plan assertions passed.")


if __name__ == "__main__":
    main()
