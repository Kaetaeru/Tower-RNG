"""First-15-minute economy benchmark for Tower RNG.

This is a deterministic planning model, not the Roblox runtime. It links the
verified Stage 1 cycle to provisional Stage 2/3 proxy cycles, early permanent
purchases, physical coin collection efficiency, and the first rebirth target.

Canonical assumptions and limitations are documented in
`docs/reference/EARLY_ECONOMY_BENCHMARK.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pow

TUTORIAL_SECONDS = 25.0
TUTORIAL_COIN = 10.0
TUTORIAL_DEFENSE_XP = 10.0
FIRST_REBIRTH_XP = 8_500.0

BASE_WAVE_VALUES = (60.0, 75.0, 70.0, 70.0, 125.0)
BASE_WAVE_TIME_WEIGHTS = (9.98, 9.85, 9.97, 10.48, 16.00)
BASE_WAVE_TIME_SUM = sum(BASE_WAVE_TIME_WEIGHTS)


def stage_scale(stage: int) -> float:
    return pow(10.0, (stage - 1) / 3.0)


def stage_reward_scale(stage: int) -> float:
    return stage_scale(stage) * pow(1.08, stage - 1)


PURCHASE_COSTS: dict[str, float] = {
    "auto_formation": 100.0,
    "magnet_radius_1": 150.0,
    "core_power_1": 300.0,
    "stage_2_gate": 800.0,
    "roll_speed_1": 400.0,
    "first_branch_gate": 750.0,
    "stage_3_gate": 2_500.0,
    "coin_gain_1": 600.0,
    "luck_1": 700.0,
}


@dataclass(frozen=True)
class Profile:
    name: str
    cycle_seconds: dict[int, float]
    pickup_before_magnet: float
    pickup_after_magnet: float
    purchase_order: tuple[str, ...]
    decision_seconds_per_purchase: float
    target_rebirth_minutes: tuple[float, float]


@dataclass(frozen=True)
class Event:
    seconds: float
    name: str
    coins_after: float
    defense_xp_after: float
    stage_after: int


@dataclass(frozen=True)
class Result:
    profile: Profile
    rebirth_seconds: float
    coins_at_rebirth: float
    defense_xp: float
    stage: int
    events: tuple[Event, ...]


PROFILES = (
    Profile(
        name="fast",
        cycle_seconds={1: 51.50, 2: 58.0, 3: 68.0},
        pickup_before_magnet=0.90,
        pickup_after_magnet=0.97,
        purchase_order=(
            "auto_formation",
            "magnet_radius_1",
            "stage_2_gate",
            "roll_speed_1",
            "stage_3_gate",
            "core_power_1",
            "first_branch_gate",
            "coin_gain_1",
            "luck_1",
        ),
        decision_seconds_per_purchase=0.0,
        target_rebirth_minutes=(7.0, 9.0),
    ),
    Profile(
        name="standard",
        cycle_seconds={1: 56.28, 2: 70.0, 3: 82.0},
        pickup_before_magnet=0.75,
        pickup_after_magnet=0.90,
        purchase_order=(
            "auto_formation",
            "magnet_radius_1",
            "core_power_1",
            "stage_2_gate",
            "roll_speed_1",
            "first_branch_gate",
            "stage_3_gate",
            "coin_gain_1",
            "luck_1",
        ),
        decision_seconds_per_purchase=0.0,
        target_rebirth_minutes=(9.5, 11.5),
    ),
    Profile(
        name="slow",
        cycle_seconds={1: 60.25, 2: 88.0, 3: 105.0},
        pickup_before_magnet=0.60,
        pickup_after_magnet=0.76,
        purchase_order=(
            "auto_formation",
            "magnet_radius_1",
            "core_power_1",
            "stage_2_gate",
            "roll_speed_1",
            "first_branch_gate",
            "stage_3_gate",
            "coin_gain_1",
            "luck_1",
        ),
        decision_seconds_per_purchase=3.0,
        target_rebirth_minutes=(13.0, 15.0),
    ),
)


def simulate(profile: Profile) -> Result:
    seconds = TUTORIAL_SECONDS
    coins = 0.0  # Tutorial coin is immediately spent on Auto Roll.
    defense_xp = TUTORIAL_DEFENSE_XP
    stage = 1
    wave_index = 0
    magnet_unlocked = False
    core_power_unlocked = False
    coin_multiplier = 1.0
    remaining_purchases = list(profile.purchase_order)
    events: list[Event] = [
        Event(
            seconds=seconds,
            name="auto_roll",
            coins_after=coins,
            defense_xp_after=defense_xp,
            stage_after=stage,
        )
    ]

    while defense_xp < FIRST_REBIRTH_XP:
        wave_index = (wave_index % 5) + 1
        cycle_seconds = profile.cycle_seconds[stage]
        if core_power_unlocked:
            cycle_seconds /= 1.10

        wave_seconds = (
            cycle_seconds
            * BASE_WAVE_TIME_WEIGHTS[wave_index - 1]
            / BASE_WAVE_TIME_SUM
        )
        seconds += wave_seconds

        wave_value = (
            BASE_WAVE_VALUES[wave_index - 1]
            * stage_reward_scale(stage)
        )
        defense_xp += wave_value

        pickup_efficiency = (
            profile.pickup_after_magnet
            if magnet_unlocked
            else profile.pickup_before_magnet
        )
        coins += wave_value * pickup_efficiency * coin_multiplier

        while (
            remaining_purchases
            and coins >= PURCHASE_COSTS[remaining_purchases[0]]
        ):
            purchase = remaining_purchases.pop(0)
            coins -= PURCHASE_COSTS[purchase]
            seconds += profile.decision_seconds_per_purchase

            if purchase == "magnet_radius_1":
                magnet_unlocked = True
            elif purchase == "core_power_1":
                core_power_unlocked = True
            elif purchase == "coin_gain_1":
                coin_multiplier = 1.10
            elif purchase == "stage_2_gate":
                stage = 2
                wave_index = 0
            elif purchase == "stage_3_gate":
                stage = 3
                wave_index = 0

            events.append(
                Event(
                    seconds=seconds,
                    name=purchase,
                    coins_after=coins,
                    defense_xp_after=defense_xp,
                    stage_after=stage,
                )
            )

        if seconds > 20 * 60:
            raise RuntimeError(f"{profile.name} exceeded 20 minutes")

    return Result(
        profile=profile,
        rebirth_seconds=seconds,
        coins_at_rebirth=coins,
        defense_xp=defense_xp,
        stage=stage,
        events=tuple(events),
    )


def validate(result: Result) -> None:
    minutes = result.rebirth_seconds / 60.0
    low, high = result.profile.target_rebirth_minutes
    if not low <= minutes <= high:
        raise SystemExit(
            f"{result.profile.name}: rebirth {minutes:.2f}m "
            f"outside {low:.1f}-{high:.1f}m"
        )

    event_names = {event.name for event in result.events}
    required = {
        "auto_roll",
        "auto_formation",
        "magnet_radius_1",
        "stage_2_gate",
        "stage_3_gate",
    }
    missing = required - event_names
    if missing:
        raise SystemExit(
            f"{result.profile.name}: missing required events {sorted(missing)}"
        )


def main() -> None:
    print("Tower RNG first-15-minute economy benchmark")
    print(f"First rebirth requirement: {FIRST_REBIRTH_XP:,.0f} Defense XP")
    print(
        "Proxy cycle values: "
        + ", ".join(
            f"S{stage}={sum(BASE_WAVE_VALUES) * stage_reward_scale(stage):.2f}"
            for stage in (1, 2, 3)
        )
    )

    for profile in PROFILES:
        result = simulate(profile)
        validate(result)
        print(
            f"\n[{profile.name}] rebirth={result.rebirth_seconds / 60:.2f}m "
            f"stage={result.stage} xp={result.defense_xp:.0f} "
            f"coins={result.coins_at_rebirth:.0f}"
        )
        for event in result.events:
            print(
                f"  {event.seconds / 60:>5.2f}m "
                f"{event.name:<20} "
                f"coins={event.coins_after:>7.0f} "
                f"xp={event.defense_xp_after:>7.0f} "
                f"stage={event.stage_after}"
            )


if __name__ == "__main__":
    main()
