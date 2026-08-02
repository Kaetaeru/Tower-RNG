# Tower RNG 문서 인덱스

- 상태: **Active**
- 마지막 정리: 2026-08-03
- 필수 참고: `../AGENTS.md`

## 먼저 볼 문서

| 문서 | 책임 |
|---|---|
| `PROJECT_STATUS.md` | 전체 진행률·체크리스트·현재 작업 |
| `catalog/INDEX.md` | 실제 채택 ID·수치·콘텐츠 상태 |
| `catalog/TOWER_CATALOG.md` | 일반 타워 50종·역할·확률·테마·행동 |
| `catalog/TOWER_SYSTEM_CATALOG.md` | 변종·합체 공통 규칙 |
| `catalog/STAGE_CATALOG.md` | 5지역·15스테이지·웨이브 |
| `catalog/MONSTER_CATALOG.md` | 몬스터 39종·전투 프로필·행동 |
| `catalog/STAGE_GATE_CATALOG.md` | 스테이지 2~15 영구 문 |
| `catalog/STAT_TREE_CATALOG.md` | 코인 스탯 트리 채택값 |
| `technical/MONSTER_CONTENT_ARCHITECTURE.md` | 몬스터 전투와 시각 자산 분리 구조 |
| `balance/FINAL_BALANCE_BATCH.md` | 최종 계산과 재계산 규칙 |
| `balance/INDEX.md` | 공식·가정·시뮬레이션·재현 도구 |
| `../README.md` | 게임 루프와 V1 범위 |
| `../AGENTS.md` | 승인·동기화·수치 작업 원칙 |

현재 준비도:

```text
전체 V1 약 53%
기획·밸런스 약 91%
콘텐츠 카탈로그 약 66%
Roblox 구현·QA는 저장소 기준 초기 단계
```

---

# 문서 책임 구조

```text
balance에서 계산
→ 사용자가 승인
→ catalog가 영구 ID·값·콘텐츠 채택
→ spec·implementation이 동일 데이터 사용
→ Roblox 런타임에서 검증
```

기존 `reference` 폴더는 링크 호환 영역입니다. 충돌 시 `docs/catalog`의 권위 문서를 사용합니다.

---

# 콘텐츠 카탈로그

| 문서 | 채택 범위 | 상태 |
|---|---|---|
| `catalog/TOWER_CATALOG.md` | TowerId 50개, 역할·확률·PowerBudget·ThemeStageId·ActionProfileId | Confirmed Identity · Runtime Parameters Pending |
| `catalog/TOWER_SYSTEM_CATALOG.md` | 변종 티켓·PowerBudget·합체 조합 | Confirmed System Values |
| `catalog/STAGE_GATE_CATALOG.md` | GateId 14개와 가격 | Confirmed |
| `catalog/STAGE_CATALOG.md` | RegionId 5개, StageId·WaveSetId 15개 | Confirmed Combat Data |
| `catalog/MONSTER_CATALOG.md` | MonsterId 39개와 스테이지별 전투 프로필 | Confirmed Gameplay Identity |
| `catalog/STAT_TREE_CATALOG.md` | 초기·슬롯·전투·특수·숙련 노드 | Confirmed Values · Layout Pending |

현재 카탈로그 핵심 수치:

```text
일반 타워 TowerId 50 / 50
일반 타워 역할·공식 확률·PowerBudget 50 / 50
정확한 런타임 수치 6 / 50
StageId·WaveSetId 15 / 15
MonsterId 39
영구 문 14 / 14
```

타워와 몬스터 모델은 교체 가능한 `VisualProfileId`로 분리합니다. 제작 난도가 높으면 모델과 연출만 교체하고 전투 정체성·확률·행동을 유지합니다.

---

# 일반 타워 역할 분포

```text
단일 화력 9
광역 화력 9
제어 8
마무리 8
지원 8
대형 사냥 8
합계 50
```

각 타워는 15개 스테이지 중 하나의 `ThemeStageId`를 가집니다. 이는 외형·설정·공격 연출의 출신 테마이며 획득·사용 제한이 아닙니다.

---

# 계산·검증

```text
최종 계산 6 / 6
스테이지 수치 검증 15 / 15
빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
Stage15 FirstClearEC 10,050
Stage15 StableFarmEC 12,200
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

실제 Roblox RuntimeEfficiency만 측정 대기입니다.

---

# 주요 게임 기획

## 진행·경제

| 문서 | 책임 |
|---|---|
| `design/PROGRESSION.md` | 최초 25초와 장기 진행 |
| `design/V1_COMPLETION_PACING.md` | 완주 시간 |
| `design/RNG_PROBABILITY.md` | 공식 확률과 행운 |
| `design/ECONOMY_PACING.md` | 코인·문·환생 경제 |
| `design/STAT_TREE.md` | 코인 트리와 환생 스탯 |
| `design/OFFLINE_PROGRESS.md` | 오프라인 코인 |
| `design/MASTERY_CONTROL_ROOM.md` | 후반 숙련 편의 |

## 타워·전투

| 문서 | 책임 |
|---|---|
| `design/TOWERS.md` | 타워 역할·희귀도 |
| `design/COMBAT.md` | 추종 자동 전투 |
| `design/FORMATION.md` | 4→12슬롯과 역할 상한 |
| `design/EFFECT_STACKING.md` | 지원·제어 중첩 |
| `design/TARGETING.md` | 타겟 선정과 예약 피해 |
| `design/TOWER_BEHAVIOR.md` | 행동 문법 |
| `design/TOWER_VARIANTS.md` | 변종 기획 |
| `design/FUSION.md` | 수동 합체 기획 |

## 월드·몬스터

| 문서 | 책임 |
|---|---|
| `design/WORLD_NAVIGATION.md` | 영구 문과 복귀 |
| `design/LEVEL_DESIGN.md` | 15스테이지 구조 |
| `design/WAVE_PACING.md` | 목표 처리시간 |
| `design/STAGE_VALIDATION.md` | 검증 정책 |
| `design/STAGE_BOSSES.md` | 보스 예산과 보상 |
| `design/MONSTERS.md` | 몬스터 공통 규칙 |

---

# 기술 구조

| 문서 | 책임 |
|---|---|
| `technical/STATE_LIFECYCLE.md` | 프로필·재접속·환생 원자성 |
| `technical/TOWER_MODELING.md` | 타워 3D 제작 규약 |
| `technical/MONSTER_MODELING.md` | 몬스터 3D 제작 규약 |
| `technical/MONSTER_CONTENT_ARCHITECTURE.md` | MonsterId·수치·행동·시각 분리 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | 타워 행동 데이터 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | 확장 모듈과 훅 |

---

# 현재 다음 작업

```text
CAT-NEXT-004
일반 타워 50종의 AllowedVariantFamilies와 개별 변종 정체성 채택
```

그 다음:

```text
CAT-NEXT-005 기본형·변종 합체 계보
CAT-NEXT-006 스탯 트리 좌표·아이콘·연결선
CAT-NEXT-007 타워 7~50 역할별 런타임 수치 변환
```

별도 실측:

```text
RUN-NEXT-001
지역 1 수직 슬라이스에서 RuntimeEfficiency 측정
```
