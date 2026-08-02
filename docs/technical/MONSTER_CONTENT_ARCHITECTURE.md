# 몬스터 콘텐츠 확장 구조

- 계층: 기술 구조
- 상태: **Confirmed Architecture**
- 관련 카탈로그: `../catalog/MONSTER_CATALOG.md`, `../catalog/STAGE_CATALOG.md`
- 상위 기획: `../design/MONSTERS.md`, `../design/LEVEL_DESIGN.md`
- 마지막 정리: 2026-08-03

## 목적

몬스터의 전투 정체성, 스테이지 수치, 행동과 시각 자산을 분리합니다.

```text
MonsterId
→ StageMonsterProfileId
→ BehaviorSetId
→ VisualProfileId
```

모델 제작이 어렵거나 더 적합한 에셋을 발견하면 `VisualProfileId`만 교체합니다. 전투 수치와 웨이브를 바꾸지 않는 시각 교체는 밸런스 재검증을 요구하지 않습니다.

---

# 1. 안정 ID

## MonsterId

몬스터의 게임플레이 정체성을 나타냅니다.

소유 정보:

- 표시 이름
- 지역과 기본 유형
- 기본 태그
- 보상 계열
- 허용 행동 집합
- 도감 항목

`MonsterId`는 모델 파일명이나 Roblox AssetId를 포함하지 않습니다.

## StageMonsterProfileId

같은 몬스터가 여러 스테이지에서 강화될 때 사용하는 수치 프로필입니다.

```text
StageMonsterProfileId
MonsterId
StageId
HPFactor
TimeToBaseSeconds
SpawnCost
BaseDamage
BehaviorParameters
RewardModifier
```

최종 HP:

```text
HP = HPFactor × StageScale(StageId)
```

같은 `MonsterId`라도 스테이지별 보호막 비율이나 행동 강도가 달라질 수 있습니다.

## BehaviorSetId

행동을 조합형 데이터로 정의합니다. 특정 모델의 뼈나 애니메이션 길이가 판정 원인이 되지 않습니다.

V1 행동 구성요소:

```text
Shield
PhaseShield
SplitOnDeath
DeathRemnant
RouteDash
LowHpFrenzy
PhaseHeal
ShortUntargetableStep
BurrowStep
ShellBreakDelay
ExposedCore
Eruption
```

행동 판정은 서버 시간이 기준입니다. 애니메이션과 VFX는 판정 결과를 표현합니다.

## VisualProfileId

다음 시각 자산을 묶습니다.

```text
ModelAssetId
RigProfileId
AnimationProfileId
MaterialProfileId
VfxProfileId
SfxProfileId
DisplayScale
CollisionProfileId
```

`VisualProfileId`는 교체 가능한 참조입니다. 도감 초상화와 UI 아이콘도 별도 참조를 사용할 수 있습니다.

---

# 2. 모델 독립 규칙

- 경로 이동은 `MonsterRoot`의 서버 위치로 처리합니다.
- 애니메이션 Root Motion으로 실제 진행도를 바꾸지 않습니다.
- 피격 판정은 모델 메시가 아니라 공통 충돌 캡슐을 사용합니다.
- 모델 크기는 `DisplayScale`과 `CollisionProfileId`로 조정합니다.
- 행동 코드는 특정 Bone·Motor6D 이름을 직접 찾지 않습니다.
- 선택 애니메이션이 없으면 공통 이동·피격·사망 표현으로 대체합니다.
- 모델 교체 뒤에도 `PathProgress`, 체력, 보호막과 상태 효과가 유지되어야 합니다.

---

# 3. 시각 복잡도 단계

## Simple

- 단일 메시 또는 2~4파트
- 공통 흔들림·회전·스케일 애니메이션
- 군집형·잔여물·작은 정령에 사용

## Standard

- 단순 리그 또는 4족 보행 리그
- 이동·피격·사망 3개 필수 모션
- 일반 몬스터 대부분에 사용

## Complex

- 보스·대형 거수
- 단계 전환과 전용 효과 지원
- 모델 제작 난도가 높으면 Standard 리그와 대형 VFX로 대체 가능

복잡도는 전투력을 나타내지 않습니다.

---

# 4. 시각 대체 규칙

모델링이 어려운 경우 다음 순서로 대체합니다.

```text
동일 VisualFamily의 다른 모델
→ 단순 리그 + 재질·크기·VFX 변형
→ 공통 원형·4족·골렘 프로토타입
```

시각 교체로 바꿀 수 있는 항목:

- 모델과 리그
- 애니메이션
- 재질과 크기
- VFX·SFX
- 표시 이름과 설명 문구

시각 교체로 바꾸면 안 되는 항목:

- `MonsterId`
- `StageMonsterProfileId`
- HP·이동시간·SpawnCost·BaseDamage
- 행동 발동 조건과 수치
- 웨이브 구성과 보상

전투 정체성까지 바꿀 필요가 있으면 새 `MonsterId` 또는 새 프로필 버전을 만들고 관련 스테이지를 다시 검증합니다.

---

# 5. 필수 시각 능력

모든 VisualProfile은 최소 다음 이벤트를 처리합니다.

```text
OnSpawn
OnMove
OnHit
OnDeath
OnLeak
```

선택 이벤트:

```text
OnShieldCreated
OnShieldBroken
OnHeal
OnDash
OnSplit
OnBurrow
OnExposed
OnEruption
OnPhaseChanged
```

선택 이벤트용 전용 애니메이션이 없으면 공통 VFX와 짧은 스케일·재질 변화로 대체합니다.

---

# 6. 데이터 예시

```text
MonsterId = MON_MAGMA_GUARD
StageMonsterProfileId = SMP_STAGE_15_MAGMA_GUARD
BehaviorSetId = BEHAVIOR_MAGMA_GUARD_STAGE_15
VisualProfileId = VIS_MAGMA_GUARD_PROTOTYPE

HPFactor = 11.80
ShieldFraction = 0.22
ShellBreakDelay = 0.35
```

모델 교체:

```text
VIS_MAGMA_GUARD_PROTOTYPE
→ VIS_MAGMA_GUARD_FINAL
```

위 교체는 전투 데이터와 저장 데이터에 영향을 주지 않습니다.

---

# 7. 버전과 저장

프로필은 버전 필드를 가집니다.

```text
ContentVersion
BalanceVersion
VisualVersion
```

플레이어 저장 데이터에는 일반적으로 `MonsterId`를 저장하지 않습니다. 도감과 처치 기록이 필요하면 안정 `MonsterId`만 저장하고 VisualProfile은 저장하지 않습니다.

---

# 8. 구현 검사

- 모든 스테이지 프로필이 존재하는 `MonsterId`를 참조하는지 검사
- 모든 행동 구성요소가 서버 해석기에 등록됐는지 검사
- 누락 VisualProfile은 프로토타입으로 자동 대체
- 모델 교체 전후 충돌 캡슐과 경로 진행도가 같은지 검사
- 보스 전용 애니메이션 누락이 전투 판정을 멈추지 않는지 검사
- 모델 삭제·AssetId 실패 시 기본 프로토타입으로 복구
