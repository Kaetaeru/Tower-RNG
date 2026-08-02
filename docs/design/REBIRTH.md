# 환생 기획

- 계층: 게임 기획
- 상태: **Confirmed (Living Document)**
- 필수 참고: `../../AGENTS.md`
- 관련 문서: `BALANCE_MODEL.md`, `STAT_TREE.md`, `CURRENCY.md`, `ROLLING.md`, `LEVEL_DESIGN.md`, `TUTORIAL.md`, `PROGRESSION.md`, `ECONOMY_PACING.md`, `OFFLINE_PROGRESS.md`, `WORLD_NAVIGATION.md`, `RNG_PROBABILITY.md`, `../technical/STATE_LIFECYCLE.md`, `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md`, `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md`, `../reference/V1_REBIRTH_STAT_BENCHMARK.md`, `../reference/V1_REBIRTH_XP_BENCHMARK.md`
- 하위 문서 예정: `../spec/REBIRTH.md`
- 마지막 정리: 2026-08-02

## 요약

환생은 진행을 처음으로 되돌리는 프레스티지가 아니라, 전투로 모은 **Defense XP를 영구 스탯 토큰으로 전환하는 연속 성장 행동**입니다.

```text
유지
- 코인
- 열린 스테이지 문
- 현재 위치와 활성 스테이지
- 현재 웨이브와 전투
- 타워·코인 스탯·도감·합체·변종

변경
- Defense XP → 0
- RebirthCount +1
- 환생 스탯 토큰 4개 지급
```

토큰 배분처:

```text
행운
성능
재화
주사위 속도
```

첫 환생은 `7,000 Defense XP`, 이후 요구량은 실제로 XP를 얻은 가장 높은 스테이지의 기준 수입과 목표 환생 간격으로 계산합니다.

---

## 1. Defense XP

### REB-001: 환생 전용 진행도

```text
Defense XP
= 처치한 SpawnCost
× StageRewardScale
× BossModifier
```

- 일반 몬스터 BossModifier: 1.00
- 보스 본체 BossModifier: 1.15
- 코인 수집 여부와 무관하게 자동 지급
- 베이스에 도달한 몬스터는 지급하지 않음
- 오프라인에는 증가하지 않음
- 코인 또는 Robux로 직접 구매하지 않음
- 재화 스탯으로 증가하지 않음

첫 버전은 별도 웨이브 완료 XP 보너스를 사용하지 않습니다.

### REB-002: 실행 조건

```text
현재 Defense XP >= 다음 환생 요구 XP
→ 환생 가능
```

- 자동 실행 없음
- 전투 중에도 실행 가능
- 요구량을 채운 뒤 계속 파밍 가능
- 초과 XP는 환생 시 기본적으로 이월하지 않음

---

## 2. 첫 환생

### REB-003: 고정 요구량

```text
FirstRebirthXP = 7,000
```

| 소비 성향 | 첫 환생 범위 |
|---|---:|
| 균형 소비 | 7.96~13.41분 |
| 문 우선 | 7.80~14.34분 |
| 트리 우선 | 9.63~12.70분 |

중앙 통합 시뮬레이션에서는 약 9.42분에 도달합니다. 첫 환생은 초기화 구간의 끝이 아니라 첫 토큰 4개를 얻는 시점입니다.

---

## 3. 두 번째 이후 요구량

### REB-004: XP 기준 스테이지

```text
RebirthXPAnchorStage
= Defense XP를 한 번 이상 획득한 가장 높은 스테이지
```

- 단순 입장으로는 상승하지 않음
- 높은 스테이지에서 첫 유효 처치 XP가 발생하면 상승
- 한 번 상승한 기준은 감소하지 않음
- 낮은 스테이지에서 파밍하면 진행이 느려질 수 있음

높은 스테이지에 들어가 행운만 받고 돌아오는 전략은 요구량을 올리지 않습니다.

### REB-005: 기준 상승 시 진행률 보존

```text
ProgressRatio
= CurrentDefenseXP / OldRequiredDefenseXP

NewRequiredDefenseXP
= Requirement(NextRebirth, NewAnchorStage)

NewCurrentDefenseXP
= ProgressRatio × NewRequiredDefenseXP
```

현재 XP 숫자와 요구량 숫자는 함께 바뀌지만 막대의 퍼센트는 그대로 유지합니다.

이 규칙은 다음을 동시에 방지합니다.

- 높은 스테이지 첫 처치로 진행 막대가 뒤로 밀리는 체감
- 낮은 요구량을 유지한 채 높은 스테이지 XP를 받는 악용

### REB-006: 목표 시간

```text
두 번째 환생: 기준 20분
세 번째 환생: 기준 35분
네 번째~50번째: 기준 50분
```

V1 이후 장기 성장:

```text
51~100번째: 55분
101~150번째: 60분
151~200번째: 65분
201번째 이후: 최대 70분
```

이는 스탯이 없는 기준 처리속도입니다. 좋은 타워와 성능 투자는 실제 시간을 단축할 수 있습니다.

### REB-007: 요구량 공식

```text
PlannedDefenseXPPerMinute(Stage)
= PlannedCycleDefenseXP(Stage)
× 60
/ PlannedFarmCycleSeconds(Stage)
```

```text
RequiredDefenseXP(NextRebirth, AnchorStage)
= NiceRound(
    PlannedDefenseXPPerMinute(AnchorStage)
    × TargetRebirthMinutes(NextRebirth)
  )
```

- V1 계획용 CycleDefenseXP는 `400 × StageRewardScale`
- 실제 스테이지 작성 뒤 실제 BaseBudget 주기로 교체
- `NiceRound`는 세 자리 유효숫자
- 큰 값은 `MagnitudeNumber` 사용

세부 표는 `V1_REBIRTH_XP_BENCHMARK.md`를 따릅니다.

---

## 4. 환생 횟수 검증

중앙 스테이지 경로와 실제 성능 배분을 결합한 결과입니다.

| 활성 플레이 | 성능 미투자 | 균형형 | 성능 2 | 성능 집중 4 |
|---:|---:|---:|---:|---:|
| 30분 | 2 | 2 | 2 | 2 |
| 2시간 | 4 | 4 | 4 | 4 |
| 5시간 | 7 | 8 | 8 | 9 |
| 12시간 | 16 | 17 | 19 | 21 |
| 15시간 | 19 | 22 | 24 | 26 |
| 25시간 | 31 | 38 | 41 | 45 |
| 30시간 | 37 | **46** | 50 | 55 |

성능은 XP를 직접 배율하지 않지만 전투 주기를 단축해 환생도 간접적으로 빠르게 합니다. 계획 시뮬레이션은 clear-speed 효과를 `PerformanceMultiplier^0.60`으로 근사합니다.

---

## 5. 토큰 지급

### REB-008: 고정 지급량

```text
TokenReward = 4
```

환생 성공:

```text
RebirthCount +1
RebirthStatTokensEarned +4
UnspentRebirthStatTokens +4
DefenseXP = 0
```

- 첫 환생부터 매번 4개
- 무작위 추가 지급 없음
- 미사용 토큰 영구 이월
- 각 스탯 1포인트당 토큰 1개
- 자동 균등 배분 없음
- 환생 횟수 자체로 자동 배율을 주지 않음

### REB-009: 저장 데이터

```text
RebirthCount
RebirthXPAnchorStage
RebirthStatTokensEarned
UnspentRebirthStatTokens
RebirthStatAllocations[StatId]
RebirthRespecAvailable
```

불변조건:

```text
Σ(RebirthStatAllocations)
+ UnspentRebirthStatTokens
= RebirthStatTokensEarned
```

---

## 6. 네 가지 환생 스탯

### REB-010: 행운 — `REBIRTH_LUCK`

```text
LuckCompressionBonus(L)
= 0.0340 × min(L, 25)
+ 0.0040 × max(L - 25, 0)
```

```text
BaseCompression
= 1
+ 0.245 × (CurrentStage - 1)
+ LuckCompressionBonus(L)
+ TemporaryCompressionBonus
```

굴림 상한:

```text
일반 5.40
황금 5.65
다이아몬드 6.05
```

공식 기본 `1 / N`은 변경하지 않으며 현재 유효 확률은 표시하지 않습니다.

### REB-011: 성능 — `REBIRTH_PERFORMANCE`

```text
PerformanceMultiplier(P)
= min(
    2.50,
    1
    + 0.025 × min(P, 25)
    + 0.005 × max(P - 25, 0)
  )
```

- 모든 역할의 `EquivalentContribution`에 적용
- 피해 역할은 피해 중심
- 제어·지원·마무리는 역할별 기여 환산값에 적용
- 베이스와 몬스터 수치에는 적용하지 않음

### REB-012: 재화 — `REBIRTH_CURRENCY`

```text
CurrencyMultiplier(C)
= min(
    4.00,
    1
    + 0.040 × min(C, 25)
    + 0.010 × max(C - 25, 0)
  )
```

적용:

- 접속 중 코인
- 오프라인 코인

미적용:

- Defense XP
- 환생 토큰
- 타워 확률
- 연금 정수

### REB-013: 주사위 속도 — `REBIRTH_ROLL_SPEED`

```text
RollRateMultiplier(S)
= 1
+ 0.010 × min(S, 25)
+ 0.0025 × max(S - 25, 0)

FinalRollInterval
= max(
    2.00초,
    BaseRollInterval / RollRateMultiplier(S)
  )
```

- 코인 굴리기 속도 노드 뒤 적용
- 현재 Speed I 이후 BaseRollInterval은 3.6초
- V1 하한 2.0초
- 황금·다이아몬드 진행도도 실제 굴림 수만큼 빨라짐

---

## 7. 소프트캡 철학

- 첫 25포인트가 주 성장 구간
- 26포인트부터 감소 효율
- 성능 최대 ×2.50
- 재화 최대 ×4.00
- 굴리기 최소 2.00초
- 행운은 Compression 상한과 강한 후반 감소 효율

한 분야 집중을 금지하지 않지만 일정 지점부터 다른 분야 투자가 자연스럽게 경쟁력을 가져야 합니다.

---

## 8. 재분배

### REB-014: 사용과 유지

- 새 미사용 토큰은 언제든 배분 가능
- 기존 배분은 다음 환생 전까지 유지
- 환생 직후 전체 재분배 기회 1회
- 비용 없음
- 사용하지 않으면 기존 배분 유지

상시 재분배는 다음 행동을 유도하므로 사용하지 않습니다.

```text
공격 직전 성능
→ 처치 직전 재화
→ 굴림 직전 행운
→ 대기 중 주사위 속도
```

---

## 9. 환생 실행 결과

### REB-015: 초기화

```text
Defense XP만 0
```

초기화하지 않음:

- 코인
- 열린 문
- 현재 위치·스테이지
- 현재 웨이브·몬스터·보스·베이스
- 바닥 코인
- 타워 타겟·투사체·소환체
- 포션 활성 시간

### REB-016: 유지

- 보유 타워·보호·편성
- 도감·최초 획득 기록
- 코인 스탯 트리
- 합체·변종
- 굴림 횟수·특수 주사위 진행
- 연금 정수·포션
- 오프라인 업그레이드
- 열린 문·텔레포터 목적지
- 튜토리얼 완료 상태
- 환생 횟수·기준 스테이지·토큰·배분
- 설정

---

## 10. UI 흐름

환생 가능 상태:

- 현재 Defense XP / 요구량 / 진행률
- XP 기준 스테이지
- 이번 보상 스탯 토큰 4개
- Defense XP만 0이 된다는 설명
- 코인·문·현재 전투 유지
- 현재 네 분야 배분 요약

버튼:

```text
기존 배분 유지하고 환생
환생 후 전체 재분배
스탯 배분 보기
취소
```

기준 스테이지가 상승해 요구량이 재계산될 때는 막대 퍼센트가 유지되며, 짧게 `XP 기준: 스테이지 N`만 갱신합니다.

---

## 11. 저장과 원자성

환생:

```text
Defense XP 요구량 검증
→ 중복 TransactionId 검증
→ RebirthCount 증가
→ 토큰 누적 +4
→ 미사용 토큰 +4
→ Defense XP 0
→ 재분배 기회 설정
→ 중요 저장 큐
```

XP 기준 스테이지 상승:

```text
새 스테이지 XP 획득 검증
→ 기존 진행률 계산
→ RebirthXPAnchorStage 상승
→ 새 요구량 계산
→ Defense XP를 같은 진행률로 재조정
→ 같은 프로필 변경으로 저장
```

실패한 요청은 일부 값만 변경하지 않습니다.

---

## 12. 사용하지 않는 구조

- 환생 코인 비용
- 환생 시 코인 초기화
- 환생 시 문 재잠금
- 환생 시 로비 강제 이동
- 환생 시 웨이브·전투 초기화
- 단순 `7,000 × RebirthCount^지수`만으로 전체 구간 계산
- 높은 스테이지 첫 처치 시 진행률 하락
- 낮은 XP 요구량으로 높은 스테이지 XP 악용
- 환생 횟수만으로 자동 스탯 지급
- Defense XP 유료 직접 구매
- 오프라인 Defense XP
- 초과 XP로 여러 환생 즉시 연속 실행
- 전투 중 무제한 실시간 재분배

---

## 13. 남은 검증

- 스테이지 2~15 실제 주기 XP와 파밍 시간
- 실제 타워 분포에 따른 clear-speed 탄력성
- 실패·누수 시간이 환생 속도에 미치는 영향
- 빠른·느린 스테이지 경로
- 성능 배율의 역할별 런타임 변환
- 코인 포션·오프라인과 재화 배율의 중첩
- 후속 코인 굴리기 속도 노드
- 50회 이후 장기 환생 체감
