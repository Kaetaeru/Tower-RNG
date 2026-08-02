# 타워 카탈로그

- 계층: 참조 데이터
- 상태: **Active Template**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/RNG_PROBABILITY.md`, `../design/BALANCE_MODEL.md`, `../design/TOWERS.md`, `../design/COMBAT.md`, `../design/TOWER_BEHAVIOR.md`, `../design/TOWER_VARIANTS.md`
- 관련 문서: `MONSTER_CATALOG.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
- 마지막 정리: 2026-08-02

## 목적

실제 타워의 ID, 공식 기본 확률, 전투 예산, 역할, 행동과 제작 자산을 기록합니다.

첫 출시 일반 굴리기 타워는 최소 50종, 역할별 약 8~10종입니다. 변종과 합체 전용 타워는 별도 추가합니다.

---

## 타워 작성 양식

```markdown
## 표시 이름

- TowerId:
- 상태: Proposed | Confirmed | Implemented
- 획득 방식: 일반 굴리기 | 변종 판정 | 합체 | 이벤트 | 기타
- BaseOddsN: "10진수 문자열" | 없음
- 공식 기본 표시: 1 / N | 비굴리기
- ProbabilityTableVersion:
- CommonReserve 대상: 예 | 아니오
- 보조 등급:
- 주 역할:
- 보조 역할:
- FeedbackWeight: Micro | Standard | Heavy | Heroic

### 희귀도·전투 예산

- log10(BaseOddsN):
- RawPowerBudget:
- FinalPowerBudget:
- 동일 역할 희귀도 순위:
- 이전 타워 대비 최소 기여도 증가 검증:
- EquivalentContribution 기준값:
- 기준 전투 시나리오:

### 행동

- TargetPolicy:
- TargetLossPolicy:
- Movement:
- FacingPolicy:
- ActionRoutine:
- Delivery:
- DeliveryModifiers:
- ResourceProfile:
- Extensions:

### 기본 성능

- 기본 피해 또는 핵심 효과:
- 행동 주기:
- 대상 수:
- 역할별 기여 계산:
- 성능 강화 적용값:
- 치명타 적용 여부:
- 이동속도·교전거리:
- 큰 수 형식 사용 여부:

### 자동 편성

- 평가 기준:
- 동일 효과 중첩 규칙:
- 역할 슬롯 후보:
- 권장 타겟 정책:

### 타격감

- 준비 동작:
- 판정 순간:
- 공격자 반동:
- 대상 피격 반응:
- 효과·음향:
- 치명타 강화 표현:
- 카메라 흔들림: 없음 | 보스급 예외

### 제작 자산

- ModelKit:
- 주요 모션 견본:
- 효과·음향:
- 공격·효과 기준점:

### 성장과 수집

- 합체 결과:
- 합체 필요 수량:
- 변종 합체 규칙:
- 허용 변종 계열:
- 도감 설명:
- 제작 메모:
```

---

## 공식 확률 규칙

- 일반·변종 타워의 `BaseOddsN`은 10진수 문자열
- 공식 기본 확률만 UI에 표시
- 현재 행운 적용 확률은 카탈로그에 기록하지 않음
- 확률표 전체 합은 컴파일러가 임의 정밀도 유리수로 검증
- 신규 타워는 `CommonReserve`를 우선 사용
- 기존 중·고희귀 분모는 명시적 변경 없이는 유지

---

## 전투력 규칙

```text
RawPowerBudget(N) = (N / 10)^0.20
```

같은 역할 내 최종 예산:

```text
Final[i]
= max(Raw[i], Final[i-1] × 1.001)
```

점검:

- 분모가 큰 타워가 반드시 더 높은 기여도
- 정수 반올림 뒤에도 차이 유지
- 서로 다른 역할은 EquivalentContribution으로 비교
- 지원·제어를 표시 DPS만으로 평가하지 않음

---

## 출시 목표

| 역할 | 목표 수량 | Confirmed | Implemented |
|---|---:|---:|---:|
| 단일 화력 | 8~10 | 0 | 0 |
| 광역 화력 | 8~10 | 0 | 0 |
| 제어 | 8~10 | 0 | 0 |
| 마무리 | 8~10 | 0 | 0 |
| 지원 | 8~10 | 0 | 0 |
| 대형 사냥 | 8~10 | 0 | 0 |

복합 역할은 한 종류로만 계산합니다.

---

## 다양성 점검

- 이동 방식 분포
- 행동 루틴 분포
- 전달 방식 분포
- 실루엣 분포
- 피드백 무게 분포
- 단순 타워와 고유 확장 타워 비율
- 공식 분모 범위: 1/10부터 수십억·수조 이상
- 같은 역할의 희귀도별 단계가 비어 있지 않은가

---

## 현재 작성 상태

개별 타워는 아직 작성 전입니다. 확률과 수치를 정할 때 먼저 공식 분모·PowerBudget을 입력하고 역할별 기준 전투에서 검증합니다.