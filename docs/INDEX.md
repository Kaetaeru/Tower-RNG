# Tower RNG 문서 인덱스

- 상태: **Active**
- 마지막 정리: 2026-08-03
- 필수 참고: `../AGENTS.md`

## 먼저 볼 문서

| 문서 | 책임 |
|---|---|
| `PROJECT_STATUS.md` | 전체 진행률·체크리스트·현재 작업 |
| `catalog/INDEX.md` | 실제 채택 ID·수치·콘텐츠 상태 |
| `catalog/STAGE_GATE_CATALOG.md` | 스테이지 2~15 영구 문 |
| `catalog/STAT_TREE_CATALOG.md` | 코인 스탯 트리 채택값 |
| `catalog/TOWER_SYSTEM_CATALOG.md` | 변종·합체 공통 규칙 |
| `balance/FINAL_BALANCE_BATCH.md` | 최종 계산과 재계산 규칙 |
| `balance/FINAL_RECOMMENDATION.md` | 계산값과 채택 카탈로그 연결 |
| `balance/INDEX.md` | 공식·가정·시뮬레이션·재현 도구 |
| `../README.md` | 게임 루프와 V1 범위 |
| `../AGENTS.md` | 승인·동기화·수치 작업 원칙 |

현재 준비도:

```text
전체 V1 약 44%
기획·밸런스 약 90%
콘텐츠 카탈로그 약 26%
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
balance가 값을 계산
→ 사용자가 승인
→ catalog가 값을 채택
→ implementation이 같은 값을 사용
→ Roblox 런타임에서 검증
```

기존 `reference` 폴더는 링크 호환 영역이며 신규 문서를 추가하지 않습니다. 수치 충돌 시 `docs/catalog`의 새 문서가 우선합니다.

---

# 콘텐츠 카탈로그

권위 인덱스: `catalog/INDEX.md`

## 채택 완료

| 문서 | 채택 범위 | 상태 |
|---|---|---|
| `catalog/STAGE_GATE_CATALOG.md` | 스테이지 2~15 GateId·가격 | Confirmed |
| `catalog/STAT_TREE_CATALOG.md` | 초기 노드·슬롯·전투·변종·합체·오프라인·숙련 제어실 | Confirmed Values · Layout Pending |
| `catalog/TOWER_SYSTEM_CATALOG.md` | 변종 티켓·PowerBudget·합체 조합 | Confirmed System Values |

채택된 주요 합계:

```text
스테이지 4~15 문  1,302,495,000
편성 슬롯 5~12    2,790,686,200
공통 전투 I~XI   32,303,644,750
변종 가지        25,018,500,000
합체 가지         2,750,250,000
오프라인 가지     3,120,100,000
숙련 제어실      25,200,000,000
```

## 기존 호환 문서

| 문서 | 현재 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 기존 기준 타워·확률 슬롯 참조 |
| `reference/MONSTER_CATALOG.md` | 스테이지 1 중심 기존 몬스터 |
| `reference/STAGE_CATALOG.md` | 기존 지역·스테이지 참조 |
| `reference/STAT_TREE_CATALOG.md` | 초기 노드의 기존 설명·UI 초안 |

## 다음 채택

```text
CAT-NEXT-002
스테이지 1~15 계산용 웨이브를 최종 StageId·MonsterId 카탈로그로 채택
```

그 다음:

```text
CAT-NEXT-003 일반 타워 50종 정체성·역할·행동
CAT-NEXT-004 타워별 변종 허용 계열과 개별 변종
CAT-NEXT-005 기본형·변종 합체 계보
CAT-NEXT-006 스탯 트리 좌표·아이콘·연결선
```

---

# 게임 기획

## 진행·확률·경제

| 문서 | 책임 |
|---|---|
| `design/PROGRESSION.md` | 최초 25초와 장기 진행 |
| `design/V1_COMPLETION_PACING.md` | 빠른·중앙·느린 완주 시간 |
| `design/RNG_PROBABILITY.md` | 공식 `1/N`과 행운 압축 |
| `design/ROLLING.md` | 무료 굴리기와 특수 주사위 |
| `design/ECONOMY_PACING.md` | 코인·문·환생 경제 |
| `design/STAT_TREE.md` | 코인 트리와 환생 스탯 |
| `design/OFFLINE_PROGRESS.md` | 오프라인 코인 원칙 |
| `design/MASTERY_CONTROL_ROOM.md` | 후반 숙련 편의 가지 |

## 타워·전투

| 문서 | 책임 |
|---|---|
| `design/TOWERS.md` | 타워 역할·희귀도 |
| `design/COMBAT.md` | 추종 자동 전투 |
| `design/FORMATION.md` | 4→12슬롯과 역할 상한 |
| `design/EFFECT_STACKING.md` | 지원·제어 중첩 |
| `design/TARGETING.md` | 타겟 선정과 예약 피해 |
| `design/TOWER_BEHAVIOR.md` | 행동 문법 |
| `design/TOWER_EXTENSIONS.md` | 고유 능력 확장 |
| `design/TOWER_VARIANTS.md` | 변종 기획 |
| `design/FUSION.md` | 수동 합체 기획 |

## 월드·스테이지

| 문서 | 책임 |
|---|---|
| `design/WORLD_NAVIGATION.md` | 영구 문과 복귀 |
| `design/LEVEL_DESIGN.md` | 15스테이지와 5웨이브 |
| `design/WAVE_PACING.md` | 진입·파밍 목표시간 |
| `design/STAGE_VALIDATION.md` | 검증 정책 |
| `design/STAGE_BOSSES.md` | 보스 예산과 보상 |
| `design/MONSTERS.md` | 몬스터 스케일과 SpawnCost |

---

# 계산·검증

권위 인덱스: `balance/INDEX.md`

```text
최종 계산 단계 6 / 6
수학 계산 완료 6 / 6
스테이지 수치 검증 15 / 15
카탈로그 채택 완료
런타임 실측 대기
```

최종 완주 결과:

```text
빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
중앙 안정 파밍 약 13.5h

Stage15 FirstClearEC = 10,050
Stage15 StableFarmEC = 12,200
```

최종 영구 코인 싱크:

```text
문·슬롯·전투  36.3968252B
변종           25.0185B
합체            2.75025B
오프라인        3.1201B
숙련 제어실    25.2000B
합계           92.4856752B
```

---

# 밸런스 재현 도구

경로: `../tools/balance`

주요 도구:

```text
v1_probability_ladder.py
v1_luck_compression.py
v1_rebirth_xp_curve.py
rebirth_stat_tokens.py
v1_roster_power_distribution.py
v1_formation_slot_economy.py
v1_coin_combat_curve.py
v1_gate_economy.py
support_control_stacking.py
v1_tower_variant_benchmark.py
v1_fusion_benchmark.py
offline_coin_benchmark.py
runtime_loss_budget.py
final_economy_integration.py
mastery_utility_sink.py
final_account_paths.py
```

스테이지는 `stage1_wave_sim.py`부터 `stage15_action_wave_sim.py`까지의 개별 재현 도구를 사용합니다.

---

# 기술·구현

| 문서 | 책임 |
|---|---|
| `technical/STATE_LIFECYCLE.md` | 프로필·재접속·환생 원자성 |
| `technical/TOWER_MODELING.md` | 타워 3D 제작 규약 |
| `technical/MONSTER_MODELING.md` | 몬스터 3D 제작 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | 행동 데이터 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | 확장 모듈과 훅 |

서비스 계약은 `spec/`, 실제 Roblox 파일과 Remote 명세는 `implementation/`에 작성합니다.

별도 실측 작업:

```text
RUN-NEXT-001
지역 1 수직 슬라이스에서 RuntimeEfficiency 측정
```
