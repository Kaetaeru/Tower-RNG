# 환생 기획

- 계층: 게임 기획
- 상태: **Confirmed (Living Document)**
- 필수 참고: `../../AGENTS.md`
- 관련 문서: `BALANCE_MODEL.md`, `STAT_TREE.md`, `CURRENCY.md`, `ROLLING.md`, `LEVEL_DESIGN.md`, `TUTORIAL.md`, `PROGRESSION.md`, `ECONOMY_PACING.md`, `OFFLINE_PROGRESS.md`, `WORLD_NAVIGATION.md`, `RNG_PROBABILITY.md`, `../technical/STATE_LIFECYCLE.md`, `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md`, `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md`, `../reference/V1_REBIRTH_STAT_BENCHMARK.md`
- 하위 문서 예정: `../spec/REBIRTH.md`
- 마지막 정리: 2026-08-02

## 요약

환생은 진행을 처음으로 되돌리는 프레스티지가 아니라, 전투로 모은 **Defense XP를 영구 스탯 토큰으로 전환하는 연속 성장 행동**입니다.

환생 시 초기화되는 영구 상태는 Defense XP뿐입니다.

```text
유지
- 코인
- 열린 스테이지 문
- 현재 위치와 활성 스테이지
- 현재 웨이브와 전투
- 타워·스탯·도감·합체·변종

변경
- Defense XP → 0
- RebirthCount +1
- 환생 스탯 토큰 4개 지급
```

토큰은 다음 네 분야에 배분합니다.

```text
행운
성능
재화
주사위 속도
```

첫 환생 요구량은 `7,000 Defense XP`이며 기존 첫 경제 벤치마크의 도달 시간 `7.80~14.34분`은 그대로 유효합니다. 환생 뒤 코인과 문을 다시 모으는 이전 순환 구조는 사용하지 않습니다.

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

첫 버전은 별도 웨이브 완료 XP 보너스를 사용하지 않습니다.

### REB-002: 실행 조건

```text
현재 Defense XP >= 다음 환생 요구 XP
→ 환생 가능
```

- 자동 실행 없음
- 전투 중에도 원하는 시점에 실행 가능
- 요구량을 채운 뒤 계속 파밍 가능
- 초과 XP는 환생 시 기본적으로 이월하지 않음

---

## 2. 요구량과 시간

### REB-003: 첫 환생

```text
FirstRebirthXP = 7,000
```

| 소비 성향 | 첫 환생 범위 |
|---|---:|
| 균형 소비 | 7.96~13.41분 |
| 문 우선 | 7.80~14.34분 |
| 트리 우선 | 9.63~12.70분 |

첫 환생까지의 경제·전투 계산은 변경되지 않습니다. 첫 환생은 진행 초기화가 아니라 첫 토큰 4개를 얻는 시점입니다.

### REB-004: 이후 환생

초기 방향:

- 두 번째 환생 약 15~25분 목표
- 초기 여러 회 약 20~40분 중심
- 중기 이후 점진적으로 증가
- 고정 대기시간·일일 제한 없음

초기 요구량 후보:

```text
RequiredDefenseXP(r)
= 7,000 × (r + 1)^1.65
```

첫 항만 검증되었습니다. 코인·문 초기화가 사라졌으므로 지수 `1.65`는 새 연속 진행 모델에서 다시 시뮬레이션한 뒤 확정합니다.

---

## 3. 토큰 지급

### REB-005: 고정 지급량

```text
TokenReward = 4
```

환생 성공:

```text
RebirthCount +1
UnspentRebirthStatTokens +4
DefenseXP = 0
```

- 첫 환생부터 매번 4개
- 무작위 추가 지급 없음
- 미사용 토큰 영구 이월
- 각 스탯 1포인트당 토큰 1개
- 자동 균등 배분 없음
- 환생 횟수 자체로 자동 배율을 주지 않음

4개를 사용하는 이유:

- 균형형은 매 환생 네 분야에 한 개씩 투자 가능
- 집중형은 한 분야에 네 개 전부 투자 가능
- 배분 선택이 첫 환생부터 즉시 보임

### REB-006: 저장 데이터

```text
RebirthStatTokensEarned
UnspentRebirthStatTokens
RebirthStatAllocations[StatId]
```

불변조건:

```text
Σ(RebirthStatAllocations)
+ UnspentRebirthStatTokens
= RebirthStatTokensEarned
```

---

## 4. 네 가지 환생 스탯

### REB-007: 행운 — `REBIRTH_LUCK`

```text
LuckCompressionBonus(L)
= 0.0315 × min(L, 25)
+ 0.0090 × max(L - 25, 0)
```

전체 공식:

```text
BaseCompression
= 1
+ 0.245 × (CurrentStage - 1)
+ LuckCompressionBonus(L)
+ TemporaryCompressionBonus
```

굴림 종류별 상한:

```text
일반 5.40
황금 5.65
다이아몬드 6.05
```

공식 기본 `1 / N`은 변경하지 않으며 현재 유효 확률은 표시하지 않습니다.

### REB-008: 성능 — `REBIRTH_PERFORMANCE`

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
- 공격속도만 올리는 별도 배율이 아님
- 베이스와 몬스터 수치에는 적용하지 않음

### REB-009: 재화 — `REBIRTH_CURRENCY`

```text
CurrencyMultiplier(C)
= min(
    4.00,
    1
    + 0.040 × min(C, 25)
    + 0.010 × max(C - 25, 0)
  )
```

V1 적용 대상:

- 접속 중 획득 코인
- 오프라인 코인

적용하지 않음:

- Defense XP
- 환생 스탯 토큰
- 타워 획득 확률
- 연금 정수

### REB-010: 주사위 속도 — `REBIRTH_ROLL_SPEED`

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

- 코인 굴리기 속도 노드가 만든 BaseRollInterval에 적용
- 현재 `굴리기 속도 I` 이후 BaseRollInterval은 3.6초
- V1 최소 간격 2.0초
- 실제 굴림이 늘어나므로 황금·다이아몬드 진행도도 빨라짐

세부 표와 시뮬레이션은 `V1_REBIRTH_STAT_BENCHMARK.md`를 따릅니다.

---

## 5. 소프트캡 철학

네 분야 모두 첫 25포인트의 증가량이 큽니다.

- 1~25포인트: 주 성장 구간
- 26포인트 이후: 감소 효율
- 성능 최대 ×2.50
- 재화 최대 ×4.00
- 굴리기 최소 2.00초
- 행운은 Compression 상한으로 제한

한 분야 집중을 금지하지 않습니다. 다만 일정 지점 이후 다른 분야에 투자하는 것이 자연스럽게 효율적이어야 합니다.

---

## 6. 재분배

### REB-011: 사용과 유지

- 새로 받은 미사용 토큰은 언제든 배분 가능
- 기존 배분은 다음 환생 전까지 유지
- 환생을 실행한 직후 전체 재분배 기회 1회 제공
- 재분배 비용 없음
- 선택하지 않으면 기존 배분 그대로 유지

### REB-012: 제한 이유

상시 무료 재분배는 다음 행동을 유도할 수 있으므로 사용하지 않습니다.

```text
공격 직전 성능 몰입
→ 처치 직전 재화 몰입
→ 굴림 직전 행운 몰입
→ 즉시 주사위 속도 몰입
```

재분배를 환생 시점으로 제한하면 빌드 선택은 유지하면서 영구 실수를 방지할 수 있습니다.

---

## 7. 환생 실행 결과

### REB-013: 초기화

```text
Defense XP만 0으로 초기화
```

초기화하지 않음:

- 코인
- 열린 문
- 최고 도달 스테이지
- 마지막 활동 스테이지
- 현재 위치
- 현재 웨이브·몬스터·보스·베이스
- 바닥 코인
- 타워 타겟·투사체·소환체
- 포션 활성 시간

환생 때문에 로비로 이동하거나 웨이브 1로 되돌리지 않습니다.

### REB-014: 유지

- 보유 타워·보호·편성
- 도감·최초 획득 기록
- 코인 스탯 트리 노드
- 합체·변종 진행
- 굴림 횟수와 특수 주사위 진행
- 연금 정수와 포션
- 오프라인 업그레이드
- 열린 문과 텔레포터 목적지
- 최초 튜토리얼 완료 상태
- 환생 횟수·토큰·배분
- 설정

---

## 8. UI 흐름

환생 가능 상태 표시:

- 현재 Defense XP와 요구량
- 이번 환생 보상 `스탯 토큰 4개`
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

환생 직후:

```text
토큰 4개 획득 연출
→ 미사용 토큰 갱신
→ 선택했다면 전체 재분배 화면
→ 현재 전투 계속
```

연출은 자동 전투와 굴리기를 장시간 멈추지 않습니다.

---

## 9. 저장과 원자성

환생은 하나의 원자적 프로필 변경입니다.

```text
Defense XP 요구량 검증
→ 중복 TransactionId 검증
→ RebirthCount 증가
→ RebirthStatTokensEarned +4
→ UnspentRebirthStatTokens +4
→ Defense XP 0
→ 재분배 기회 플래그 설정
→ 중요 저장 큐 등록
```

토큰 배분과 재분배도 서버 권위로 처리합니다. 실패한 요청은 토큰 또는 기존 배분을 변경하지 않습니다.

---

## 10. 사용하지 않는 구조

- 환생 코인 비용
- 환생 시 코인 초기화
- 환생 시 문 재잠금
- 환생 시 로비 강제 이동
- 환생 시 웨이브·전투 초기화
- 환생 횟수에 따른 자동 고정 스탯 지급
- Defense XP 유료 직접 구매
- 오프라인 Defense XP
- 초과 XP로 여러 환생 즉시 연속 실행
- 타워·도감·코인 스탯·합체·변종 초기화
- 환생 실패 확률과 무작위 토큰 보상
- 전투 중 무제한 실시간 재분배

---

## 11. 남은 검증

- 새 연속 진행 구조의 두 번째 이후 Defense XP 요구량
- 실제 환생 횟수와 토큰 획득 속도
- 성능 배율의 역할별 런타임 변환
- 코인 포션·오프라인과 재화 배율의 중첩 순서
- 후속 코인 굴리기 속도 노드
- 토큰 배분별 스테이지 15 도달 시간
- 환생·재분배 UI 실제 조작성
