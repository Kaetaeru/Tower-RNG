from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50


@dataclass(frozen=True)
class Slot:
    rank: int
    entry_id: str
    role: str
    base_odds_n: int
    status: str


ROLES = (
    ("SingleTarget", "단일 화력"),
    ("AreaDamage", "광역 화력"),
    ("Control", "제어"),
    ("Finisher", "마무리"),
    ("Support", "지원"),
    ("BossHunter", "대형 사냥"),
)

ROLE_LABEL = dict(ROLES)

BASE_TOWERS = (
    ("TWR_APPRENTICE_ARCHER", "SingleTarget"),
    ("TWR_STONE_SLINGER", "AreaDamage"),
    ("TWR_FROST_NOVICE", "Control"),
    ("TWR_ALLEY_CUTPURSE", "Finisher"),
    ("TWR_ROOKIE_DRUMMER", "Support"),
    ("TWR_BOAR_HUNTER", "BossHunter"),
)

TAIL = (
    (256, "AreaDamage"),
    (12_500, "SingleTarget"),
    (78_125, "Control"),
    (1_250_000, "Finisher"),
    (7_812_500, "Support"),
    (48_828_125, "BossHunter"),
    (781_250_000, "AreaDamage"),
    (4_882_812_500, "SingleTarget"),
    (30_517_578_125, "Control"),
    (488_281_250_000, "Finisher"),
    (3_051_757_812_500, "Support"),
    (19_073_486_328_125, "BossHunter"),
    (305_175_781_250_000, "AreaDamage"),
    (1_953_125_000_000_000, "SingleTarget"),
    (10_000_000_000_000_000, "Control"),
    (500_000_000_000_000_000, "Finisher"),
    (3_125_000_000_000_000_000, "Support"),
    (20_000_000_000_000_000_000, "BossHunter"),
    (50_000_000_000_000_000_000, "AreaDamage"),
    (100_000_000_000_000_000_000, "SingleTarget"),
)


def build_slots() -> list[Slot]:
    slots: list[Slot] = []

    for entry_id, role in BASE_TOWERS:
        slots.append(
            Slot(
                rank=len(slots) + 1,
                entry_id=entry_id,
                role=role,
                base_odds_n=10,
                status="Confirmed (Provisional Balance)",
            )
        )

    for denominator in (20, 100, 200):
        for role, _ in ROLES:
            rank = len(slots) + 1
            slots.append(
                Slot(
                    rank=rank,
                    entry_id=f"V1_SLOT_{rank:02d}",
                    role=role,
                    base_odds_n=denominator,
                    status="Proposed Slot",
                )
            )

    # This exact correction term belongs between the 1/200 and 1/1000 groups.
    rank = len(slots) + 1
    slots.append(
        Slot(
            rank=rank,
            entry_id=f"V1_SLOT_{rank:02d}",
            role="AreaDamage",
            base_odds_n=256,
            status="Proposed Slot",
        )
    )

    for role, _ in ROLES:
        rank = len(slots) + 1
        slots.append(
            Slot(
                rank=rank,
                entry_id=f"V1_SLOT_{rank:02d}",
                role=role,
                base_odds_n=1_000,
                status="Proposed Slot",
            )
        )

    for denominator, role in TAIL[1:]:
        rank = len(slots) + 1
        slots.append(
            Slot(
                rank=rank,
                entry_id=f"V1_SLOT_{rank:02d}",
                role=role,
                base_odds_n=denominator,
                status="Proposed Slot",
            )
        )

    return slots


def raw_power_budget(base_odds_n: int) -> Decimal:
    return (Decimal(base_odds_n) / Decimal(10)) ** Decimal("0.20")


def validate(slots: list[Slot]) -> None:
    assert len(slots) == 50, f"expected 50 slots, got {len(slots)}"
    assert [slot.rank for slot in slots] == list(range(1, 51))
    assert all(
        left.base_odds_n <= right.base_odds_n
        for left, right in zip(slots, slots[1:])
    ), "denominators must be nondecreasing"

    probability_sum = sum(Fraction(1, slot.base_odds_n) for slot in slots)
    assert probability_sum == 1, f"probability sum is {probability_sum}, not 1"

    role_counts = Counter(slot.role for slot in slots)
    assert role_counts == Counter(
        {
            "SingleTarget": 9,
            "AreaDamage": 9,
            "Control": 8,
            "Finisher": 8,
            "Support": 8,
            "BossHunter": 8,
        }
    )

    assert slots[-1].base_odds_n == 10**20
    assert slots[-1].role == "SingleTarget"

    by_role: dict[str, list[int]] = defaultdict(list)
    for slot in slots:
        by_role[slot.role].append(slot.base_odds_n)
    for role, denominators in by_role.items():
        assert all(a < b for a, b in zip(denominators, denominators[1:])), (
            f"role ladder must be strictly increasing: {role} {denominators}"
        )

    tail_sum = sum(Fraction(1, denominator) for denominator, _ in TAIL)
    assert tail_sum == Fraction(1, 250), f"tail sum is {tail_sum}"


def print_summary(slots: list[Slot]) -> None:
    probability_sum = sum(Fraction(1, slot.base_odds_n) for slot in slots)
    role_counts = Counter(slot.role for slot in slots)

    print(f"slots={len(slots)}")
    print(f"probability_sum={probability_sum}")
    print(f"max_base_odds_n={slots[-1].base_odds_n}")
    print(
        "role_counts="
        + ", ".join(
            f"{ROLE_LABEL[role]}:{role_counts[role]}" for role, _ in ROLES
        )
    )
    print()
    print("| Rank | EntryId | Role | Base odds | RawPowerBudget | Status |")
    print("|---:|---|---|---:|---:|---|")
    for slot in slots:
        print(
            f"| {slot.rank} | `{slot.entry_id}` | {ROLE_LABEL[slot.role]} | "
            f"`1 / {slot.base_odds_n:,}` | {raw_power_budget(slot.base_odds_n):.6f} | "
            f"{slot.status} |"
        )


if __name__ == "__main__":
    ladder = build_slots()
    validate(ladder)
    print_summary(ladder)
