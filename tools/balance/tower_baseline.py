"""Deterministic first-pass benchmark for the six lowest-tier Tower RNG towers.

This is not the runtime combat simulator. It validates the provisional catalog
numbers against the shared benchmark assumptions documented in
`docs/reference/TOWER_BALANCE_BENCHMARK.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil

STANDARD_HP = 5.0
STANDARD_TIME_TO_BASE = 10.0
FORMATION_INITIAL_DELAY = 0.25
ENGAGE_APPROACH_DELAY = 0.50
NORMAL_WAVE_SECONDS = 10.0
BOSS_WAVE_SECONDS = 17.5
OTHER_FORMATION_SLOTS = 3
BASELINE_ALLY_CONTRIBUTION = 1.0
EC_TOLERANCE = 0.03


@dataclass(frozen=True)
class BenchmarkResult:
    tower: str
    solo_ttk: float
    arrival_time: float
    equivalent_contribution: float
    note: str

    @property
    def solo_pass(self) -> bool:
        return self.solo_ttk < self.arrival_time

    @property
    def contribution_pass(self) -> bool:
        return abs(self.equivalent_contribution - 1.0) <= EC_TOLERANCE


def periodic_ttk(
    damage: float,
    interval: float,
    first_delay: float,
    *,
    hp: float = STANDARD_HP,
    execute_threshold: float | None = None,
    execute_multiplier: float = 1.0,
) -> float:
    """Return deterministic kill time for an impact-style periodic attacker."""

    remaining = hp
    time = first_delay

    for _ in range(10_000):
        dealt = damage
        if execute_threshold is not None and remaining / hp <= execute_threshold:
            dealt *= execute_multiplier

        remaining -= dealt
        if remaining <= 0:
            return time
        time += interval

    raise RuntimeError("Benchmark attacker failed to kill the target")


def cycle_weighted_contribution(normal_dps: float, boss_dps: float) -> float:
    normal_time = 4 * NORMAL_WAVE_SECONDS
    total_time = normal_time + BOSS_WAVE_SECONDS
    return (
        normal_time * normal_dps + BOSS_WAVE_SECONDS * boss_dps
    ) / total_time


def build_results() -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []

    results.append(
        BenchmarkResult(
            tower="견습 궁수",
            solo_ttk=periodic_ttk(1.0, 1.0, FORMATION_INITIAL_DELAY),
            arrival_time=STANDARD_TIME_TO_BASE,
            equivalent_contribution=1.0,
            note="단일 DPS 1.00",
        )
    )

    results.append(
        BenchmarkResult(
            tower="돌팔매꾼",
            solo_ttk=periodic_ttk(0.6, 1.0, FORMATION_INITIAL_DELAY),
            arrival_time=STANDARD_TIME_TO_BASE,
            equivalent_contribution=0.6 * 1.67,
            note="평균 동시 명중 1.67대상",
        )
    )

    frost_ttk = periodic_ttk(0.55, 1.0, FORMATION_INITIAL_DELAY)
    progress_before_slow = FORMATION_INITIAL_DELAY / STANDARD_TIME_TO_BASE
    remaining_progress = 1.0 - progress_before_slow
    frost_arrival = FORMATION_INITIAL_DELAY + (
        remaining_progress * STANDARD_TIME_TO_BASE / 0.85
    )
    results.append(
        BenchmarkResult(
            tower="서리 견습생",
            solo_ttk=frost_ttk,
            arrival_time=frost_arrival,
            equivalent_contribution=(
                0.55
                + OTHER_FORMATION_SLOTS
                * BASELINE_ALLY_CONTRIBUTION
                * 0.15
            ),
            note="직접 0.55 + 지속 감속 기여 0.45",
        )
    )

    results.append(
        BenchmarkResult(
            tower="골목 도적",
            solo_ttk=periodic_ttk(
                0.8,
                1.0,
                FORMATION_INITIAL_DELAY + ENGAGE_APPROACH_DELAY,
                execute_threshold=0.30,
                execute_multiplier=2.0,
            ),
            arrival_time=STANDARD_TIME_TO_BASE,
            equivalent_contribution=0.8 * (1.0 + 0.40) * 0.90,
            note="마무리 공격 비중 40%, Engage 유효 가동률 90%",
        )
    )

    results.append(
        BenchmarkResult(
            tower="신참 북잡이",
            solo_ttk=periodic_ttk(0.55, 1.0, FORMATION_INITIAL_DELAY),
            arrival_time=STANDARD_TIME_TO_BASE,
            equivalent_contribution=(
                0.55
                + OTHER_FORMATION_SLOTS
                * BASELINE_ALLY_CONTRIBUTION
                * 0.15
            ),
            note="직접 0.55 + 아군 3슬롯 강화 0.45",
        )
    )

    normal_dps = 1.6 / 2.0
    adjusted_boss_damage = 1.6 * 1.80
    adjusted_boss_dps = adjusted_boss_damage / 2.0
    results.append(
        BenchmarkResult(
            tower="멧돼지 사냥꾼",
            solo_ttk=periodic_ttk(1.6, 2.0, 0.50),
            arrival_time=STANDARD_TIME_TO_BASE,
            equivalent_contribution=cycle_weighted_contribution(
                normal_dps,
                adjusted_boss_dps,
            ),
            note="일반 40초 + 보스 17.5초 시간 가중, 대형 피해 +80%",
        )
    )

    return results


def main() -> None:
    results = build_results()

    print(
        f"{'Tower':20} {'SoloTTK':>8} {'Arrival':>8} "
        f"{'EC':>8} {'Delta':>8} {'Status':>12}"
    )
    for result in results:
        delta = (result.equivalent_contribution - 1.0) * 100
        status = "PASS" if result.solo_pass and result.contribution_pass else "FAIL"
        print(
            f"{result.tower:20} {result.solo_ttk:8.2f} "
            f"{result.arrival_time:8.2f} "
            f"{result.equivalent_contribution:8.3f} "
            f"{delta:7.1f}% {status:>12}"
        )
        print(f"  - {result.note}")

    failed = [
        result
        for result in results
        if not (result.solo_pass and result.contribution_pass)
    ]
    if failed:
        names = ", ".join(result.tower for result in failed)
        raise SystemExit(f"Benchmark failed: {names}")


if __name__ == "__main__":
    main()
