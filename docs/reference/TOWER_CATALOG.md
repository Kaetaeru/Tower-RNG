# 타워 카탈로그

- 계층: 참조 데이터
- 상태: **Active Template**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/TOWERS.md`, `../design/COMBAT.md`, `../design/TOWER_BEHAVIOR.md`
- 관련 문서: `MONSTER_CATALOG.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
- 마지막 정리: 2026-08-02

## 목적

이 문서는 실제 타워 종류와 수치를 한곳에 기록하는 카탈로그입니다. 타워 시스템의 공통 규칙은 기획 문서에서 관리하고, 개별 타워의 이름·확률·역할·행동·수치는 이 문서에서 관리합니다.

새 타워를 추가할 때 공통 규칙을 반복해서 적지 않습니다. 기존 행동 문법으로 표현할 수 없는 기능이 필요하면 먼저 상위 기획과 기술 문서를 갱신합니다.

---

## 타워 작성 양식

```markdown
## 표시 이름

- TowerId:
- 상태: Proposed | Confirmed | Implemented
- 보조 등급:
- 실제 획득 확률: 1 / N
- 획득 방식: 일반 굴리기 | 변종 굴리기 | 합체 | 이벤트 | 기타
- 주 역할:
- 보조 역할:
- 자동 편성 평가 등급:

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
- 성능 강화 적용값:
- 치명타 적용 여부:
- 이동속도·교전거리:

### 제작 자산

- ModelKit:
- 주요 모션 견본:
- 효과·음향:
- 공격·효과 기준점:

### 성장과 수집

- 합체 결과:
- 변종 관계:
- 도감 설명:
- 제작 메모:
```

---

## 출시 타워 목록

아직 개별 타워를 확정하지 않았습니다. 역할별 대표 타워, 실제 확률과 수치는 사용자가 이 문서의 양식에 따라 순차적으로 작성합니다.

### 역할별 최소 검토 항목

- 단일 화력
- 광역 화력
- 제어
- 마무리
- 지원
- 대형 사냥

각 역할에 여러 행동 형태가 들어갈 수 있으며 역할과 행동 문법을 같은 것으로 취급하지 않습니다.
