# 몬스터 카탈로그

- 계층: 참조 데이터
- 상태: **Active Catalog**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/BALANCE_MODEL.md`, `../design/MONSTERS.md`, `../design/LEVEL_DESIGN.md`, `../design/STAGE_BOSSES.md`
- 관련 문서: `TOWER_CATALOG.md`, `TOWER_BALANCE_BENCHMARK.md`, `STAGE1_WAVE_BENCHMARK.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
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
- 상태: Proposed | Confirmed (Provisional Balance) | Confirmed | Implemented
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

# 지역 1 기준 일반 몬스터

아래 세 몬스터는 스테이지 1 일반 웨이브 1~4를 검증하기 위한 첫 기준 세트입니다. 이름과 역할은 확정하고, 세부 수치는 Roblox 런타임 전투 전까지 임시 밸런스 값으로 취급합니다.

## 초원 슬라임

- MonsterId: `MON_PRAIRIE_SLIME`
- 상태: **Confirmed (Provisional Balance)**
- 등장 지역: 지역 1 초원·숲
- 유형: 일반형
- SpawnCost: 10
- 변종 가능 여부: 예

### 스테이지 1 기준 성능

- ArchetypeBaseHP: 5
- 목표 이동시간 보정: 1.00, 기준 10.0초
- 기준 베이스 피해 배율: 1.00, 베이스 피해 1
- WaveStatModifier 기본값: 1.00
- 큰 수 형식 사용 여부: StageScale 적용 이후 공통 큰 수 모듈

### 위협도 산정

- EffectiveHP 구성: 기본 HP 5
- DurabilityRatio: 1.00
- SpeedPressure: 1.00
- BaseThreat: 1.00
- SpecialThreatFactor: 1.00
- RawSpawnCost: 10.00
- 최종 SpawnCost 반올림 근거: 표준 일반형 기준값
- 기준 편성 처리시간: 웨이브 1의 여섯 마리 평균 약 9.98초

### 특수 행동

- 행동 설명: 없음
- 발동 조건·주기: 없음
- 회복 최대량: 0
- 보호막 최대량: 0
- 분열 횟수·자식 재분열 가능 여부: 분열 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 특수 지속 행동 없음

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00
- 변종 보상 예외: 변종 카탈로그에서 별도 정의

스테이지 1 기준:

```text
기본 CoinValue = 10 × StageCoinUnit
기본 Defense XP = 10
```

### 제작 자산

- ModelKit: `PrairieSlime`
- 주요 모션: `SquashMove`, `HitCompress`, `PopDeath`
- 피격·사망 반응: 피격 방향으로 눌렸다 복원, 처치 시 부풀었다 터짐
- 효과·음향: 젤리 탄성음, 작은 점액 파편

### 배치 메모

- 적합 웨이브: 기본 소개, 혼합 웨이브
- 함께 배치하기 좋은 몬스터: 들쥐, 어린 멧돼지
- 강조 역할: 특정 역할 강제 없음

---

## 들쥐

- MonsterId: `MON_FIELD_RAT`
- 상태: **Confirmed (Provisional Balance)**
- 등장 지역: 지역 1 초원·숲
- 유형: 군집형
- SpawnCost: 5
- 변종 가능 여부: 예

### 스테이지 1 기준 성능

- ArchetypeBaseHP: 2
- 목표 이동시간 보정: 0.85, 기준 8.5초
- 기준 베이스 피해 배율: 1.00, 베이스 피해 1
- WaveStatModifier 기본값: 1.00
- 큰 수 형식 사용 여부: StageScale 적용 이후 공통 큰 수 모듈

### 위협도 산정

- EffectiveHP 구성: 기본 HP 2
- DurabilityRatio: 0.40
- SpeedPressure: 약 1.176
- BaseThreat: 1.00
- SpecialThreatFactor: 1.00
- RawSpawnCost: 약 5.54
- 최종 SpawnCost 반올림 근거: 군집형 제작 단계 5로 반올림
- 기준 편성 처리시간: 웨이브 2의 열다섯 마리 평균 약 9.85초

### 특수 행동

- 행동 설명: 개별 능력은 없으며 낮은 비용과 짧은 생성 간격으로 군집 압박
- 발동 조건·주기: 없음
- 회복 최대량: 0
- 보호막 최대량: 0
- 분열 횟수·자식 재분열 가능 여부: 분열 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 개체 수는 웨이브 `MaxCount`로 제한

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00
- 변종 보상 예외: 변종 카탈로그에서 별도 정의

스테이지 1 기준:

```text
기본 CoinValue = 5 × StageCoinUnit
기본 Defense XP = 5
```

### 제작 자산

- ModelKit: `FieldRat`
- 주요 모션: `Scurry`, `Flinch`, `TumbleDeath`
- 피격·사망 반응: 빠른 옆틀기, 처치 시 짧게 굴러 사라짐
- 효과·음향: 가벼운 발소리, 짧은 찍 소리, 작은 먼지

### 배치 메모

- 적합 웨이브: 군집 소개, 고체력 몬스터 사이의 빈 공간 채우기
- 함께 배치하기 좋은 몬스터: 초원 슬라임, 어린 멧돼지
- 강조 역할: 광역 화력 효율이 높지만 다른 역할도 처리 가능

---

## 어린 멧돼지

- MonsterId: `MON_YOUNG_BOAR`
- 상태: **Confirmed (Provisional Balance)**
- 등장 지역: 지역 1 초원·숲
- 유형: 고체력형
- SpawnCost: 20
- 변종 가능 여부: 예

### 스테이지 1 기준 성능

- ArchetypeBaseHP: 12
- 목표 이동시간 보정: 1.20, 기준 12.0초
- 기준 베이스 피해 배율: 2.00, 베이스 피해 2
- WaveStatModifier 기본값: 1.00
- 큰 수 형식 사용 여부: StageScale 적용 이후 공통 큰 수 모듈

### 위협도 산정

- EffectiveHP 구성: 기본 HP 12
- DurabilityRatio: 2.40
- SpeedPressure: 약 0.833
- BaseThreat: 2.00
- SpecialThreatFactor: 1.00
- RawSpawnCost: 약 19.85
- 최종 SpawnCost 반올림 근거: 고체력형 제작 단계 20으로 반올림
- 기준 편성 처리시간: 혼합 웨이브 3·4에서 전체 평균 약 9.97~10.48초

### 특수 행동

- 행동 설명: 특수 능력 없이 높은 HP와 베이스 피해로 압박
- 발동 조건·주기: 없음
- 회복 최대량: 0
- 보호막 최대량: 0
- 분열 횟수·자식 재분열 가능 여부: 분열 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 목표 이동시간 12초로 자연 해소

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00
- 변종 보상 예외: 변종 카탈로그에서 별도 정의

스테이지 1 기준:

```text
기본 CoinValue = 20 × StageCoinUnit
기본 Defense XP = 20
```

### 제작 자산

- ModelKit: `YoungBoar`
- 주요 모션: `Trot`, `HeavyFlinch`, `RollOverDeath`
- 피격·사망 반응: 몸통 전체가 짧게 밀리고, 처치 시 옆으로 구르며 쓰러짐
- 효과·음향: 무거운 발굽음, 낮은 울음, 흙먼지

### 배치 메모

- 적합 웨이브: 첫 고체력 소개, 혼합, 보스 전 압박
- 함께 배치하기 좋은 몬스터: 들쥐와 초원 슬라임
- 강조 역할: 지속 단일 화력과 마무리 효율, 대형 사냥 보너스는 적용하지 않음

---

## 기준 세트 검증

| 몬스터 | SpawnCost | RawSpawnCost | 기준 역할 |
|---|---:|---:|---|
| 초원 슬라임 | 10 | 10.00 | 표준 일반형 |
| 들쥐 | 5 | 약 5.54 | 군집형 |
| 어린 멧돼지 | 20 | 약 19.85 | 고체력형 |

`stage1_wave_sim.py`의 15개 혼합 편성 검증에서 이 세 몬스터로 구성한 웨이브 1~4는 모두 베이스 누수 없이 평균 10.07초에 해소되었습니다.

---

## 제작 점검

- [x] StageScale을 SpawnCost에 중복 반영하지 않았는가
- [x] EffectiveHP에 보호막·회복·분열이 포함되는가
- [x] 회복·보호막·분열에 유한 상한이 있는가
- [x] SpawnCost와 실제 처리시간이 비슷한가
- [x] 베이스 도달 시 코인·Defense XP가 없는가
- [x] 높은 위협에 더 큰 보상이 있는가
- [x] 일반 피격에 화면 흔들림을 사용하지 않는가
- [x] 강제 원소 상성·완전 면역이 없는가

---

## 현재 작성 상태

지역 1 스테이지 1의 기준 일반 몬스터 3종을 등록했습니다.

```text
일반형: 초원 슬라임
군집형: 들쥐
고체력형: 어린 멧돼지
```

다음 몬스터 작업은 스테이지 1 보스와 보스 웨이브 동반 구성을 작성하는 것입니다.
