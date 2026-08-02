# V1 영구 스테이지 문 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed**
- 카탈로그 버전: `V1-2026-08-03`
- 계산 근거: `../balance/V1_GATE_ECONOMY_BENCHMARK.md`, `../balance/FINAL_RECOMMENDATION.md`
- 상위 기획: `../design/WORLD_NAVIGATION.md`, `../design/ECONOMY_PACING.md`
- 구현 상태: **Not Implemented**
- 마지막 정리: 2026-08-03

## 책임

이 문서는 스테이지 2~15를 여는 영구 문의 실제 ID와 코인 가격을 소유합니다.

```text
BalanceStatus = Confirmed
ImplementationStatus = Not Implemented
```

가격을 변경하려면 `docs/balance`의 통합 경제와 전체 계정 경로를 다시 검증한 뒤 이 카탈로그를 명시적으로 갱신해야 합니다.

---

# 공통 규칙

- 이전 스테이지 문을 먼저 열어야 합니다.
- 구매는 계정당 한 번만 수행합니다.
- 입장할 때 반복 비용을 받지 않습니다.
- 코인 차감과 문 해금을 하나의 서버 권위 프로필 변경으로 처리합니다.
- 접속 종료, 서버 이동과 환생 후에도 해금 상태를 유지합니다.
- 다른 플레이어의 문 상태는 내 계정에 영향을 주지 않습니다.
- Robux로 문을 직접 우회하거나 구매하지 않습니다.
- 문 구매는 해당 스테이지의 전투 클리어를 의미하지 않습니다.

---

# 채택 데이터

| GateId | OpensStageId | 표시 이름 | 가격 | BalanceStatus | ImplementationStatus |
|---|---|---|---:|---|---|
| `GATE_STAGE_02` | `STAGE_02` | 스테이지 2 문 | 750 | Confirmed | Not Implemented |
| `GATE_STAGE_03` | `STAGE_03` | 스테이지 3 문 | 3,200 | Confirmed | Not Implemented |
| `GATE_STAGE_04` | `STAGE_04` | 스테이지 4 문 | 15,000 | Confirmed | Not Implemented |
| `GATE_STAGE_05` | `STAGE_05` | 스테이지 5 문 | 60,000 | Confirmed | Not Implemented |
| `GATE_STAGE_06` | `STAGE_06` | 스테이지 6 문 | 120,000 | Confirmed | Not Implemented |
| `GATE_STAGE_07` | `STAGE_07` | 스테이지 7 문 | 300,000 | Confirmed | Not Implemented |
| `GATE_STAGE_08` | `STAGE_08` | 스테이지 8 문 | 1,500,000 | Confirmed | Not Implemented |
| `GATE_STAGE_09` | `STAGE_09` | 스테이지 9 문 | 3,000,000 | Confirmed | Not Implemented |
| `GATE_STAGE_10` | `STAGE_10` | 스테이지 10 문 | 7,500,000 | Confirmed | Not Implemented |
| `GATE_STAGE_11` | `STAGE_11` | 스테이지 11 문 | 30,000,000 | Confirmed | Not Implemented |
| `GATE_STAGE_12` | `STAGE_12` | 스테이지 12 문 | 60,000,000 | Confirmed | Not Implemented |
| `GATE_STAGE_13` | `STAGE_13` | 스테이지 13 문 | 150,000,000 | Confirmed | Not Implemented |
| `GATE_STAGE_14` | `STAGE_14` | 스테이지 14 문 | 250,000,000 | Confirmed | Not Implemented |
| `GATE_STAGE_15` | `STAGE_15` | 스테이지 15 문 | 800,000,000 | Confirmed | Not Implemented |

스테이지 4~15 문의 채택 가격 합계:

```text
1,302,495,000
```

스테이지 2·3 문을 포함한 전체 합계:

```text
1,302,498,950
```

---

# 저장 계약

최소 저장 데이터:

```text
UnlockedStageGates[GateId] = true
HighestUnlockedStageId
```

구매 처리:

```text
GateId와 이전 문 검증
→ 현재 코인 검증
→ 코인 차감
→ GateId 영구 해금
→ HighestUnlockedStageId 갱신
→ 중요 저장 예약
```

동일 요청 재전송 시 이미 열린 문을 다시 결제하지 않습니다.

---

# 아직 미작성인 콘텐츠

다음 항목은 가격 채택과 별개이며 향후 전체 스테이지 카탈로그에서 작성합니다.

- 각 스테이지의 최종 플레이어 표시 이름
- 문의 월드 좌표와 실제 모델
- 잠금·해금 애니메이션과 음향
- 문 주변 랜드마크와 빠른 복귀 지점
- 모바일·PC 상호작용 UI

표시 이름이 나중에 바뀌어도 `GateId`, `OpensStageId`와 채택 가격은 유지합니다.
