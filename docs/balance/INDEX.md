# Tower RNG 계산·검증 인덱스

- 상태: **Balance Calculations Complete · Runtime Measurement Pending**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 최종 계산 배치: `FINAL_BALANCE_BATCH.md`
- 최종 권고값: `FINAL_RECOMMENDATION.md`
- 채택 카탈로그: `../catalog/INDEX.md`
- 재현 스크립트: `../../tools/balance`

## 책임

```text
balance에서 계산·검증
→ catalog에서 최종 채택
→ spec·implementation에서 사용
→ Roblox 런타임에서 측정
```

수학적으로 수행 가능한 V1 밸런스 계산은 완료됐으며, 승인된 주요 값은 카탈로그에 채택됐습니다.

---

# 최종 상태

```text
최종 계산 단계 6 / 6 수행
수학 계산 완료 6 / 6
카탈로그 채택 완료
스테이지 수치 검증 15 / 15
실제 Roblox RuntimeEfficiency 측정 대기
```

| 문서 | 상태 | 책임 |
|---|---|---|
| `FINAL_BALANCE_BATCH.md` | 완료 | 최종 계산·채택 상태와 재계산 규칙 |
| `FINAL_RECOMMENDATION.md` | 채택 완료 | 계산값과 권위 카탈로그 연결 |
| `FINAL_ACCOUNT_PATHS.md` | 완료 | 10,000계정 완주 경로 |
| `FINAL_ECONOMY_INTEGRATION.md` | 완료 | 후반 선택 경제 통합 |
| `MASTERY_UTILITY_SINK_BENCHMARK.md` | 완료 | 숙련 제어실 25.2B와 30h 잔여 |
| `RUNTIME_LOSS_BUDGET.md` | 실측 대기 | Roblox 런타임 손실 예산 |

---

# 채택된 카탈로그

| 범위 | 권위 문서 |
|---|---|
| 스테이지 2~15 영구 문 | `../catalog/STAGE_GATE_CATALOG.md` |
| 초기 노드·슬롯·공통 전투 | `../catalog/STAT_TREE_CATALOG.md` |
| 변종·합체·오프라인·숙련 노드 | `../catalog/STAT_TREE_CATALOG.md` |
| 변종 티켓·PowerBudget·합체 조합 | `../catalog/TOWER_SYSTEM_CATALOG.md` |

계산 문서의 숫자가 바뀌어도 카탈로그를 별도로 갱신하지 않으면 실제 채택값은 바뀌지 않습니다.

---

# 확률·타워 성장

| 문서 | 책임 |
|---|---|
| `../reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 분모와 정확한 합 1 |
| `../reference/V1_TOP_TOWER_BENCHMARK.md` | 최고 일반 타워 `1/10^20` |
| `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축과 획득률 |
| `../reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 분포 |
| `../reference/TOWER_BALANCE_BENCHMARK.md` | 최저급 6역할 기준 기여도 |
| `V1_TOWER_VARIANT_BENCHMARK.md` | 변종 확률·전투력·코인 가지 |
| `V1_FUSION_BENCHMARK.md` | 합체 재료·배율·획득시간 |

---

# 환생·경제·편성

| 문서 | 책임 |
|---|---|
| `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | 첫 환생 경제 |
| `../reference/V1_REBIRTH_XP_BENCHMARK.md` | 환생 XP 곡선 |
| `../reference/V1_REBIRTH_STAT_BENCHMARK.md` | 네 분야 환생 스탯 |
| `../reference/V1_FORMATION_SLOT_BENCHMARK.md` | 4→12슬롯과 역할 상한 |
| `../reference/V1_COIN_COMBAT_BENCHMARK.md` | 독립 전투 성장 |
| `V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투 통합 경제 |
| `SUPPORT_CONTROL_STACKING_BENCHMARK.md` | 지원·제어 중첩 |
| `OFFLINE_COIN_BENCHMARK.md` | 오프라인 코인 |
| `FINAL_ECONOMY_INTEGRATION.md` | 선택 가지 통합 |
| `MASTERY_UTILITY_SINK_BENCHMARK.md` | 최종 숙련 싱크 |

채택된 영구 싱크:

```text
문·슬롯·전투  36.3968252B
변종           25.0185B
합체            2.75025B
오프라인        3.1201B
숙련 제어실    25.2000B
합계           92.4856752B
```

30시간 잔여:

```text
문 우선        4.870B
균형형         0.034B
전투 우선      0.648B
슬롯 우선      0.648B
코인 실현 70%  3.798B
```

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
스테이지 수치 검증 15 / 15
Stage15 FirstClearEC 10,050
Stage15 StableFarmEC 12,200
```

---

# 완주 결과

```text
빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
중앙 안정 파밍 약 13.5h
```

특정 극희귀, 변종 또는 합체 결과는 완주 필수가 아닙니다.

---

# 주요 재현 스크립트

```text
tower_baseline.py
v1_probability_ladder.py
v1_luck_compression.py
v1_rebirth_xp_curve.py
rebirth_stat_tokens.py
v1_roster_power_distribution.py
v1_formation_slot_economy.py
v1_coin_combat_curve.py
v1_gate_economy.py
support_control_stacking.py
v1_tower_variant_benchmark.py
v1_fusion_benchmark.py
offline_coin_benchmark.py
runtime_loss_budget.py
final_economy_integration.py
mastery_utility_sink.py
final_account_paths.py
```

스테이지는 `stage1_wave_sim.py`부터 `stage15_action_wave_sim.py`까지의 개별 도구를 사용합니다.

---

# 다음 작업

```text
CAT-NEXT-002
스테이지 1~15 계산용 웨이브를 최종 StageId·MonsterId 카탈로그로 채택
```

별도 실측:

```text
RUN-NEXT-001
지역 1 수직 슬라이스에서 RuntimeEfficiency 측정
```
