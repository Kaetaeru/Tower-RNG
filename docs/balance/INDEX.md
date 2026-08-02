# Tower RNG 계산·검증 인덱스

- 상태: **Active Balance Index**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 최종 권고값: `FINAL_RECOMMENDATION.md`
- 콘텐츠 카탈로그: `../catalog/INDEX.md`
- 재현 스크립트: `../../tools/balance`

## 책임

```text
balance에서 계산
→ catalog에서 최종 채택
→ implementation에 반영
→ Roblox 런타임 검증
```

계산용 이름과 임시 가격은 카탈로그 완료로 세지 않습니다. 기존 `docs/reference`는 링크 호환 영역이며 새 계산 문서는 `docs/balance`에만 작성합니다.

---

# 최종 배치

| 문서 | 상태 | 책임 |
|---|---|---|
| `FINAL_BALANCE_BATCH.md` | 계산 6/6 수행 | 최종 계산 순서와 체크리스트 |
| `FINAL_RECOMMENDATION.md` | 완료 | 카탈로그 채택 후보값 묶음 |
| `V1_FUSION_BENCHMARK.md` | 완료 | 수동 합체 재료·배율·가격·획득시간 |
| `RUNTIME_LOSS_BUDGET.md` | 조건부 | Roblox 잔여 손실 예산, 실측 대기 |
| `OFFLINE_COIN_BENCHMARK.md` | 완료 | 오프라인 기준·효율·상한·가격 |
| `FINAL_ECONOMY_INTEGRATION.md` | 조건부 | 후반 선택 경제와 추가 싱크 요구량 |
| `FINAL_ACCOUNT_PATHS.md` | 완료 | 빠른·중앙·느린 완주 경로 |

현재 판정:

```text
계산 수행 6 / 6
완전 완료 4
조건부 완료 2
```

조건부 항목:

```text
실제 Roblox RuntimeEfficiency 측정
추가 15~25B 숙련 코인 싱크의 콘텐츠 정체성
```

---

# 확률·타워 성장

| 문서 | 책임 |
|---|---|
| `../reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 분모와 정확한 합 |
| `../reference/V1_TOP_TOWER_BENCHMARK.md` | 최고 일반 타워 기준 |
| `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축과 획득률 |
| `../reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 분포 |
| `../reference/TOWER_BALANCE_BENCHMARK.md` | 최저급 6역할 기준 기여도 |
| `V1_TOWER_VARIANT_BENCHMARK.md` | 변종 확률·전투력·해금·코인 가지 |
| `V1_FUSION_BENCHMARK.md` | 중복 합체와 슬롯 압축 |

---

# 환생·경제·편성

| 문서 | 책임 |
|---|---|
| `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | 첫 환생 경제 |
| `../reference/V1_REBIRTH_XP_BENCHMARK.md` | 이후 환생 XP 곡선 |
| `../reference/V1_REBIRTH_STAT_BENCHMARK.md` | 네 분야 환생 스탯 |
| `../reference/V1_FORMATION_SLOT_BENCHMARK.md` | 4→12슬롯과 역할 상한 |
| `../reference/V1_COIN_COMBAT_BENCHMARK.md` | 독립 전투 성장 |
| `V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투 통합 경제 |
| `SUPPORT_CONTROL_STACKING_BENCHMARK.md` | 지원·제어 중첩과 한계 기여 |
| `OFFLINE_COIN_BENCHMARK.md` | 오프라인 코인 |
| `FINAL_ECONOMY_INTEGRATION.md` | 전체 선택 가지 통합 |

현재 주요 가격 권고:

```text
스테이지 4~15 문        1,302,495,000
편성 슬롯 5~12          2,790,686,200
전투 III~XI            32,303,644,000
변종 가지              25,018,500,000
합체 가지               2,750,250,000
오프라인 가지           3,120,100,000
현재 전체 영구 싱크     67,285,675,200
```

추가 선택형 숙련 싱크 `15~25B`가 필요합니다.

---

# 스테이지 전투

| 문서 | 깊이 | 상태 |
|---|---|---|
| `../reference/STAGE1_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `../reference/STAGE2_WAVE_BENCHMARK.md` | 추가 완전 | 완료 |
| `../reference/STAGE3_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `../reference/STAGE4_5_LIGHT_BENCHMARK.md` | 경량 | 완료 |
| `../reference/STAGE6_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `STAGE7_8_LIGHT_BENCHMARK.md` | 경량 | 완료 |
| `STAGE9_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `STAGE10_11_LIGHT_BENCHMARK.md` | 경량 | 완료 |
| `STAGE12_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `STAGE13_14_LIGHT_BENCHMARK.md` | 경량 | 완료 |
| `STAGE15_ACTION_WAVE_BENCHMARK.md` | 행동형 완전 | 완료 |
| `RUNTIME_LOSS_BUDGET.md` | 구현 예산 | 실측 대기 |

```text
스테이지 수치 검증: 15 / 15
```

---

# 최종 완주 결과

`FINAL_ACCOUNT_PATHS.md`의 10,000계정 결과:

```text
빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
중앙 안정 파밍 약 13.5h
```

```text
Stage15 FirstClearEC = 10,050
Stage15 StableFarmEC = 12,200
```

변종과 합체는 완주 필수 전력에서 제외했습니다.

---

# 재현 스크립트

## 성장·경제·편성

| 경로 | 책임 |
|---|---|
| `../../tools/balance/tower_baseline.py` | 최저급 6역할 기여도 |
| `../../tools/balance/v1_probability_ladder.py` | 공식 확률 합 |
| `../../tools/balance/v1_luck_compression.py` | 행운 압축 |
| `../../tools/balance/v1_rebirth_xp_curve.py` | 환생 XP |
| `../../tools/balance/rebirth_stat_tokens.py` | 환생 스탯·굴림 통합 |
| `../../tools/balance/v1_roster_power_distribution.py` | 보유 전력 분포 |
| `../../tools/balance/v1_formation_slot_economy.py` | 슬롯 경제 |
| `../../tools/balance/v1_coin_combat_curve.py` | 코인 전투 성장 |
| `../../tools/balance/v1_gate_economy.py` | 문·슬롯·전투 통합 경제 |
| `../../tools/balance/support_control_stacking.py` | 지원·제어 중첩 |
| `../../tools/balance/v1_tower_variant_benchmark.py` | 변종 |
| `../../tools/balance/v1_fusion_benchmark.py` | 합체 |
| `../../tools/balance/offline_coin_benchmark.py` | 오프라인 코인 |
| `../../tools/balance/runtime_loss_budget.py` | 런타임 손실 예산 |
| `../../tools/balance/final_economy_integration.py` | 후반 경제 통합 |
| `../../tools/balance/final_account_paths.py` | 전체 계정 경로 |

## 스테이지

기존 `stage1_wave_sim.py`부터 `stage15_action_wave_sim.py`까지의 개별 도구를 사용합니다.

---

# 다음 작업

계산 기준으로 카탈로그 채택을 시작할 수 있습니다.

```text
CAT-NEXT-001
문·슬롯·전투·변종·합체·오프라인 권고값 채택 검토
```

별도 미완료:

```text
DES-NEXT-001 추가 15~25B 숙련 싱크 정체성
RUN-NEXT-001 지역 1 수직 슬라이스 런타임 측정
```
