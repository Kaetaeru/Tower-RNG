# 상태·저장 생명주기 기술 계약

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 필수 참고: `../../AGENTS.md`
- 상위 기획: `../design/REBIRTH.md`, `../design/ROLLING.md`, `../design/TOWERS.md`, `../design/FORMATION.md`, `../design/TUTORIAL.md`, `../design/FUSION.md`, `../design/CURRENCY.md`, `../design/OFFLINE_PROGRESS.md`, `../design/WORLD_NAVIGATION.md`, `../design/SETTINGS.md`
- 하위 문서 예정: `../implementation/STATE_LIFECYCLE.md`
- 마지막 정리: 2026-08-02

## 요약

Tower RNG의 계정 상태는 서버 권위의 단일 프로필 스냅샷을 중심으로 관리합니다. 굴리기, 문 구매, 스탯 구매, 수동 합체, 환생과 오프라인 지급은 서로 다른 저장 체계를 만들지 않고 같은 프로필 계약을 사용합니다.

핵심 목표:

- 클라이언트 조작으로 재화·타워 생성 불가
- 중복 요청으로 두 번 지급·차감 불가
- 환생과 접속 종료의 초기화 경계가 시스템마다 달라지지 않음
- 데이터 스키마 변경 시 순차 마이그레이션 가능
- 최초 튜토리얼은 계정당 한 번만 실행
- 현재 환생의 열린 문은 재접속 후 유지
- 재접속은 항상 로비에서 시작
- 마지막 활동 스테이지로 돌아가는 빠른 버튼 제공
- 웨이브·몬스터·바닥 코인 같은 전투 세션 상태는 저장하지 않음

---

## 1. 권위와 프로필 단위

### STA-001: 서버 권위

클라이언트는 다음을 직접 결정하지 않습니다.

- 굴리기 결과
- 코인·정수·방어 경험치 증가
- 타워 보유 수량
- 문 해금
- 스탯 구매
- 합체 성공과 재료 차감
- 환생 가능 여부
- 최초 튜토리얼 보상 완료 여부
- 오프라인 보상
- 리더보드 희귀 타워

클라이언트는 입력 의도를 요청하고 서버가 현재 프로필을 검증해 결과를 반환합니다.

### STA-002: 핵심 진행 단일 키

```text
PlayerProfile/<UserId>
```

코인, 타워, 스탯, 문과 환생을 서로 다른 DataStore 키에 분산해 교차 저장 성공 여부에 의존하지 않습니다. 전역 리더보드와 분석 데이터는 파생 데이터로 별도 저장할 수 있지만 복구 가능한 원본은 프로필입니다.

### STA-003: 세션 잠금

한 계정은 동시에 하나의 서버 세션만 프로필 쓰기 권한을 가집니다.

- 입장 시 세션 잠금 획득
- 잠금 실패 시 중복 세션 쓰기 금지
- 서버 종료·정상 이탈 시 잠금 해제
- 비정상 종료를 위한 만료와 복구 절차
- 다른 서버가 잠긴 프로필을 임의 덮어쓰지 않음

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
├─ CurrentCycle
├─ Offline
├─ Settings
└─ Audit
```

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

### STA-007: Progression

```text
Progression
- RebirthCount
- PermanentCoinMultiplier
- PermanentLuckValue
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

튜토리얼 플래그는 계정 영구 상태입니다. 환생·서버 이동·재접속으로 초기화하지 않습니다.

불변조건:

```text
InitialTutorialCompleted
→ InitialRollCompleted
→ InitialSlimeDefeated
→ AutoRollTutorialPurchased
→ InitialFormationFilled
```

부분 완료 상태로 접속이 끊기면 이미 지급된 타워·코인·XP를 되돌리거나 다시 지급하지 않고 다음 미완료 단계부터 재개합니다.

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

굴리기 카운터와 결과 타워 지급은 같은 메모리 프로필 변경에 포함합니다.

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

`EquippedCount`는 편성 데이터에서 계산하며 영구 중복 저장하지 않습니다.

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

현재 편성 수량은 타워 보유 수량을 초과할 수 없습니다.

`EmptySlotFillEnabled`는 완전히 비어 있는 슬롯만 채우는 편의 설정입니다. 자동 편성처럼 기존 타워를 교체하지 않습니다. 신규 계정 기본값은 `true`이며 계정 설정으로 저장합니다.

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

오프라인 동안 남은 시간은 감소하지 않습니다.

### STA-013: CurrentCycle

```text
CurrentCycle
- OpenStageGates
- LastActiveStageId
```

유지:

- 서버 이동
- 접속 종료와 재접속

초기화:

- 환생

저장하지 않음:

- 현재 웨이브
- 현재 몬스터
- 보스 체력
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

같은 오프라인 구간을 두 번 지급하지 않게 시각 갱신과 코인 지급을 같은 프로필 변경으로 처리합니다.

### STA-015: Settings

설정 값은 `../design/SETTINGS.md`의 ID와 허용값을 사용합니다.

- 효과와 카메라
- 음향
- UI와 접근성
- 알림
- 성능

장치별로 달라야 하는 값은 계정 기본값과 로컬 장치 오버라이드를 분리할 수 있습니다.

### STA-016: Audit

```text
Audit
- RecentTransactionIds
- LastCriticalMutation
- LastRareSaveAt
- LastMigrationVersion
```

`RecentTransactionIds`는 최근 중요 거래의 제한된 순환 버퍼를 사용합니다.

---

## 3. 저장하지 않는 런타임 상태

### STA-017: 전투 세션 상태

다음은 재접속·서버 이동 후 복구하지 않습니다.

- 현재 스테이지 웨이브 번호
- 생성 대기열
- 몬스터와 보스 체력
- 경로 진행도
- 예약 피해
- 타워 타겟과 Engage 위치
- 공격 준비·Channel·Burst 상태
- 투사체·Beam·장판
- 소환체·설치물
- 개인 베이스 현재 체력
- 바닥 코인과 드롭 수명
- 카메라·파티클·음향 상태

재접속하면 로비에서 시작하며 전투는 스테이지에 들어갈 때 새 1웨이브로 생성합니다. 단, 최초 튜토리얼이 미완료라면 저장된 튜토리얼 플래그에 따라 다음 미완료 단계부터 재개합니다.

### STA-018: 파생 캐시

저장하지 않고 원본에서 재계산:

- 현재 가장 희귀한 보유 타워
- 자동 편성 평가 점수
- 타워별 EquippedCount
- 현재 행운 적용 확률표
- 최종 전투 능력치
- 현재 스테이지 보상 배율

---

## 4. 이벤트별 생명주기

### STA-019: 최초 튜토리얼

최초 튜토리얼은 단계별 원자 변경으로 처리합니다.

#### 첫 굴리기

```text
InitialRollCompleted 검증
→ 굴림 카운터 증가
→ 결과 타워 지급
→ 첫 빈 슬롯 배치
→ InitialRollCompleted = true
```

#### 최초 슬라임 처치

```text
InitialRollCompleted 검증
→ 정규 MON_PRAIRIE_SLIME 처치 검증
→ Coins +10
→ DefenseXP +10
→ InitialSlimeDefeated = true
```

같은 슬라임 처치 ID를 다시 제출해 코인·XP를 중복 획득할 수 없습니다.

#### 자동 굴리기 구매

```text
InitialSlimeDefeated 검증
→ Coins >= 10 검증
→ Coins -10
→ NODE_AUTO_ROLL 구매
→ AutoRollEnabled = true
→ AutoRollTutorialPurchased = true
```

#### 시작 편성 완성

```text
보유·역할 슬롯 검증
→ 세 번의 정상 굴리기 결과로 빈 슬롯 채움
→ 시작 4슬롯 충족
→ InitialFormationFilled = true
→ InitialTutorialCompleted = true
→ 정규 웨이브 1 시작 가능
```

튜토리얼 슬라임과 보상은 계정당 한 번뿐이며 환생 후 재실행하지 않습니다.

### STA-020: 스테이지 이동

초기화:

- 이전 웨이브와 몬스터
- 보스 상태
- 바닥 코인
- 타워 전투 컨텍스트

유지:

- 코인과 방어 경험치
- 열린 문
- 타워와 편성
- 굴리기 카운터
- 포션
- 스탯

새 스테이지는 1웨이브부터 시작합니다.

### STA-021: 베이스 과부하

초기화:

- 현재 몬스터와 보스
- 현재 웨이브
- 예약 피해와 전투 생성물

유지:

- 이미 바닥에 떨어진 코인
- 획득 코인
- 방어 경험치
- 열린 문
- 굴리기와 타워
- 포션

3초 뒤 같은 스테이지 1웨이브를 시작합니다.

### STA-022: 접속 종료

저장:

- 전체 영구 상태
- 모든 `TutorialFlags`
- Formation 설정
- `CurrentCycle.OpenStageGates`
- `CurrentCycle.LastActiveStageId`
- 오프라인 계산 시각
- 설정

폐기:

- 전투 세션 상태
- 바닥 코인

### STA-023: 재접속

```text
1. 세션 잠금 획득
2. 프로필 로드
3. SchemaVersion 마이그레이션
4. 프로필 불변조건 검증·복구
5. 오프라인 보상 계산과 LastAccrualAt 갱신
6. 로비에 플레이어 생성
7. 편성·설정·HUD 복구
8. 미완료 최초 튜토리얼 단계 판정
9. 오프라인 요약 표시
10. 마지막 활동 스테이지 빠른 복귀 버튼 활성화
```

재접속 위치는 항상 로비입니다. 최초 튜토리얼이 미완료라면 빠른 복귀보다 튜토리얼 재개 안내를 우선합니다.

### STA-024: 마지막 스테이지 복귀

`LastActiveStageId`가 현재 환생에서 아직 열린 스테이지이면 로비 HUD에 빠른 복귀 버튼을 표시합니다.

```text
빠른 복귀
→ 목적지 해금 검증
→ 해당 스테이지로 이동
→ 새 1웨이브 시작
```

### STA-025: 환생

하나의 원자적 프로필 변경으로 처리합니다.

검증:

- 현재 DefenseXP가 요구량 이상
- 중복 TransactionId 아님

변경:

- RebirthCount 증가
- 영구 코인·행운 성장 갱신
- Coins 0
- DefenseXP 0
- OpenStageGates 초기화
- LastActiveStageId 초기화
- 현재 전투 종료

유지:

- 타워와 보호 수량
- 도감
- 스탯 트리
- 굴리기 카운터
- 변종·합체 진행
- 연금 정수와 포션
- 오프라인 업그레이드
- `TutorialFlags`
- Formation 설정과 `EmptySlotFillEnabled`
- 설정

### STA-026: 서버 이동

서버 이동은 접속 종료·재접속과 같은 영구 저장 규칙을 사용합니다.

- 문 해금 유지
- 코인·방어 경험치 유지
- 최초 튜토리얼 상태 유지
- 전투 세션 폐기
- 새 서버 로비 시작
- 빠른 복귀 버튼 제공

---

## 5. 원자적 프로필 변경

### STA-027: 거래 단위

#### 굴리기

```text
굴림 카운터 증가
→ 특수 주사위 판정
→ RNG 결과 확정
→ OwnedCount 증가
→ 빈 슬롯 채움 여부 판정
→ 도감·최초 획득 기록
→ 희귀 기록과 리더보드 후보 갱신
```

#### 문 구매

```text
가격 검증
→ Coins 차감
→ OpenStageGates 갱신
```

#### 스탯 구매

```text
선행 조건 검증
→ 가격 차감
→ 노드 단계 증가
```

#### 수동 합체

```text
재료·보호·편성 수량 검증
→ 재료 OwnedCount 차감
→ 결과 OwnedCount 증가
→ FusionProgress·도감 갱신
```

#### 환생

```text
DefenseXP 검증
→ 영구 보상 증가
→ 현재 주기 상태 초기화
```

#### 오프라인 지급

```text
시간 검증
→ 보상 계산
→ Coins 증가
→ LastAccrualAt 갱신
```

### STA-028: TransactionId와 사건 ID

구매·합체·환생·오프라인 지급처럼 중복 실행 위험이 큰 요청은 `TransactionId`를 사용합니다.

최초 슬라임처럼 서버가 생성한 단일 전투 보상은 계정 튜토리얼 세션의 고유 사건 ID를 사용합니다.

- 이미 처리된 ID는 같은 결과를 재지급하지 않음
- 실패한 검증은 재화 차감 없음
- 클라이언트가 임의 ID로 과거 거래를 재생하지 못함

굴리기처럼 빈도가 높은 작업은 세션 내 `MutationSequence`로 순서를 보장합니다.

---

## 6. 저장 정책

### STA-029: 메모리 원본과 저장 스냅샷

접속 중 원본은 서버 메모리 프로필입니다. 모든 게임 로직은 이 프로필을 먼저 변경하고 저장 큐가 스냅샷을 지속 반영합니다.

### STA-030: 저장 시점

- 일정 간격 자동 저장
- 정상 플레이어 이탈
- 서버 종료
- 최초 튜토리얼 중요 단계 완료
- 환생 완료
- 수동 합체 완료
- 큰 스탯 구매
- 극희귀 타워 획득
- 스키마 마이그레이션 직후

매 굴림마다 DataStore 쓰기를 수행하지 않습니다. 단, 최초 튜토리얼의 첫 타워·슬라임 보상·자동 굴리기 구매처럼 중복 위험이 있는 단계는 중요 저장 큐에 등록합니다.

### STA-031: UpdateAsync와 버전 검증

검증 대상:

- SessionId
- MutationSequence
- SchemaVersion
- 마지막 저장 시각

오래된 세션이 최신 프로필을 덮어쓰지 못하게 합니다.

### STA-032: 저장 실패

- 프로필은 세션 메모리에서 유지
- 지수 백오프로 재시도
- 반복 실패 시 사용자에게 저장 불안정 안내
- 실패 중 같은 합체·환생·튜토리얼 보상을 중복 실행하지 않음
- 서버 종료 시 제한된 마지막 저장 시도

---

## 7. 마이그레이션

### STA-033: 순차 마이그레이션

```text
SchemaVersion 1
→ Migration 1 to 2
→ Migration 2 to 3
→ 최신 버전
```

### STA-034: 마이그레이션 불변조건

- 타워 총수량 음수 금지
- 보호 수량이 보유 수량 초과 금지
- 편성 수량이 보유 수량 초과 금지
- 최초 튜토리얼 완료 플래그와 지급 내역 일치
- 존재하지 않는 NodeId 제거 또는 명시적 대체
- 제거된 TowerId는 보상 변환 규칙 필요
- 큰 수 형식 정규화
- 문 비트와 최고 스테이지 일관성

기존 계정에 새 튜토리얼 플래그를 추가할 때 이미 자동 굴리기 노드나 정상 진행 기록이 있으면 `InitialTutorialCompleted = true`로 마이그레이션하여 최초 보상을 다시 지급하지 않습니다.

---

## 8. 수동 합체 계약

### STA-035: 자동 합체 없음

- 백그라운드 합체 없음
- 타워 획득 직후 자동 소비 없음
- 접속 종료 중 합체 없음
- 자동 합체 설정 필드 없음

### STA-036: 합체 가능 수량

```text
AvailableForFusion
= OwnedCount
- ProtectedCount
- EquippedCount
```

### STA-037: 혼합 합체 금지

- 기본형 + 같은 기본형 가능
- 같은 변종 + 같은 변종 가능
- 기본형 + 변종 불가
- 서로 다른 변종 혼합 불가

---

## 9. 거래 금지

### STA-038: 플레이어 간 자산 이전 없음

다음의 플레이어 간 거래·우편·양도는 지원하지 않습니다.

- 타워
- 코인
- 연금 정수
- 방어 경험치
- 포션
- 합체 재료

프로필에는 소유자 변경 기록이나 거래 잠금 상태를 만들지 않습니다.

---

## 10. 테스트 요구사항

- 같은 계정 동시 접속 세션 잠금
- 첫 굴리기 직후 강제 종료
- 최초 슬라임 처치와 보상 저장 사이 강제 종료
- 자동 굴리기 구매 버튼 연타
- 세 번의 시작 굴림 중 재접속
- 완료 계정에서 최초 튜토리얼이 재실행되지 않음
- 빈 슬롯 채움이 기존 타워를 교체하지 않음
- 역할 슬롯이 가득 찬 상태의 빈 슬롯 처리
- 구매 중 재접속
- 합체 버튼 연타
- 환생 버튼 연타
- 오프라인 지급 직후 서버 종료
- 극희귀 획득 직후 강제 종료
- SchemaVersion 다단계 마이그레이션
- 보유·보호·편성 불변조건 복구
- 환생 후 문 초기화와 튜토리얼 완료 상태 유지
- 재접속 로비 생성과 빠른 복귀
- 잘못된 LastActiveStageId 처리
- 큰 수 저장·복원
- 리더보드 파생값 재계산

---

## 11. 미확정 사항

- 실제 프로필 라이브러리 선택
- 세션 잠금 만료 시간
- 자동 저장 간격
- 중요 희귀도 즉시 저장 기준
- RecentTransactionIds 버퍼 크기
- 큰 수 직렬화의 정확한 필드명
- 장치별 설정 오버라이드 저장 위치
- 데이터 백업·롤백 운영 절차
