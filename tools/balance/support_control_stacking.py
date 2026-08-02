#!/usr/bin/env python3
"""Formation-level support/control stacking benchmark for Tower RNG.

The benchmark does not replace wave simulators. It establishes effect stacking
contracts and checks their formation-level contribution at the representative
4, 9 and 12 slot milestones.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from statistics import mean, median

BASE_DIRECT_EC = 1.0
UTILITY_DIRECT_EC = 0.55
SUPPORT_RATE = 0.15
SUPPORT_TARGET_CAP = 3
CONTROL_SLOW = 0.15
SUPPORT_CHANNEL_CAP = 0.50
SUPPORT_TOTAL_OUTPUT_CAP = 1.75
NORMAL_EFFECTIVE_TARGETS = 2
BOSS_EFFECTIVE_TARGETS = 1
NORMAL_WAVE_WEIGHT = 0.80
BOSS_WAVE_WEIGHT = 0.20

SLOW_CAPS = {
    "normal": 0.60,
    "elite": 0.45,
    "boss": 0.35,
}
HARD_CONTROL_DOWNTIME_CAPS = {
    "normal": 0.60,
    "elite": 0.40,
    "boss": 0.25,
}


@dataclass(frozen=True)
class SlotProfile:
    label: str
    slots: int
    role_cap: int
    minimum_roles: int


PROFILES = (
    SlotProfile("Stage 1", 4, 2, 2),
    SlotProfile("Stage 9", 9, 3, 5),
    SlotProfile("Stage 15", 12, 4, 5),
)


def support_bonus_for_target(source_ec: float, target_ec: float) -> float:
    """15% target bonus, capped to 15% of source EC per target."""

    return min(target_ec * SUPPORT_RATE, source_ec * SUPPORT_RATE)


def support_lineup_total(slots: int, support_count: int) -> float:
    """Equal-power same-group support copies using coverage-first targeting."""

    damage_count = slots - support_count
    covered = min(damage_count, support_count * SUPPORT_TARGET_CAP)
    direct = support_count * UTILITY_DIRECT_EC + damage_count * BASE_DIRECT_EC
    indirect = covered * support_bonus_for_target(1.0, 1.0)
    return direct + indirect


def control_scenario_total(
    slots: int,
    control_count: int,
    effective_targets: int,
) -> float:
    """Same-group controls spread to unique targets; magnitude does not stack."""

    damage_count = slots - control_count
    direct = control_count * UTILITY_DIRECT_EC + damage_count * BASE_DIRECT_EC
    if control_count == 0:
        return direct
    coverage = min(control_count, effective_targets) / effective_targets
    indirect = damage_count * BASE_DIRECT_EC * CONTROL_SLOW * coverage
    return direct + indirect


def control_cycle_total(slots: int, control_count: int) -> float:
    normal = control_scenario_total(
        slots,
        control_count,
        NORMAL_EFFECTIVE_TARGETS,
    )
    boss = control_scenario_total(
        slots,
        control_count,
        BOSS_EFFECTIVE_TARGETS,
    )
    return normal * NORMAL_WAVE_WEIGHT + boss * BOSS_WAVE_WEIGHT


def combined_scenario_total(
    slots: int,
    support_count: int,
    control_count: int,
    effective_targets: int,
) -> float:
    damage_count = slots - support_count - control_count
    if damage_count < 0:
        raise ValueError("Utility count exceeds slots")

    capacity = support_count * SUPPORT_TARGET_CAP
    covered_damage = min(damage_count, capacity)
    capacity -= covered_damage
    covered_control = min(control_count, max(0, capacity))

    support_bonus = (
        covered_damage * support_bonus_for_target(1.0, 1.0)
        + covered_control
        * support_bonus_for_target(1.0, UTILITY_DIRECT_EC)
    )

    base_direct = (
        damage_count * BASE_DIRECT_EC
        + support_count * UTILITY_DIRECT_EC
        + control_count * UTILITY_DIRECT_EC
    )

    non_controller_output = (
        damage_count * BASE_DIRECT_EC
        + support_count * UTILITY_DIRECT_EC
        + support_bonus
    )
    coverage = (
        min(control_count, effective_targets) / effective_targets
        if control_count > 0
        else 0.0
    )
    control_bonus = non_controller_output * CONTROL_SLOW * coverage
    return base_direct + support_bonus + control_bonus


def combined_cycle_total(
    slots: int,
    support_count: int,
    control_count: int,
) -> float:
    normal = combined_scenario_total(
        slots,
        support_count,
        control_count,
        NORMAL_EFFECTIVE_TARGETS,
    )
    boss = combined_scenario_total(
        slots,
        support_count,
        control_count,
        BOSS_EFFECTIVE_TARGETS,
    )
    return normal * NORMAL_WAVE_WEIGHT + boss * BOSS_WAVE_WEIGHT


def combined_support_channel(distinct_effect_count: int) -> float:
    """Different support StackGroups in one stat channel add, then cap."""

    return min(distinct_effect_count * SUPPORT_RATE, SUPPORT_CHANNEL_CAP)


def combined_slow(distinct_effect_count: int, target_class: str) -> float:
    raw = 1.0 - prod(1.0 - CONTROL_SLOW for _ in range(distinct_effect_count))
    return min(raw, SLOW_CAPS[target_class])


def legacy_to_budgeted_support_ratio(
    slots: int,
    role_cap: int,
    minimum_roles: int,
) -> list[float]:
    """Compare old global +15% aura to 3-target source-budgeted support."""

    role_direct = (1.0, 1.002, 0.55, 1.008, 0.55, 0.995)
    support_index = 4
    ratios: list[float] = []

    for counts in product(range(role_cap + 1), repeat=6):
        if sum(counts) != slots:
            continue
        if sum(count > 0 for count in counts) < minimum_roles:
            continue

        support_count = counts[support_index]
        support_direct = support_count * role_direct[support_index]
        recipients = [
            role_direct[index]
            for index, count in enumerate(counts)
            if index != support_index
            for _ in range(count)
        ]

        if support_count == 0:
            legacy = sum(recipients)
            budgeted = legacy
        else:
            legacy = support_direct + sum(recipients) * (1.0 + SUPPORT_RATE)
            coverage = min(len(recipients), support_count * SUPPORT_TARGET_CAP)
            selected = sorted(recipients, reverse=True)[:coverage]
            budgeted = support_direct + sum(recipients) + sum(
                support_bonus_for_target(1.0, target_ec)
                for target_ec in selected
            )

        ratios.append(budgeted / legacy)

    return ratios


def validate() -> None:
    for profile in PROFILES:
        baseline = float(profile.slots)

        assert abs(support_lineup_total(profile.slots, 1) - baseline) < 1e-9

        support_ratios = [
            support_lineup_total(profile.slots, count) / baseline
            for count in range(profile.role_cap + 1)
        ]
        control_ratios = [
            control_cycle_total(profile.slots, count) / baseline
            for count in range(profile.role_cap + 1)
        ]
        assert max(support_ratios) <= 1.0000001
        assert min(support_ratios) >= 0.85 - 1e-9
        assert max(control_ratios) <= 1.05 + 1e-9
        assert min(control_ratios) >= 0.85 - 1e-9

        utility_ratios = []
        for support_count in range(profile.role_cap + 1):
            for control_count in range(profile.role_cap + 1):
                if support_count + control_count > profile.role_cap:
                    continue
                utility_ratios.append(
                    combined_cycle_total(
                        profile.slots,
                        support_count,
                        control_count,
                    )
                    / baseline
                )
        assert max(utility_ratios) <= 1.05 + 1e-9
        assert min(utility_ratios) >= 0.85 - 1e-9

    assert abs(combined_support_channel(3) - 0.45) < 1e-9
    assert abs(combined_support_channel(4) - 0.50) < 1e-9

    assert abs(combined_slow(2, "normal") - 0.2775) < 1e-9
    assert abs(combined_slow(3, "boss") - 0.35) < 1e-9
    assert abs(combined_slow(4, "elite") - 0.45) < 1e-9

    for slots, cap, minimum_roles in ((9, 3, 5), (10, 4, 5), (12, 4, 5)):
        ratios = legacy_to_budgeted_support_ratio(slots, cap, minimum_roles)
        assert mean(ratios) >= 0.96


def main() -> None:
    validate()

    print("Support/control stacking benchmark")
    for profile in PROFILES:
        print(
            f"\n{profile.label}: slots={profile.slots}, "
            f"role_cap={profile.role_cap}"
        )
        print("support_count | total_EC | baseline_ratio")
        for count in range(profile.role_cap + 1):
            total = support_lineup_total(profile.slots, count)
            print(f"{count:>13} | {total:>8.3f} | {total/profile.slots:>14.3%}")

        print("control_count | cycle_EC | baseline_ratio")
        for count in range(profile.role_cap + 1):
            total = control_cycle_total(profile.slots, count)
            print(f"{count:>13} | {total:>8.3f} | {total/profile.slots:>14.3%}")

        utility_rows = []
        for support_count in range(profile.role_cap + 1):
            for control_count in range(profile.role_cap + 1):
                if support_count + control_count > profile.role_cap:
                    continue
                total = combined_cycle_total(
                    profile.slots,
                    support_count,
                    control_count,
                )
                utility_rows.append((total / profile.slots, support_count, control_count))
        best = max(utility_rows)
        worst = min(utility_rows)
        print(
            "utility<=role_cap: "
            f"min={worst[0]:.3%} at S{worst[1]}/C{worst[2]}, "
            f"max={best[0]:.3%} at S{best[1]}/C{best[2]}"
        )

    print("\nSupport source-power safety")
    for source_ec, target_ec in ((1.0, 1.0), (1.0, 100.0), (100.0, 100.0)):
        each = support_bonus_for_target(source_ec, target_ec)
        print(
            f"source={source_ec:>6.1f}, target={target_ec:>6.1f}, "
            f"bonus_per_target={each:>6.2f}, three_target_total={each*3:>7.2f}"
        )

    print("\nDistinct +15% support groups in one stat channel")
    print("groups | combined bonus")
    for count in range(1, 5):
        print(f"{count:>6} | {combined_support_channel(count):>14.1%}")
    print(f"total cross-channel output cap: x{SUPPORT_TOTAL_OUTPUT_CAP:.2f}")

    print("\nDistinct 15% slow groups")
    print("groups | raw | normal | elite | boss")
    for count in range(1, 5):
        raw = 1.0 - prod(1.0 - CONTROL_SLOW for _ in range(count))
        print(
            f"{count:>6} | {raw:>5.1%} | "
            f"{combined_slow(count, 'normal'):>6.1%} | "
            f"{combined_slow(count, 'elite'):>5.1%} | "
            f"{combined_slow(count, 'boss'):>5.1%}"
        )

    print("\nHard-control rolling 5-second budget")
    for target_class, cap in HARD_CONTROL_DOWNTIME_CAPS.items():
        print(
            f"{target_class:>6}: cap={cap:.0%}, "
            f"maximum_disabled_time={5.0*cap:.2f}s"
        )

    print("\nLegacy global support aura sensitivity")
    for slots, cap, minimum_roles in ((9, 3, 5), (10, 4, 5), (12, 4, 5)):
        ratios = legacy_to_budgeted_support_ratio(slots, cap, minimum_roles)
        timing_factor = 1.0 / mean(ratios)
        print(
            f"slots={slots}: lineups={len(ratios)}, "
            f"avg_output_ratio={mean(ratios):.3%}, "
            f"median={median(ratios):.3%}, worst={min(ratios):.3%}, "
            f"proxy_cycle_change=+{(timing_factor-1.0)*100:.2f}%"
        )

    print("All support/control stacking assertions passed.")


if __name__ == "__main__":
    main()
