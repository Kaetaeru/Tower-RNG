# Tower RNG 문서 인덱스

- 상태: Active
- 필수 참고: `../AGENTS.md`
- 마지막 정리: 2026-08-02

## 문서 사용 순서

```text
AGENTS.md
    ↓
README.md / docs/INDEX.md
    ↓
관련 design 문서
    ↓
관련 spec 문서
    ↓
관련 technical 문서
    ↓
관련 implementation 문서
    ↓
실제 코드
```

하위 계층의 공개 규칙이 변경되면 영향을 받는 상위 문서도 같은 작업에서 함께 갱신합니다. 새 시스템을 추가하면 이 인덱스와 프로젝트 전체 루프에 영향을 주는 경우 README도 수정합니다.

---

## 프로젝트 진입 문서

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 게임 전체 개요와 최신 핵심 루프 |
| `../AGENTS.md` | Required | 승인, 문서 계층, 상하위 동기화와 구현 원칙 |
| `INDEX.md` | Active | 전체 문서 위치와 상태 |

---

## 게임 기획 문서

### 핵심 획득과 성장

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/ROLLING.md` | Confirmed · Living | 무료 굴리기, 극초반 자동 굴리기, 특수 주사위와 스테이지 행운 |
| `design/TOWERS.md` | Confirmed · Living | 고정 타워 데이터, 보유 수량, 보호와 자동 편성 연동 |
| `design/STAT_TREE.md` | Confirmed · Living | 계정 영구 성장, 자동 기능, 자석과 환생 조건 구역 |
| `design/REBIRTH.md` | Confirmed · Living | 코인·지역 진행 초기화와 영구 코인·행운 배율 |
| `design/TUTORIAL.md` | Confirmed · Living | 첫 굴리기, 코인 수집, 자동 기능과 지연형 안내 |
| `design/FUSION.md` | Confirmed · Living | 중후반 중복 타워 합체와 영구 누적 진행 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 별도 고정 변종 타워와 해금 규칙 |

### 전투와 편성

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투, 역할, 공통 성장과 Engage 타이밍 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟, 이동, 행동 루틴과 전달 방식의 조합 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 타워별 고유 능력, 사건 반응과 플레이어 조작 |
| `design/FORMATION.md` | Confirmed · Living | 전체·역할 슬롯, 자동 편성 토글과 역할 성향 |
| `design/TARGETING.md` | Confirmed | 경로 진행도, 실제 거리와 예약 피해 기반 타겟팅 |
| `design/MONSTERS.md` | Confirmed · Living | 몬스터 유형, 코인 드롭, 특수 행동과 변종 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 5개 지역·15개 지속형 파밍 스테이지와 스테이지 행운 |

### 경제와 소비품

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed · Living | 코인 월드 드롭·직접 수집, 자석과 연금 정수 |
| `design/POTIONS.md` | Confirmed · Living | 포션 상점, 효과, 지속시간과 환생 보존 |

### 추가 전투 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/STAGE_BOSSES.md` | Draft | 플레이어별 개인 보스, 출현과 월드 코인 보상 |
| `design/LIVE_WAVE.md` | Draft | 실제 시간 기반 서버 공동 전투와 기여 보상 |

---

## 시스템 명세 예정

기획 규칙이 충분히 확정된 시스템부터 다음 경로에 작성합니다.

```text
spec/ROLLING.md
spec/TOWERS.md
spec/STAT_TREE.md
spec/REBIRTH.md
spec/TUTORIAL.md
spec/FUSION.md
spec/TOWER_VARIANTS.md
spec/COMBAT.md
spec/TOWER_BEHAVIOR.md
spec/TOWER_EXTENSIONS.md
spec/FORMATION.md
spec/TARGETING.md
spec/MONSTERS.md
spec/LEVEL_DESIGN.md
spec/CURRENCY.md
spec/POTIONS.md
spec/STAGE_BOSSES.md
spec/LIVE_WAVE.md
```

시스템 명세는 구현 방식과 무관한 입력·출력·판정 순서·예외·수용 조건을 담당합니다.

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/TOWER_MODELING.md` | Confirmed · Living | Basic 모델, 자유 이름 모션과 전체 시각 상태 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 이동, 행동 루틴, 전달, 생성물과 자원 프로필 제작 양식 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | Confirmed · Living | 확장 모듈, 이벤트 훅, 고유 능력과 조작 세션 |
| `technical/MONSTER_MODELING.md` | Confirmed · Living | 타워 모션 엔진을 공유하는 몬스터 모델·모션 규약 |

관련 문서는 다음 순서로 읽습니다.

```text
타워 제작
TOWER_MODELING.md
→ TOWER_BEHAVIOR_GRAMMAR.md
→ TOWER_EXTENSION_FRAMEWORK.md

몬스터 제작
TOWER_MODELING.md의 공통 시각 규칙
→ MONSTER_MODELING.md
```

다른 시스템의 기술 설계는 시스템 명세가 확정된 뒤 `technical/<SYSTEM>.md`에 작성합니다.

---

## 구현 명세

아직 작성 전입니다.

```text
implementation/<SYSTEM>.md
```

구현 명세는 실제 파일 경로, 공개 타입, 공개 함수, Remote 계약, 저장 스키마와 테스트 대상을 담당합니다.

---

## 참조 문서 예정

| 예정 문서 | 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 타워 ID, 역할, 확률과 전투 데이터 |
| `reference/MONSTER_CATALOG.md` | 몬스터 ID, 생성 비용, 능력치와 태그 |
| `reference/REGION_CATALOG.md` | 지역·스테이지, 코인 단가와 행운 데이터 |
| `reference/TERMS.md` | 공통 용어와 명명 규칙 |

실제 카탈로그 데이터가 정해지기 전에는 빈 문서를 만들지 않습니다.

---

## 주요 결정 기록 후보

- 추종형 타워 전투
- 일반 스테이지 공격 사거리 제거
- PathProgress와 WorldPosition 이중 판정
- Engage 이동 시간이 실제 공격 타이밍에 영향
- 일반 행동 문법과 선택적 고유 확장 분리
- 코인 월드 드롭과 직접 수집
- 환생 시 코인·모든 지역 진행 초기화, 계정 성장 유지

ADR 작성 전에는 필요성을 사용자에게 확인합니다.

---

## 현재 우선순위

```text
1. 핵심 루프의 남은 상위 기획 정리
2. 환생·지역·자동 편성·코인 수집의 밸런스 범위 결정
3. 핵심 시스템 명세 작성
4. 기술 설계와 구현 명세 작성
5. 실제 코드 구현 및 검증
```

우선 명세화하기 적합한 시스템:

1. 굴리기
2. 코인 수집
3. 스탯 트리
4. 환생
5. 편성·자동 편성
6. 지역·스테이지
7. 타워 보유
8. 타겟팅과 전투 행동
