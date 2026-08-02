# Tower RNG 문서 인덱스

- 상태: **Active**
- 마지막 정리: 2026-08-03
- 필수 참고: `../AGENTS.md`

## 먼저 볼 문서

| 문서 | 책임 |
|---|---|
| `PROJECT_STATUS.md` | 전체 진행률, 체크리스트, 현재 다음 작업 |
| `../README.md` | 게임 루프와 V1 범위 |
| `../AGENTS.md` | 승인·동기화·수치 작업 원칙 |
| `catalog/INDEX.md` | 실제 콘텐츠 ID·이름·채택 수치 |
| `balance/INDEX.md` | 수식·가정·시뮬레이션·검증 결과 |

현재 준비도:

```text
전체 V1 약 35%
기획·밸런스 약 76%
콘텐츠 카탈로그 약 12%
Roblox 구현·QA는 저장소 기준 초기 단계
```

---

# 문서 책임 구조

```text
AGENTS.md
→ README.md / docs/INDEX.md / docs/PROJECT_STATUS.md
→ design          게임 규칙과 플레이어 경험
→ catalog         실제 콘텐츠와 최종 채택 수치
→ balance         계산·시뮬레이션·검증
→ spec            정확한 시스템 동작 계약
→ technical       서버·클라이언트·저장 구조
→ implementation  실제 파일·함수·Remote 명세
→ code            Roblox 구현
```

```text
balance가 값을 추천
→ catalog가 값을 채택
→ implementation이 동일 값을 사용
```

기존 `reference` 폴더는 링크 호환 영역이며 신규 문서는 추가하지 않습니다.

---

# 게임 기획

## 진행·확률·경제

| 문서 | 책임 |
|---|---|
| `design/PROGRESSION.md` | 최초 25초와 장기 진행 |
| `design/V1_COMPLETION_PACING.md` | 12~15시간 중앙 완주 |
| `design/RNG_PROBABILITY.md` | 공식 `1/N`과 행운 압축 |
| `design/ROLLING.md` | 굴리기 속도와 특수 굴림 |
| `design/BALANCE_MODEL.md` | 공통 수치 공식 |
| `design/ECONOMY_PACING.md` | 코인·문·환생 경제 |
| `design/CURRENCY.md` | 코인·정수·XP·토큰 |
| `design/REBIRTH.md` | 진행 유지 환생과 네 스탯 |
| `design/STAT_TREE.md` | 코인 트리와 환생 스탯 |
| `design/OFFLINE_PROGRESS.md` | 제한된 오프라인 코인 |

## 타워·전투

| 문서 | 책임 |
|---|---|
| `design/TOWERS.md` | 50종 이상과 역할·희귀도 |
| `design/COMBAT.md` | 추종 자동 전투 |
| `design/FORMATION.md` | 4→12슬롯과 역할 상한 |
| `design/TARGETING.md` | 타겟 선정과 예약 피해 |
| `design/TOWER_BEHAVIOR.md` | 타워 행동 문법 |
| `design/TOWER_EXTENSIONS.md` | 고유 능력 확장 |
| `design/FUSION.md` | 수동 합체 |
| `design/TOWER_VARIANTS.md` | 변종 계열 |

## 월드·스테이지

| 문서 | 책임 |
|---|---|
| `design/WORLD_NAVIGATION.md` | 영구 문과 복귀 |
| `design/LEVEL_DESIGN.md` | 15스테이지와 5웨이브 |
| `design/WAVE_PACING.md` | 진입·파밍 목표시간 |
| `design/STAGE_VALIDATION.md` | 완전·경량 검증 정책 |
| `design/STAGE_BOSSES.md` | 보스 예산과 보상 |
| `design/MONSTERS.md` | 몬스터 스케일과 SpawnCost |

---

# 콘텐츠 카탈로그

권위 인덱스: `catalog/INDEX.md`

현재 호환 문서:

| 문서 | 책임 |
|---|---|
| `reference/TOWER_CATALOG.md` | 타워 ID·행동·수치·자산 |
| `reference/MONSTER_CATALOG.md` | 몬스터·보스 데이터 |
| `reference/STAGE_CATALOG.md` | 지역·스테이지 데이터 |
| `reference/STAT_TREE_CATALOG.md` | 코인 스탯 트리 데이터 |

새 카탈로그 문서는 `docs/catalog`에만 작성합니다.

---

# 계산·검증

권위 인덱스: `balance/INDEX.md`

## 확률·경제

| 문서 | 책임 |
|---|---|
| `reference/V1_TOWER_PROBABILITY_LADDER.md` | 50자리 공식 확률표 |
| `reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | 행운 압축 |
| `reference/V1_ROSTER_POWER_DISTRIBUTION.md` | 시간대별 보유 전력 |
| `reference/V1_REBIRTH_XP_BENCHMARK.md` | 환생 XP |
| `reference/V1_REBIRTH_STAT_BENCHMARK.md` | 환생 스탯 |
| `reference/V1_FORMATION_SLOT_BENCHMARK.md` | 슬롯 가격과 역할 제한 |
| `reference/V1_COIN_COMBAT_BENCHMARK.md` | 독립 전투 성장 |
| `balance/V1_GATE_ECONOMY_BENCHMARK.md` | 문·슬롯·전투 통합 경제 |

## 스테이지 전투

| 문서 | 상태 |
|---|---|
| `reference/STAGE1_WAVE_BENCHMARK.md` | 완전 완료 |
| `reference/STAGE2_WAVE_BENCHMARK.md` | 추가 완전 완료 |
| `reference/STAGE3_WAVE_BENCHMARK.md` | 완전 완료 |
| `reference/STAGE4_5_LIGHT_BENCHMARK.md` | 경량 완료 |
| `reference/STAGE6_WAVE_BENCHMARK.md` | 완전 완료 |
| `balance/STAGE7_8_LIGHT_BENCHMARK.md` | 경량 완료 |
| `balance/STAGE9_WAVE_BENCHMARK.md` | 완전 완료 |
| `balance/STAGE10_11_LIGHT_BENCHMARK.md` | 경량 완료 |
| `balance/STAGE12_WAVE_BENCHMARK.md` | 완전 완료 |
| `reference/STAGE15_WAVE_BENCHMARK.md` | 집계 완료·행동형 예정 |

현재:

```text
행동형 검증 완료: 스테이지 1~12
집계 검증 완료: 스테이지 15
수치상 완료: 13 / 15
```

---

# 밸런스 재현 도구

경로: `../tools/balance`

| 도구 | 책임 |
|---|---|
| `tower_baseline.py` | 최저급 역할 기여도 |
| `v1_probability_ladder.py` | 공식 확률 합 |
| `v1_luck_compression.py` | 행운 압축 |
| `v1_rebirth_xp_curve.py` | 환생 XP |
| `rebirth_stat_tokens.py` | 환생 스탯·굴림 통합 |
| `v1_roster_power_distribution.py` | 보유 전력 분포 |
| `v1_formation_slot_economy.py` | 슬롯 경제 |
| `v1_coin_combat_curve.py` | 독립 코인 전투 성장 |
| `v1_gate_economy.py` | 문·슬롯·전투 통합 경제 |
| `stage1_wave_sim.py` | 스테이지 1 |
| `stage2_wave_sim.py` | 스테이지 2 |
| `stage3_wave_sim.py` | 스테이지 3 |
| `stage4_5_light_sim.py` | 스테이지 4·5 |
| `stage6_wave_sim.py` | 스테이지 6 |
| `stage7_8_light_sim.py` | 스테이지 7·8 |
| `stage9_wave_sim.py` | 스테이지 9 |
| `stage10_11_light_sim.py` | 스테이지 10·11 |
| `stage12_wave_sim.py` | 스테이지 12 |
| `stage15_wave_sim.py` | 스테이지 15 집계 검증 |
| `stage_validation_plan.py` | 검증 정책과 계획 주기 |

---

# 시스템·기술 문서

| 문서 | 책임 |
|---|---|
| `technical/STATE_LIFECYCLE.md` | 프로필·재접속·환생 원자성 |
| `technical/TOWER_MODELING.md` | 타워 3D 제작 규약 |
| `technical/MONSTER_MODELING.md` | 몬스터 3D 제작 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | 행동 데이터 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | 확장 모듈과 훅 |

서비스별 정확한 계약은 `spec/`, 실제 Roblox 파일·Remote 명세는 `implementation/`에 작성합니다.

---

# 현재 완료 범위

```text
확률·행운·환생·슬롯·코인 성장 계산 완료
문 가격과 12~15시간 통합 경제 계산 완료
스테이지 1~12 행동형 전투 검증 완료
스테이지 15 집계 클리어 검증 완료
실제 타워 콘텐츠는 기준 6종 중심
용암 행동·변종·합체·런타임 계산 미완료
가격 권고안은 카탈로그 채택 전
Roblox 수직 슬라이스는 저장소 기준 미완료
```

---

# 현재 다음 작업

```text
BAL-NEXT-006
스테이지 15 용암지대 실제 행동형 완전 검증
```

이후:

```text
스테이지 13·14 경량 검증
→ 지원·제어·변종·합체
→ 최종 통합
→ 카탈로그 채택
→ 지역 1 수직 슬라이스
```
