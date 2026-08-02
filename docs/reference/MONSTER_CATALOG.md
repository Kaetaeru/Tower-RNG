# 몬스터 카탈로그

- 계층: 참조 데이터
- 상태: **Active Template**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/BALANCE_MODEL.md`, `../design/MONSTERS.md`, `../design/LEVEL_DESIGN.md`, `../design/STAGE_BOSSES.md`
- 관련 문서: `TOWER_CATALOG.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
- 마지막 정리: 2026-08-02

## 목적

실제 몬스터와 보스의 기준 능력치, 상대 위협도 `SpawnCost`, 특수 행동과 보상 보정을 기록합니다.

원시 HP는 스테이지 `StageScale`로 증가하지만 `SpawnCost`는 같은 스테이지 안에서의 상대 위협도입니다.

---

## 공통 기준

```text
표준 일반형
- ArchetypeBaseHP: 5
- StandardTimeToBase: 스테이지 지정
- StandardBaseDamage: 스테이지 지정 기준
- SpawnCost: 10
```

최종 HP:

```text
ArchetypeBaseHP
× StageScale
× WaveStatModifier
× VariantModifier
× BossModifier
```

---

## 일반 몬스터 작성 양식

```markdown
## 표시 이름

- MonsterId:
- 상태: Proposed | Confirmed | Implemented
- 등장 지역:
- 유형: 일반형 | 군집형 | 고체력형 | 고속형 | 지원형 | 보호형 | 분열형 | 기타
- SpawnCost:
- 변종 가능 여부:

### 스테이지 1 기준 성능

- ArchetypeBaseHP:
- 목표 이동시간 보정:
- 기준 베이스 피해 배율:
- WaveStatModifier 기본값:
- 큰 수 형식 사용 여부:

### 위협도 산정

- EffectiveHP 구성:
- DurabilityRatio:
- SpeedPressure:
- BaseThreat:
- SpecialThreatFactor:
- RawSpawnCost:
- 최종 SpawnCost 반올림 근거:
- 기준 편성 처리시간:

### 특수 행동

- 행동 설명:
- 발동 조건·주기:
- 회복 최대량:
- 보호막 최대량:
- 분열 횟수·자식 재분열 가능 여부:
- 상태 효과 상호작용:
- 무한 정체 방지 제한:

### 보상

- CoinRewardModifier:
- DefenseXPModifier:
- AlchemyModifier:
- 변종 보상 예외:

### 제작 자산

- ModelKit:
- 주요 모션:
- 피격·사망 반응:
- 효과·음향:

### 배치 메모

- 적합 웨이브:
- 함께 배치하기 좋은 몬스터:
- 강조 역할:
```

---

## 보스 작성 양식

```markdown
## 보스 표시 이름

- BossId:
- 상태: Proposed | Confirmed | Implemented
- 지역·전용 스테이지:
- 보스 계열: 초·중반 | 지역 최종
- SpawnCost:
- BudgetRatio:
- MinCount: 1
- MaxCount:

### 기준 성능

- ArchetypeBaseHP:
- BossModifier:
- 목표 이동시간:
- 베이스 도달 피해:
- 제어 감소:
- 큰 수 형식 사용 여부:

### 위협도

- EffectiveHP:
- SpecialThreatFactor:
- 기준 편성 처리시간:
- 일반 웨이브 대비 목표 시간:

### 행동

- 기본 행동:
- 체력 구간 변화:
- 지원·보호·분열 제한:
- 상태 효과 규칙:

### 보상

- CoinRewardModifier:
- DefenseXPModifier:
- 연금 정수 보너스:
- 코인 묶음 표현:

### 연출

- 등장:
- 피격:
- 처치:
- 제한된 카메라 연출:

### 제작 자산

- ModelKit:
- 주요 모션:
- 효과·음향:
```

---

## SpawnCost 공식

```text
RawSpawnCost
= 10
× (EffectiveHP / StandardEffectiveHP)^0.75
× (StandardTimeToBase / TimeToBase)^0.60
× (BaseDamage / StandardBaseDamage)^0.20
× SpecialThreatFactor
```

제작용 단계:

```text
2, 3, 5, 8, 10, 15, 20, 30, 40,
50, 75, 100, 150, 200, 300...
```

최종 비용은 타워 기준 편성 시뮬레이션으로 검증합니다.

---

## 제작 점검

- [ ] StageScale을 SpawnCost에 중복 반영하지 않았는가
- [ ] EffectiveHP에 보호막·회복·분열이 포함되는가
- [ ] 회복·보호막·분열에 유한 상한이 있는가
- [ ] SpawnCost와 실제 처리시간이 비슷한가
- [ ] 베이스 도달 시 코인·Defense XP가 없는가
- [ ] 높은 위협에 더 큰 보상이 있는가
- [ ] 일반 피격에 화면 흔들림을 사용하지 않는가
- [ ] 강제 원소 상성·완전 면역이 없는가

---

## 현재 작성 상태

개별 몬스터와 보스는 아직 작성 전입니다. 지역 1의 표준 일반형부터 작성해 나머지 유형과 비용의 기준점으로 사용합니다.