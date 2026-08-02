# Tower RNG 계산·검증 인덱스

- 상태: **Active Balance Index**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 콘텐츠 카탈로그: `../catalog/INDEX.md`
- 재현 스크립트: `../../tools/balance`

## 책임

`docs/balance`는 수치가 필요한 이유, 입력·가정, 재현 방법과 수용 조건을 소유합니다.

```text
balance에서 계산
→ 수용 조건 통과
→ catalog에서 최종 채택
→ implementation에 반영
→ Roblox 런타임 검증
```

계산용 이름과 외형은 카탈로그 완료로 세지 않습니다. 기존 계산 문서는 링크 호환을 위해 일부 `docs/reference`에 남아 있으며 새 계산 문서는 `docs/balance`에만 작성합니다.

---

# 현재 계산 문서

## 확률·타워 성장

| 문서 | 책임 |
|---|---|
| `../reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 분모와 정확한 합 |
| `../reference/V1_TOP_TOWER_BENCHMARK.md` | 최고 일반 타워 기준 |
| `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축과 획득률 |
| `../reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 분포 |
| `../reference/TOWER_BALANCE_BENCHMARK.md` | 최저급 6역할 기준 기여도 |

## 환생·경제·편성

| 문서 | 책임 |
|---|---|
| `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | 첫 환생 경제 |
| `../reference/V1_REBIRTH_XP_BENCHMARK.md` | 이후 환생 XP 곡선 |
| `../reference/V1_REBIRTH_STAT_BENCHMARK.md` | 네 분야 환생 스탯 |
| `../reference/V1_FORMATION_SLOT_BENCHMARK.md` | 4→12슬롯 가격과 역할 상한 |
| `../reference/V1_COIN_COMBAT_BENCHMARK.md` | 독립 전투 성장 구성요소 |
| `V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투·유연 예산 통합 경제 |

현재 통합 경제 권고안:

```text
스테이지 4~15 문 누적 가격: 1,302,495,000
균형형 스테이지 15 문: 약 12.05시간
균형형 12슬롯 + 전투 ×4.50: 약 12.91시간
전투 ×5.00 최종 노드: 30,000,000,000
균형형 전투 ×5.00: 약 20.39시간
```

위 가격은 아직 카탈로그 채택 전입니다.

## 스테이지 전투

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
| `../reference/STAGE15_WAVE_BENCHMARK.md` | 집계 완전 | 완료·행동형 재검증 예정 |

현재 범위:

```text
행동형 검증 완료: 스테이지 1~12
집계 검증 완료: 스테이지 15
미완료: 스테이지 13·14, 스테이지 15 행동형
수치상 완료 스테이지: 13 / 15
```

최근 실측:

```text
S7  계획 68초 → 실제 68.82초
S8  계획 75초 → 실제 74.96초
S9  계획 82초 → 실제 81.98초
S10 계획 76초 → 실제 75.74초
S11 계획 84초 → 실제 84.25초
S12 계획 90초 → 실제 90.25초
```

---

# 재현 스크립트

## 성장·경제

| 경로 | 책임 |
|---|---|
| `../../tools/balance/tower_baseline.py` | 최저급 6역할 기여도 |
| `../../tools/balance/v1_probability_ladder.py` | 공식 확률 합 |
| `../../tools/balance/v1_luck_compression.py` | 행운 압축 |
| `../../tools/balance/v1_rebirth_xp_curve.py` | 환생 XP 곡선 |
| `../../tools/balance/rebirth_stat_tokens.py` | 환생 스탯·굴림 통합 |
| `../../tools/balance/v1_roster_power_distribution.py` | 보유 전력 분포 |
| `../../tools/balance/v1_formation_slot_economy.py` | 슬롯 경제 |
| `../../tools/balance/v1_coin_combat_curve.py` | 독립 코인 전투 성장 |
| `../../tools/balance/v1_gate_economy.py` | 문·슬롯·전투 통합 경제 |

## 스테이지

| 경로 | 책임 |
|---|---|
| `../../tools/balance/stage1_wave_sim.py` | 스테이지 1 |
| `../../tools/balance/stage2_wave_sim.py` | 스테이지 2 |
| `../../tools/balance/stage3_wave_sim.py` | 스테이지 3 |
| `../../tools/balance/stage4_5_light_sim.py` | 스테이지 4·5 |
| `../../tools/balance/stage6_wave_sim.py` | 스테이지 6 |
| `../../tools/balance/stage7_8_light_sim.py` | 스테이지 7·8 |
| `../../tools/balance/stage9_wave_sim.py` | 스테이지 9 |
| `../../tools/balance/stage10_11_light_sim.py` | 스테이지 10·11 |
| `../../tools/balance/stage12_wave_sim.py` | 스테이지 12 |
| `../../tools/balance/stage15_wave_sim.py` | 스테이지 15 집계 검증 |
| `../../tools/balance/stage_validation_plan.py` | 검증 깊이와 계획 주기 |

---

# 완료된 계산 묶음

```text
[x] 정확한 합 1의 50자리 확률 사다리
[x] 최고 일반 타워 1/10^20
[x] 행운 압축과 누적 획득률
[x] 첫 환생과 이후 환생 XP
[x] 환생 토큰 네 분야
[x] 시간대별 굴림·보유 전력 분포
[x] 4→12슬롯과 역할 상한
[x] 코인 전투 ×1.25→×5.00
[x] 스테이지 4~15 문 가격 권고안
[x] 문·슬롯·전투 통합 경제와 소비 전략
[x] 스테이지 1~12 행동형 전투 검증
[x] 스테이지 15 15h/30h 집계 클리어
```

---

# 남은 계산 체크리스트

## 경제

- [ ] 오프라인 코인 민감도
- [~] 20~30시간 후반 코인 과잉과 반복 싱크
- [ ] 합체·변종·편의 가격을 포함한 최종 코인 싱크 검사

## 스테이지

- [ ] 스테이지 15 용암지대 행동형 완전 검증
- [ ] 스테이지 13·14 용암지대 경량 검증

## 전투 확장

- [ ] 지원 중첩
- [ ] 제어 중첩과 감쇠
- [ ] 변종 전투력·획득률
- [ ] 합체 비용·획득시간·전투력
- [ ] 런타임 오버킬·투사체·타겟 전환 손실

## 최종 통합

- [ ] P10/P50/P90 전 계정 경로 재실행
- [ ] 빠른·중앙·느린 완주 시간 검증
- [ ] 20~30시간 숙련 파밍 검증
- [ ] 카탈로그 채택용 최종 권고값 묶음

---

# 현재 다음 계산

```text
BAL-NEXT-006
스테이지 15 용암지대 실제 행동형 완전 검증
```

기존에는 스테이지 13·14를 먼저 작성하려 했지만, 경량 스테이지가 재사용할 용암 행동이 아직 완전 검증되지 않았습니다. 따라서 다음 순서를 사용합니다.

```text
스테이지 15 행동형 완전 검증
→ 용암 행동과 예산 경계 확정
→ 스테이지 13·14 경량 검증
→ 지원·제어·변종·합체
→ 최종 통합과 카탈로그 채택
```

---

# 작성 규칙

- 모든 계산은 입력·가정·수용 조건·재현 경로를 기록합니다.
- 계산용 임시 이름은 카탈로그 완료로 세지 않습니다.
- 새 계산 문서는 `docs/balance`에 작성합니다.
- 완료 시 `PROJECT_STATUS.md`를 같은 작업에서 갱신합니다.
- 실제 콘텐츠 값은 별도 카탈로그 채택 단계를 거칩니다.
