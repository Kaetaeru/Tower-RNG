# Tower RNG 문서 인덱스

- 상태: Active
- 필수 참고: `../AGENTS.md`
- 마지막 정리: 2026-08-02

## 문서 사용 순서

모든 기획·설계·구현 작업은 다음 순서로 문서를 확인합니다.

```text
AGENTS.md
    ↓
docs/INDEX.md
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

문서 또는 코드 사이에 충돌이 있거나 새로운 결정이 필요하면 임의로 선택하지 않고 사용자에게 질문합니다.

---

## 프로젝트 진입 문서

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 게임 전체 개요, 핵심 루프와 문서 링크 |
| `../AGENTS.md` | Required | 문서 작성, 승인, 설계와 구현의 최우선 규칙 |
| `INDEX.md` | Active | 문서 위치, 상태와 읽기 순서 |

---

## 게임 기획 문서

### 핵심 루프

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/ROLLING.md` | Confirmed | 무료 굴리기, 실제 확률, 특수 주사위와 카운터 |
| `design/TOWERS.md` | Confirmed | 타워 고정 데이터, 보유 수량, 보호와 도감 |
| `design/FUSION.md` | Confirmed | 중복 타워 합체, 고정 결과와 합체 누적 진행 |
| `design/TOWER_VARIANTS.md` | Confirmed | 변종 타워 해금, 고정 개체와 획득 가치 |
| `design/STAT_TREE.md` | Draft | 공통 스탯, 편성 성장과 시스템 해금 |

### 전투와 편성

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/COMBAT.md` | Confirmed | 자동 전투, 역할, 전투 스탯과 상태 효과 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟, 이동, 행동 루틴, 전달 방식과 Engage 타이밍의 조합 규칙 |
| `design/FORMATION.md` | Confirmed | 추종 편대, 전체·역할 슬롯과 편성 UI |
| `design/TARGETING.md` | Confirmed | 타겟 우선순위, 경로 진행도와 실제 거리 판정 |
| `design/MONSTERS.md` | Confirmed | 몬스터 능력치, 이동, 도달 피해와 변종 몬스터 |
| `design/LEVEL_DESIGN.md` | Confirmed | 지속형 스테이지, 경로, 생성 예산과 베이스 |

### 경제와 소비품

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed | 일반 성장 재화, 연금 정수, 획득과 소비 |
| `design/POTIONS.md` | Confirmed | 포션 상점, 효과, 지속시간과 중첩 규칙 |

### 추가 전투 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/STAGE_BOSSES.md` | Draft | 플레이어별 개인 보스, 출현과 보상 |
| `design/LIVE_WAVE.md` | Draft | 실제 시간 기반 서버 공동 전투와 기여 보상 |

---

## 시스템 명세

아직 작성 전입니다. 기획 규칙이 충분히 확정된 시스템부터 다음 경로에 작성합니다.

```text
spec/ROLLING.md
spec/TOWERS.md
spec/FUSION.md
spec/TOWER_VARIANTS.md
spec/STAT_TREE.md
spec/COMBAT.md
spec/TOWER_BEHAVIOR.md
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
| `technical/TOWER_MODELING.md` | Confirmed · Living | Basic 3D 모델, 자유 이름 모션, 이름·경로 대응과 전체 시각 상태 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 이동, 타겟, 행동 루틴, 전달, 생성물과 자원 프로필의 제작 양식 |

두 문서는 함께 읽습니다.

```text
TOWER_MODELING.md
- 3D 모델과 모션 견본을 어떻게 만드는가

TOWER_BEHAVIOR_GRAMMAR.md
- 제작한 모션을 이동·공격 함수와 어떻게 조합하는가
```

다른 시스템의 기술 설계는 시스템 명세가 확정된 뒤 다음 경로에 작성합니다.

```text
technical/<SYSTEM>.md
```

기술 설계는 다음을 담당합니다.

- 서버와 클라이언트 책임
- 상태 소유권과 데이터 흐름
- 저장과 복구
- 네트워크
- 성능
- 보안과 악용 방지
- 시스템 간 의존 관계

---

## 구현 명세

아직 작성 전입니다. 기술 설계가 확정된 뒤 다음 경로에 작성합니다.

```text
implementation/<SYSTEM>.md
```

구현 명세는 실제 파일 경로, 공개 타입, 공개 함수, Remote 계약, 저장 스키마와 테스트 대상을 담당합니다.

---

## 참조 문서 예정

반복되는 데이터 표와 공통 용어는 기획 문서에 중복하지 않고 다음 경로로 분리합니다.

| 예정 문서 | 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 타워 ID, 역할, 확률과 전투 데이터 표 |
| `reference/MONSTER_CATALOG.md` | 몬스터 ID, 생성 비용, 능력치와 태그 표 |
| `reference/TERMS.md` | 공통 용어와 명명 규칙 |

실제 카탈로그 데이터가 확정되기 전에는 빈 문서를 만들지 않습니다.

---

## 주요 결정 기록 예정

여러 시스템에 장기적으로 영향을 주는 결정만 `decisions/`에 ADR로 기록합니다.

후보:

- 추종형 타워 전투
- 일반 스테이지 공격 사거리 제거
- PathProgress와 WorldPosition 이중 판정
- 회복형 베이스와 과부하 복구
- Engage 이동 시간이 실제 공격 타이밍에 영향을 주는 구조

ADR 작성 전에는 결정의 범위와 필요성을 사용자에게 확인합니다.

---

## 현재 우선순위

```text
1. Confirmed Living 문서의 미확정 세부 계약 해결
2. 핵심 루프 시스템 명세 작성
3. 기술 설계 보완
4. 구현 명세 작성
5. 실제 코드 구현 및 검증
```

우선 명세화하기 적합한 시스템:

1. 굴리기
2. 타워 보유
3. 합체
4. 편성
5. 타겟팅
6. 타워 행동
7. 재화

개인 보스, 라이브 웨이브와 전체 스탯 트리는 사용자 승인이 필요한 세부 결정이 남아 있으므로 먼저 질문하고 확정합니다.
