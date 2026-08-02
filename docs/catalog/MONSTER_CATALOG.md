# V1 몬스터·보스 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed Gameplay Identity · Replaceable Visuals**
- 카탈로그 버전: `V1-2026-08-03`
- 기술 구조: `../technical/MONSTER_CONTENT_ARCHITECTURE.md`
- 스테이지 구성: `STAGE_CATALOG.md`
- 계산 근거: 스테이지 1~15의 `docs/balance`·`docs/reference` 웨이브 벤치마크
- 구현 상태: **Not Implemented**
- 마지막 정리: 2026-08-03

## 책임

이 문서는 V1 몬스터의 안정 `MonsterId`, 표시 이름, 전투 유형, 스테이지별 수치 프로필과 행동을 소유합니다.

```text
MonsterId·표시 이름·전투 행동 = Confirmed
VisualProfileId = Replaceable Prototype
실제 ModelAssetId = Pending
```

모델 제작이 어렵거나 더 적합한 에셋을 발견하면 `VisualProfileId`만 교체합니다. 전투 수치와 웨이브를 바꾸지 않는 모델 교체는 밸런스 재검증을 요구하지 않습니다.

---

# 1. 공통 수치 계약

```text
StageScale(S) = 10 ^ ((S - 1) / 3)
MonsterHP = HPFactor × StageScale(StageId)
```

프로필 ID 규칙:

```text
SMP_<StageId>_<MonsterId에서 MON_/BOSS_ 제거>
```

예:

```text
SMP_STAGE_15_MAGMA_GUARD
```

보상:

- 일반 몬스터: `SpawnCost × StageRewardScale`
- 보스: 기본 SpawnCost 보상에 `×1.15`
- 자식·잔여물: SpawnCost 0, 추가 보상 없음
- 별도 웨이브 완료 보너스 없음

시각 프로필은 전부 프로토타입이며 교체 가능합니다.

---

# 2. 행동 구성요소

| BehaviorSetId | 효과 |
|---|---|
| `BEHAVIOR_NONE` | 공통 이동·피격·사망만 사용 |
| `BEHAVIOR_START_SHIELD` | 생성 시 최대 HP 비율 보호막 |
| `BEHAVIOR_PHASE_SHIELD` | 지정 HP 이하에서 1회 보호막 생성 |
| `BEHAVIOR_BURROW_STEP` | 지정 HP에서 잠깐 비대상화되고 경로 전진 |
| `BEHAVIOR_SPLIT_POD` | 처치 시 보상 없는 자식 2개 생성 |
| `BEHAVIOR_ROUTE_DASH` | 경로 55%에서 1회 즉시 전진 |
| `BEHAVIOR_PHASE_HEAL` | 지정 HP 이하에서 1회 회복, 치명타 처치 시 미발동 |
| `BEHAVIOR_LOW_HP_FRENZY` | 지정 HP 이하에서 이동속도 증가 |
| `BEHAVIOR_ICE_SHELL` | 보호막 보유 중 감속, 파괴 뒤 가속 |
| `BEHAVIOR_ATTACK_DELAY` | 조건 발동 시 모든 타워의 다음 공격을 짧게 지연 |
| `BEHAVIOR_DEATH_REMNANT` | 처치 시 보상 없는 잔여물 생성 |
| `BEHAVIOR_SHELL_BREAK_DELAY` | 최초 갑각 파괴 시 짧은 타워 공격 지연, 중첩 없음 |
| `BEHAVIOR_EXPOSED_CORE` | 지정 HP 이하에서 받는 피해와 이동속도 증가 |
| `BEHAVIOR_ERUPTION` | 지정 HP 구간마다 공격 지연·경로 전진·잔여물 생성 |

행동은 서버 데이터로 처리하고 전용 애니메이션이 없으면 공통 VFX로 표현합니다.

---

# 3. 지역 1 — 초원·숲

## 정체성

| MonsterId | 표시 이름 | 유형 | VisualFamily | 시각 상태 |
|---|---|---|---|---|
| `MON_PRAIRIE_SLIME` | 초원 슬라임 | 표준 일반형 | `BLOB_SMALL` | Replaceable Prototype |
| `MON_FIELD_RAT` | 들쥐 | 군집형 | `QUADRUPED_TINY` | Replaceable Prototype |
| `MON_YOUNG_BOAR` | 어린 멧돼지 | 고체력형 | `QUADRUPED_MEDIUM` | Replaceable Prototype |
| `BOSS_PRAIRIE_BOAR_ALPHA` | 우두머리 멧돼지 | 초반 보스 | `QUADRUPED_LARGE` | Replaceable Prototype |
| `MON_MOSS_SPRITE` | 이끼 정령 | 표준 일반형 | `ELEMENTAL_SMALL` | Replaceable Prototype |
| `MON_BRAMBLE_HARE` | 가시덤불 토끼 | 군집·고속형 | `QUADRUPED_SMALL` | Replaceable Prototype |
| `MON_BARK_BEETLE` | 수피 딱정벌레 | 고체력형 | `INSECT_LOW` | Replaceable Prototype |
| `BOSS_THORNHORN_STAG` | 가시뿔 수사슴 | 중간 보스 | `QUADRUPED_LARGE` | Replaceable Prototype |
| `MON_GLOW_MOTH` | 빛나방 | 군집형 | `FLYING_SMALL` | Replaceable Prototype |
| `MON_ROOT_SPRITE` | 뿌리 정령 | 표준 일반형 | `ELEMENTAL_SMALL` | Replaceable Prototype |
| `MON_BARK_GUARD` | 수피 수호자 | 보호·고체력형 | `TREE_GOLEM_MEDIUM` | Replaceable Prototype |
| `BOSS_ANCIENT_TREANT` | 고대 수호목 | 지역 최종 보스 | `TREE_GOLEM_LARGE` | Replaceable Prototype |

## 스테이지 프로필

| StageMonsterProfileId | MonsterId | Stage | HPFactor | 이동시간 | SpawnCost | 베이스 피해 | 행동 |
|---|---|---:|---:|---:|---:|---:|---|
| `SMP_STAGE_01_PRAIRIE_SLIME` | `MON_PRAIRIE_SLIME` | 1 | 5.00 | 10.0s | 10 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_01_FIELD_RAT` | `MON_FIELD_RAT` | 1 | 2.00 | 8.5s | 5 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_01_YOUNG_BOAR` | `MON_YOUNG_BOAR` | 1 | 12.00 | 12.0s | 20 | 2 | `BEHAVIOR_NONE` |
| `SMP_STAGE_01_PRAIRIE_BOAR_ALPHA` | `BOSS_PRAIRIE_BOAR_ALPHA` | 1 | 55.00 | 22.0s | 100 | 5 | `BEHAVIOR_NONE` |
| `SMP_STAGE_02_MOSS_SPRITE` | `MON_MOSS_SPRITE` | 2 | 5.00 | 11.0s | 10 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_02_BRAMBLE_HARE` | `MON_BRAMBLE_HARE` | 2 | 2.00 | 9.0s | 5 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_02_BARK_BEETLE` | `MON_BARK_BEETLE` | 2 | 11.14 | 15.5s | 20 | 2 | `BEHAVIOR_NONE` |
| `SMP_STAGE_02_THORNHORN_STAG` | `BOSS_THORNHORN_STAG` | 2 | 46.42 | 25.0s | 100 | 6 | `BEHAVIOR_NONE` |
| `SMP_STAGE_03_GLOW_MOTH` | `MON_GLOW_MOTH` | 3 | 1.30 | 12.0s | 5 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_03_ROOT_SPRITE` | `MON_ROOT_SPRITE` | 3 | 4.50 | 15.5s | 10 | 1 | `BEHAVIOR_NONE` |
| `SMP_STAGE_03_BARK_GUARD` | `MON_BARK_GUARD` | 3 | 8.30 | 21.0s | 30 | 3 | 시작 보호막 25% |
| `SMP_STAGE_03_ANCIENT_TREANT` | `BOSS_ANCIENT_TREANT` | 3 | 32.00 | 42.0s | 100 | 8 | 시작 보호막 15%, HP 60%에서 보호막 20% |

스테이지 2의 절대 HP를 `HPFactor`로 환산해 기록했습니다. 표시 반올림으로 원본 절대값과 미세한 차이가 생길 수 있으므로 구현 데이터는 해당 벤치마크 값을 우선합니다.

---

# 4. 지역 2 — 사막

## 정체성

| MonsterId | 표시 이름 | 유형 | VisualFamily | 시각 상태 |
|---|---|---|---|---|
| `MON_DUST_SCARAB` | 먼지 풍뎅이 | 군집형 | `INSECT_LOW` | Replaceable Prototype |
| `MON_DUNE_JACKAL` | 사구 자칼 | 고속형 | `QUADRUPED_SMALL` | Replaceable Prototype |
| `MON_SANDSTONE_SENTINEL` | 사암 파수꾼 | 보호·고체력형 | `STONE_GOLEM_MEDIUM` | Replaceable Prototype |
| `BOSS_DUNE_JACKAL_ALPHA` | 사구 자칼 우두머리 | 초반 보스 | `QUADRUPED_LARGE` | Replaceable Prototype |
| `BOSS_SANDSTONE_BEHEMOTH` | 사암 거수 | 중간 보스 | `STONE_GOLEM_LARGE` | Replaceable Prototype |
| `BOSS_GLASS_SCORPION` | 유리 전갈 | 지역 최종 보스 | `ARACHNID_LARGE` | Replaceable Prototype |

## 스테이지 프로필

| Profile | MonsterId | Stage | HPFactor | 이동시간 | Cost | 피해 | 행동 |
|---|---|---:|---:|---:|---:|---:|---|
| `SMP_STAGE_04_DUST_SCARAB` | `MON_DUST_SCARAB` | 4 | 0.75 | 14.0s | 5 | 1 | 없음 |
| `SMP_STAGE_04_DUNE_JACKAL` | `MON_DUNE_JACKAL` | 4 | 2.60 | 19.0s | 10 | 1 | 없음 |
| `SMP_STAGE_04_SANDSTONE_SENTINEL` | `MON_SANDSTONE_SENTINEL` | 4 | 5.20 | 27.0s | 30 | 3 | 시작 보호막 10% |
| `SMP_STAGE_04_DUNE_JACKAL_ALPHA` | `BOSS_DUNE_JACKAL_ALPHA` | 4 | 14.00 | 38.0s | 100 | 8 | 시작 보호막 5% |
| `SMP_STAGE_05_DUST_SCARAB` | `MON_DUST_SCARAB` | 5 | 0.85 | 14.5s | 5 | 1 | 없음 |
| `SMP_STAGE_05_DUNE_JACKAL` | `MON_DUNE_JACKAL` | 5 | 2.90 | 19.5s | 10 | 1 | 없음 |
| `SMP_STAGE_05_SANDSTONE_SENTINEL` | `MON_SANDSTONE_SENTINEL` | 5 | 6.00 | 27.5s | 30 | 3 | 시작 보호막 15% |
| `SMP_STAGE_05_SANDSTONE_BEHEMOTH` | `BOSS_SANDSTONE_BEHEMOTH` | 5 | 17.50 | 44.0s | 100 | 9 | 시작 보호막 12%, HP 60%에서 보호막 10% |
| `SMP_STAGE_06_DUST_SCARAB` | `MON_DUST_SCARAB` | 6 | 0.95 | 15.0s | 5 | 1 | 없음 |
| `SMP_STAGE_06_DUNE_JACKAL` | `MON_DUNE_JACKAL` | 6 | 3.20 | 20.0s | 10 | 1 | 없음 |
| `SMP_STAGE_06_SANDSTONE_SENTINEL` | `MON_SANDSTONE_SENTINEL` | 6 | 6.70 | 28.0s | 30 | 3 | 시작 보호막 20% |
| `SMP_STAGE_06_GLASS_SCORPION` | `BOSS_GLASS_SCORPION` | 6 | 21.80 | 50.0s | 100 | 10 | 시작 보호막 12%, HP 60% 보호막 18%, HP 35%에서 1.25s 잠복·경로 6% 전진 |

---

# 5. 지역 3 — 정글

## 정체성

| MonsterId | 표시 이름 | 유형 | VisualFamily | 시각 상태 |
|---|---|---|---|---|
| `MON_JUNGLE_SPORELING` | 포자충 | 보상 없는 자식 | `PLANT_TINY` | Replaceable Prototype |
| `MON_SPORE_POD` | 포자낭 | 분열 군집형 | `PLANT_POD` | Replaceable Prototype |
| `MON_VINE_STALKER` | 덩굴 추적자 | 고속형 | `VINE_QUADRUPED` | Replaceable Prototype |
| `MON_REGROWTH_GUARDIAN` | 재생 수호자 | 회복·고체력형 | `PLANT_GOLEM_MEDIUM` | Replaceable Prototype |
| `BOSS_SPORE_MATRIARCH` | 포자 여왕 | 초반 보스 | `PLANT_MASS_LARGE` | Replaceable Prototype |
| `BOSS_VINE_BEHEMOTH` | 덩굴 거수 | 중간 보스 | `PLANT_GOLEM_LARGE` | Replaceable Prototype |
| `BOSS_ANCIENT_MAWFLOWER` | 고대 아귀꽃 | 지역 최종 보스 | `PLANT_MASS_LARGE` | Replaceable Prototype |

## 공통 프로필

지역 3 일반 몬스터는 스테이지 7~9에서 같은 HPFactor와 행동 문법을 사용합니다. 각 스테이지에 별도 `SMP_STAGE_07_*`, `SMP_STAGE_08_*`, `SMP_STAGE_09_*` 프로필을 생성합니다.

| MonsterId | HPFactor | 이동시간 | Cost | 피해 | 행동 |
|---|---:|---:|---:|---:|---|
| `MON_JUNGLE_SPORELING` | 0.20 | 14.0s | 0 | 1 | 추가 보상 없음, 재분열 없음 |
| `MON_SPORE_POD` | 0.55 | 17.0s | 5 | 1 | 처치 시 같은 위치에 포자충 2개 |
| `MON_VINE_STALKER` | 3.00 | 22.0s | 10 | 1 | 경로 55%에서 1회 8% 전진 |
| `MON_REGROWTH_GUARDIAN` | 6.50 | 34.0s | 30 | 3 | HP 45%에서 최대 HP 15% 1회 회복 |

## 보스 프로필

| Profile | BossId | Stage | HPFactor | 이동시간 | Cost | 피해 | 행동 |
|---|---|---:|---:|---:|---:|---:|---|
| `SMP_STAGE_07_SPORE_MATRIARCH` | `BOSS_SPORE_MATRIARCH` | 7 | 17.00 | 56.0s | 100 | 10 | 시작 보호막 6%, HP 55%에서 8% 회복 |
| `SMP_STAGE_08_VINE_BEHEMOTH` | `BOSS_VINE_BEHEMOTH` | 8 | 19.00 | 57.0s | 100 | 11 | 시작 보호막 8%, HP 55%에서 12% 회복, HP 30%에서 0.80s 비대상·경로 3% 전진 |
| `SMP_STAGE_09_ANCIENT_MAWFLOWER` | `BOSS_ANCIENT_MAWFLOWER` | 9 | 22.00 | 58.0s | 100 | 12 | 시작 보호막 10%, HP 55%에서 15% 회복, HP 30%에서 1.20s 비대상·경로 4% 전진 |

---

# 6. 지역 4 — 설원

## 정체성

| MonsterId | 표시 이름 | 유형 | VisualFamily | 시각 상태 |
|---|---|---|---|---|
| `MON_SNOW_HARE` | 설원 토끼 | 군집형 | `QUADRUPED_SMALL` | Replaceable Prototype |
| `MON_FROST_WOLF` | 서리 늑대 | 저체력 폭주형 | `QUADRUPED_MEDIUM` | Replaceable Prototype |
| `MON_RIME_GUARDIAN` | 빙설 수호자 | 빙갑·고체력형 | `ICE_GOLEM_MEDIUM` | Replaceable Prototype |
| `BOSS_FROSTFANG_ALPHA` | 서리송곳니 우두머리 | 초반 보스 | `QUADRUPED_LARGE` | Replaceable Prototype |
| `BOSS_RIME_BEHEMOTH` | 빙설 거수 | 중간 보스 | `ICE_GOLEM_LARGE` | Replaceable Prototype |
| `BOSS_GLACIER_COLOSSUS` | 빙하 거상 | 지역 최종 보스 | `ICE_GOLEM_LARGE` | Replaceable Prototype |

## 공통 프로필

스테이지 10~12 일반 몬스터는 아래 값을 사용하며 각 스테이지별 프로필을 별도 생성합니다.

| MonsterId | HPFactor | 이동시간 | Cost | 피해 | 행동 |
|---|---:|---:|---:|---:|---|
| `MON_SNOW_HARE` | 0.60 | 18.0s | 5 | 1 | 없음 |
| `MON_FROST_WOLF` | 3.20 | 25.0s | 10 | 1 | HP 40% 이하 이동속도 ×1.25 |
| `MON_RIME_GUARDIAN` | 7.20 | 40.0s | 30 | 4 | 시작 보호막 25%, 보호막 중 속도 ×0.85, 파괴 후 ×1.15 |

## 보스 프로필

| Profile | BossId | Stage | HPFactor | 이동시간 | 피해 | 행동 |
|---|---|---:|---:|---:|---:|---|
| `SMP_STAGE_10_FROSTFANG_ALPHA` | `BOSS_FROSTFANG_ALPHA` | 10 | 21.50 | 66.0s | 12 | 보호막 8%, 보호막 중 ×0.92·파괴 후 ×1.06 |
| `SMP_STAGE_11_RIME_BEHEMOTH` | `BOSS_RIME_BEHEMOTH` | 11 | 20.50 | 67.0s | 14 | 보호막 12%, HP 60% 보호막 10%, 보호막 중 ×0.90·파괴 후 ×1.08, HP 30%에서 공격 0.45s 지연·경로 2% 전진 |
| `SMP_STAGE_12_GLACIER_COLOSSUS` | `BOSS_GLACIER_COLOSSUS` | 12 | 23.50 | 68.0s | 15 | 보호막 15%, HP 60% 보호막 15%, 보호막 중 ×0.90·파괴 후 ×1.08, HP 30%에서 공격 0.80s 지연·경로 3% 전진 |

보스 SpawnCost는 모두 100입니다.

---

# 7. 지역 5 — 용암지대

## 정체성

| MonsterId | 표시 이름 | 유형 | VisualFamily | 시각 상태 |
|---|---|---|---|---|
| `MON_LAVA_EMBER` | 용암 잔불 | 보상 없는 잔여물 | `ELEMENTAL_TINY` | Replaceable Prototype |
| `MON_CINDERLING` | 잿불 정령 | 잔여물 군집형 | `ELEMENTAL_SMALL` | Replaceable Prototype |
| `MON_LAVA_HOUND` | 용암 사냥개 | 저체력 폭주형 | `QUADRUPED_MEDIUM` | Replaceable Prototype |
| `MON_MAGMA_GUARD` | 마그마 파수꾼 | 갑각·고체력형 | `MAGMA_GOLEM_MEDIUM` | Replaceable Prototype |
| `MON_OBSIDIAN_COLOSSUS` | 흑요석 거상 | 노출형 정예 | `OBSIDIAN_GOLEM_LARGE` | Replaceable Prototype |
| `BOSS_LAVA_PACK_ALPHA` | 용암 무리 우두머리 | 초반 보스 | `QUADRUPED_LARGE` | Replaceable Prototype |
| `BOSS_OBSIDIAN_TITAN` | 흑요석 거신 | 중간 보스 | `OBSIDIAN_GOLEM_LARGE` | Replaceable Prototype |
| `BOSS_CALDERA_HEART` | 칼데라의 심장 | V1 최종 보스 | `MAGMA_CORE_LARGE` | Replaceable Prototype |

## 공통 프로필

| MonsterId | HPFactor | 이동시간 | Cost | 피해 | 행동 |
|---|---:|---:|---:|---:|---|
| `MON_LAVA_EMBER` | 0.12 | 13.0s | 0 | 1 | 추가 보상 없음 |
| `MON_CINDERLING` | 0.60 | 17.0s | 5 | 1 | 처치 시 같은 위치에 용암 잔불 1개 |
| `MON_LAVA_HOUND` | 3.80 | 24.0s | 15 | 2 | HP 45% 이하 이동속도 ×1.30 |

## 마그마 파수꾼

| Profile | Stage | HPFactor | 보호막 | 갑각 파열 |
|---|---:|---:|---:|---|
| `SMP_STAGE_13_MAGMA_GUARD` | 13 | 10.80 | 16% | 없음 |
| `SMP_STAGE_14_MAGMA_GUARD` | 14 | 11.30 | 20% | 최초 파괴 시 공격 최대 0.25s 지연 |
| `SMP_STAGE_15_MAGMA_GUARD` | 15 | 11.80 | 22% | 최초 파괴 시 공격 최대 0.35s 지연 |

공통 이동시간 42.0초, SpawnCost 50, 베이스 피해 5입니다. 여러 갑각이 동시에 깨져도 공격 지연은 합산되지 않습니다.

## 흑요석 거상

| Profile | Stage | HPFactor | 보호막 | 용융 노출 |
|---|---:|---:|---:|---|
| `SMP_STAGE_14_OBSIDIAN_COLOSSUS` | 14 | 11.60 | 15% | HP 50% 이하 받는 피해 ×1.12, 이동속도 ×1.15 |
| `SMP_STAGE_15_OBSIDIAN_COLOSSUS` | 15 | 12.00 | 18% | HP 50% 이하 받는 피해 ×1.15, 이동속도 ×1.18 |

공통 이동시간 52.0초, SpawnCost 75, 베이스 피해 8입니다.

## 보스 프로필

| Profile | BossId | Stage | HPFactor | 이동시간 | 피해 | 행동 |
|---|---|---:|---:|---:|---:|---|
| `SMP_STAGE_13_LAVA_PACK_ALPHA` | `BOSS_LAVA_PACK_ALPHA` | 13 | 18.00 | 70.0s | 14 | 보호막 8%, HP 40% 이하 이동속도 ×1.18 |
| `SMP_STAGE_14_OBSIDIAN_TITAN` | `BOSS_OBSIDIAN_TITAN` | 14 | 19.50 | 74.0s | 16 | 보호막 10%, HP 58% 보호막 10%, 갑각 파열 0.30s, HP 45% 이하 받는 피해 ×1.10·속도 ×1.12 |
| `SMP_STAGE_15_CALDERA_HEART` | `BOSS_CALDERA_HEART` | 15 | 21.00 | 78.0s | 18 | 보호막 10%, HP 58% 보호막 14%, HP 70%·35%에서 공격 0.45s 지연·경로 2% 전진·잔불 2개 생성 |

보스 SpawnCost는 모두 100입니다.

---

# 8. VisualProfile 교체 정책

각 MonsterId의 기본 참조:

```text
VisualProfileId = VIS_<MonsterId>_PROTOTYPE
VisualStatus = Replaceable
```

실제 모델이 준비되면:

```text
VIS_<MonsterId>_PROTOTYPE
→ VIS_<MonsterId>_FINAL
```

다음 조건을 지키면 전투 카탈로그를 수정하지 않습니다.

- 공통 충돌 캡슐 유지
- 경로 이동은 MonsterRoot 기준
- 행동 발동 시간과 판정 유지
- 표시 크기가 타겟 선택을 방해하지 않음
- 보스 VFX가 타워·코인 UI를 가리지 않음

---

# 9. 미구현 항목

- 실제 ModelAssetId와 리그
- 애니메이션·VFX·SFX 프로필
- 도감 초상화와 아이콘
- 지역별 재질 팔레트
- 모바일 저사양용 LOD
- Roblox 런타임에서 실제 이동·행동 효율 측정

이 항목은 MonsterId와 밸런스 프로필을 유지한 채 확장합니다.
