# Tower RNG 문서 인덱스

- 상태: **Active**
- 마지막 정리: 2026-08-03
- 필수 참고: `../AGENTS.md`

## 먼저 볼 문서

| 문서 | 책임 |
|---|---|
| `PROJECT_STATUS.md` | 전체 진행률·마스터 체크리스트·현재 다음 작업 |
| `balance/FINAL_BALANCE_BATCH.md` | 남은 계산 6단계의 완료·조건부 상태 |
| `balance/FINAL_RECOMMENDATION.md` | 카탈로그로 넘길 계산 권고값 묶음 |
| `catalog/INDEX.md` | 실제 콘텐츠 ID·이름·채택 수치 |
| `balance/INDEX.md` | 공식·가정·시뮬레이션·재현 도구 |
| `../README.md` | 게임 루프와 V1 범위 |
| `../AGENTS.md` | 승인·동기화·수치 작업 원칙 |

현재 준비도:

```text
전체 V1 약 40%
기획·밸런스 약 87%
콘텐츠 카탈로그 약 12%
Roblox 구현·QA는 저장소 기준 초기 단계
```

---

# 문서 책임 구조

```text
AGENTS.md
→ README.md / docs/INDEX.md / docs/PROJECT_STATUS.md
→ design          게임 규칙과 플레이어 경험
→ catalog         실제 콘텐츠와 최종 채택 수치
→ balance         계산·시뮬레이션·검증
→ spec            정확한 시스템 동작 계약
→ technical       서버·클라이언트·저장 구조
→ implementation  실제 파일·함수·Remote 명세
→ code            Roblox 구현
```

```text
balance가 값을 추천
→ catalog가 값을 채택
→ implementation이 동일 값을 사용
→ Roblox 런타임에서 검증
```

기존 `reference` 폴더는 링크 호환 영역이며 신규 문서는 추가하지 않습니다.

---

# 게임 기획

## 진행·확률·경제

| 문서 | 책임 |
|---|---|
| `design/PROGRESSION.md` | 최초 25초와 장기 진행 |
| `design/V1_COMPLETION_PACING.md` | 빠른·중앙·느린 최종 완주 시간 |
| `design/RNG_PROBABILITY.md` | 공식 `1/N`과 행운 압축 |
| `design/ROLLING.md` | 무료 굴리기·속도·특수 주사위 |
| `design/BALANCE_MODEL.md` | 공통 수치 공식 |
| `design/ECONOMY_PACING.md` | 코인·문·환생 경제 |
| `design/CURRENCY.md` | 코인·정수·XP·토큰 |
| `design/REBIRTH.md` | 진행 유지 환생과 네 스탯 |
| `design/STAT_TREE.md` | 코인 트리와 환생 스탯 |
| `design/OFFLINE_PROGRESS.md` | 오프라인 코인 공식·효율·상한 |

## 타워·전투

| 문서 | 책임 |
|---|---|
| `design/TOWERS.md` | 50종 이상과 역할·희귀도 |
| `design/COMBAT.md` | 추종 자동 전투 |
| `design/FORMATION.md` | 4→12슬롯과 역할 상한 |
| `design/EFFECT_STACKING.md` | 지원·제어 중첩 계약 |
| `design/TARGETING.md` | 타겟 선정과 예약 피해 |
| `design/TOWER_BEHAVIOR.md` | 타워 행동 문법 |
| `design/TOWER_EXTENSIONS.md` | 고유 능력 확장 |
| `design/TOWER_VARIANTS.md` | 변종 티켓·계열·허용 범위 |
| `design/FUSION.md` | 수동 합체 3→1·최대 2단계 |

## 월드·스테이지

| 문서 | 책임 |
|---|---|
| `design/WORLD_NAVIGATION.md` | 영구 문과 복귀 |
| `design/LEVEL_DESIGN.md` | 15스테이지와 5웨이브 |
| `design/WAVE_PACING.md` | 진입·파밍 목표시간 |
| `design/STAGE_VALIDATION.md` | 완전·경량 검증 정책 |
| `design/STAGE_BOSSES.md` | 보스 예산과 보상 |
| `design/MONSTERS.md` | 몬스터 스케일과 SpawnCost |

---

# 콘텐츠 카탈로그

권위 인덱스: `catalog/INDEX.md`

현재 호환 문서:

| 문서 | 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 타워 ID·행동·수치·자산 |
| `reference/MONSTER_CATALOG.md` | 몬스터·보스 데이터 |
| `reference/STAGE_CATALOG.md` | 지역·스테이지 데이터 |
| `reference/STAT_TREE_CATALOG.md` | 코인 스탯 트리 데이터 |

새 카탈로그 문서는 `docs/catalog`에만 작성합니다.

현재 실제 콘텐츠:

```text
공식 일반 확률 슬롯 50 / 50
기준 타워 정체성 6 / 최소 50
스테이지 1 상세 중심
스테이지 2~15는 계산용 콘텐츠 중심
```

---

# 계산·검증

권위 인덱스: `balance/INDEX.md`

## 최종 배치

| 문서 | 상태 |
|---|---|
| `balance/FINAL_BALANCE_BATCH.md` | 계산 수행 6/6·완전 4·조건부 2 |
| `balance/FINAL_RECOMMENDATION.md` | 카탈로그 채택 후보값 정리 완료 |
| `balance/FINAL_ACCOUNT_PATHS.md` | 빠른·중앙·느린 10,000계정 경로 완료 |
| `balance/FINAL_ECONOMY_INTEGRATION.md` | 선택 경제 통합·추가 싱크 15~25B 산출 |
| `balance/RUNTIME_LOSS_BUDGET.md` | 계산 예산 완료·실제 Roblox 측정 대기 |

## 확률·경제·편성

| 문서 | 책임 |
|---|---|
| `reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 확률표 |
| `reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축 |
| `reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 |
| `reference/V1_REBIRTH_XP_BENCHMARK.md` | 환생 XP |
| `reference/V1_REBIRTH_STAT_BENCHMARK.md` | 환생 스탯 |
| `reference/V1_FORMATION_SLOT_BENCHMARK.md` | 슬롯 가격과 역할 제한 |
| `reference/V1_COIN_COMBAT_BENCHMARK.md` | 독립 전투 성장 |
| `balance/V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투 통합 경제 |
| `balance/SUPPORT_CONTROL_STACKING_BENCHMARK.md` | 지원·제어 중첩 |
| `balance/V1_TOWER_VARIANT_BENCHMARK.md` | 변종 확률·전투력·코인 가지 |
| `balance/V1_FUSION_BENCHMARK.md` | 합체 재료·전투력·코인 가지 |
| `balance/OFFLINE_COIN_BENCHMARK.md` | 오프라인 민감도 |

현재 계산된 영구 코인 싱크:

```text
문·슬롯·전투 36.397B
변종          25.019B
합체           2.750B
오프라인       3.120B
합계          67.286B
```

추가 선택형 숙련 싱크 `15~25B`의 콘텐츠 정체성은 아직 결정 전입니다.

## 스테이지 전투

| 문서 | 상태 |
|---|---|
| `reference/STAGE1_WAVE_BENCHMARK.md` | 완전 완료 |
| `reference/STAGE2_WAVE_BENCHMARK.md` | 추가 완전 완료 |
| `reference/STAGE3_WAVE_BENCHMARK.md` | 완전 완료 |
| `reference/STAGE4_5_LIGHT_BENCHMARK.md` | 경량 완료 |
| `reference/STAGE6_WAVE_BENCHMARK.md` | 완전 완료 |
| `balance/STAGE7_8_LIGHT_BENCHMARK.md` | 경량 완료 |
| `balance/STAGE9_WAVE_BENCHMARK.md` | 완전 완료 |
| `balance/STAGE10_11_LIGHT_BENCHMARK.md` | 경량 완료 |
| `balance/STAGE12_WAVE_BENCHMARK.md` | 완전 완료 |
| `balance/STAGE13_14_LIGHT_BENCHMARK.md` | 경량 완료 |
| `balance/STAGE15_ACTION_WAVE_BENCHMARK.md` | 행동형 완전 완료 |

```text
스테이지 수치 검증 완료: 15 / 15
```

---

# 최종 계산 결과

```text
Stage15 FirstClearEC = 10,050
Stage15 StableFarmEC = 12,200

빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
중앙 안정 파밍 약 13.5h
```

합체:

```text
기본형 3개 → 1단계 ×1.45
기본형 총 9개 → 2단계 ×2.1025
V1 최대 2단계
```

오프라인:

```text
효율 25→40%
저장 8→24h
가지 총가격 3.1201B
```

런타임 목표:

```text
Stage1 >= 0.992
Stage9 >= 0.990
Stage12 >= 0.988
Stage15 >= 0.986
```

---

# 밸런스 재현 도구

경로: `../tools/balance`

## 성장·경제·편성

| 도구 | 책임 |
|---|---|
| `tower_baseline.py` | 최저급 역할 기여도 |
| `v1_probability_ladder.py` | 공식 확률 합 |
| `v1_luck_compression.py` | 행운 압축 |
| `v1_rebirth_xp_curve.py` | 환생 XP |
| `rebirth_stat_tokens.py` | 환생 스탯·굴림 통합 |
| `v1_roster_power_distribution.py` | 보유 전력 분포 |
| `v1_formation_slot_economy.py` | 슬롯 경제 |
| `v1_coin_combat_curve.py` | 코인 전투 성장 |
| `v1_gate_economy.py` | 문·슬롯·전투 통합 경제 |
| `support_control_stacking.py` | 지원·제어 중첩 |
| `v1_tower_variant_benchmark.py` | 변종 |
| `v1_fusion_benchmark.py` | 합체 |
| `offline_coin_benchmark.py` | 오프라인 코인 |
| `runtime_loss_budget.py` | 런타임 손실 예산 |
| `final_economy_integration.py` | 후반 경제 통합 |
| `final_account_paths.py` | 전체 계정 경로 |

## 스테이지

`stage1_wave_sim.py`부터 `stage15_action_wave_sim.py`까지의 개별 재현 도구를 사용합니다.

---

# 시스템·기술 문서

| 문서 | 책임 |
|---|---|
| `technical/STATE_LIFECYCLE.md` | 프로필·재접속·환생 원자성 |
| `technical/TOWER_MODELING.md` | 타워 3D 제작 규약 |
| `technical/MONSTER_MODELING.md` | 몬스터 3D 제작 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | 행동 데이터 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | 확장 모듈과 훅 |

서비스별 정확한 계약은 `spec/`, 실제 Roblox 파일·Remote 명세는 `implementation/`에 작성합니다.

---

# 현재 다음 작업

```text
CAT-NEXT-001
문·슬롯·전투·변종·합체·오프라인 권고값의 카탈로그 채택 검토
```

별도 미완료:

```text
DES-NEXT-001
추가 15~25B 숙련 코인 싱크 정체성 결정

RUN-NEXT-001
지역 1 수직 슬라이스에서 실제 RuntimeEfficiency 측정
```
