#!/usr/bin/env python3
"""Budget residual Roblox runtime losses after modeled combat behavior.

This is a pre-implementation sensitivity benchmark, not an observed Roblox
profile. Engage approach, attack intervals, spawn timing, shields, and monster
behaviors are already represented by the wave simulators. The factors below
therefore cover only residual implementation loss such as unresolved overkill,
projectile settlement, retarget latency, and server scheduling.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Anchor:
    stage: int
    ideal_cycle: float
    support_retention: float
    overkill: float
    projectile: float
    retarget: float
    tick: float

    @property
    def runtime_efficiency(self) -> float:
        return self.overkill * self.projectile * self.retarget * self.tick

    @property
    def combined_efficiency(self) -> float:
        return self.support_retention * self.runtime_efficiency

    @property
    def adjusted_cycle(self) -> float:
        return self.ideal_cycle / self.combined_efficiency


ANCHORS = [
    Anchor(1, 56.28, 1.00000, 0.998, 0.998, 0.998, 0.998),
    Anchor(9, 81.98, 0.96855, 0.997, 0.997, 0.998, 0.998),
    Anchor(12, 90.25, 0.96567, 0.996, 0.997, 0.997, 0.998),
    Anchor(15, 113.20, 0.96672, 0.995, 0.997, 0.996, 0.998),
]

STAGE15_OTHER = {
    "15h P50": 60.26,
    "30h P10": 34.81,
}

# Sensitivity case when damage reservation, prompt retargeting, and bounded
# server scheduling are not implemented.
STRESS_RUNTIME_EFFICIENCY = 0.90


def run() -> tuple[list[dict[str, float]], float]:
    rows = []
    for anchor in ANCHORS:
        rows.append(
            {
                "stage": float(anchor.stage),
                "runtime_efficiency": anchor.runtime_efficiency,
                "combined_efficiency": anchor.combined_efficiency,
                "ideal_cycle": anchor.ideal_cycle,
                "adjusted_cycle": anchor.adjusted_cycle,
                "increase": anchor.adjusted_cycle / anchor.ideal_cycle - 1.0,
            }
        )

    assert all(row["runtime_efficiency"] >= 0.985 for row in rows)
    assert all(row["increase"] <= 0.05 for row in rows)
    assert rows[-1]["adjusted_cycle"] <= 120.0

    stage15 = ANCHORS[-1]
    stress_cycle = stage15.ideal_cycle / (
        stage15.support_retention * STRESS_RUNTIME_EFFICIENCY
    )
    assert stress_cycle > 125.0
    return rows, stress_cycle


def main() -> None:
    rows, stress_cycle = run()
    for row in rows:
        print(row)

    stage15 = ANCHORS[-1]
    for label, cycle in STAGE15_OTHER.items():
        print(label, cycle / stage15.combined_efficiency)

    print("stage15 stress", stress_cycle)
    print(
        "All runtime budget assertions passed. "
        "Actual Roblox measurement remains pending."
    )


if __name__ == "__main__":
    main()
