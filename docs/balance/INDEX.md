# Tower RNG 계산·검증 인덱스

- 상태: **Active Balance Index**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 콘텐츠 카탈로그: `../catalog/INDEX.md`
- 재현 스크립트: `../../tools/balance`

## 책임

계산·검증 문서는 수치가 왜 필요한지, 어떤 조건에서 통과했는지를 소유합니다.

포함:

- 수식과 가정
- 시뮬레이션 입력
- 계정 프로필과 분위수
- 처리시간·누수·경제 결과
- 민감도 분석
- 수용 조건과 실패 조건
- 재현 스크립트 경로
- 카탈로그에 권장하는 값

포함하지 않음:

- 최종 콘텐츠 이름을 확정하는 권한
- 모델·애니메이션·자산의 최종 채택
- 구현 데이터의 독립 원본
- 계산 없이 작성한 콘텐츠 목록

계산 문서는 값을 추천합니다. 실제 게임에 들어가는 값은 `docs/catalog`가 채택합니다.

---

## 계산 문서 상태

기존 계산 문서는 링크 호환을 위해 잠시 `docs/reference`에 남아 있습니다. 새 계산 문서는 이 폴더에만 작성합니다.

### 확률·타워 성장

| 문서 | 책임 |
|---|---|
| `../reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 분모와 정확한 합 |
| `../reference/V1_TOP_TOWER_BENCHMARK.md` | 최고 일반 타워 기준 |
| `../reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축과 획득률 |
| `../reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 분포 |
| `../reference/TOWER_BALANCE_BENCHMARK.md` | 최저급 6역할 기준 기여도 |

### 환생·경제·편성

| 문서 | 책임 |
|---|---|
| `../reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | 첫 7,000 XP와 초기 구매 |
| `../reference/V1_REBIRTH_XP_BENCHMARK.md` | 이후 환생 XP 곡선 |
| `../reference/V1_REBIRTH_STAT_BENCHMARK.md` | 네 분야 환생 스탯 |
| `../reference/V1_FORMATION_SLOT_BENCHMARK.md` | 4→12슬롯 가격과 역할 제한 |
| `../reference/V1_COIN_COMBAT_BENCHMARK.md` | 코인 전투 성장의 독립 구성요소 계산 |
| `V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투·유연 예산 통합과 소비 전략 비교 |

통합 경제의 가격 우선순위:

```text
V1_GATE_ECONOMY_BENCHMARK.md
→ 문 가격과 코인 전투 XI 가격의 현재 계산 권고안

기존 V1_COIN_COMBAT_BENCHMARK.md
→ 독립 전투 예산 구성요소와 배율 단계 참고
```

### 스테이지 전투

| 문서 | 검증 깊이 | 상태 |
|---|---|---|
| `../reference/STAGE1_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `../reference/STAGE2_WAVE_BENCHMARK.md` | 추가 완전 | 완료 |
| `../reference/STAGE3_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `../reference/STAGE4_5_LIGHT_BENCHMARK.md` | 경량 | 완료 |
| `../reference/STAGE6_WAVE_BENCHMARK.md` | 완전 | 완료 |
| `../reference/STAGE15_WAVE_BENCHMARK.md` | 집계 완전 | 완료·행동형 재검증 예정 |

---

## 재현 스크립트

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
| `../../tools/balance/v1_gate_economy.py` | 문·슬롯·전투 통합 코인 경제 |
| `../../tools/balance/stage1_wave_sim.py` | 스테이지 1 |
| `../../tools/balance/stage2_wave_sim.py` | 스테이지 2 |
| `../../tools/balance/stage3_wave_sim.py` | 스테이지 3 |
| `../../tools/balance/stage4_5_light_sim.py` | 스테이지 4·5 |
| `../../tools/balance/stage6_wave_sim.py` | 스테이지 6 |
| `../../tools/balance/stage15_wave_sim.py` | 스테이지 15 집계 검증 |
| `../../tools/balance/stage_validation_plan.py` | 검증 깊이와 계획 주기 |

---

## 완료된 계산 묶음

```text
- 정확한 합 1의 50자리 확률 사다리
- 최고 일반 타워 1/10^20
- 스테이지·환생 행운 압축
- 첫 환생과 이후 환생 XP
- 환생 토큰 네 분야
- 시간대별 굴림·보유 전력 분포
- 4→12슬롯과 역할 상한
- 코인 전투 ×1.25→×5.00
- 스테이지 4~15 문 가격 권고안
- 문·슬롯·전투·유연 예산 통합 12~15시간 경제
- 문 우선·전투 우선·슬롯 우선 소비 전략 비교
- 합리적 재분배에서도 ×5.00을 약 20시간에 유지하는 최종 전투 노드 가격
- 스테이지 1~6 전투 주기
- 스테이지 15 15h/30h 집계 클리어
```

---

## 남은 계산 체크리스트

### 경제

- [x] 스테이지 4~15 문 가격
- [x] 전체 12~15시간 핵심 코인 흐름
- [x] 소비 전략별 도달시간
- [ ] 오프라인 코인 민감도
- [~] V1 코인 과잉·부족 검사

현재 확인된 경제 후속 문제:

```text
20~30시간에는 문·슬롯·공통 전투 성장 이후 큰 잔여 코인이 발생
→ 합체·변종·편의·수집 엔드게임 코인 싱크가 필요
```

### 스테이지

- [ ] 스테이지 9 완전 검증
- [ ] 스테이지 7·8 경량 검증
- [ ] 스테이지 12 완전 검증
- [ ] 스테이지 10·11 경량 검증
- [ ] 스테이지 13·14 경량 검증
- [ ] 스테이지 15 행동형 재검증

### 전투 확장

- [ ] 지원 중첩
- [ ] 제어 중첩과 감쇠
- [ ] 변종 전투력·획득률
- [ ] 합체 비용·획득시간·전투력
- [ ] 런타임 오버킬·투사체·타겟 전환 손실

### 최종 통합

- [ ] P10/P50/P90 전 계정 경로 재실행
- [ ] 빠른·중앙·느린 완주 시간 검증
- [ ] 20~30시간 숙련 파밍 검증
- [ ] 카탈로그 채택용 최종 권장값 묶음

---

## 현재 다음 계산

```text
BAL-NEXT-002
스테이지 9 지역 3 최종전 완전 검증
```

이후 순서:

```text
스테이지 9 완전 검증
→ 스테이지 7·8 경량 검증
→ 스테이지 12와 10·11
→ 스테이지 13·14와 스테이지 15 행동형
```

---

## 물리 경로 이전 계획

```text
docs/reference/*BENCHMARK*.md
→ docs/balance/*.md
```

이전 순서:

1. 새 경로에 동일 문서 생성
2. 내부 상대 링크 수정
3. `docs/INDEX.md`와 상위 문서 수정
4. 기존 경로를 호환 문서로 교체
5. 전체 링크 검사 후 호환 문서 제거

물리 이전이 완료되기 전에도 논리적 권위는 이 인덱스의 분류를 따릅니다.

---

## 작성 규칙

- 모든 계산은 재현 입력과 수용 조건을 기록합니다.
- 임시 이름은 `계산용`으로 표시합니다.
- 계산값과 채택값을 구분합니다.
- 새 계산 문서는 `docs/balance`에 작성합니다.
- 완료 시 `PROJECT_STATUS.md`를 같은 작업에서 갱신합니다.
- 카탈로그를 바꿀 필요가 있으면 별도의 채택 단계로 넘깁니다.
