# Tower RNG 문서 인덱스

- 상태: Active
- 필수 참고: `../AGENTS.md`
- 마지막 정리: 2026-08-02

## 문서 사용 순서

```text
AGENTS.md
→ README.md / docs/INDEX.md
→ 관련 design 문서
→ 관련 reference 데이터
→ 관련 spec 문서
→ 관련 technical 문서
→ 관련 implementation 문서
→ 실제 코드
```

하위 계층의 공개 규칙이 바뀌면 영향을 받는 상위 문서도 같은 작업에서 갱신합니다.

---

## 프로젝트 진입

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 최신 핵심 루프·확률·인플레이션·첫 경제·V1 완주 개요 |
| `../AGENTS.md` | Required | 승인, 계층, 동기화, 감각·수치·저장 원칙 |
| `INDEX.md` | Active | 전체 문서 위치와 상태 |

---

## 게임 기획

### 진행·확률·밸런스

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/PROGRESSION.md` | Confirmed · Living | 최초 25초, 첫 15분, V1 완주와 기능 순서 |
| `design/V1_COMPLETION_PACING.md` | Confirmed · Living | 스테이지 15까지 12~15시간, 숙련·수집 시간층 |
| `design/RNG_PROBABILITY.md` | Confirmed · Living | 임의 정밀도 `1/N`, 확률표, 숨겨진 유효 확률과 행운 |
| `design/BALANCE_MODEL.md` | Confirmed · Living | 희귀도 PowerBudget, StageScale, SpawnCost, 보상 인플레이션 |
| `design/ECONOMY_PACING.md` | Confirmed · Living | 초기 가격, 문·스탯·환생 시간과 경제 검증 지표 |
| `design/WAVE_PACING.md` | Confirmed · Living | 진입·파밍 목표 시간, 후반 상한과 보스 시간 비중 |
| `design/ROLLING.md` | Confirmed · Living | 4.0초 무료 굴리기, 전역 풀과 특수 주사위 |
| `design/TOWERS.md` | Confirmed · Living | 최소 50종, 역할 분포, 희귀도별 엄격한 성능 증가 |
| `design/STAT_TREE.md` | Confirmed · Living | 하나의 거대한 트리와 첫 환생 전 중심 노드 |
| `design/REBIRTH.md` | Confirmed · Living | 첫 7,000 XP, 증가하는 환생 주기와 초기화 범위 |
| `design/TUTORIAL.md` | Confirmed · Living | 최초 슬라임·4슬롯 준비·첫 굴리기·환생 안내 |
| `design/FUSION.md` | Confirmed · Living | 수동 합체, 보호·편성 수량과 원자적 처리 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 인화성·독성·공허·거대 변종과 최종 공식 분모 |

### 월드·전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/WORLD_NAVIGATION.md` | Confirmed · Living | 로비, 물리적 문, 재접속 빠른 복귀, 텔레포터 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 15스테이지, 5웨이브, StageScale과 예산 |
| `design/STAGE_BOSSES.md` | Confirmed · Living | 지역별 보스 계열, 비율 예산과 보상 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투, 역할, Engage와 타격감 |
| `design/PRESENTATION_FEEL.md` | Confirmed · Living | 과장된 움직임, 일반 화면 흔들림 금지와 완료 기준 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟·이동·행동 루틴·전달 방식 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 고유 능력·사건 반응·조작 |
| `design/FORMATION.md` | Confirmed · Living | 빈 슬롯 채움, 전체·역할 슬롯, 자동 편성과 퀵 HUD |
| `design/TARGETING.md` | Confirmed | 경로 진행도, 실제 거리와 예약 피해 |
| `design/MONSTERS.md` | Confirmed · Living | StageScale 몬스터, SpawnCost와 정체 방지 |

### 경제·UI·운영

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed · Living | StageCoinUnit 1, 보스 1.15배, 코인·정수·Defense XP |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 |
| `design/POTIONS.md` | Confirmed · Living | 포션 효과·시간·중첩 |
| `design/UI_FLOW.md` | Confirmed · Living | HUD, 인벤토리, 수동 합체, Defense XP와 설정 진입 |
| `design/SETTINGS.md` | Confirmed · Living | 파티클·카메라·음향·접근성·성능 설정 |
| `design/SOCIAL.md` | Confirmed · Living | 공식 분모 리더보드, 공개 프로필과 거래 금지 |
| `design/MONETIZATION.md` | Confirmed · Living | RNG 게임 조사 기반 상품 방향과 금지선 |

### 추가 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/LIVE_WAVE.md` | Draft | 로비 진입 서버 공동 전투 |

---

## 콘텐츠 참조와 벤치마크

| 문서 | 상태 | 책임 |
|---|---|---|
| `reference/TOWER_CATALOG.md` | Active Catalog | 공식 분모, PowerBudget, 행동·수치·타격감과 기준 타워 |
| `reference/TOWER_BALANCE_BENCHMARK.md` | Active Benchmark | 최저급 6종의 솔로·혼합·보스 주기 역할 기여도 검증 |
| `reference/MONSTER_CATALOG.md` | Active Catalog | 스테이지 1 일반 몬스터 3종과 우두머리 멧돼지 보스 |
| `reference/STAGE_CATALOG.md` | Active Catalog | 최초 준비 전투, 스테이지 1 전투·보상과 문 가격 |
| `reference/STAGE1_WAVE_BENCHMARK.md` | Active Benchmark | 15개 4역할 편성의 전체 5웨이브·보상 검증 |
| `reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | Active Benchmark | 초기 노드·문·7,000 XP와 첫 환생 7.80~14.34분 검증 |
| `reference/STAT_TREE_CATALOG.md` | Active Catalog | 첫 환생 전 중심 노드 10개, 좌표·가격·효과 |

지역:

```text
1 초원·숲
2 사막
3 정글
4 설원
5 용암지대
```

---

## 밸런스 도구

| 경로 | 상태 | 책임 |
|---|---|---|
| `../tools/balance/tower_baseline.py` | Active | 최저급 기준 타워 6종의 솔로·EquivalentContribution 재현 |
| `../tools/balance/stage1_wave_sim.py` | Active | 스테이지 1 웨이브 1~5와 15개 혼합 편성 재현 |
| `../tools/balance/first_rebirth_economy.py` | Active | 튜토리얼·소비 성향·전투 준비별 첫 환생 경제 재현 |

도구 결과는 기획 계약을 대체하지 않습니다. 가정과 허용 범위는 대응하는 reference 문서에 기록합니다.

---

## 시스템 명세 예정

```text
spec/PROGRESSION.md
spec/V1_COMPLETION_PACING.md
spec/RNG_PROBABILITY.md
spec/BALANCE_MODEL.md
spec/ECONOMY_PACING.md
spec/WAVE_PACING.md
spec/ROLLING.md
spec/TOWERS.md
spec/STAT_TREE.md
spec/REBIRTH.md
spec/TUTORIAL.md
spec/FUSION.md
spec/TOWER_VARIANTS.md
spec/WORLD_NAVIGATION.md
spec/LEVEL_DESIGN.md
spec/STAGE_BOSSES.md
spec/COMBAT.md
spec/PRESENTATION_FEEL.md
spec/FORMATION.md
spec/TARGETING.md
spec/MONSTERS.md
spec/CURRENCY.md
spec/OFFLINE_PROGRESS.md
spec/POTIONS.md
spec/UI_FLOW.md
spec/SETTINGS.md
spec/SOCIAL.md
spec/MONETIZATION.md
spec/LIVE_WAVE.md
```

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/STATE_LIFECYCLE.md` | Confirmed · Living | 프로필, 최초 튜토리얼, 초기화·재접속·원자성·마이그레이션 |
| `technical/TOWER_MODELING.md` | Confirmed · Living | Basic 모델과 자유 이름 모션 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 이동·행동·전달·자원 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | Confirmed · Living | 확장 모듈·훅·조작 세션 |
| `technical/MONSTER_MODELING.md` | Confirmed · Living | 공유 모션 엔진 몬스터 제작 규약 |

---

## 구현 전에 지켜야 할 수치·상태 계약

```text
공식 확률과 행운
→ design/RNG_PROBABILITY.md

타워·몬스터·스테이지 수치
→ design/BALANCE_MODEL.md

V1 전체 완주 시간
→ design/V1_COMPLETION_PACING.md

웨이브 목표시간
→ design/WAVE_PACING.md

첫 환생 가격·시간
→ design/ECONOMY_PACING.md
→ reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md

저장·최초 튜토리얼·재접속
→ technical/STATE_LIFECYCLE.md

효과·카메라·접근성
→ design/PRESENTATION_FEEL.md
→ design/SETTINGS.md
```

---

## 현재 우선순위

```text
완료
- 역할별 최저급 기준 타워 6종
- 스테이지 1 일반 몬스터 3종과 기준 보스
- 최초 슬라임 전투와 4슬롯 준비 규칙
- 15개 혼합 편성 전체 5웨이브 검증
- 일반 웨이브 약 10초, 보스 평균 16초
- 전체 주기 56.28초, 누수 0
- 보스 시간 비중 28.4%, 보스 보상 1.15배
- StageCoinUnit 1
- 중심 스탯 노드 10개와 가격·좌표
- 스테이지 2 문 750, 스테이지 3 문 3,200
- 첫 환생 7,000 Defense XP
- 소비 성향별 첫 환생 7.80~14.34분 검증
- 최초 튜토리얼·빈 슬롯 채움 저장 계약
- V1 스테이지 15 최초 클리어 중앙값 12~15시간
- 빠른 8~10시간, 느린 18~22시간, 숙련 20~30시간

다음
1. V1 최고 일반 굴리기 타워의 공식 분모와 PowerBudget 기준 설정
2. 최고점에서 역산한 50종 희귀도 사다리 초안
3. 스테이지 15 권장 편성·환생 배율 목표 설정
4. 스테이지 2 실제 몬스터·웨이브·보스 작성
5. 스테이지 2 진입·파밍 목표 시간 시뮬레이션
6. 역할별 `1 / 100` 기준 타워 6종 작성
7. 초기 확률 사다리와 4초 굴림의 전투력 분포 시뮬레이션
8. 경제의 스테이지 2 준비 시나리오를 실제 분포로 교체
9. 스테이지 1 Min·MaxBudget 변형 검증
10. 두 번째 환생과 환생 영구 보상 시뮬레이션
11. 확률 컴파일러·PowerBudget·SpawnCost 통합 도구 설계
12. UI·전투 피드백 토큰과 설정 Preview 기준 작성
13. 지역 1 수직 슬라이스 구현
14. 검증 후 타워 50종·15스테이지 확장
```

라이브 웨이브는 기본 수직 슬라이스와 저장·밸런스 계약 검증 뒤 진행합니다.
