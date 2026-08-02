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

하위 계층의 공개 규칙이 변경되면 영향을 받는 상위 문서도 같은 작업에서 함께 갱신합니다.

---

## 프로젝트 진입 문서

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 최신 핵심 루프, 월드 진행과 주요 시스템 개요 |
| `../AGENTS.md` | Required | 승인, 문서 계층, 상하위 동기화와 구현 원칙 |
| `INDEX.md` | Active | 전체 문서 위치와 상태 |

---

## 게임 기획 문서

### 전체 진행과 핵심 획득

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/PROGRESSION.md` | Confirmed · Living | 전역 타워 풀, 기능 순서, 첫 환생과 반복 주기 |
| `design/ROLLING.md` | Confirmed · Living | 무료 굴리기, 전역 일반 타워 풀, 특수 주사위와 스테이지 행운 |
| `design/TOWERS.md` | Confirmed · Living | 고정 타워 데이터, 보유 수량, 보호와 자동 편성 연동 |
| `design/STAT_TREE.md` | Confirmed · Living | 계정 영구 성장, 자동 기능, 자석·오프라인·텔레포터 |
| `design/REBIRTH.md` | Confirmed · Living | 짧은 반복 환생과 완만한 코인·행운 배율 |
| `design/TUTORIAL.md` | Confirmed · Living | 첫 굴리기, 코인 수집, 자동 기능과 지연 안내 |
| `design/FUSION.md` | Confirmed · Living | 중후반 합체와 영구 누적 진행 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 별도 고정 변종 타워와 해금 규칙 |

### 월드와 전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/WORLD_NAVIGATION.md` | Confirmed · Living | 로비, 선형 스테이지, 잠긴 문, 전환과 텔레포터 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 5개 지역·15개 지속형 스테이지, 경로와 생성 예산 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투, 역할, Engage와 스테이지 전환 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟, 이동, 행동 루틴과 전달 방식 조합 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 고유 능력, 사건 반응과 플레이어 조작 |
| `design/FORMATION.md` | Confirmed · Living | 전체·역할 슬롯, 자동 편성과 퀵 편성 HUD |
| `design/TARGETING.md` | Confirmed | 경로 진행도, 실제 거리와 예약 피해 타겟팅 |
| `design/MONSTERS.md` | Confirmed · Living | 몬스터 유형, 코인 드롭, 특수 행동과 변종 |

### 경제와 UI

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed · Living | 코인 드롭·수집, 문 구매, 오프라인 코인과 연금 정수 |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 효율과 시간 상한 |
| `design/POTIONS.md` | Confirmed · Living | 포션 상점, 효과, 지속시간과 중첩 |
| `design/UI_FLOW.md` | Confirmed · Living | HUD, 퀵 편성, 통합 인벤토리와 주요 메뉴 |

### 추가 전투 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/STAGE_BOSSES.md` | Draft | 플레이어별 개인 보스, 출현과 보상 |
| `design/LIVE_WAVE.md` | Draft | 로비에서 진입하는 서버 공동 전투와 기여 보상 |

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
spec/COMBAT.md
spec/TOWER_BEHAVIOR.md
spec/TOWER_EXTENSIONS.md
spec/FORMATION.md
spec/TARGETING.md
spec/MONSTERS.md
spec/CURRENCY.md
spec/OFFLINE_PROGRESS.md
spec/POTIONS.md
spec/UI_FLOW.md
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

다른 시스템의 기술 설계는 관련 게임 기획과 시스템 명세가 확정된 뒤 `technical/<SYSTEM>.md`에 작성합니다.

---

## 구현 명세

기술 설계가 확정된 뒤 `implementation/<SYSTEM>.md`에 실제 파일, 공개 타입, 함수, Remote, 저장 스키마와 테스트 대상을 기록합니다.

---

## 참조 문서 예정

| 예정 문서 | 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 타워 ID, 역할, 확률과 전투 데이터 |
| `reference/MONSTER_CATALOG.md` | 몬스터 ID, 생성 비용, 능력치와 태그 |
| `reference/STAGE_CATALOG.md` | 지역·스테이지, 문 가격, 코인·행운·생성 데이터 |
| `reference/TERMS.md` | 공통 용어와 명명 규칙 |

실제 카탈로그 데이터가 확정되기 전에는 빈 문서를 만들지 않습니다.

---

## 현재 우선순위

```text
1. 전체 진행·월드 이동·오프라인·UI의 남은 상위 질문 해결
2. 지역 1의 3개 스테이지와 초기 타워·몬스터 콘텐츠 구성
3. 핵심 루프 시스템 명세 작성
4. 기술 설계와 구현 명세 작성
5. 지역 1 수직 슬라이스 구현 및 밸런스 측정
```

먼저 명세화하기 적합한 시스템:

1. 전체 진행과 환생
2. 월드·스테이지 이동
3. 굴리기와 타워 보유
4. 재화와 오프라인 진행
5. 편성과 UI 흐름
6. 전투·타겟팅·타워 행동
