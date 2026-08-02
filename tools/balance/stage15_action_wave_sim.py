#!/usr/bin/env python3
"""Action-based Stage 15 full validation for Tower RNG.

The benchmark uses the six deterministic baseline tower roles, the current
12-slot role cap, and the account power profiles from the roster benchmark.
All player-visible monster identities remain provisional until catalog adoption.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from statistics import mean, median
from typing import Optional

TICK_SECONDS = 0.05
MAX_SIMULATION_SECONDS = 180.0
STAGE = 15
STAGE_SCALE = 10 ** ((STAGE - 1) / 3)
STAGE_REWARD_SCALE = STAGE_SCALE * (1.08 ** (STAGE - 1))
BOSS_REWARD_MODIFIER = 1.15

TOWER_IDS = (
    "archer",
    "slinger",
    "frost",
    "rogue",
    "drummer",
    "hunter",
)
SLOTS = 12
ROLE_CAP = 4
MINIMUM_DISTINCT_ROLES = 5

EC_PROFILES = {
    "15h_P10": 10_188.0,
    "15h_P50": 19_665.0,
    "30h_P10": 60_575.0,
}


@dataclass(frozen=True)
class MonsterSpec:
    monster_id: str
    hp: float
    time_to_base: float
    spawn_cost: int
    base_damage: int
    tags: frozenset[str] = frozenset()
    shield_fraction: float = 0.0
    phase_shield_at_fraction: float = 0.0
    phase_shield_fraction: float = 0.0
    frenzy_at_fraction: float = 0.0
    frenzy_speed_multiplier: float = 1.0
    death_remnant_count: int = 0
    death_remnant: Optional["MonsterSpec"] = None
    shell_break_delay: float = 0.0
    exposed_at_fraction: float = 0.0
    exposed_damage_taken_multiplier: float = 1.0
    exposed_speed_multiplier: float = 1.0
    eruption_points: tuple[float, ...] = ()
    eruption_delay: float = 0.0
    eruption_progress: float = 0.0
    eruption_spawn_count: int = 0
    eruption_spawn: Optional["MonsterSpec"] = None
    reward_modifier: float = 1.0


@dataclass(frozen=True)
class SpawnEntry:
    spawn_time: float
    spec: MonsterSpec


@dataclass
class MonsterState:
    uid: int
    spec: MonsterSpec
    hp: float
    shield: float
    progress: float = 0.0
    alive: bool = True
    leaked: bool = False
    slow_until: float = 0.0
    slow_fraction: float = 0.0
    phase_shield_triggered: bool = False
    frenzy_triggered: bool = False
    shell_broken: bool = False
    shell_delay_pending: bool = False
    exposed: bool = False
    eruption_index: int = 0
    death_remnant_triggered: bool = False


@dataclass
class TowerState:
    tower_id: str
    next_attack: float
    current_target: Optional[int] = None


@dataclass(frozen=True)
class SimulationResult:
    clear_time: float
    leaks: int
    base_damage: int


LAVA_EMBER = MonsterSpec(
    monster_id="MON_LAVA_EMBER",
    hp=0.12 * STAGE_SCALE,
    time_to_base=13.0,
    spawn_cost=0,
    base_damage=1,
    tags=frozenset({"swarm", "remnant"}),
    reward_modifier=0.0,
)

CINDERLING = MonsterSpec(
    monster_id="MON_CINDERLING",
    hp=0.60 * STAGE_SCALE,
    time_to_base=17.0,
    spawn_cost=5,
    base_damage=1,
    tags=frozenset({"swarm"}),
    death_remnant_count=1,
    death_remnant=LAVA_EMBER,
)

LAVA_HOUND = MonsterSpec(
    monster_id="MON_LAVA_HOUND",
    hp=3.80 * STAGE_SCALE,
    time_to_base=24.0,
    spawn_cost=15,
    base_damage=2,
    tags=frozenset({"fast"}),
    frenzy_at_fraction=0.45,
    frenzy_speed_multiplier=1.30,
)

MAGMA_GUARD = MonsterSpec(
    monster_id="MON_MAGMA_GUARD",
    hp=11.80 * STAGE_SCALE,
    time_to_base=42.0,
    spawn_cost=50,
    base_damage=5,
    tags=frozenset({"thick", "armored"}),
    shield_fraction=0.22,
    shell_break_delay=0.35,
)

OBSIDIAN_COLOSSUS = MonsterSpec(
    monster_id="MON_OBSIDIAN_COLOSSUS",
    hp=12.0 * STAGE_SCALE,
    time_to_base=52.0,
    spawn_cost=75,
    base_damage=8,
    tags=frozenset({"elite", "thick", "large"}),
    shield_fraction=0.18,
    exposed_at_fraction=0.50,
    exposed_damage_taken_multiplier=1.15,
    exposed_speed_multiplier=1.18,
)

CALDERA_HEART = MonsterSpec(
    monster_id="BOSS_CALDERA_HEART",
    hp=21.0 * STAGE_SCALE,
    time_to_base=78.0,
    spawn_cost=100,
    base_damage=18,
    tags=frozenset({"boss", "elite", "large", "armored"}),
    shield_fraction=0.10,
    phase_shield_at_fraction=0.58,
    phase_shield_fraction=0.14,
    eruption_points=(0.70, 0.35),
    eruption_delay=0.45,
    eruption_progress=0.02,
    eruption_spawn_count=2,
    eruption_spawn=LAVA_EMBER,
    reward_modifier=BOSS_REWARD_MODIFIER,
)

WAVES: dict[int, list[SpawnEntry]] = {
    1: [SpawnEntry(index * 0.55, CINDERLING) for index in range(12)],
    2: [SpawnEntry(index * 1.50, LAVA_HOUND) for index in range(4)],
    3: [SpawnEntry(0.0, MAGMA_GUARD)]
    + [SpawnEntry(1.5 + index * 1.5, CINDERLING) for index in range(4)],
    4: [
        SpawnEntry(0.0, OBSIDIAN_COLOSSUS),
        SpawnEntry(3.0, LAVA_HOUND),
        SpawnEntry(6.0, LAVA_HOUND),
    ],
    5: [SpawnEntry(0.0, CALDERA_HEART)]
    + [SpawnEntry(2.0 + index * 2.0, CINDERLING) for index in range(6)],
}


def formation_lineups() -> list[tuple[str, ...]]:
    lineups: list[tuple[str, ...]] = []
    for counts in product(range(ROLE_CAP + 1), repeat=len(TOWER_IDS)):
        if sum(counts) != SLOTS:
            continue
        if sum(count > 0 for count in counts) < MINIMUM_DISTINCT_ROLES:
            continue
        lineups.append(
            tuple(
                tower_id
                for tower_id, count in zip(TOWER_IDS, counts)
                for _ in range(count)
            )
        )
    return lineups


def choose_front(monsters: list[MonsterState]) -> MonsterState:
    return max(monsters, key=lambda monster: (monster.progress, -monster.uid))


def choose_low_health(monsters: list[MonsterState]) -> MonsterState:
    return min(
        monsters,
        key=lambda monster: (
            monster.hp / max(monster.spec.hp, 1e-9),
            -monster.progress,
            monster.uid,
        ),
    )


def choose_high_hp(monsters: list[MonsterState]) -> MonsterState:
    return max(
        monsters,
        key=lambda monster: (
            monster.spec.hp + monster.shield,
            monster.progress,
            -monster.uid,
        ),
    )


def choose_splash_group(monsters: list[MonsterState]) -> list[MonsterState]:
    best_group: list[MonsterState] = []
    for center in monsters:
        group = sorted(
            (
                monster
                for monster in monsters
                if abs(monster.progress - center.progress) <= 0.075
            ),
            key=lambda monster: abs(monster.progress - center.progress),
        )[:3]
        if len(group) > len(best_group):
            best_group = group
    return best_group


def create_monster(
    uid: int,
    spec: MonsterSpec,
    progress: float = 0.0,
) -> MonsterState:
    return MonsterState(
        uid=uid,
        spec=spec,
        hp=spec.hp,
        shield=spec.hp * spec.shield_fraction,
        progress=progress,
    )


def deal_damage(monster: MonsterState, damage: float) -> None:
    if monster.exposed:
        damage *= monster.spec.exposed_damage_taken_multiplier

    shield_before = monster.shield
    if monster.shield > 0.0:
        absorbed = min(monster.shield, damage)
        monster.shield -= absorbed
        damage -= absorbed

    if shield_before > 0.0 and monster.shield <= 1e-9 and not monster.shell_broken:
        monster.shell_broken = True
        if monster.spec.shell_break_delay > 0.0:
            monster.shell_delay_pending = True

    monster.hp -= damage

    if (
        not monster.phase_shield_triggered
        and monster.spec.phase_shield_at_fraction > 0.0
        and 0.0 < monster.hp
        <= monster.spec.hp * monster.spec.phase_shield_at_fraction
    ):
        monster.phase_shield_triggered = True
        monster.shield += monster.spec.hp * monster.spec.phase_shield_fraction

    if (
        not monster.frenzy_triggered
        and monster.spec.frenzy_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.frenzy_at_fraction
    ):
        monster.frenzy_triggered = True

    if (
        not monster.exposed
        and monster.spec.exposed_at_fraction > 0.0
        and 0.0 < monster.hp <= monster.spec.hp * monster.spec.exposed_at_fraction
    ):
        monster.exposed = True


def simulate(
    lineup: tuple[str, ...],
    wave_number: int,
    account_multiplier: float,
) -> SimulationResult:
    has_drummer = "drummer" in lineup
    ally_output_multiplier = 1.15 if has_drummer else 1.0
    towers = [
        TowerState(
            tower_id=tower_id,
            next_attack={"rogue": 0.75, "hunter": 0.50}.get(tower_id, 0.25),
        )
        for tower_id in lineup
    ]

    pending = list(WAVES[wave_number])
    monsters: list[MonsterState] = []
    next_uid = 0
    current_time = 0.0
    leaks = 0
    base_damage = 0

    while current_time < MAX_SIMULATION_SECONDS:
        while pending and pending[0].spawn_time <= current_time + 1e-9:
            spawn = pending.pop(0)
            monsters.append(create_monster(next_uid, spawn.spec))
            next_uid += 1

        pending_delay = 0.0
        spawned: list[MonsterState] = []

        for tower in towers:
            if current_time + 1e-9 < tower.next_attack:
                continue

            active = [
                monster
                for monster in monsters
                if monster.alive and not monster.leaked
            ]
            if not active:
                tower.next_attack += 0.05
                continue

            interval = 2.0 if tower.tower_id == "hunter" else 1.0
            multiplier = ally_output_multiplier * account_multiplier

            if tower.tower_id == "archer":
                deal_damage(choose_front(active), 1.0 * multiplier)
            elif tower.tower_id == "slinger":
                for target in choose_splash_group(active):
                    deal_damage(target, 0.60 * multiplier)
            elif tower.tower_id == "frost":
                target = choose_front(active)
                deal_damage(target, 0.55 * multiplier)
                slow_fraction = 0.15 * (1.15 if has_drummer else 1.0)
                target.slow_fraction = max(target.slow_fraction, slow_fraction)
                target.slow_until = max(target.slow_until, current_time + 1.25)
            elif tower.tower_id == "rogue":
                target = choose_low_health(active)
                if tower.current_target is not None and tower.current_target != target.uid:
                    tower.current_target = target.uid
                    tower.next_attack = current_time + 0.25
                    continue
                tower.current_target = target.uid
                damage = 0.80 * multiplier
                if target.hp / target.spec.hp <= 0.30:
                    damage *= 2.0
                deal_damage(target, damage)
            elif tower.tower_id == "drummer":
                deal_damage(choose_front(active), 0.55 * account_multiplier)
            elif tower.tower_id == "hunter":
                target = choose_high_hp(active)
                damage = 1.60 * multiplier
                if "elite" in target.spec.tags or "boss" in target.spec.tags:
                    damage *= 1.80
                deal_damage(target, damage)

            tower.next_attack += interval

            for monster in active:
                if monster.shell_delay_pending:
                    pending_delay = max(
                        pending_delay,
                        monster.spec.shell_break_delay,
                    )
                    monster.shell_delay_pending = False

            for monster in list(active):
                while (
                    monster.eruption_index < len(monster.spec.eruption_points)
                    and 0.0 < monster.hp
                    <= monster.spec.hp
                    * monster.spec.eruption_points[monster.eruption_index]
                ):
                    pending_delay = max(
                        pending_delay,
                        monster.spec.eruption_delay,
                    )
                    monster.progress = min(
                        0.98,
                        monster.progress + monster.spec.eruption_progress,
                    )
                    if monster.spec.eruption_spawn is not None:
                        for child_index in range(monster.spec.eruption_spawn_count):
                            offset = (
                                child_index
                                - (monster.spec.eruption_spawn_count - 1) / 2
                            ) * 0.008
                            spawned.append(
                                create_monster(
                                    next_uid,
                                    monster.spec.eruption_spawn,
                                    max(0.0, min(0.97, monster.progress + offset)),
                                )
                            )
                            next_uid += 1
                    monster.eruption_index += 1

                if not monster.alive or monster.hp > 1e-9:
                    continue

                monster.alive = False
                if (
                    monster.spec.death_remnant is not None
                    and monster.spec.death_remnant_count > 0
                    and not monster.death_remnant_triggered
                ):
                    monster.death_remnant_triggered = True
                    for _ in range(monster.spec.death_remnant_count):
                        spawned.append(
                            create_monster(
                                next_uid,
                                monster.spec.death_remnant,
                                monster.progress,
                            )
                        )
                        next_uid += 1

                for rogue in towers:
                    if rogue.tower_id == "rogue" and rogue.current_target == monster.uid:
                        rogue.current_target = None

            monsters.extend(spawned)
            spawned.clear()

            if pending_delay > 0.0:
                for other_tower in towers:
                    other_tower.next_attack = max(
                        other_tower.next_attack,
                        current_time + pending_delay,
                    )
                pending_delay = 0.0

        for monster in monsters:
            if not monster.alive or monster.leaked:
                continue

            speed_multiplier = 1.0
            if monster.frenzy_triggered:
                speed_multiplier *= monster.spec.frenzy_speed_multiplier
            if monster.exposed:
                speed_multiplier *= monster.spec.exposed_speed_multiplier
            if current_time < monster.slow_until:
                speed_multiplier *= 1.0 - monster.slow_fraction
            else:
                monster.slow_fraction = 0.0

            monster.progress += (
                TICK_SECONDS / monster.spec.time_to_base * speed_multiplier
            )
            if monster.progress >= 1.0:
                monster.leaked = True
                leaks += 1
                base_damage += monster.spec.base_damage

        if not pending and all(
            not monster.alive or monster.leaked for monster in monsters
        ):
            return SimulationResult(current_time, leaks, base_damage)

        current_time += TICK_SECONDS

    raise RuntimeError(
        f"Wave {wave_number} did not resolve within {MAX_SIMULATION_SECONDS}s"
    )


def wave_budget(wave_number: int) -> int:
    return sum(entry.spec.spawn_cost for entry in WAVES[wave_number])


def wave_reward_units(wave_number: int) -> float:
    return sum(
        entry.spec.spawn_cost * entry.spec.reward_modifier
        for entry in WAVES[wave_number]
    )


def effective_hp(spec: MonsterSpec) -> float:
    total = spec.hp * (
        1.0 + spec.shield_fraction + spec.phase_shield_fraction
    )
    if spec.death_remnant is not None:
        total += spec.death_remnant_count * effective_hp(spec.death_remnant)
    if spec.eruption_spawn is not None:
        total += (
            len(spec.eruption_points)
            * spec.eruption_spawn_count
            * effective_hp(spec.eruption_spawn)
        )
    return total


def wave_effective_hp(wave_number: int) -> float:
    return sum(effective_hp(entry.spec) for entry in WAVES[wave_number])


def profile_multiplier(equivalent_contribution: float) -> float:
    return 3350.0 * equivalent_contribution / EC_PROFILES["15h_P10"]


def profile_results(account_multiplier: float):
    lineups = formation_lineups()
    rows = {
        wave_number: [
            (lineup, simulate(lineup, wave_number, account_multiplier))
            for lineup in lineups
        ]
        for wave_number in range(1, 6)
    }
    result_maps = {
        wave_number: dict(rows[wave_number]) for wave_number in rows
    }
    cycles = [
        sum(
            result_maps[wave_number][lineup].clear_time
            for wave_number in range(1, 6)
        )
        for lineup in lineups
    ]
    return lineups, rows, cycles


def six_role_cycles(account_multiplier: float) -> list[float]:
    cycles: list[float] = []
    for lineup in formation_lineups():
        if not all(role in lineup for role in TOWER_IDS):
            continue
        cycles.append(
            sum(
                simulate(lineup, wave_number, account_multiplier).clear_time
                for wave_number in range(1, 6)
            )
        )
    return cycles


def validate():
    assert [wave_budget(wave) for wave in range(1, 6)] == [60, 60, 70, 105, 130]
    assert [wave_reward_units(wave) for wave in range(1, 6)] == [
        60.0,
        60.0,
        70.0,
        105.0,
        145.0,
    ]
    assert len(formation_lineups()) == 1266

    results = {
        name: profile_results(profile_multiplier(ec))
        for name, ec in EC_PROFILES.items()
    }

    for _, rows, _ in results.values():
        assert all(
            result.leaks == 0
            for wave_rows in rows.values()
            for _, result in wave_rows
        )

    _, p10_rows, p10_cycles = results["15h_P10"]
    p10_wave_averages = [
        mean(result.clear_time for _, result in p10_rows[wave])
        for wave in range(1, 6)
    ]
    p10_average = mean(p10_cycles)
    assert 108.0 <= p10_average <= 118.0
    assert max(p10_cycles) <= 145.0
    assert 0.31 <= p10_wave_averages[4] / p10_average <= 0.35

    healthy_cycles = six_role_cycles(
        profile_multiplier(EC_PROFILES["15h_P10"])
    )
    assert len(healthy_cycles) == 336
    assert mean(healthy_cycles) <= 114.0
    assert max(healthy_cycles) <= 140.0

    _, _, p50_cycles = results["15h_P50"]
    assert mean(p50_cycles) <= 70.0
    assert max(p50_cycles) <= 80.0

    _, _, farm_cycles = results["30h_P10"]
    assert mean(farm_cycles) <= 40.0
    assert max(farm_cycles) <= 40.0

    aggregate_reference_seconds = 112.24
    assert (
        abs(p10_average - aggregate_reference_seconds)
        / aggregate_reference_seconds
        <= 0.02
    )
    return results


def print_profile(name: str, data) -> None:
    lineups, rows, cycles = data
    print(
        f"{name}: multiplier=x{profile_multiplier(EC_PROFILES[name]):,.2f}, "
        f"lineups={len(lineups)}"
    )
    for wave_number in range(1, 6):
        times = [result.clear_time for _, result in rows[wave_number]]
        print(
            f"  W{wave_number}: budget={wave_budget(wave_number):>3}, "
            f"reward={wave_reward_units(wave_number):>5.1f}, "
            f"effective_hp={wave_effective_hp(wave_number):>12,.2f}, "
            f"avg={mean(times):>6.2f}s, median={median(times):>6.2f}s, "
            f"best={min(times):>6.2f}s, worst={max(times):>6.2f}s"
        )
    boss_average = mean(result.clear_time for _, result in rows[5])
    print(
        f"  Cycle: avg={mean(cycles):.2f}s, median={median(cycles):.2f}s, "
        f"best={min(cycles):.2f}s, worst={max(cycles):.2f}s, "
        f"boss_share={boss_average / mean(cycles) * 100:.1f}%"
    )


def main() -> None:
    results = validate()
    print("Stage 15 action-based full validation")
    print(
        f"StageScale={STAGE_SCALE:,.8f}, "
        f"RewardScale={STAGE_REWARD_SCALE:,.8f}, "
        f"SpawnBudget={sum(wave_budget(wave) for wave in range(1, 6))}, "
        f"RewardUnits={sum(wave_reward_units(wave) for wave in range(1, 6)):.1f}"
    )
    for name in EC_PROFILES:
        print_profile(name, results[name])

    healthy = six_role_cycles(profile_multiplier(EC_PROFILES["15h_P10"]))
    print(
        f"15h P10 six-role subset: lineups={len(healthy)}, "
        f"avg={mean(healthy):.2f}s, median={median(healthy):.2f}s, "
        f"best={min(healthy):.2f}s, worst={max(healthy):.2f}s"
    )
    print("All Stage 15 action benchmark assertions passed.")


if __name__ == "__main__":
    main()
