# 타워 카탈로그

- 계층: 참조 데이터
- 상태: **Active Template**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/TOWERS.md`, `../design/COMBAT.md`, `../design/TOWER_BEHAVIOR.md`, `../design/TOWER_VARIANTS.md`
- 관련 문서: `MONSTER_CATALOG.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
- 마지막 정리: 2026-08-02

## 목적

이 문서는 실제 타워 종류와 수치를 한곳에 기록하는 카탈로그입니다. 타워 시스템의 공통 규칙은 기획 문서에서 관리하고, 개별 타워의 이름·확률·역할·행동·수치는 이 문서에서 관리합니다.

첫 출시 일반 굴리기 타워는 최소 50종을 목표로 하며 여섯 역할마다 약 8~10종을 준비합니다. 변종과 합체 전용 타워는 이 목표에 추가됩니다.

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
- FeedbackWeight: Light | Normal | Heavy | Finisher

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

### 타격감

- 준비 동작:
- 판정 순간:
- 공격자 반동:
- 대상 피격 반응:
- 효과·음향:
- 치명타 강화 표현:

### 제작 자산

- ModelKit:
- 주요 모션 견본:
- 효과·음향:
- 공격·효과 기준점:

### 성장과 수집

- 합체 결과:
- 허용 변종 계열:
- 도감 설명:
- 제작 메모:
```

---

## 출시 목표

| 역할 | 목표 수량 | 현재 Confirmed | 현재 Implemented |
|---|---:|---:|---:|
| 단일 화력 | 8~10 | 0 | 0 |
| 광역 화력 | 8~10 | 0 | 0 |
| 제어 | 8~10 | 0 | 0 |
| 마무리 | 8~10 | 0 | 0 |
| 지원 | 8~10 | 0 | 0 |
| 대형 사냥 | 8~10 | 0 | 0 |

```text
일반 굴리기 타워 최소 50종
복합 역할 타워는 한 종류로만 계산
변종·합체 전용 타워는 별도 추가
```

---

## 다양성 점검

출시 목록을 작성할 때 다음 분포를 함께 확인합니다.

- Formation·Engage·ChargeThrough·Orbit 등 이동 방식
- Impact·Sequence·Burst·Channel·Summon 등 행동 루틴
- Contact·Projectile·Beam·Area 등 전달 방식
- 인간형·기계·생물·추상 오브젝트 실루엣
- 가벼운 연속 공격·보통 공격·강공격·결정타 피드백
- 단순 행동 타워와 고유 확장 타워

역할 수량을 채우기 위해 수치와 색만 바꾼 타워를 반복하지 않습니다.

---

## 현재 작성 상태

아직 개별 타워를 확정하지 않았습니다. 사용자가 이 양식에 따라 순차적으로 작성합니다.
