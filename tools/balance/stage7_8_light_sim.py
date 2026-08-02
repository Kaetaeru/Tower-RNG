#!/usr/bin/env python3
"""Lightweight Stage 7 and Stage 8 jungle benchmarks for Tower RNG.

The model reuses the behavior implementation that was fully validated by the
Stage 9 regional-finale benchmark. Six representative role formations are used
for each stage. Promote either stage to full validation if these acceptance
checks fail or its catalog later introduces a materially different behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median

import stage9_wave_sim as core

BOSS_REWARD_MODIFIER = 1.15

SEVEN_SLOT_LINEUPS: dict[str, tuple[str, ...]] = {
    "balanced": (
        "archer", "slinger", "frost", "rogue", "drummer", "hunter", "archer"
    ),
    "aoe_missing": (
        "archer", "archer", "archer", "frost", "rogue", "drummer", "hunter"
    ),
    "single_missing": (
        "slinger", "slinger", "frost", "frost", "rogue", "drummer", "hunter"
    ),
    "control_missing": (
        "archer", "archer", "slinger", "rogue", "drummer", "hunter", "hunter"
    ),
    "support_missing": (
        "archer", "archer", "slinger", "frost", "rogue", "hunter", "hunter"
    ),
    "large_missing": (
        "archer", "archer", "slinger", "slinger", "frost", "rogue", "drummer"
    ),
}

EIGHT_SLOT_LINEUPS: dict[str, tuple[str, ...]] = {
    "balanced": (
        "archer", "slinger", "frost", "rogue", "drummer", "hunter",
        "archer", "slinger",
    ),
    "aoe_missing": (
        "archer", "archer", "archer", "frost", "rogue", "drummer",
        "hunter", "hunter",
    ),
    "single_missing": (
        "slinger", "slinger", "slinger", "frost", "rogue", "drummer",
        "hunter", "hunter",
    ),
    "control_missing": (
        "archer", "archer", "slinger", "slinger", "rogue", "drummer",
        "hunter", "hunter",
    ),
    "support_missing": (
        "archer", "archer", "slinger", "slinger", "frost", "rogue",
        "hunter", "hunter",
    ),
    "large_missing": (
        "archer", "archer", "slinger", "slinger", "frost", "rogue",
        "drummer", "rogue",
    ),
}


@dataclass(frozen=True)
class StageDefinition:
    stage: int
    planned_cycle_seconds: float
    entry_multiplier: float
    farm_multiplier: float
    lineups: dict[str, tuple[str, ...]]
    waves: dict[int, list[core.SpawnEntry]]

    @property
    def stage_scale(self) -> float:
        return 10 ** ((self.stage - 1) / 3)

    @property
    def reward_scale(self) -> float:
        return self.stage_scale * (1.08 ** (self.stage - 1))


def build_stage_7() -> StageDefinition:
    scale = 10 ** ((7 - 1) / 3)
    child = core.MonsterSpec(
        monster_id="MON_JUNGLE_SPORELING",
        hp=0.20 * scale,
        time_to_base=14.0,
        spawn_cost=0,
        base_damage=1,
        tags=frozenset({"swarm", "child"}),
        reward_modifier=0.0,
    )
    pod = core.MonsterSpec(
        monster_id="MON_SPORE_POD",
        hp=0.55 * scale,
        time_to_base=17.0,
        spawn_cost=5,
        base_damage=1,
        tags=frozenset({"swarm"}),
        split_count=2,
        split_child=child,
    )
    vine = core.MonsterSpec(
        monster_id="MON_VINE_STALKER",
        hp=3.00 * scale,
        time_to_base=22.0,
        spawn_cost=10,
        base_damage=1,
        tags=frozenset({"fast"}),
        dash_at_progress=0.55,
        dash_progress=0.08,
    )
    guardian = core.MonsterSpec(
        monster_id="MON_REGROWTH_GUARDIAN",
        hp=6.50 * scale,
        time_to_base=34.0,
        spawn_cost=30,
        base_damage=3,
        tags=frozenset({"thick", "regenerating"}),
        phase_heal_at_fraction=0.45,
        phase_heal_fraction=0.15,
    )
    boss = core.MonsterSpec(
        monster_id="BOSS_SPORE_MATRIARCH",
        hp=17.0 * scale,
        time_to_base=56.0,
        spawn_cost=100,
        base_damage=10,
        tags=frozenset({"boss", "elite", "large", "regenerating"}),
        shield_fraction=0.06,
        phase_heal_at_fraction=0.55,
        phase_heal_fraction=0.08,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )
    waves = {
        1: [core.SpawnEntry(index * 0.55, pod) for index in range(12)],
        2: [core.SpawnEntry(index * 0.85, vine) for index in range(6)],
        3: [
            core.SpawnEntry(0.00, guardian),
            core.SpawnEntry(0.90, pod),
            core.SpawnEntry(1.80, vine),
            core.SpawnEntry(2.70, pod),
            core.SpawnEntry(3.60, vine),
            core.SpawnEntry(4.50, pod),
        ],
        4: [
            core.SpawnEntry(0.00, guardian),
            core.SpawnEntry(1.10, guardian),
            core.SpawnEntry(2.20, vine),
            core.SpawnEntry(3.30, pod),
        ],
        5: [core.SpawnEntry(0.00, boss)]
        + [core.SpawnEntry(1.60 + index * 1.40, pod) for index in range(5)],
    }
    return StageDefinition(7, 68.0, 16.0, 18.8, SEVEN_SLOT_LINEUPS, waves)


def build_stage_8() -> StageDefinition:
    scale = 10 ** ((8 - 1) / 3)
    child = core.MonsterSpec(
        monster_id="MON_JUNGLE_SPORELING",
        hp=0.20 * scale,
        time_to_base=14.0,
        spawn_cost=0,
        base_damage=1,
        tags=frozenset({"swarm", "child"}),
        reward_modifier=0.0,
    )
    pod = core.MonsterSpec(
        monster_id="MON_SPORE_POD",
        hp=0.55 * scale,
        time_to_base=17.0,
        spawn_cost=5,
        base_damage=1,
        tags=frozenset({"swarm"}),
        split_count=2,
        split_child=child,
    )
    vine = core.MonsterSpec(
        monster_id="MON_VINE_STALKER",
        hp=3.00 * scale,
        time_to_base=22.0,
        spawn_cost=10,
        base_damage=1,
        tags=frozenset({"fast"}),
        dash_at_progress=0.55,
        dash_progress=0.08,
    )
    guardian = core.MonsterSpec(
        monster_id="MON_REGROWTH_GUARDIAN",
        hp=6.50 * scale,
        time_to_base=34.0,
        spawn_cost=30,
        base_damage=3,
        tags=frozenset({"thick", "regenerating"}),
        phase_heal_at_fraction=0.45,
        phase_heal_fraction=0.15,
    )
    boss = core.MonsterSpec(
        monster_id="BOSS_VINE_BEHEMOTH",
        hp=19.0 * scale,
        time_to_base=57.0,
        spawn_cost=100,
        base_damage=11,
        tags=frozenset({"boss", "elite", "large", "regenerating"}),
        shield_fraction=0.08,
        phase_heal_at_fraction=0.55,
        phase_heal_fraction=0.12,
        untargetable_at_fraction=0.30,
        untargetable_duration=0.80,
        untargetable_progress=0.03,
        reward_modifier=BOSS_REWARD_MODIFIER,
    )
    waves = {
        1: [core.SpawnEntry(index * 0.55, pod) for index in range(12)],
        2: [core.SpawnEntry(index * 0.85, vine) for index in range(6)],
        3: [
            core.SpawnEntry(0.00, guardian),
            core.SpawnEntry(0.90, pod),
            core.SpawnEntry(1.80, vine),
            core.SpawnEntry(2.70, pod),
            core.SpawnEntry(3.60, vine),
            core.SpawnEntry(4.50, pod),
        ],
        4: [
            core.SpawnEntry(0.00, guardian),
            core.SpawnEntry(1.10, guardian),
            core.SpawnEntry(2.20, vine),
            core.SpawnEntry(3.30, pod),
        ],
        5: [core.SpawnEntry(0.00, boss)]
        + [core.SpawnEntry(1.60 + index * 1.40, pod) for index in range(5)],
    }
    return StageDefinition(8, 75.0, 28.0, 32.5, EIGHT_SLOT_LINEUPS, waves)


def wave_budget(stage: StageDefinition, wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in stage.waves[wave_number])


def wave_reward_units(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in stage.waves[wave_number]
    )


def spec_effective_hp(spec: core.MonsterSpec) -> float:
    total = spec.hp * (
        1.0 + spec.shield_fraction + spec.phase_heal_fraction
    )
    if spec.split_count and spec.split_child is not None:
        total += spec.split_count * spec_effective_hp(spec.split_child)
    return total


def wave_effective_hp(stage: StageDefinition, wave_number: int) -> float:
    return sum(
        spec_effective_hp(entry.spec)
        for entry in stage.waves[wave_number]
    )


def profile_results(stage: StageDefinition, multiplier: float):
    previous_waves = core.WAVES
    core.WAVES = stage.waves
    try:
        rows: dict[int, dict[str, core.SimulationResult]] = {}
        for wave_number in range(1, 6):
            rows[wave_number] = {
                name: core.simulate(lineup, wave_number, multiplier)
                for name, lineup in stage.lineups.items()
            }
    finally:
        core.WAVES = previous_waves

    cycles = {
        name: sum(rows[wave][name].clear_time for wave in range(1, 6))
        for name in stage.lineups
    }
    return rows, cycles


def validate_stage(stage: StageDefinition) -> None:
    assert [wave_budget(stage, wave) for wave in range(1, 6)] == [
        60, 60, 65, 75, 125
    ]
    assert abs(
        sum(wave_reward_units(stage, wave) for wave in range(1, 6)) - 400.0
    ) < 1e-9

    entry_rows, entry_cycles = profile_results(stage, stage.entry_multiplier)
    farm_rows, farm_cycles = profile_results(stage, stage.farm_multiplier)

    assert all(
        result.leaks == 0
        for rows in (entry_rows, farm_rows)
        for wave in rows.values()
        for result in wave.values()
    )

    farm_average = mean(farm_cycles.values())
    assert abs(farm_average - stage.planned_cycle_seconds) / stage.planned_cycle_seconds <= 0.05
    assert max(farm_cycles.values()) <= stage.planned_cycle_seconds * 1.20

    boss_average = mean(
        result.clear_time for result in farm_rows[5].values()
    )
    boss_share = boss_average / farm_average
    assert 0.25 <= boss_share <= 0.35

    balanced = farm_cycles["balanced"]
    assert max(farm_cycles.values()) <= balanced * 1.25

    assert mean(entry_cycles.values()) > farm_average
    assert max(entry_cycles.values()) <= stage.planned_cycle_seconds * 1.40


def print_profile(stage: StageDefinition, label: str, multiplier: float) -> None:
    rows, cycles = profile_results(stage, multiplier)
    print(
        f"Stage {stage.stage} {label}: multiplier=x{multiplier:.2f} "
        f"lineups={len(stage.lineups)}"
    )
    for wave_number in range(1, 6):
        results = list(rows[wave_number].values())
        times = [result.clear_time for result in results]
        print(
            f"  W{wave_number}: budget={wave_budget(stage, wave_number):>3} "
            f"reward={wave_reward_units(stage, wave_number):>6.1f} "
            f"effective_hp={wave_effective_hp(stage, wave_number):>9.2f} "
            f"avg={mean(times):>5.2f}s median={median(times):>5.2f}s "
            f"best={min(times):>5.2f}s worst={max(times):>5.2f}s "
            f"leaks={sum(result.leaks for result in results)}"
        )
    boss_average = mean(
        result.clear_time for result in rows[5].values()
    )
    print(
        f"  Cycle: avg={mean(cycles.values()):.2f}s "
        f"median={median(cycles.values()):.2f}s "
        f"best={min(cycles.values()):.2f}s "
        f"worst={max(cycles.values()):.2f}s "
        f"boss_share={boss_average / mean(cycles.values()) * 100:.1f}%"
    )
    print(
        "  Lineups: "
        + ", ".join(
            f"{name}={seconds:.2f}s"
            for name, seconds in cycles.items()
        )
    )


def main() -> None:
    stages = [build_stage_7(), build_stage_8()]
    for stage in stages:
        validate_stage(stage)
        print(
            f"\nSTAGE {stage.stage}: scale={stage.stage_scale:.8f} "
            f"reward_scale={stage.reward_scale:.8f} "
            f"planned={stage.planned_cycle_seconds:.2f}s"
        )
        print_profile(stage, "entry", stage.entry_multiplier)
        print_profile(stage, "farm", stage.farm_multiplier)
        _, farm_cycles = profile_results(stage, stage.farm_multiplier)
        xp_per_minute = (
            sum(wave_reward_units(stage, wave) for wave in range(1, 6))
            * stage.reward_scale
            * 60.0
            / mean(farm_cycles.values())
        )
        print(f"  Defense XP/min={xp_per_minute:,.2f}")

    print("\nAll Stage 7-8 lightweight benchmark assertions passed.")


if __name__ == "__main__":
    main()
