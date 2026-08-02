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

하위 계층의 공개 규칙이 변경되면 영향을 받는 상위 문서도 같은 작업에서 함께 갱신합니다.

---

## 프로젝트 진입 문서

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 최신 핵심 루프, 지역, 웨이브, 타격감과 주요 시스템 개요 |
| `../AGENTS.md` | Required | 승인, 문서 계층, 상하위 동기화와 구현 원칙 |
| `INDEX.md` | Active | 전체 문서 위치와 상태 |

---

## 게임 기획 문서

### 전체 진행과 획득

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/PROGRESSION.md` | Confirmed · Living | 전역 타워 풀, 기능 순서, 첫 환생과 반복 주기 |
| `design/ROLLING.md` | Confirmed · Living | 무료 굴리기, 전역 일반 타워 풀과 특수 주사위 |
| `design/TOWERS.md` | Confirmed · Living | 고정 타워 데이터, 보유 수량과 자동 편성 연동 |
| `design/STAT_TREE.md` | Confirmed · Living | 계정 영구 성장, 자석·오프라인·텔레포터 |
| `design/REBIRTH.md` | Confirmed · Living | 짧은 반복 환생과 완만한 영구 배율 |
| `design/TUTORIAL.md` | Confirmed · Living | 첫 굴리기, 코인 수집과 기능 안내 |
| `design/FUSION.md` | Confirmed · Living | 중후반 합체와 영구 누적 진행 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 별도 고정 변종 타워와 해금 규칙 |

### 월드와 전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/WORLD_NAVIGATION.md` | Confirmed · Living | 로비, 선형 스테이지, 문, 웨이브 초기화와 텔레포터 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 5개 지역, 15개 스테이지, 5웨이브와 생성 예산 |
| `design/STAGE_BOSSES.md` | Confirmed · Living | 각 스테이지 5웨이브 보스와 반복 주기 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투, 역할, Engage와 전투 타격감 |
| `design/PRESENTATION_FEEL.md` | Confirmed · Living | UI·굴리기·전투의 과장된 움직임과 피드백 완료 기준 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟, 이동, 행동 루틴과 전달 방식 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 고유 능력, 사건 반응과 플레이어 조작 |
| `design/FORMATION.md` | Confirmed · Living | 전체·역할 슬롯, 자동 편성과 퀵 편성 HUD |
| `design/TARGETING.md` | Confirmed | 경로 진행도, 실제 거리와 예약 피해 타겟팅 |
| `design/MONSTERS.md` | Confirmed · Living | 몬스터 유형, 생성 비용, 웨이브 배치와 변종 |

### 경제와 UI

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed · Living | 코인 드롭·수집, 문 구매와 연금 정수 |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 효율과 시간 상한 |
| `design/POTIONS.md` | Confirmed · Living | 포션 효과, 지속시간과 중첩 |
| `design/UI_FLOW.md` | Confirmed · Living | HUD, 퀵 편성, 인벤토리와 즉각적인 클릭 피드백 |
| `design/MONETIZATION.md` | Draft · Research Pending | RNG 게임 벤치마크 기준, 잠정 상품 방향과 금지선 |

### 추가 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/LIVE_WAVE.md` | Draft | 로비에서 진입하는 서버 공동 전투 |

---

## 콘텐츠 참조 문서

공통 시스템 규칙은 design에 두고, 실제 콘텐츠 목록과 수치는 reference에 기록합니다.

| 문서 | 상태 | 책임 |
|---|---|---|
| `reference/TOWER_CATALOG.md` | Active Template | 타워 ID, 확률, 역할, 행동과 수치 작성 양식 |
| `reference/MONSTER_CATALOG.md` | Active Template | 몬스터·보스 ID, 생성 비용, 능력치와 행동 |
| `reference/STAT_TREE_CATALOG.md` | Active Template | 노드 ID, 연결, 가격, 단계와 환생 조건 |
| `reference/STAGE_CATALOG.md` | Active Template | 5개 지역, 15개 스테이지, 맵·웨이브·보스 데이터 |

현재 확정된 지역 테마:

```text
지역 1: 초원·숲
지역 2: 사막
지역 3: 정글
지역 4: 설원
지역 5: 용암지대
```

스테이지 구성과 디자인은 `STAGE_CATALOG.md` 양식을 복제해 사용자가 직접 작성합니다.

---

## 시스템 명세 예정

```text
spec/PROGRESSION.md
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
spec/TOWER_BEHAVIOR.md
spec/TOWER_EXTENSIONS.md
spec/FORMATION.md
spec/TARGETING.md
spec/MONSTERS.md
spec/CURRENCY.md
spec/OFFLINE_PROGRESS.md
spec/POTIONS.md
spec/UI_FLOW.md
spec/MONETIZATION.md
spec/LIVE_WAVE.md
```

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/TOWER_MODELING.md` | Confirmed · Living | Basic 모델, 자유 이름 모션, 과장된 준비·공격·반동 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 이동, 행동 루틴, 전달과 자원 프로필 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | Confirmed · Living | 확장 모듈, 훅, 고유 능력과 조작 세션 |
| `technical/MONSTER_MODELING.md` | Confirmed · Living | 공유 모션 엔진을 사용하는 몬스터 제작 규약 |

---

## 구현 명세

기술 설계가 확정된 뒤 `implementation/<SYSTEM>.md`에 실제 파일, 공개 타입, 함수, Remote, 저장 스키마와 테스트 대상을 기록합니다.

---

## 현재 우선순위

```text
1. RNG 게임 과금 벤치마크 재조사와 MONETIZATION 검증
2. 공통 UI·전투 피드백 토큰과 Preview 기준 정의
3. STAGE_CATALOG에서 지역 1의 3개 스테이지 작성
4. MONSTER_CATALOG에서 지역 1 몬스터와 보스 작성
5. TOWER_CATALOG에서 초기 타워 풀 작성
6. STAT_TREE_CATALOG에서 첫 환생 전 노드 작성
7. 웨이브·환생·경제 밸런스 시뮬레이션
8. 핵심 시스템 명세 작성
9. 지역 1 수직 슬라이스 구현
```
