# V1 일반 타워 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed Gameplay Identity · Confirmed Probability and Power Budget · Runtime Parameters Pending**
- 카탈로그 버전: `V1-2026-08-03-R2`
- 확률 근거: `../reference/V1_TOWER_PROBABILITY_LADDER.md`
- 공통 시스템: `TOWER_SYSTEM_CATALOG.md`
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
FantasyTier
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

## 세계관 규모 상승

타워를 스테이지 테마에 대응시키지 않습니다. 모든 타워는 어느 스테이지에서나 획득하고 편성할 수 있습니다.

희귀도에 따라 설정과 연출의 규모가 상승합니다.

```text
FantasyTier I   생활인·견습병·초보 모험가
FantasyTier II  숙련병·전문 사냥꾼·초급 마법 사용자
FantasyTier III 고위 마도사·기사단장·영웅
FantasyTier IV  전설적 영웅·용과 거인을 다루는 존재
FantasyTier V   신화·천상·운명·종말급 존재
```

권장 구간:

| 슬롯 | FantasyTier | 방향 |
|---:|---|---|
| 1~12 | I | 소박하고 이해하기 쉬운 병사·모험가 |
| 13~24 | II | 전문 기술과 제한적인 마법 |
| 25~36 | III | 명확한 초자연 능력과 영웅적 연출 |
| 37~44 | IV | 전설·용·세계수·시간을 다루는 존재 |
| 45~50 | V | 운명·심판·천상·신수·종말·영원 |

FantasyTier는 전투 배율이 아닙니다. 실제 전투력은 공식 PowerBudget으로만 결정합니다.

## 모델 교체

```text
TowerId
→ ActionProfileId
→ VisualProfileId
```

- `TowerId`와 `ActionProfileId`는 전투 정체성을 유지합니다.
- `VisualProfileId`는 모델·리그·애니메이션·재질·VFX·SFX 묶음입니다.
- 모델 제작이 어렵다면 같은 VisualFamily의 단순 모델로 교체합니다.
- 공격 판정은 애니메이션 길이나 특정 Bone 이름에 의존하지 않습니다.
- 신화 타워도 공통 휴머노이드 리그와 대형 VFX만으로 대체할 수 있습니다.

---

# 2. 일반 타워 50종

| # | TowerId | 표시 이름 | 역할 | 공식 확률 | PowerBudget | Tier | ActionProfileId | 핵심 행동 | VisualProfileId / 난이도 |
|---:|---|---|---|---:|---:|---:|---|---|---|
| 1 | `TWR_APPRENTICE_ARCHER` | 견습 궁수 | 단일 화력 | `1 / 10` | 1.000000 | I | `ACTION_STEADY_ARROW` | 선두 적에게 일정한 단일 화살을 발사하는 기준 타워 | `VIS_HUMANOID_ARCHER_BASIC` / Standard |
| 2 | `TWR_STONE_SLINGER` | 돌팔매꾼 | 광역 화력 | `1 / 10` | 1.000000 | I | `ACTION_STONE_SPLASH` | 가장 밀집된 지점에 돌을 던져 최대 3대상을 타격 | `VIS_HUMANOID_SLINGER_BASIC` / Standard |
| 3 | `TWR_FROST_NOVICE` | 서리 견습생 | 제어 | `1 / 10` | 1.000000 | I | `ACTION_NOVICE_FROSTBOLT` | 선두 적에게 약한 피해와 짧은 감속 적용 | `VIS_HUMANOID_FROST_MAGE_BASIC` / Standard |
| 4 | `TWR_ALLEY_CUTPURSE` | 골목 도적 | 마무리 | `1 / 10` | 1.000000 | I | `ACTION_CUTPURSE_FINISH` | 체력 비율이 가장 낮은 적을 노리고 30% 이하에서 피해 증가 | `VIS_HUMANOID_ROGUE_BASIC` / Standard |
| 5 | `TWR_ROOKIE_DRUMMER` | 신참 북잡이 | 지원 | `1 / 10` | 1.000000 | I | `ACTION_ROOKIE_RHYTHM` | 약한 직접 공격과 최대 3명의 비중첩 지원 | `VIS_HUMANOID_DRUMMER_BASIC` / Standard |
| 6 | `TWR_BOAR_HUNTER` | 멧돼지 사냥꾼 | 대형 사냥 | `1 / 10` | 1.000000 | I | `ACTION_BOAR_HUNTER_SHOT` | 최대 체력이 높은 적을 우선하고 정예·보스·대형에게 추가 피해 | `VIS_HUMANOID_HUNTER_BASIC` / Standard |
| 7 | `TWR_VETERAN_CROSSBOWMAN` | 숙련 쇠뇌수 | 단일 화력 | `1 / 20` | 1.148698 | I | `ACTION_VETERAN_BOLT` | 같은 대상에 연속 사격하면 다음 볼트의 관통력이 증가 | `VIS_HUMANOID_CROSSBOW_VETERAN` / Standard |
| 8 | `TWR_POWDER_GRENADIER` | 화약 투척수 | 광역 화력 | `1 / 20` | 1.148698 | I | `ACTION_POWDER_GRENADE` | 밀집 지점에 짧은 지연 뒤 폭발하는 화약탄 투척 | `VIS_HUMANOID_GRENADIER_BASIC` / Standard |
| 9 | `TWR_CHAIN_TRAPPER` | 사슬 덫꾼 | 제어 | `1 / 20` | 1.148698 | I | `ACTION_CHAIN_TRAP` | 아직 제어되지 않은 선두 적에게 사슬 덫을 걸어 감속 | `VIS_HUMANOID_TRAPPER_CHAIN` / Standard |
| 10 | `TWR_BOUNTY_DUELIST` | 현상금 결투가 | 마무리 | `1 / 20` | 1.148698 | I | `ACTION_BOUNTY_DUEL` | 가장 약해진 적을 표식하고 낮은 체력에서 강한 찌르기 | `VIS_HUMANOID_DUELIST_BASIC` / Standard |
| 11 | `TWR_BANNER_SQUIRE` | 군기 수행원 | 지원 | `1 / 20` | 1.148698 | I | `ACTION_SQUIRE_BANNER` | 아직 강화되지 않은 아군 최대 3명의 다음 공격을 보조 | `VIS_HUMANOID_BANNER_SQUIRE` / Standard |
| 12 | `TWR_PIKE_HUNTER` | 장창 사냥꾼 | 대형 사냥 | `1 / 20` | 1.148698 | I | `ACTION_PIKE_WOUND` | 대형 적에게 깊은 상처 표식을 남겨 자신의 후속 공격 강화 | `VIS_HUMANOID_PIKE_HUNTER` / Standard |
| 13 | `TWR_RUNEBOLT_MARKSMAN` | 룬탄 사수 | 단일 화력 | `1 / 100` | 1.584893 | II | `ACTION_RUNEBOLT_MARK` | 같은 대상에 룬을 쌓고 일정 횟수마다 추가 파열 | `VIS_HUMANOID_RUNE_MARKSMAN` / Standard |
| 14 | `TWR_ALCHEMY_BOMBARDIER` | 연금 폭격수 | 광역 화력 | `1 / 100` | 1.584893 | II | `ACTION_ALCHEMY_BARRAGE` | 화염·산성·충격 병을 정해진 순서로 투척해 군집 타격 | `VIS_HUMANOID_ALCHEMIST_BOMBER` / Standard |
| 15 | `TWR_GALE_BINDER` | 바람 결박사 | 제어 | `1 / 100` | 1.584893 | II | `ACTION_GALE_BIND` | 짧은 회오리로 적을 모으고 감속하되 경로 이동은 제한적으로만 변경 | `VIS_HUMANOID_WIND_MAGE` / Standard |
| 16 | `TWR_SHADOW_PURSUER` | 그림자 추격자 | 마무리 | `1 / 100` | 1.584893 | II | `ACTION_SHADOW_PURSUIT` | 낮은 체력의 적을 추적하고 처치 시 다음 재타겟 손실 감소 | `VIS_HUMANOID_SHADOW_ROGUE` / Standard |
| 17 | `TWR_BATTLE_CHAPLAIN` | 전투 사제 | 지원 | `1 / 100` | 1.584893 | II | `ACTION_BATTLE_BLESSING` | 최대 3명의 공격에 축복을 부여하고 약한 성광탄으로 직접 기여 | `VIS_HUMANOID_BATTLE_PRIEST` / Standard |
| 18 | `TWR_GIANTBREAKER_LANCER` | 거인파쇄 창기병 | 대형 사냥 | `1 / 100` | 1.584893 | II | `ACTION_GIANTBREAKER_THRUST` | 대형·보호막 적에게 강한 느린 돌격창 공격 | `VIS_HUMANOID_HEAVY_LANCER` / Standard |
| 19 | `TWR_SPELLSHOT_MUSKETEER` | 마탄 총사 | 단일 화력 | `1 / 200` | 1.820564 | II | `ACTION_SPELLSHOT_CYCLE` | 세 종류의 마탄을 순환 발사하며 세 번째 탄환이 강화 | `VIS_HUMANOID_MAGIC_MUSKETEER` / Standard |
| 20 | `TWR_THUNDER_ARTILLERIST` | 천둥 포병 | 광역 화력 | `1 / 200` | 1.820564 | II | `ACTION_THUNDER_SHELL` | 충돌 지점에서 주변 적에게 제한된 연쇄 번개 발생 | `VIS_HUMANOID_THUNDER_GUNNER` / Standard |
| 21 | `TWR_TIME_SNARER` | 시간 덫술사 | 제어 | `1 / 200` | 1.820564 | II | `ACTION_TIME_SNARE` | 미제어 대상을 우선해 시간 덫을 설치하고 이동을 늦춤 | `VIS_HUMANOID_TIME_MAGE_MINOR` / Standard |
| 22 | `TWR_SOUL_REAPER` | 영혼 수확자 | 마무리 | `1 / 200` | 1.820564 | II | `ACTION_SOUL_REAP` | 낮은 체력의 적을 베고 처치 초과 피해 일부를 다음 대상에 전달 | `VIS_HUMANOID_REAPER_MINOR` / Standard |
| 23 | `TWR_BATTLE_ORACLE` | 전장의 예언자 | 지원 | `1 / 200` | 1.820564 | II | `ACTION_FORESEEN_STRIKE` | 최대 3명의 다음 공격을 예견해 준비시간과 명중 손실을 감소 | `VIS_HUMANOID_ORACLE_BATTLE` / Standard |
| 24 | `TWR_WYRM_HUNTER_CAPTAIN` | 용사냥 석궁대장 | 대형 사냥 | `1 / 200` | 1.820564 | II | `ACTION_WYRM_HUNTER_MARK` | 정예·보스에 사냥 표식을 축적하고 반복 명중 보너스 획득 | `VIS_HUMANOID_WYRM_HUNTER` / Standard |
| 25 | `TWR_ARCANE_MORTAR` | 비전 박격포 | 광역 화력 | `1 / 256` | 1.912705 | III | `ACTION_ARCANE_MORTAR` | 가장 밀집된 예측 지점에 큰 비전탄을 낙하시킴 | `VIS_ARCANE_MORTAR_PLATFORM` / Standard |
| 26 | `TWR_DAWN_KNIGHT` | 여명 기사 | 단일 화력 | `1 / 1,000` | 2.511886 | III | `ACTION_DAWN_SEAL` | 하나의 적에 태양 인장을 쌓아 마지막 일격을 강화 | `VIS_HUMANOID_DAWN_KNIGHT` / Standard |
| 27 | `TWR_METEOR_SCHOLAR` | 유성학자 | 광역 화력 | `1 / 1,000` | 2.511886 | III | `ACTION_MINOR_METEOR_CLUSTER` | 여러 작은 유성을 밀집 구간에 순차 낙하시킴 | `VIS_HUMANOID_METEOR_MAGE` / Standard |
| 28 | `TWR_GRAVITY_WEAVER` | 중력 직조자 | 제어 | `1 / 1,000` | 2.511886 | III | `ACTION_GRAVITY_WELL` | 주변 적을 한 지점으로 끌어모으고 감속 상한 내에서 묶음 | `VIS_HUMANOID_GRAVITY_MAGE` / Standard |
| 29 | `TWR_PHANTOM_BLADE` | 환영검객 | 마무리 | `1 / 1,000` | 2.511886 | III | `ACTION_PHANTOM_EXECUTION` | 약해진 적에게 순간이동해 참격하고 처치 시 원위치 복귀 손실 감소 | `VIS_HUMANOID_PHANTOM_SWORD` / Standard |
| 30 | `TWR_STAR_CANTOR` | 별의 성가대장 | 지원 | `1 / 1,000` | 2.511886 | III | `ACTION_STAR_CHORUS` | 최대 3명의 다음 행동 주기와 공격 효율을 예산형으로 강화 | `VIS_HUMANOID_STAR_CANTOR` / Standard |
| 31 | `TWR_COLOSSUS_STALKER` | 거상 추적자 | 대형 사냥 | `1 / 1,000` | 2.511886 | III | `ACTION_COLOSSUS_WEAKPOINT` | 가장 큰 적의 약점을 지정하고 대형 대상 반복 공격 강화 | `VIS_HUMANOID_COLOSSUS_HUNTER` / Standard |
| 32 | `TWR_MOONLIGHT_SNIPER` | 월광 저격수 | 단일 화력 | `1 / 12,500` | 4.162766 | III | `ACTION_MOONLIGHT_SNIPE` | 긴 조준 후 하나의 적에게 강한 월광탄 발사 | `VIS_HUMANOID_MOON_SNIPER` / Standard |
| 33 | `TWR_DREAM_WARDEN` | 꿈의 간수 | 제어 | `1 / 78,125` | 6.005622 | III | `ACTION_DREAM_PRISON` | 적 무리를 꿈의 장막에 가두고 대상별 정지시간 상한 적용 | `VIS_HUMANOID_DREAM_WARDEN` / Standard |
| 34 | `TWR_DEATH_EXECUTIONER` | 죽음의 집행관 | 마무리 | `1 / 1,250,000` | 10.456396 | III | `ACTION_DEATH_SENTENCE` | 체력이 낮을수록 강해지는 판결을 내리고 처치 시 힘 일부 보존 | `VIS_HUMANOID_DARK_EXECUTIONER` / Standard |
| 35 | `TWR_PHOENIX_HERALD` | 불사조 전령 | 지원 | `1 / 7,812,500` | 15.085441 | III | `ACTION_PHOENIX_BLESSING` | 최대 3명에게 재점화 축복을 부여해 다음 공격에 추가 불꽃 발생 | `VIS_HUMANOID_PHOENIX_HERALD` / Complex |
| 36 | `TWR_TITANSPEAR_SAINT` | 티탄창 성인 | 대형 사냥 | `1 / 48,828,125` | 21.763764 | III | `ACTION_TITANSPEAR_ASCENT` | 같은 대형 적을 찌를수록 티탄파쇄 단계가 상승 | `VIS_HUMANOID_SPEAR_SAINT` / Complex |
| 37 | `TWR_STORM_DRAGON_CALLER` | 폭풍룡 소환사 | 광역 화력 | `1 / 781,250,000` | 37.892914 | IV | `ACTION_STORM_DRAGON_BREATH` | 소형 폭풍룡이 군집을 가로지르며 번개 숨결과 연쇄 타격 | `VIS_DRAGON_CALLER_WITH_VFX` / Complex |
| 38 | `TWR_SUN_KING_ARCHER` | 태양왕의 궁수 | 단일 화력 | `1 / 4,882,812,500` | 54.668104 | IV | `ACTION_SOLAR_CROWN_ARROW` | 한 대상 주위에 태양 화살을 축적한 뒤 동시에 관통 | `VIS_HUMANOID_SOLAR_ARCHER` / Complex |
| 39 | `TWR_CHRONOS_JAILER` | 크로노스의 간수 | 제어 | `1 / 30,517,578,125` | 78.869668 | IV | `ACTION_CHRONOS_CELL` | 강한 적을 시간 감옥에 가두며 보스 정지시간 상한을 준수 | `VIS_HUMANOID_CHRONOS_JAILER` / Complex |
| 40 | `TWR_RED_MOON_SWORD_SAINT` | 적월의 검성 | 마무리 | `1 / 488,281,250,000` | 137.320068 | IV | `ACTION_RED_MOON_CRESCENT` | 낮은 체력의 적을 초승달 참격으로 마무리하고 다음 대상으로 이어짐 | `VIS_HUMANOID_RED_MOON_SAINT` / Complex |
| 41 | `TWR_WORLDTREE_HIGH_PRIEST` | 세계수의 대사제 | 지원 | `1 / 3,051,757,812,500` | 198.111649 | IV | `ACTION_WORLDTREE_BENEDICTION` | 최대 3명에게 서로 다른 성장 축복을 배분하고 같은 채널 상한 적용 | `VIS_HUMANOID_WORLDTREE_PRIEST` / Complex |
| 42 | `TWR_LEVIATHAN_HARPOON_KING` | 레비아탄 작살왕 | 대형 사냥 | `1 / 19,073,486,328,125` | 285.815657 | IV | `ACTION_LEVIATHAN_HARPOON` | 거대한 적에게 심해 작살을 고정하고 반복 타격과 제한된 이동 억제 | `VIS_HUMANOID_LEVIATHAN_HUNTER` / Complex |
| 43 | `TWR_CELESTIAL_METEOR_LORD` | 천공 유성군주 | 광역 화력 | `1 / 305,175,781,250,000` | 497.633963 | IV | `ACTION_CELESTIAL_METEOR_COURT` | 여러 예측 지점에 대형 유성을 순차 낙하시켜 넓은 구역 장악 | `VIS_CELESTIAL_METEOR_LORD` / Complex |
| 44 | `TWR_VALHALLA_GODSPEAR` | 발할라의 신창 | 단일 화력 | `1 / 1,953,125,000,000,000` | 721.349953 | IV | `ACTION_VALHALLA_GODSPEAR` | 하늘에서 하나의 적을 지정해 반복 관통하는 신창 소환 | `VIS_VALHALLA_SPEAR_HERO` / Complex |
| 45 | `TWR_FATE_WEAVER` | 운명 직조자 | 제어 | `1 / 10,000,000,000,000,000` | 1000.000000 | V | `ACTION_FATE_THREADS` | 여러 적의 운명 실을 묶어 감속·정지 상한 안에서 행동 순서를 지연 | `VIS_MYTHIC_FATE_WEAVER` / Complex |
| 46 | `TWR_LAST_JUDGE` | 최후의 심판자 | 마무리 | `1 / 500,000,000,000,000,000` | 2186.724148 | V | `ACTION_LAST_JUDGMENT` | 가장 약해진 적에게 심판을 내리고 남은 힘을 다음 판결에 이전 | `VIS_MYTHIC_LAST_JUDGE` / Complex |
| 47 | `TWR_SERAPH_COMMANDER` | 치천사 군단장 | 지원 | `1 / 3,125,000,000,000,000,000` | 3154.786722 | V | `ACTION_SERAPH_HOST` | 최대 3명의 아군에 천상 군기를 배분하고 공격마다 성광 후속타 생성 | `VIS_MYTHIC_SERAPH_COMMANDER` / Complex |
| 48 | `TWR_GODBEAST_SLAYER` | 신수 멸절자 | 대형 사냥 | `1 / 20,000,000,000,000,000,000` | 4573.050519 | V | `ACTION_GODBEAST_ANNIHILATION` | 보스·대형 적의 체력 구간이 바뀔 때마다 새로운 사냥 태세로 강화 | `VIS_MYTHIC_GODBEAST_SLAYER` / Complex |
| 49 | `TWR_APOCALYPSE_NEBULA` | 묵시의 성운 | 광역 화력 | `1 / 50,000,000,000,000,000,000` | 5492.802717 | V | `ACTION_APOCALYPSE_NEBULA` | 전장 여러 밀집 구역에 성운 균열과 종말성 낙하물을 순차 생성 | `VIS_MYTHIC_APOCALYPSE_NEBULA` / Complex |
| 50 | `TWR_ETERNAL_SUNLANCE_KNIGHT` | 영원의 태양창 기사 | 단일 화력 | `1 / 100,000,000,000,000,000,000` | 6309.573445 | V | `ACTION_ETERNAL_SUNLANCE` | 하나의 적에게 조준을 유지할수록 태양창의 위력이 상승하는 최고 단일 공격 | `VIS_MYTHIC_ETERNAL_SUNLANCE` / Complex |

---

# 3. 희귀도 연출 원칙

## Tier I

- 소박한 무기와 명확한 실루엣
- 활·돌·북·덫·창처럼 즉시 이해되는 행동
- 짧고 가벼운 타격 효과

## Tier II

- 룬·연금술·초급 시간술 같은 전문 기술
- 일반 휴머노이드 리그를 유지하면서 장비와 VFX 강화
- 한 가지 분명한 전투 기믹

## Tier III

- 유성·중력·꿈·불사조·티탄 같은 영웅적 능력
- 소환물이나 대형 마법진을 사용할 수 있음
- 전투 판정은 여전히 공통 행동 문법으로 처리

## Tier IV

- 폭풍룡·태양왕·크로노스·세계수·레비아탄 같은 전설적 상징
- 화면에서 즉시 희귀함이 드러나는 등장·공격 연출
- 지속 카메라 흔들림이나 전투 시야 방해는 금지

## Tier V

- 운명·심판·천상 군단·신수·종말·영원
- 모델보다 오라·후광·소환체·하늘 연출로 신화성을 표현
- 모델링 부담이 크면 공통 영웅 리그와 전용 VFX로 대체
- 희귀함은 크고 선명하게 표현하되 다른 플레이어의 화면을 장시간 가리지 않음

---

# 4. 역할별 희귀도 순서

## 단일 화력

```text
견습 궁수
→ 숙련 쇠뇌수
→ 룬탄 사수
→ 마탄 총사
→ 여명 기사
→ 월광 저격수
→ 태양왕의 궁수
→ 발할라의 신창
→ 영원의 태양창 기사
```

## 광역 화력

```text
돌팔매꾼
→ 화약 투척수
→ 연금 폭격수
→ 천둥 포병
→ 비전 박격포
→ 유성학자
→ 폭풍룡 소환사
→ 천공 유성군주
→ 묵시의 성운
```

## 제어

```text
서리 견습생
→ 사슬 덫꾼
→ 바람 결박사
→ 시간 덫술사
→ 중력 직조자
→ 꿈의 간수
→ 크로노스의 간수
→ 운명 직조자
```

## 마무리

```text
골목 도적
→ 현상금 결투가
→ 그림자 추격자
→ 영혼 수확자
→ 환영검객
→ 죽음의 집행관
→ 적월의 검성
→ 최후의 심판자
```

## 지원

```text
신참 북잡이
→ 군기 수행원
→ 전투 사제
→ 전장의 예언자
→ 별의 성가대장
→ 불사조 전령
→ 세계수의 대사제
→ 치천사 군단장
```

## 대형 사냥

```text
멧돼지 사냥꾼
→ 장창 사냥꾼
→ 거인파쇄 창기병
→ 용사냥 석궁대장
→ 거상 추적자
→ 티탄창 성인
→ 레비아탄 작살왕
→ 신수 멸절자
```

---

# 5. 구현 안전선

- 신화적 이름과 연출은 직접적인 추가 전투 배율이 아닙니다.
- 모든 행동은 예약 피해·재타겟·지원 예산·제어 상한 규칙을 따릅니다.
- 광역 타워는 전장 전체를 무조건 타격하지 않고 대상 수·범위·행동 주기로 PowerBudget을 맞춥니다.
- 마무리 타워는 즉사 면역 적을 우회하지 않으며, 처형 효과도 EquivalentContribution으로 환산합니다.
- 지원 타워는 최대 3대상 예산형 규칙과 최종 지원 배율 상한을 지킵니다.
- 제어 타워는 일반·정예·보스별 감속·정지 상한을 지킵니다.
- 대형 사냥 타워의 추가 피해는 대형·정예·보스 태그에만 적용하고 일반 적 상대 최소 기여를 유지합니다.
- 50번 최고 타워도 스테이지 15 완주 필수 조건이 아닙니다.

---

# 6. 다음 작업 연결

```text
CAT-NEXT-004
50종 AllowedVariantFamilies와 개별 변종 정체성
```

후속 수치 작업:

```text
CAT-NEXT-007
7~50번 피해·주기·범위·투사체·지원·제어 수치 변환
```

변종과 합체는 이 문서의 `TowerId`와 `ActionProfileId`를 기준으로 파생하며, 모델은 `VisualProfileId`만 교체할 수 있습니다.
