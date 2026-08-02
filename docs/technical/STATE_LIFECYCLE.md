# 상태·저장 생명주기 기술 계약

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 필수 참고: `../../AGENTS.md`
- 상위 기획: `../design/REBIRTH.md`, `../design/ROLLING.md`, `../design/TOWERS.md`, `../design/FORMATION.md`, `../design/TUTORIAL.md`, `../design/FUSION.md`, `../design/CURRENCY.md`, `../design/OFFLINE_PROGRESS.md`, `../design/WORLD_NAVIGATION.md`, `../design/SETTINGS.md`
- 하위 문서 예정: `../implementation/STATE_LIFECYCLE.md`
- 마지막 정리: 2026-08-02

## 요약

Tower RNG의 계정 상태는 서버 권위의 단일 프로필 스냅샷으로 관리합니다. 굴리기, 문 구매, 스탯 구매, 수동 합체, 환생과 오프라인 지급은 같은 프로필 계약을 사용합니다.

환생의 영구 상태 변경은 다음으로 제한합니다.

```text
DefenseXP = 0
RebirthCount +1
RebirthStatTokens 지급
```

코인, 열린 문, 현재 스테이지와 전투는 환생으로 변경하지 않습니다.

핵심 목표:

- 클라이언트 조작으로 재화·타워·토큰 생성 불가
- 중복 요청으로 두 번 지급·차감 불가
- 최초 튜토리얼은 계정당 한 번
- 열린 문은 계정 영구 진행
- 재접속은 로비에서 시작하되 마지막 열린 스테이지로 빠른 복귀
- 웨이브·몬스터·바닥 코인은 접속 종료 후 복구하지 않음
- 환생은 현재 전투를 중단하지 않음

---

## 1. 권위와 프로필 단위

### STA-001: 서버 권위

클라이언트가 직접 결정하지 않는 값:

- 굴리기 결과
- 코인·정수·Defense XP 증가
- 환생 스탯 토큰 지급·배분
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

코인, 타워, 문, 스탯과 환생을 서로 다른 DataStore 키에 분산하지 않습니다. 전역 리더보드와 분석 데이터는 복구 가능한 프로필에서 파생합니다.

### STA-003: 세션 잠금

- 한 계정은 한 서버 세션만 쓰기 권한 보유
- 입장 시 잠금 획득
- 종료 시 해제
- 비정상 종료 만료·복구 절차 필요
- 오래된 세션이 최신 프로필을 덮어쓰지 못함

---

## 2. 프로필 스키마

### STA-004: 최상위 구조

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

기존 `CurrentCycle`은 더 이상 사용하지 않습니다. 마이그레이션에서 영구 `WorldProgress`로 변환합니다.

### STA-005: Meta

```text
Meta
- SchemaVersion
- CreatedAt
- LastLoadedAt
- LastSavedAt
- SessionId
- MutationSequence
```

### STA-006: Economy

```text
Economy
- Coins: MagnitudeNumber
- AlchemyEssence: integer 또는 MagnitudeNumber
- DefenseXP: MagnitudeNumber
```

코인은 환생으로 초기화하지 않습니다.

### STA-007: Progression

```text
Progression
- RebirthCount
- RebirthStatTokensEarned
- UnspentRebirthStatTokens
- RebirthStatAllocations[StatId]
- HighestStageEver
- StatTreeNodes
- UnlockedVariantFamilies
- UnlockedSystems
- TutorialFlags
  - InitialRollCompleted
  - InitialSlimeDefeated
  - AutoRollTutorialPurchased
  - InitialFormationFilled
  - InitialTutorialCompleted
- CodexRecords
```

`PermanentCoinMultiplier`, `PermanentLuckValue`처럼 환생 횟수만으로 자동 증가하는 필드는 사용하지 않습니다. 최종 영구 보너스는 `RebirthStatAllocations`에서 파생합니다.

토큰 불변조건:

```text
0 <= UnspentRebirthStatTokens
sum(RebirthStatAllocations) + UnspentRebirthStatTokens
= RebirthStatTokensEarned
```

튜토리얼 플래그는 계정 영구 상태이며 환생·서버 이동·재접속으로 초기화하지 않습니다.

### STA-008: Rolling

```text
Rolling
- TotalRolls
- GoldenProgress
- DiamondProgress
- AutoRollEnabled
- ProbabilityTableVersion
- RecentRareAcquisitions
```

굴림 카운터와 결과 지급은 같은 메모리 변경에 포함합니다.

### STA-009: Towers

```text
Towers[TowerId]
- OwnedCount
- ProtectedCount
- FirstObtainedAt
- FirstObtainedBaseOddsN
```

불변조건:

```text
0 <= ProtectedCount <= OwnedCount
0 <= EquippedCount <= OwnedCount
```

### STA-010: Formation

```text
Formation
- EquippedEntries
- EmptySlotFillEnabled
- AutoFormationEnabled
- RolePresetId
- GlobalTargetPolicy
- RoleTargetPolicies
- TowerTargetPolicies
- SavedManualPreset
- QuickHudPreferences
```

`EmptySlotFillEnabled`는 빈 슬롯만 채우며 기존 타워를 교체하지 않습니다.

### STA-011: Fusion

```text
Fusion
- Unlocked
- FusionProgress
- DiscoveredRecipes
- CompletedCounts
```

자동 합체 설정은 존재하지 않습니다.

### STA-012: Potions

```text
Potions
- InventoryByPotionId
- ActiveEffects
  - PotionId
  - RemainingActiveSeconds
```

오프라인에는 남은 시간이 감소하지 않습니다. 환생도 활성 시간을 변경하지 않습니다.

### STA-013: WorldProgress

```text
WorldProgress
- OpenStageGates
- LastActiveStageId
```

유지:

- 접속 종료·재접속
- 서버 이동
- 환생

저장하지 않음:

- 현재 웨이브
- 몬스터와 보스 체력
- 베이스 체력
- 바닥 코인

### STA-014: Offline

```text
Offline
- AccrualUnlocked
- EfficiencyLevel
- StorageLevel
- LastAccrualAt
- LastGrantedAt
```

같은 오프라인 구간을 두 번 지급하지 않게 시각 갱신과 코인 지급을 같은 변경으로 처리합니다.

### STA-015: Settings

설정 값은 `../design/SETTINGS.md`의 ID와 허용값을 사용합니다. 장치별 값은 계정 기본과 로컬 오버라이드를 분리할 수 있습니다.

### STA-016: Audit

```text
Audit
- RecentTransactionIds
- LastCriticalMutation
- LastRareSaveAt
- LastMigrationVersion
```

---

## 3. 저장하지 않는 런타임 상태

### STA-017: 전투 세션 상태

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

환생은 접속 종료가 아니므로 위 런타임 상태를 폐기하지 않습니다.

### STA-018: 파생 캐시

저장하지 않고 원본에서 계산:

- 가장 희귀한 보유 타워
- 자동 편성 평가 점수
- EquippedCount
- 현재 행운 적용 확률표
- 환생 스탯 배분의 최종 보너스
- 최종 전투 능력치
- 현재 스테이지 보상 배율

---

## 4. 주요 이벤트

### STA-019: 최초 튜토리얼

#### 첫 굴리기

```text
플래그 검증
→ 굴림 카운터 증가
→ 타워 지급
→ 첫 빈 슬롯 배치
→ InitialRollCompleted = true
```

#### 최초 슬라임

```text
정규 슬라임 처치 사건 검증
→ Coins +10
→ DefenseXP +10
→ InitialSlimeDefeated = true
```

#### 자동 굴리기

```text
Coins >= 10
→ Coins -10
→ NODE_AUTO_ROLL 구매
→ AutoRollEnabled = true
→ AutoRollTutorialPurchased = true
```

#### 시작 편성

```text
세 번의 정상 굴림으로 빈 슬롯 채움
→ 4슬롯 충족
→ InitialFormationFilled = true
→ InitialTutorialCompleted = true
```

튜토리얼은 환생 후 반복하지 않습니다.

### STA-020: 스테이지 이동

초기화:

- 이전 전투 컨텍스트
- 웨이브·몬스터·보스
- 바닥 코인
- 타워 전투 생성물

유지:

- 코인·Defense XP·토큰
- 열린 문
- 타워·편성·굴림
- 포션·스탯

새 스테이지는 1웨이브부터 시작합니다.

### STA-021: 베이스 과부하

초기화:

- 현재 몬스터·보스·웨이브
- 예약 피해와 전투 생성물

유지:

- 이미 떨어진 코인
- 보유 코인·Defense XP·토큰
- 열린 문
- 굴리기·타워·포션

3초 뒤 같은 스테이지 1웨이브를 시작합니다.

### STA-022: 재접속

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

### STA-023: 환생

검증:

- 현재 DefenseXP가 요구량 이상
- 중복 TransactionId가 아님

원자적 변경:

```text
RebirthCount +1
RebirthStatTokensEarned + TokenReward
UnspentRebirthStatTokens + TokenReward
DefenseXP = 0
```

변경하지 않음:

- Coins
- WorldProgress.OpenStageGates
- WorldProgress.LastActiveStageId
- 현재 위치·웨이브·몬스터·보스·베이스
- 바닥 코인
- 타워 전투 상태
- 타워·스탯·합체·변종·포션·설정

환생 완료 후 현재 전투를 계속합니다.

### STA-024: 스탯 토큰 배분

```text
UnspentRebirthStatTokens >= Cost
→ StatId와 단계 상한 검증
→ UnspentRebirthStatTokens 차감
→ RebirthStatAllocations[StatId] 증가
→ 파생 능력치·행운 캐시 재계산
```

재분배는 아직 미확정이므로 관련 요청과 필드를 구현하지 않습니다.

---

## 5. 원자적 프로필 변경

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
→ WorldProgress.OpenStageGates 영구 갱신
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

### 환생

```text
DefenseXP 검증
→ 환생 횟수·토큰 증가
→ DefenseXP 0
```

### 오프라인 지급

```text
시간 검증
→ Coins 증가
→ 지급 시각 갱신
```

중복 위험이 큰 요청은 `TransactionId`를 사용합니다.

---

## 6. 저장 정책

우선 저장 사건:

- 최초 튜토리얼 중요 단계
- 환생 완료
- 스탯 토큰 배분
- 문 구매
- 수동 합체
- 큰 코인 스탯 구매
- 극희귀 타워 획득
- 스키마 마이그레이션

매 굴림마다 DataStore 쓰기를 수행하지 않습니다. 서버 메모리 프로필이 접속 중 원본이며 저장 큐가 스냅샷을 반영합니다.

저장 실패 시:

- 세션 메모리 유지
- 지수 백오프 재시도
- 같은 거래 중복 실행 금지
- 반복 실패 사용자 안내

---

## 7. 마이그레이션

순차 마이그레이션:

```text
SchemaVersion N
→ Migration N to N+1
→ 최신 버전
```

이번 구조 변경 마이그레이션:

```text
CurrentCycle.OpenStageGates
→ WorldProgress.OpenStageGates

CurrentCycle.LastActiveStageId
→ WorldProgress.LastActiveStageId

기존 PermanentCoinMultiplier·PermanentLuckValue
→ 제거하지 않고 구버전 보상 보존용 별도 LegacyBonus로 이동하거나
  출시 전 데이터라면 명시적으로 0으로 초기화
```

출시 전 프로필에는 후자를 사용할 수 있지만 실제 서비스 데이터가 존재하면 보상 손실 없이 변환해야 합니다.

불변조건:

- 타워·보호·편성 수량 유효
- 토큰 획득 총량과 배분 합 일치
- 열린 문과 최고 도달 스테이지 일관성
- 큰 수 형식 정규화
- 튜토리얼 완료 계정에 보상 재지급 없음

---

## 8. 합체와 거래

```text
AvailableForFusion
= OwnedCount - ProtectedCount - EquippedCount
```

- 자동 합체 없음
- 기본형과 변종 혼합 금지
- 서로 다른 변종 혼합 금지
- 플레이어 간 타워·코인·정수·Defense XP·토큰·포션 거래 없음

---

## 9. 테스트 요구사항

- 동시 접속 세션 잠금
- 최초 튜토리얼 각 단계 강제 종료
- 문 구매 버튼 연타
- 합체 버튼 연타
- 환생 버튼 연타
- 환생 직전·직후 서버 종료
- 환생 후 코인 동일
- 환생 후 열린 문 동일
- 환생 후 현재 웨이브·몬스터 유지
- 환생 후 Defense XP만 0
- 환생 토큰 정확히 한 번 지급
- 스탯 토큰 배분 버튼 연타
- 토큰 총량 불변조건
- `CurrentCycle`에서 `WorldProgress` 마이그레이션
- 재접속 로비 생성과 빠른 복귀
- 극희귀 획득 직후 강제 종료
- 큰 수 저장·복원

---

## 10. 미확정 사항

- 실제 프로필 라이브러리
- 세션 잠금 만료 시간
- 자동 저장 간격
- 환생당 TokenReward
- 토큰 재분배 데이터 구조
- 중요 희귀도 즉시 저장 기준
- TransactionId 버퍼 크기
- 큰 수 직렬화 필드명
- 장치별 설정 오버라이드 위치
- 데이터 백업·롤백 절차
