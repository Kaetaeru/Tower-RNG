# 몬스터 카탈로그

- 계층: 참조 데이터
- 상태: **Active Catalog**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/BALANCE_MODEL.md`, `../design/MONSTERS.md`, `../design/LEVEL_DESIGN.md`, `../design/STAGE_BOSSES.md`, `../design/WAVE_PACING.md`
- 관련 문서: `TOWER_CATALOG.md`, `TOWER_BALANCE_BENCHMARK.md`, `STAGE1_WAVE_BENCHMARK.md`, `FIRST_REBIRTH_ECONOMY_BENCHMARK.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
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
- 상태: Proposed | Confirmed (Provisional Balance) | Confirmed | Implemented
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
- RawSpawnCost:
- 최종 SpawnCost 근거:
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

공식은 시작점이며 최종 비용은 실제 기준 편성 처리시간과 보상 비율을 함께 검증합니다.

---

# 지역 1 기준 일반 몬스터

아래 세 몬스터는 스테이지 1 일반 웨이브의 기준 세트입니다. 이름과 역할은 확정하고, 세부 수치는 Roblox 런타임 전까지 임시 밸런스 값으로 취급합니다.

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
- 기준 편성 처리시간: 웨이브 1 평균 9.98초

### 특수 행동

- 행동 설명: 없음
- 회복·보호막·분열: 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 특수 지속 행동 없음

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00

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

- 적합 웨이브: 최초 준비 전투, 기본 소개, 혼합 웨이브
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
- 기준 편성 처리시간: 웨이브 2 평균 9.85초

### 특수 행동

- 행동 설명: 낮은 비용과 짧은 생성 간격으로 군집 압박
- 회복·보호막·분열: 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 웨이브 `MaxCount` 적용

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00

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

- 적합 웨이브: 군집 소개, 큰 적 사이의 빈 공간 채우기
- 함께 배치하기 좋은 몬스터: 초원 슬라임, 어린 멧돼지, 우두머리 멧돼지
- 강조 역할: 광역 화력에 효율적이지만 다른 역할도 처리 가능

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
- 기준 편성 처리시간: 혼합 웨이브 3·4 평균 9.97~10.48초

### 특수 행동

- 행동 설명: 특수 능력 없이 높은 HP와 베이스 피해로 압박
- 회복·보호막·분열: 없음
- 상태 효과 상호작용: 공통 규칙 적용
- 무한 정체 방지 제한: 목표 이동시간 12초로 자연 해소

### 보상

- CoinRewardModifier: 1.00
- DefenseXPModifier: 1.00
- AlchemyModifier: 1.00

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

# 지역 1 스테이지 1 보스

## 우두머리 멧돼지

- BossId: `BOSS_PRAIRIE_BOAR_ALPHA`
- 상태: **Confirmed (Provisional Balance)**
- 지역·전용 스테이지: 지역 1, 스테이지 1
- 보스 계열: 초·중반 기본형
- SpawnCost: 100
- BudgetRatio: 웨이브 5 BaseBudget의 90.91%
- MinCount: 1
- MaxCount: 1

### 기준 성능

- ArchetypeBaseHP: 55
- BossModifier: 1.00, HP에 이미 반영
- 목표 이동시간: 22.0초
- 베이스 도달 피해: 5
- 제어 감소: 없음, 첫 보스 기준
- 큰 수 형식 사용 여부: StageScale 적용 이후 공통 큰 수 모듈

### 위협도

- EffectiveHP: 55
- DurabilityRatio: 11.00
- SpeedPressure: 약 0.455
- BaseThreat: 5.00
- SpecialThreatFactor: 보스 집중 압박과 5웨이브 절정 보정을 포함해 시뮬레이션 검증
- 공식 원시값만으로는 약 52 이상이며 보스 보정에 따라 75 전후
- 최종 SpawnCost 근거: 15개 기준 편성에서 평균 16초의 보스 웨이브와 대형 사냥 역할 기여를 만족하도록 100으로 설정
- 기준 편성 처리시간: 동반 들쥐 2마리 포함 평균 16.00초, 최장 20.00초
- 누수: 15개 편성 모두 0

`SpawnCost 100`은 단순 공식 반올림만으로 확정한 값이 아니라 보스 주기의 실제 처리시간과 베이스 위험을 함께 반영한 잠정값입니다. 보상 프리미엄은 SpawnCost와 분리된 RewardModifier로 관리합니다.

### 행동

- 기본 행동: 무겁게 경로를 전진하는 단순 기준 보스
- 체력 구간 변화: 50% 이하에서 호흡, 발굽 먼지와 울음 연출 강화. 수치 변화 없음
- 지원·보호·분열 제한: 회복, 보호막, 분열 없음
- 상태 효과 규칙: 일반 상태 효과 적용. 완전 면역 없음
- 무한 정체 방지 제한: 22초의 자연 도달시간, 회복 없음

첫 보스는 복잡한 기믹보다 보스 체력과 대형 사냥 역할의 가치를 읽게 하는 기준점으로 사용합니다.

### 보상

- CoinRewardModifier: **1.15**
- DefenseXPModifier: **1.15**
- 연금 정수 보너스: 미정
- 코인 묶음 표현: 일반 적보다 큰 물리 코인 묶음을 분출

```text
기본 CoinValue = 100 × StageCoinUnit × 1.15 = 115
기본 Defense XP = 100 × 1.15 = 115
```

웨이브 5의 들쥐 2마리를 합치면 생성 SpawnCost는 110, 코인·Defense XP 가치는 125입니다.

### 연출

- 등장: 길 입구의 풀과 흙먼지가 크게 갈라지고 우두머리가 짧게 포효
- 피격: 일반 몬스터보다 무거운 몸통 반동과 낮은 충격음
- 처치: 앞다리가 꺾이고 몸통이 옆으로 크게 구른 뒤 코인 묶음 분출
- 제한된 카메라 연출: 등장과 처치에만 `Low` 흔들림 허용, 설정에서 Off 가능

### 제작 자산

- ModelKit: `PrairieBoarAlpha`
- 주요 모션: `HeavyTrot`, `Roar`, `HeavyFlinch`, `CollapseRoll`
- 효과·음향: 발굽 먼지, 낮은 포효, 무거운 명중음, 큰 코인 분출

---

## 기준 세트 검증

| 몬스터 | SpawnCost | 기준 역할 | 검증 결과 |
|---|---:|---|---|
| 초원 슬라임 | 10 | 표준 일반형 | 웨이브 1 평균 9.98초 |
| 들쥐 | 5 | 군집형 | 웨이브 2 평균 9.85초 |
| 어린 멧돼지 | 20 | 고체력형 | 웨이브 3~4 평균 9.97~10.48초 |
| 우두머리 멧돼지 | 100 | 초·중반 기준 보스 | 웨이브 5 평균 16.00초 |

전체 5웨이브는 15개 혼합 편성에서 평균 56.28초, 누수 0으로 검증되었습니다.

```text
전체 생성 SpawnCost: 385
전체 코인·Defense XP 가치: 400
보스 시간 비중: 약 28.4%
```

---

## 제작 점검

- [x] StageScale을 SpawnCost에 중복 반영하지 않았는가
- [x] EffectiveHP에 보호막·회복·분열이 포함되는가
- [x] 회복·보호막·분열에 유한 상한이 있는가
- [x] SpawnCost와 실제 처리시간을 함께 검증했는가
- [x] 베이스 도달 시 코인·Defense XP가 없는가
- [x] 높은 위협에 더 큰 보상이 있는가
- [x] 일반 피격에 화면 흔들림을 사용하지 않는가
- [x] 보스 화면 흔들림이 설정 가능한 제한 연출인가
- [x] 강제 원소 상성·완전 면역이 없는가

---

## 현재 작성 상태

지역 1 스테이지 1의 일반 몬스터 3종과 기준 보스 1종을 등록했습니다.

```text
일반형: 초원 슬라임
군집형: 들쥐
고체력형: 어린 멧돼지
보스: 우두머리 멧돼지
```

다음 몬스터 작업은 스테이지 2의 실제 몬스터·웨이브를 작성해 현재 경제 프록시를 교체하는 것입니다.
