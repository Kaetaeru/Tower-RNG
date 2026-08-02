# V1 일반 타워 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed Gameplay Identity · Confirmed Probability and Power Budget · Runtime Parameters Pending**
- 카탈로그 버전: `V1-2026-08-03`
- 확률 근거: `../reference/V1_TOWER_PROBABILITY_LADDER.md`
- 공통 시스템: `TOWER_SYSTEM_CATALOG.md`
- 스테이지 테마: `STAGE_CATALOG.md`
- 상위 기획: `../design/TOWERS.md`, `../design/COMBAT.md`, `../design/TOWER_BEHAVIOR.md`, `../design/EFFECT_STACKING.md`
- 구현 상태: **Not Implemented**
- 마지막 정리: 2026-08-03

## 책임

이 문서는 V1 일반 굴리기 타워 50종의 다음 항목을 소유합니다.

```text
TowerId
플레이어 표시 이름
공식 BaseOddsN
역할
RawPowerBudget
ThemeStageId
전투 행동 정체성
교체 가능한 VisualProfileId
```

아직 별도 작업으로 남는 항목:

- 7~50번의 정확한 피해량·주기·범위·투사체 속도
- 타워별 허용 변종 계열
- 기본형·변종 합체 계보
- 실제 ModelAssetId·AnimationAssetId·VFX·SFX
- Roblox 런타임 효율 측정

확률과 PowerBudget은 확정값입니다. 7~50번의 실제 수치 변환은 아래 행동 정체성을 유지하며 역할별 EquivalentContribution이 RawPowerBudget에 맞도록 수행합니다.

---

# 1. 공통 규칙

## 공식 확률

```text
RawPowerBudget(N) = (N / 10)^0.20
```

- 50종의 공식 단위분수 합은 정확히 1입니다.
- 기존 중·고희귀 분모를 변경하지 않습니다.
- 공식 UI는 기본 `1 / N`과 현재 Luck만 표시합니다.
- 현재 압축 후 개별 획득 확률은 카탈로그에 표시하지 않습니다.
- 같은 역할 안에서는 순위가 높을수록 PowerBudget이 반드시 증가합니다.

## 역할 수

| 역할 | 타워 수 |
|---|---:|
| 단일 화력 | 9 |
| 광역 화력 | 9 |
| 제어 | 8 |
| 마무리 | 8 |
| 지원 | 8 |
| 대형 사냥 | 8 |
| 합계 | **50** |

## ThemeStageId

`ThemeStageId`는 타워의 외형·설정·공격 연출이 어느 스테이지에서 영감을 받았는지를 나타냅니다.

```text
ThemeStageId는 획득 조건이 아님
ThemeStageId는 편성 제한이 아님
ThemeStageId는 원소 상성이 아님
```

모든 일반 타워는 어느 스테이지에서나 획득하고 편성할 수 있습니다.

## 모델 교체

```text
TowerId
→ ActionProfileId
→ VisualProfileId
```

- `TowerId`와 `ActionProfileId`는 전투 정체성을 유지합니다.
- `VisualProfileId`는 모델·리그·애니메이션·재질·VFX·SFX 묶음입니다.
- 모델 제작이 어렵다면 같은 VisualFamily의 단순 모델로 교체합니다.
- 모델 교체만으로 확률·전투력·행동·합체 계보를 바꾸지 않습니다.
- 공격 판정은 애니메이션 길이나 특정 Bone 이름에 의존하지 않습니다.

시각 복잡도:

```text
Simple   단일 메시·소형 소환체·단순 도구
Standard 공통 휴머노이드·4족·마법사 리그
Complex  대형 공성병기·고희귀 영웅 연출
```

---

# 2. 일반 타워 50종

| # | TowerId | 표시 이름 | 역할 | 공식 확률 | PowerBudget | ThemeStageId | ActionProfileId | 핵심 행동 | VisualProfileId / 난이도 |
|---:|---|---|---|---:|---:|---|---|---|---|
| 1 | `TWR_APPRENTICE_ARCHER` | 견습 궁수 | 단일 화력 | `1 / 10` | 1.000000 | `STAGE_01` | `ACTION_STEADY_ARROW` | 선두 적에게 일정한 단일 화살을 발사하는 기준 타워 | `VIS_HUMANOID_ARCHER_BASIC` / Standard |
| 2 | `TWR_STONE_SLINGER` | 돌팔매꾼 | 광역 화력 | `1 / 10` | 1.000000 | `STAGE_01` | `ACTION_STONE_SPLASH` | 가장 밀집된 지점에 돌을 던져 최대 3대상을 타격 | `VIS_HUMANOID_SLINGER_BASIC` / Standard |
| 3 | `TWR_FROST_NOVICE` | 서리 견습생 | 제어 | `1 / 10` | 1.000000 | `STAGE_10` | `ACTION_NOVICE_FROSTBOLT` | 선두 적에게 약한 피해와 짧은 감속을 적용 | `VIS_HUMANOID_FROST_MAGE_BASIC` / Standard |
| 4 | `TWR_ALLEY_CUTPURSE` | 골목 도적 | 마무리 | `1 / 10` | 1.000000 | `STAGE_02` | `ACTION_CUTPURSE_FINISH` | 체력 비율이 가장 낮은 적을 노리고 30% 이하에서 피해 증가 | `VIS_HUMANOID_ROGUE_BASIC` / Standard |
| 5 | `TWR_ROOKIE_DRUMMER` | 신참 북잡이 | 지원 | `1 / 10` | 1.000000 | `STAGE_01` | `ACTION_ROOKIE_RHYTHM` | 약한 직접 공격과 함께 아직 강화되지 않은 아군 최대 3명을 지원 | `VIS_HUMANOID_DRUMMER_BASIC` / Standard |
| 6 | `TWR_BOAR_HUNTER` | 멧돼지 사냥꾼 | 대형 사냥 | `1 / 10` | 1.000000 | `STAGE_01` | `ACTION_BOAR_HUNTER_SHOT` | 최대 체력이 높은 적을 우선하며 정예·보스·대형에게 추가 피해 | `VIS_HUMANOID_HUNTER_BASIC` / Standard |
| 7 | `TWR_MOSSWOOD_RANGER` | 이끼숲 순찰자 | 단일 화력 | `1 / 20` | 1.148698 | `STAGE_02` | `ACTION_MOSS_MARK` | 같은 대상 연속 명중 시 이끼 표식이 쌓여 다음 화살이 강화됨 | `VIS_HUMANOID_RANGER_MOSS` / Standard |
| 8 | `TWR_PINECONE_BOMBER` | 솔방울 폭격수 | 광역 화력 | `1 / 20` | 1.148698 | `STAGE_02` | `ACTION_PINECONE_BURST` | 밀집 지점에 솔방울탄을 던져 충돌과 짧은 후속 파열로 피해 | `VIS_HUMANOID_THROWER_FOREST` / Standard |
| 9 | `TWR_ROOT_SNARER` | 뿌리 덫꾼 | 제어 | `1 / 20` | 1.148698 | `STAGE_03` | `ACTION_ROOT_SNARE_ZONE` | 선두 구간에 짧게 유지되는 뿌리 감속 지대를 생성 | `VIS_HUMANOID_TRAPPER_ROOT` / Standard |
| 10 | `TWR_THORNBLADE_DUELIST` | 가시검 결투가 | 마무리 | `1 / 20` | 1.148698 | `STAGE_03` | `ACTION_THORNBLADE_DUEL` | 가장 약해진 적에게 접근해 낮은 체력일수록 강해지는 단일 참격 | `VIS_HUMANOID_DUELIST_THORN` / Standard |
| 11 | `TWR_ANCIENTWOOD_PIPER` | 고목 피리꾼 | 지원 | `1 / 20` | 1.148698 | `STAGE_03` | `ACTION_ANCIENTWOOD_TEMPO` | 피리 선율로 최대 3명의 다음 행동 주기를 단축하는 예산형 지원 | `VIS_HUMANOID_PIPER_WOOD` / Standard |
| 12 | `TWR_DUNE_SPEAR_HUNTER` | 사막 창사냥꾼 | 대형 사냥 | `1 / 20` | 1.148698 | `STAGE_04` | `ACTION_DUNE_HARPOON` | 대형 적을 갈고리창으로 지정하고 자신의 후속 공격을 강화 | `VIS_HUMANOID_SPEAR_DESERT` / Standard |
| 13 | `TWR_SUNSTONE_CROSSBOWMAN` | 태양석 쇠뇌수 | 단일 화력 | `1 / 100` | 1.584893 | `STAGE_04` | `ACTION_SUNSTONE_BOLT` | 긴 준비 뒤 하나의 적에게 강한 태양석 볼트를 발사 | `VIS_HUMANOID_CROSSBOW_DESERT` / Standard |
| 14 | `TWR_SANDJAR_THROWER` | 모래항아리 투척수 | 광역 화력 | `1 / 100` | 1.584893 | `STAGE_04` | `ACTION_SANDJAR_FIELD` | 항아리 충돌 지점에 짧은 지속 피해 구역을 남김 | `VIS_HUMANOID_JAR_THROWER` / Standard |
| 15 | `TWR_SANDSTORM_SHAMAN` | 모래바람 주술사 | 제어 | `1 / 100` | 1.584893 | `STAGE_04` | `ACTION_SANDSTORM_PULSE` | 전방 군집에 반복 감속 파동을 발생시키며 같은 감속은 중첩하지 않음 | `VIS_HUMANOID_SHAMAN_SAND` / Standard |
| 16 | `TWR_TOMB_BLADE` | 묘실 단검사 | 마무리 | `1 / 100` | 1.584893 | `STAGE_05` | `ACTION_TOMB_BLADE_EXECUTE` | 약해진 적을 우선 공격하고 처치 시 한 번의 제한된 빠른 후속 행동 획득 | `VIS_HUMANOID_ROGUE_RELIC` / Standard |
| 17 | `TWR_RELIC_ACOLYTE` | 유물 시종 | 지원 | `1 / 100` | 1.584893 | `STAGE_05` | `ACTION_RELIC_BLESSING` | 최대 3명의 공격에 유물 축복을 부여해 보호막 대상 기여를 높임 | `VIS_HUMANOID_ACOLYTE_RELIC` / Standard |
| 18 | `TWR_RUIN_BREAKER` | 유적 파쇄자 | 대형 사냥 | `1 / 100` | 1.584893 | `STAGE_05` | `ACTION_RUIN_BREAKER_SMASH` | 보호막·대형 적에게 강한 느린 망치 타격 | `VIS_HUMANOID_HAMMER_RUIN` / Standard |
| 19 | `TWR_GLASS_NEEDLE_MARKSMAN` | 유리침 사수 | 단일 화력 | `1 / 200` | 1.820564 | `STAGE_06` | `ACTION_GLASS_NEEDLE_MARK` | 같은 대상에 유리침 표식을 축적하고 일정 횟수마다 파열 | `VIS_HUMANOID_MARKSMAN_GLASS` / Standard |
| 20 | `TWR_VENOM_SAC_BOMBARDIER` | 독낭 폭격수 | 광역 화력 | `1 / 200` | 1.820564 | `STAGE_06` | `ACTION_VENOM_SAC_BOMB` | 밀집 지역에 독낭을 투척해 여러 적에게 제한된 지속 피해 | `VIS_HUMANOID_BOMBARDIER_VENOM` / Standard |
| 21 | `TWR_MIRAGE_BINDER` | 신기루 결박사 | 제어 | `1 / 200` | 1.820564 | `STAGE_06` | `ACTION_MIRAGE_HESITATION` | 아직 영향을 받지 않은 적에게 우선적으로 짧은 망설임과 감속 적용 | `VIS_HUMANOID_MAGE_MIRAGE` / Standard |
| 22 | `TWR_SPOREKNIFE_STALKER` | 포자칼 추적자 | 마무리 | `1 / 200` | 1.820564 | `STAGE_07` | `ACTION_SPOREKNIFE_HUNT` | 체력이 낮은 적에게 포자칼을 던지고 처치 시 다음 표적 전환 손실 감소 | `VIS_HUMANOID_STALKER_SPORE` / Standard |
| 23 | `TWR_MYCELIUM_SINGER` | 균사 노래꾼 | 지원 | `1 / 200` | 1.820564 | `STAGE_07` | `ACTION_MYCELIUM_LINK` | 균사로 최대 3명의 기여도를 연결하고 중복되지 않은 아군을 우선 지원 | `VIS_HUMANOID_SINGER_MYCELIUM` / Standard |
| 24 | `TWR_MARSH_HARPOONER` | 늪지 작살꾼 | 대형 사냥 | `1 / 200` | 1.820564 | `STAGE_07` | `ACTION_MARSH_HARPOON` | 대형·정예 적을 작살로 고정 표적화하고 연속 타격 보너스 획득 | `VIS_HUMANOID_HARPOON_MARSH` / Standard |
| 25 | `TWR_SPORE_MORTAR` | 포자 박격포수 | 광역 화력 | `1 / 256` | 1.912705 | `STAGE_07` | `ACTION_SPORE_MORTAR` | 긴 포물선으로 넓은 포자 폭발을 일으키는 느린 고범위 공격 | `VIS_SIEGE_MORTAR_SPORE` / Complex |
| 26 | `TWR_VINEBOW_SENTINEL` | 덩굴활 파수꾼 | 단일 화력 | `1 / 1,000` | 2.511886 | `STAGE_08` | `ACTION_VINEBOW_FOCUS` | 같은 대상에 활시위를 유지할수록 단일 피해가 단계적으로 증가 | `VIS_HUMANOID_ARCHER_VINE` / Standard |
| 27 | `TWR_THORNWHEEL_THROWER` | 가시바퀴 투척수 | 광역 화력 | `1 / 1,000` | 2.511886 | `STAGE_08` | `ACTION_THORNWHEEL_RICOCHET` | 가시바퀴가 가까운 적 사이를 순차적으로 튕기며 피해가 감소 | `VIS_HUMANOID_THROWER_THORN` / Standard |
| 28 | `TWR_CREEPING_VINE_SHAMAN` | 포복덩굴 주술사 | 제어 | `1 / 1,000` | 2.511886 | `STAGE_08` | `ACTION_CREEPING_VINE_FIELD` | 군집 구간에 이동하는 덩굴 지대를 만들고 미제어 적을 우선 포획 | `VIS_HUMANOID_SHAMAN_VINE` / Standard |
| 29 | `TWR_MAWFLOWER_REAPER` | 아귀꽃 수확자 | 마무리 | `1 / 1,000` | 2.511886 | `STAGE_09` | `ACTION_MAWFLOWER_HARVEST` | 낮은 체력의 적을 수확하고 처치 성공 시 다음 공격 하나를 강화 | `VIS_HUMANOID_REAPER_PLANT` / Standard |
| 30 | `TWR_BLOOM_CANTOR` | 개화 성가대장 | 지원 | `1 / 1,000` | 2.511886 | `STAGE_09` | `ACTION_BLOOM_CHORUS` | 최대 3명의 서로 다른 역할을 우선해 공격·효과 기여를 지원 | `VIS_HUMANOID_CANTOR_BLOOM` / Standard |
| 31 | `TWR_GIANTBLOOM_HUNTER` | 거대꽃 사냥꾼 | 대형 사냥 | `1 / 1,000` | 2.511886 | `STAGE_09` | `ACTION_GIANTBLOOM_CLEAVER` | 대형·재생 태그 적에게 강한 벌목도끼 타격 | `VIS_HUMANOID_CLEAVER_JUNGLE` / Standard |
| 32 | `TWR_SNOWFIELD_LONGBOW` | 설원 장궁수 | 단일 화력 | `1 / 12,500` | 4.162766 | `STAGE_10` | `ACTION_SNOWFIELD_PRECISION` | 가장 전진한 적에게 긴 조준 후 높은 정확도의 단일 사격 | `VIS_HUMANOID_LONGBOW_SNOW` / Standard |
| 33 | `TWR_WHITEWIND_SEER` | 백풍 예언자 | 제어 | `1 / 78,125` | 6.005622 | `STAGE_10` | `ACTION_WHITEWIND_CONE` | 전방 구간에 부채꼴 백풍을 보내 다수 적을 감속 | `VIS_HUMANOID_SEER_WHITEWIND` / Standard |
| 34 | `TWR_SNOW_LYNX_STALKER` | 설표 추적자 | 마무리 | `1 / 1,250,000` | 10.456396 | `STAGE_10` | `ACTION_LYNX_POUNCE` | 가장 약해진 적을 덮치고 처치하면 한 번만 빠르게 원위치 복귀·재공격 | `VIS_BEAST_LYNX_STALKER` / Standard |
| 35 | `TWR_GLACIER_HORNBLOWER` | 빙하 뿔피리꾼 | 지원 | `1 / 7,812,500` | 15.085441 | `STAGE_11` | `ACTION_GLACIER_HORN` | 긴 주기의 뿔피리로 최대 3명의 다음 강한 행동을 증폭 | `VIS_HUMANOID_HORN_GLACIER` / Standard |
| 36 | `TWR_CREVASSE_BALLISTA` | 협곡 쇠뇌대 | 대형 사냥 | `1 / 48,828,125` | 21.763764 | `STAGE_11` | `ACTION_CREVASSE_BALLISTA` | 최고 유효 체력의 대형 적을 향해 매우 강한 중쇠뇌 볼트 발사 | `VIS_SIEGE_BALLISTA_ICE` / Complex |
| 37 | `TWR_AVALANCHE_CALLER` | 눈사태 소환사 | 광역 화력 | `1 / 781,250,000` | 37.892914 | `STAGE_11` | `ACTION_AVALANCHE_LINE` | 경로의 한 구간을 따라 눈사태를 굴려 제한 수의 적을 연속 타격 | `VIS_HUMANOID_CALLER_AVALANCHE` / Complex |
| 38 | `TWR_ICEGATE_ARBALEST` | 빙문 석궁병 | 단일 화력 | `1 / 4,882,812,500` | 54.668104 | `STAGE_12` | `ACTION_ICEGATE_SHATTER_BOLT` | 동일 대상에 명중 횟수를 쌓아 일정 주기마다 강한 파쇄 볼트 발사 | `VIS_HUMANOID_ARBALEST_ICEGATE` / Standard |
| 39 | `TWR_PERMAFROST_WARDEN` | 영구동토 감시자 | 제어 | `1 / 30,517,578,125` | 78.869668 | `STAGE_12` | `ACTION_PERMAFROST_LOCK` | 강한 감속을 유지하고 일정 횟수마다 짧은 완전 제어를 적용하되 제어 예산 상한 준수 | `VIS_HUMANOID_WARDEN_PERMAFROST` / Complex |
| 40 | `TWR_RIMEBLADE_EXECUTIONER` | 서리칼 집행자 | 마무리 | `1 / 488,281,250,000` | 137.320068 | `STAGE_12` | `ACTION_RIMEBLADE_SENTENCE` | 35% 이하 대상에게 큰 피해를 주는 느린 집행 참격 | `VIS_HUMANOID_EXECUTIONER_RIME` / Complex |
| 41 | `TWR_EMBER_BELL_KEEPER` | 잿불 종지기 | 지원 | `1 / 3,051,757,812,500` | 198.111649 | `STAGE_13` | `ACTION_EMBER_BELL` | 종을 울려 최대 3명의 다음 공격에 잿불 추가 기여를 부여 | `VIS_HUMANOID_BELL_EMBER` / Complex |
| 42 | `TWR_MAGMA_SPEAR_HUNTER` | 마그마 창사냥꾼 | 대형 사냥 | `1 / 19,073,486,328,125` | 285.815657 | `STAGE_13` | `ACTION_MAGMA_SPEAR` | 최대 체력이 높은 적을 추적하며 체력이 높을수록 강한 용융 창 투척 | `VIS_HUMANOID_SPEAR_MAGMA` / Complex |
| 43 | `TWR_FURNACE_BOMB_THROWER` | 화로탄 투척수 | 광역 화력 | `1 / 305,175,781,250,000` | 497.633963 | `STAGE_13` | `ACTION_FURNACE_BOMB` | 충돌 폭발 뒤 짧은 용암 지대를 남기는 대형 화로탄 | `VIS_HUMANOID_BOMB_THROWER_FURNACE` / Complex |
| 44 | `TWR_ASH_FALCONER` | 재매 조련사 | 단일 화력 | `1 / 1,953,125,000,000,000` | 721.349953 | `STAGE_13` | `ACTION_ASH_FALCON_DIVE` | 재로 이루어진 매가 같은 대상에게 반복 급강하하며 표식을 축적 | `VIS_HUMANOID_FALCONER_ASH` / Complex |
| 45 | `TWR_OBSIDIAN_CHAINBINDER` | 흑요석 사슬술사 | 제어 | `1 / 10,000,000,000,000,000` | 1000.000000 | `STAGE_14` | `ACTION_OBSIDIAN_CHAIN` | 전방 정예를 사슬로 감속하고 대상당 한 번만 소폭 경로를 되감음 | `VIS_HUMANOID_CHAIN_MAGE_OBSIDIAN` / Complex |
| 46 | `TWR_BLACKGLASS_ASSASSIN` | 흑유리 암살자 | 마무리 | `1 / 500,000,000,000,000,000` | 2186.724148 | `STAGE_14` | `ACTION_BLACKGLASS_FIRST_STRIKE` | 새로운 부상 대상에게 첫 공격이 크게 강화되고 처형 구간에서 추가 증폭 | `VIS_HUMANOID_ASSASSIN_BLACKGLASS` / Complex |
| 47 | `TWR_MOLTEN_RUNE_SMITH` | 용융 룬대장장이 | 지원 | `1 / 3,125,000,000,000,000,000` | 3154.786722 | `STAGE_14` | `ACTION_MOLTEN_RUNE_FORGE` | 최대 3명의 무기에 용융 룬을 새겨 서로 다른 출력 채널을 지원 | `VIS_HUMANOID_RUNESMITH_MOLTEN` / Complex |
| 48 | `TWR_CALDERA_GIANT_HUNTER` | 칼데라 거인사냥꾼 | 대형 사냥 | `1 / 20,000,000,000,000,000,000` | 4573.050519 | `STAGE_15` | `ACTION_CALDERA_ANCHOR_CANNON` | 보스·대형·단계 보호막 적에게 거대한 고정포를 발사 | `VIS_SIEGE_ANCHOR_CANNON_CALDERA` / Complex |
| 49 | `TWR_ERUPTION_HERALD` | 분화의 전령 | 광역 화력 | `1 / 50,000,000,000,000,000,000` | 5492.802717 | `STAGE_15` | `ACTION_ERUPTION_SEQUENCE` | 가장 밀집된 구간에 예고 표식을 남긴 뒤 두 단계 분화를 발생 | `VIS_HUMANOID_HERALD_ERUPTION` / Complex |
| 50 | `TWR_SUNLANCE_KNIGHT` | 태양창 기사 | 단일 화력 | `1 / 100,000,000,000,000,000,000` | 6309.573445 | `STAGE_15` | `ACTION_SUNLANCE_LOCK` | 최고 유효 체력의 한 대상에 조준을 고정하고 충전할수록 강해지는 태양창을 발사 | `VIS_HUMANOID_KNIGHT_SUNLANCE` / Complex |

---

# 3. 역할별 희귀도 사다리

## 단일 화력 9종

```text
견습 궁수
→ 이끼숲 순찰자
→ 태양석 쇠뇌수
→ 유리침 사수
→ 덩굴활 파수꾼
→ 설원 장궁수
→ 빙문 석궁병
→ 재매 조련사
→ 태양창 기사
```

전투 정체성:

- 하나의 대상에 지속 또는 충전 피해 집중
- 광역 피해는 핵심 예산으로 사용하지 않음
- 대상 변경 시 일부 누적이 초기화될 수 있음
- 최고점 `태양창 기사`는 V1 공식 일반 타워 최고 단일 화력

## 광역 화력 9종

```text
돌팔매꾼
→ 솔방울 폭격수
→ 모래항아리 투척수
→ 독낭 폭격수
→ 포자 박격포수
→ 가시바퀴 투척수
→ 눈사태 소환사
→ 화로탄 투척수
→ 분화의 전령
```

전투 정체성:

- 밀집도와 경로 구간을 평가
- 대상 수·범위·지속 피해를 PowerBudget 안에서 교환
- 타겟이 사라져도 이미 발사한 범위 공격은 지정 위치에서 마무리 가능
- 무제한 대상 타격을 사용하지 않고 각 행동에 최대 대상 수를 둠

## 제어 8종

```text
서리 견습생
→ 뿌리 덫꾼
→ 모래바람 주술사
→ 신기루 결박사
→ 포복덩굴 주술사
→ 백풍 예언자
→ 영구동토 감시자
→ 흑요석 사슬술사
```

공통 중첩:

- 같은 ControlGroup 감속은 최강값만 적용하고 지속시간 갱신
- 다른 감속은 곱연산 뒤 일반 60%, 정예 45%, 보스 35% 상한
- 최근 5초 완전 제어 예산은 일반 3.00초, 정예 2.00초, 보스 1.25초
- 경로 되감기·정지는 타워별 횟수 제한을 둠

## 마무리 8종

```text
골목 도적
→ 가시검 결투가
→ 묘실 단검사
→ 포자칼 추적자
→ 아귀꽃 수확자
→ 설표 추적자
→ 서리칼 집행자
→ 흑유리 암살자
```

전투 정체성:

- 낮은 체력 비율을 우선 평가
- 처형 배율과 처치 후 후속 행동을 PowerBudget 안에서 교환
- 처치 실패 시 일반 단일 화력보다 손실이 생길 수 있음
- 무한 처치 연쇄를 막기 위해 즉시 재행동 횟수를 제한

## 지원 8종

```text
신참 북잡이
→ 고목 피리꾼
→ 유물 시종
→ 균사 노래꾼
→ 개화 성가대장
→ 빙하 뿔피리꾼
→ 잿불 종지기
→ 용융 룬대장장이
```

공통 지원 예산:

```text
직접 기여 = SourceEC × 0.55
지원 예산 = SourceEC × 0.45
기준 최대 대상 = 3
대상당 기준 상한 = 대상 전력 15%와 출처 전력 15% 중 작은 값
```

- 같은 StackGroup은 대상별 최강값만 적용
- 이미 강화된 대상보다 미강화 대상을 우선
- 같은 StatChannel 누적 +50% 상한
- 여러 지원 채널의 최종 출력 배율 ×1.75 상한

## 대형 사냥 8종

```text
멧돼지 사냥꾼
→ 사막 창사냥꾼
→ 유적 파쇄자
→ 늪지 작살꾼
→ 거대꽃 사냥꾼
→ 협곡 쇠뇌대
→ 마그마 창사냥꾼
→ 칼데라 거인사냥꾼
```

전투 정체성:

- 최대 체력·유효 체력·보스·정예·대형 태그를 평가
- 일반 군집에서는 같은 희귀도의 단일 화력보다 효율이 낮을 수 있음
- 보스전과 고체력 웨이브에서 높은 기여도를 제공
- 보호막·회복·단계 체력을 별도 무제한 배율로 중복 계산하지 않음

---

# 4. 기존 1 / 10 기준 타워 수치

아래 여섯 타워는 기존 검증값을 유지합니다.

| TowerId | 기준 행동 |
|---|---|
| `TWR_APPRENTICE_ARCHER` | 피해 1.00, 주기 1.00초, 단일 선두 표적 |
| `TWR_STONE_SLINGER` | 대상당 피해 0.60, 최대 3대상, 주기 1.00초 |
| `TWR_FROST_NOVICE` | 피해 0.55, 감속 15%, 지속 1.25초, 주기 1.00초 |
| `TWR_ALLEY_CUTPURSE` | 피해 0.80, HP 30% 이하 ×2.00, 표적 변경 0.25초 |
| `TWR_ROOKIE_DRUMMER` | 직접 기여 0.55와 지원 예산 0.45, 최대 3대상 |
| `TWR_BOAR_HUNTER` | 피해 1.60, 주기 2.00초, 정예·보스·대형 ×1.80 |

지원 타워의 과거 편성 전체 +15% 단순 모델은 폐기하고 `docs/design/EFFECT_STACKING.md`와 지원 예산형 규칙을 사용합니다.

---

# 5. 스테이지 테마 분포

| ThemeStageId | 테마 | 타워 수 | 타워 |
|---|---|---:|---|
| `STAGE_01` | 초원 입구 | 4 | 견습 궁수, 돌팔매꾼, 신참 북잡이, 멧돼지 사냥꾼 |
| `STAGE_02` | 이끼숲 오솔길 | 3 | 골목 도적, 이끼숲 순찰자, 솔방울 폭격수 |
| `STAGE_03` | 고목의 심장 | 3 | 뿌리 덫꾼, 가시검 결투가, 고목 피리꾼 |
| `STAGE_04` | 바람모래 협곡 | 4 | 사막 창사냥꾼, 태양석 쇠뇌수, 모래항아리 투척수, 모래바람 주술사 |
| `STAGE_05` | 매몰된 신전 | 3 | 묘실 단검사, 유물 시종, 유적 파쇄자 |
| `STAGE_06` | 유리전갈 둥지 | 3 | 유리침 사수, 독낭 폭격수, 신기루 결박사 |
| `STAGE_07` | 포자 습지 | 4 | 포자칼 추적자, 균사 노래꾼, 늪지 작살꾼, 포자 박격포수 |
| `STAGE_08` | 덩굴 심층 | 3 | 덩굴활 파수꾼, 가시바퀴 투척수, 포복덩굴 주술사 |
| `STAGE_09` | 식인화 정원 | 3 | 아귀꽃 수확자, 개화 성가대장, 거대꽃 사냥꾼 |
| `STAGE_10` | 서리 들판 | 4 | 서리 견습생, 설원 장궁수, 백풍 예언자, 설표 추적자 |
| `STAGE_11` | 빙결 협곡 | 3 | 빙하 뿔피리꾼, 협곡 쇠뇌대, 눈사태 소환사 |
| `STAGE_12` | 빙하 성문 | 3 | 빙문 석궁병, 영구동토 감시자, 서리칼 집행자 |
| `STAGE_13` | 잿불 비탈 | 4 | 잿불 종지기, 마그마 창사냥꾼, 화로탄 투척수, 재매 조련사 |
| `STAGE_14` | 흑요석 심부 | 3 | 흑요석 사슬술사, 흑유리 암살자, 용융 룬대장장이 |
| `STAGE_15` | 칼데라 심장부 | 3 | 칼데라 거인사냥꾼, 분화의 전령, 태양창 기사 |

분포 합계는 50종입니다.

---

# 6. 제작 우선순위와 대체 규칙

## 지역 1 수직 슬라이스 우선 제작

먼저 구현할 타워:

```text
TWR_APPRENTICE_ARCHER
TWR_STONE_SLINGER
TWR_FROST_NOVICE
TWR_ALLEY_CUTPURSE
TWR_ROOKIE_DRUMMER
TWR_BOAR_HUNTER
```

이 여섯 타워는 공통 휴머노이드 리그와 교체 가능한 장비 파츠로 제작할 수 있습니다.

## 공통 리그 재사용

```text
ARCHER / CROSSBOW / HUNTER
THROWER / BOMBARDIER
MAGE / SHAMAN / SEER
ROGUE / DUELIST / EXECUTIONER
MUSICIAN / ACOLYTE / SMITH
SIEGE_WEAPON
BEAST_COMPANION
```

한 리그에 장비·재질·실루엣 파츠를 교체해 여러 타워를 표현할 수 있습니다. 고희귀 타워도 복잡한 전용 리그가 없으면 공통 리그에 큰 VFX와 장비를 결합합니다.

## VisualProfile 교체

교체 가능:

- 캐릭터 종족·성별·체형
- 장비 메시
- 리그와 애니메이션
- 투사체·Trail·폭발·음향
- 표시 크기와 재질

교체 불가:

- `TowerId`
- 역할
- 공식 확률
- PowerBudget
- 핵심 ActionProfile
- 합체 계보

핵심 행동을 표현하기 어려우면 먼저 애니메이션을 단순화하고 공통 VFX로 대체합니다. 전투 정체성을 바꾸는 것은 마지막 선택입니다.

---

# 7. 후속 카탈로그 작업

```text
CAT-NEXT-004
50종의 AllowedVariantFamilies와 개별 변종 정체성

CAT-NEXT-005
기본형·변종 합체 계보와 결과 TowerId
```

7~50번의 정확한 전투 수치는 기술 명세와 구현 데이터 작성 시 역할별 PowerBudget 변환표로 확정합니다. 해당 수치가 기존 완주 전력 분포를 5% 이상 바꾸면 관련 스테이지와 전체 계정 경로를 다시 검증합니다.
