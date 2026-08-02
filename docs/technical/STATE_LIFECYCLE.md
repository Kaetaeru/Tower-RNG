# 상태·저장 생명주기 기술 계약

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 필수 참고: `../../AGENTS.md`
- 상위 기획: `../design/REBIRTH.md`, `../design/ROLLING.md`, `../design/TOWERS.md`, `../design/FORMATION.md`, `../design/TUTORIAL.md`, `../design/FUSION.md`, `../design/CURRENCY.md`, `../design/OFFLINE_PROGRESS.md`, `../design/WORLD_NAVIGATION.md`, `../design/SETTINGS.md`
- 관련 벤치마크: `../reference/V1_REBIRTH_STAT_BENCHMARK.md`, `../reference/V1_REBIRTH_XP_BENCHMARK.md`
- 하위 문서 예정: `../implementation/STATE_LIFECYCLE.md`
- 마지막 정리: 2026-08-02

## 요약

Tower RNG의 계정 상태는 서버 권위의 단일 프로필 스냅샷으로 관리합니다. 굴리기, 문 구매, 스탯 구매, 수동 합체, 환생, XP 기준 스테이지 상승과 오프라인 지급은 같은 프로필 계약을 사용합니다.

환생 변경:

```text
DefenseXP = 0
RebirthCount +1
RebirthStatTokensEarned +4
UnspentRebirthStatTokens +4
RebirthRespecAvailable = true
```

코인, 열린 문, 현재 스테이지와 전투는 변경하지 않습니다.

핵심 목표:

- 클라이언트 조작으로 재화·타워·토큰 생성 불가
- 중복 요청으로 두 번 지급·차감 불가
- 열린 문과 XP 기준 스테이지는 계정 영구 진행
- XP 기준 상승 시 진행률 보존
- 재접속은 로비, 마지막 열린 스테이지 빠른 복귀
- 웨이브·몬스터·바닥 코인은 접속 종료 후 복구하지 않음
- 환생은 현재 전투를 중단하지 않음

---

## 1. 권위와 프로필 단위

### STA-001: 서버 권위

클라이언트가 직접 결정하지 않는 값:

- 굴리기 결과
- 코인·정수·Defense XP 증가
- XP 기준 스테이지와 요구량
- 환생 스탯 토큰 지급·배분·재분배
- 타워 보유·보호 수량
- 문 해금
- 코인 스탯 구매
- 합체 성공과 재료 차감
- 환생 가능 여부
- 오프라인 보상
- 리더보드 희귀 타워

### STA-002: 단일 프로필 키

```text
PlayerProfile/<UserId>
```

코인, 타워, 문, 스탯과 환생을 서로 다른 DataStore 키에 분산하지 않습니다.

### STA-003: 세션 잠금

- 한 계정은 한 서버 세션만 쓰기 권한 보유
- 입장 시 잠금 획득, 종료 시 해제
- 비정상 종료 만료·복구 절차 필요
- 오래된 세션이 최신 프로필을 덮어쓰지 못함

---

## 2. 프로필 스키마

```text
Profile
├─ Meta
├─ Economy
├─ Progression
├─ Rolling
├─ Towers
├─ Formation
├─ Fusion
├─ Potions
├─ WorldProgress
├─ Offline
├─ Settings
└─ Audit
```

### Meta

```text
SchemaVersion
CreatedAt
LastLoadedAt
LastSavedAt
SessionId
MutationSequence
```

### Economy

```text
Coins: MagnitudeNumber
AlchemyEssence: integer 또는 MagnitudeNumber
DefenseXP: MagnitudeNumber
```

### Progression

```text
RebirthCount
RebirthXPAnchorStage
RebirthStatTokensEarned
UnspentRebirthStatTokens
RebirthStatAllocations[StatId]
RebirthRespecAvailable
HighestStageEver
StatTreeNodes
UnlockedVariantFamilies
UnlockedSystems
TutorialFlags
CodexRecords
```

허용 환생 StatId:

```text
REBIRTH_LUCK
REBIRTH_PERFORMANCE
REBIRTH_CURRENCY
REBIRTH_ROLL_SPEED
```

불변조건:

```text
1 <= RebirthXPAnchorStage <= HighestStageEver
0 <= UnspentRebirthStatTokens
sum(RebirthStatAllocations) + UnspentRebirthStatTokens
= RebirthStatTokensEarned
```

환생 횟수만으로 자동 증가하는 `PermanentCoinMultiplier`, `PermanentLuckValue` 필드는 사용하지 않습니다.

### Rolling

```text
TotalRolls
GoldenProgress
DiamondProgress
AutoRollEnabled
ProbabilityTableVersion
RecentRareAcquisitions
```

### Towers

```text
Towers[TowerId]
- OwnedCount
- ProtectedCount
- FirstObtainedAt
- FirstObtainedBaseOddsN
```

```text
0 <= ProtectedCount <= OwnedCount
0 <= EquippedCount <= OwnedCount
```

### Formation

```text
EquippedEntries
EmptySlotFillEnabled
AutoFormationEnabled
RolePresetId
GlobalTargetPolicy
RoleTargetPolicies
TowerTargetPolicies
SavedManualPreset
QuickHudPreferences
```

### Fusion

```text
Unlocked
FusionProgress
DiscoveredRecipes
CompletedCounts
```

자동 합체 설정은 존재하지 않습니다.

### Potions

```text
InventoryByPotionId
ActiveEffects
- PotionId
- RemainingActiveSeconds
```

오프라인과 환생은 활성 시간을 감소시키거나 제거하지 않습니다.

### WorldProgress

```text
OpenStageGates
LastActiveStageId
```

환생·재접속·서버 이동 후 유지합니다.

### Offline

```text
AccrualUnlocked
EfficiencyLevel
StorageLevel
LastAccrualAt
LastGrantedAt
```

### Settings

`../design/SETTINGS.md`의 ID와 허용값을 사용합니다.

### Audit

```text
RecentTransactionIds
LastCriticalMutation
LastRareSaveAt
LastMigrationVersion
```

---

## 3. 저장하지 않는 런타임 상태

재접속·서버 이동 뒤 복구하지 않음:

- 현재 웨이브·생성 대기열
- 몬스터·보스·베이스 체력
- 경로 진행도·예약 피해
- 타워 타겟·Engage 위치
- 공격 준비·Channel·Burst
- 투사체·Beam·장판
- 소환체·설치물
- 바닥 코인과 드롭 수명
- 카메라·파티클·음향

환생은 접속 종료가 아니므로 위 상태를 폐기하지 않습니다.

파생 캐시:

- 현재 환생 요구 XP
- 현재 환생 진행률
- 가장 희귀한 보유 타워
- 자동 편성 평가 점수
- EquippedCount
- 현재 행운 적용 확률표
- 환생 스탯 최종 보너스
- 최종 전투 능력치
- 현재 스테이지 보상 배율

요구 XP는 `RebirthCount`, `RebirthXPAnchorStage`와 카탈로그 수입 데이터에서 계산합니다.

---

## 4. 최초 튜토리얼

### 첫 굴리기

```text
플래그 검증
→ 굴림 카운터 증가
→ 타워 지급
→ 첫 빈 슬롯 배치
→ InitialRollCompleted = true
```

### 최초 슬라임

```text
처치 사건 검증
→ Coins +10
→ DefenseXP +10
→ InitialSlimeDefeated = true
```

### 자동 굴리기

```text
Coins >= 10
→ Coins -10
→ NODE_AUTO_ROLL 구매
→ AutoRollEnabled = true
→ AutoRollTutorialPurchased = true
```

### 시작 편성

```text
세 번의 정상 굴림으로 빈 슬롯 채움
→ 4슬롯 충족
→ InitialFormationFilled = true
→ InitialTutorialCompleted = true
```

튜토리얼은 환생 후 반복하지 않습니다.

---

## 5. 스테이지와 전투 이벤트

### 스테이지 이동

초기화:

- 이전 전투 컨텍스트
- 웨이브·몬스터·보스
- 바닥 코인
- 타워 전투 생성물

유지:

- 코인·Defense XP·환생 기준 스테이지·토큰
- 열린 문
- 타워·편성·굴림
- 포션·스탯

새 스테이지는 1웨이브부터 시작합니다.

### 베이스 과부하

초기화:

- 현재 몬스터·보스·웨이브
- 예약 피해와 전투 생성물

유지:

- 이미 떨어진 코인
- 보유 코인·Defense XP·토큰
- 열린 문
- 굴리기·타워·포션

3초 뒤 같은 스테이지 1웨이브를 시작합니다.

### 재접속

```text
세션 잠금
→ 프로필 로드·마이그레이션
→ 불변조건 검증
→ 오프라인 코인 지급
→ 로비 생성
→ 편성·설정·HUD 복구
→ 튜토리얼 미완료 단계 판정
→ 마지막 열린 스테이지 빠른 복귀 제공
```

---

## 6. XP 기준 스테이지 상승

### STA-023: 발동 조건

다음이 모두 참일 때만 상승합니다.

```text
유효 처치 Defense XP 지급
처치가 발생한 StageId > RebirthXPAnchorStage
```

단순 입장, 행운 적용, 몬스터에 피해만 준 상태는 기준을 올리지 않습니다.

### STA-024: 원자적 진행률 보존

```text
OldRequirement = CalculateRequirement(RebirthCount + 1, OldAnchor)
ProgressRatio = DefenseXP / OldRequirement
NewAnchor = KilledMonsterStage
NewRequirement = CalculateRequirement(RebirthCount + 1, NewAnchor)
NewDefenseXP = ProgressRatio × NewRequirement
NewDefenseXP += CurrentKillDefenseXP
```

순서상 현재 처치 XP는 기준 전환 뒤 새 기준 값으로 지급합니다.

원자적 변경:

```text
RebirthXPAnchorStage = NewAnchor
DefenseXP = NewDefenseXP
중요 저장 큐 등록
```

- 진행률은 전환 전후 동일
- 기준은 절대 감소하지 않음
- 중복 처치 사건으로 두 번 전환하지 않음
- `MagnitudeNumber` 반올림은 공통 규칙 사용

---

## 7. 환생

### STA-025: 검증

- 현재 DefenseXP가 파생 요구량 이상
- 중복 TransactionId가 아님

### STA-026: 원자적 변경

```text
RebirthCount +1
RebirthStatTokensEarned +4
UnspentRebirthStatTokens +4
DefenseXP = 0
RebirthRespecAvailable = true
```

변경하지 않음:

- Coins
- RebirthXPAnchorStage
- WorldProgress.OpenStageGates
- WorldProgress.LastActiveStageId
- 현재 위치·웨이브·몬스터·보스·베이스
- 바닥 코인
- 타워 전투 상태
- 타워·코인 스탯·합체·변종·포션·설정

환생 완료 후 현재 전투를 계속합니다.

---

## 8. 토큰 배분과 재분배

### 새 토큰 배분

```text
UnspentRebirthStatTokens >= Cost
→ StatId 검증
→ UnspentRebirthStatTokens 차감
→ RebirthStatAllocations[StatId] 증가
→ 파생 능력치·확률 캐시 재계산
```

### 전체 재분배

```text
RebirthRespecAvailable == true
→ 현재 배분 총합 계산
→ 모든 RebirthStatAllocations = 0
→ UnspentRebirthStatTokens += 반환량
→ 새 배분 요청 검증·적용
→ RebirthRespecAvailable = false
→ 파생 캐시 재계산
```

- 환생 직후 한 번만 가능
- 비용 없음
- 새 배분 확정 전 취소하면 기존 상태 유지
- 실패한 요청은 부분 변경 없음

---

## 9. 기타 원자적 변경

### 굴리기

```text
카운터 증가
→ 특수 주사위 판정
→ RNG 결과
→ OwnedCount 증가
→ 빈 슬롯 판정
→ 도감·희귀 기록 갱신
```

### 문 구매

```text
가격 검증
→ Coins 차감
→ OpenStageGates 영구 갱신
```

### 코인 스탯 구매

```text
선행 조건 검증
→ Coins 차감
→ StatTreeNodes 증가
```

### 수동 합체

```text
재료·보호·편성 수량 검증
→ 재료 차감
→ 결과 지급
→ 진행·도감 갱신
```

### 오프라인 지급

```text
시간 검증
→ Coins 증가
→ 지급 시각 갱신
```

중복 위험이 큰 요청은 `TransactionId`를 사용합니다.

---

## 10. 저장 정책

우선 저장 사건:

- 최초 튜토리얼 중요 단계
- 극희귀 타워 획득
- 문 구매
- 환생
- XP 기준 스테이지 상승
- 토큰 전체 재분배
- 수동 합체
- 오프라인 지급

일반 코인·굴림은 메모리에서 집계하고 주기 저장합니다. 종료 시 최종 저장을 시도하되 종료 저장만 신뢰하지 않습니다.

---

## 11. 마이그레이션

이전 `CurrentCycle` 구조가 존재하면:

```text
OpenStageGates → WorldProgress.OpenStageGates
LastActiveStageId → WorldProgress.LastActiveStageId
기존 최고 XP 획득 가능 스테이지 → RebirthXPAnchorStage
```

기준 스테이지를 정확히 복원할 수 없으면 `min(HighestStageEver, LastActiveStageId)`를 보수적 기본값으로 사용하고 마이그레이션 버전을 기록합니다.

이전 자동 환생 코인·행운 배율은 새 토큰 배분으로 임의 변환하지 않습니다. 출시 전 데이터라면 명시적 초기화 마이그레이션을 사용합니다.

---

## 12. 사용하지 않는 구조

- 클라이언트 권위 굴림·보상·환생
- 코인·토큰·문을 서로 다른 비원자적 키에 저장
- 환생 시 코인·문·전투 초기화
- 단순 입장으로 XP 기준 상승
- XP 기준 상승 시 진행률 감소
- 환생 시 XP 기준 스테이지 초기화
- 상시 무제한 토큰 재분배
- 자동 합체 설정
- 접속 종료 후 웨이브·바닥 코인 복구

---

## 13. 남은 기술 결정

- `MagnitudeNumber` 반올림·직렬화 세부 형식
- 요구 XP 계산 캐시 버전
- 기준 상승 HUD 사건 페이로드
- 다중 처치가 같은 프레임에 발생할 때 최고 StageId 병합 규칙
- 데이터 백업·롤백 절차
- 장치별 설정 오버라이드 위치
