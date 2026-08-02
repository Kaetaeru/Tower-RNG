# Tower RNG 문서 인덱스

- 상태: Active
- 필수 참고: `../AGENTS.md`
- 마지막 정리: 2026-08-02

## 문서 계층

```text
AGENTS.md
→ README.md / docs/INDEX.md
→ design
→ reference
→ spec
→ technical
→ implementation
→ code
```

하위 데이터가 공개 규칙을 바꾸면 영향을 받는 상위 문서를 같은 작업에서 갱신합니다.

---

## 프로젝트 진입

| 문서 | 책임 |
|---|---|
| `../README.md` | 최신 게임 루프·V1 범위·핵심 수치 |
| `../AGENTS.md` | 승인·계층·동기화·수치·저장 원칙 |
| `INDEX.md` | 문서 위치와 우선순위 |

---

## 게임 기획

### 진행·확률·경제

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/PROGRESSION.md` | Confirmed · Living | 최초 25초, V1 시간축, 스테이지 기준형 환생 |
| `design/V1_COMPLETION_PACING.md` | Confirmed · Living | 스테이지 15 12~15시간, 실제 슬롯·P10~P90 완주 전력 |
| `design/RNG_PROBABILITY.md` | Confirmed · Living | 임의 정밀도 `1/N`, 로그 압축과 환생 행운 공식 |
| `design/ROLLING.md` | Confirmed · Living | 4.0→3.6초, 환생 속도와 2.0초 하한, 특수 굴림 |
| `design/BALANCE_MODEL.md` | Confirmed · Living | PowerBudget, StageScale, SpawnCost, 보상 |
| `design/ECONOMY_PACING.md` | Confirmed · Living | 영구 코인·문, 환생 XP·토큰 경제 |
| `design/CURRENCY.md` | Confirmed · Living | 코인·정수·Defense XP·환생 토큰 |
| `design/REBIRTH.md` | Confirmed · Living | XP 기준 스테이지, 토큰 4개, 네 스탯과 재분배 |
| `design/STAT_TREE.md` | Confirmed · Living | 코인 트리와 네 분야 환생 스탯 |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 |
| `design/POTIONS.md` | Confirmed · Living | 포션 효과·시간·중첩 |

### 타워·전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/TOWERS.md` | Confirmed · Living | 최소 50종, 역할·희귀도 성능 순서 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투와 역할 |
| `design/FORMATION.md` | Confirmed · Living | 4→12슬롯 가격, 역할 상한 2→3→4, 자동 편성 |
| `design/TARGETING.md` | Confirmed | 경로 진행도·예약 피해 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 이동·행동·전달 문법 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 고유 능력·사건 반응 |
| `design/FUSION.md` | Confirmed · Living | 수동 합체·자동 합체 금지 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 인화성·독성·공허·거대 |
| `design/PRESENTATION_FEEL.md` | Confirmed · Living | 모델 동작·피격·음향 중심 타격감 |

### 월드·몬스터

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/WORLD_NAVIGATION.md` | Confirmed · Living | 물리적 영구 문·텔레포터·빠른 복귀 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 15스테이지·5웨이브·예산 |
| `design/WAVE_PACING.md` | Confirmed · Living | 진입·파밍 시간과 후반 상한 |
| `design/STAGE_BOSSES.md` | Confirmed · Living | 보스 계열·예산·보상 |
| `design/MONSTERS.md` | Confirmed · Living | 몬스터 스케일·SpawnCost |

### UI·운영

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/UI_FLOW.md` | Confirmed · Living | HUD·XP 기준 스테이지·네 스탯·재분배 흐름 |
| `design/SETTINGS.md` | Confirmed · Living | 효과·카메라·음향·접근성 |
| `design/SOCIAL.md` | Confirmed · Living | 공식 분모 리더보드·거래 금지 |
| `design/MONETIZATION.md` | Confirmed · Living | 상품 방향과 금지선 |
| `design/TUTORIAL.md` | Confirmed · Living | 최초 슬라임·4슬롯·자동 굴리기 |
| `design/LIVE_WAVE.md` | Draft | 후속 서버 공동 전투 |

---

## 참조 데이터와 벤치마크

| 문서 | 상태 | 책임 |
|---|---|---|
| `reference/TOWER_CATALOG.md` | Active Catalog | 실제 타워 ID·행동·수치·자산 |
| `reference/V1_TOWER_PROBABILITY_LADDER.md` | Active Benchmark | 50자리 공식 분모·정확한 합·전체 보유 체감 |
| `reference/V1_TOP_TOWER_BENCHMARK.md` | Active Benchmark | 최고 일반 타워 `1/10^20`, 기여도 약 6,310 |
| `reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | Active Benchmark | 실제 환생 시각·행운·속도별 최고 타워 획득률 |
| `reference/V1_REBIRTH_STAT_BENCHMARK.md` | Active Benchmark | 토큰 4개와 네 스탯 공식·집중 상한 |
| `reference/V1_REBIRTH_XP_BENCHMARK.md` | Active Benchmark | XP 기준 스테이지·진행률 보존·20/35/50분 곡선 |
| `reference/V1_ROSTER_POWER_DISTRIBUTION.md` | Active Benchmark | 20,000계정 보유·무제한 Top-K 전투력 분포 |
| `reference/V1_FORMATION_SLOT_BENCHMARK.md` | Active Benchmark | 슬롯 5~12 가격·해금 시각·역할 제한 편성 P10/P50/P90 |
| `reference/TOWER_BALANCE_BENCHMARK.md` | Active Benchmark | 최저급 6역할 기여도 |
| `reference/MONSTER_CATALOG.md` | Active Catalog | 스테이지 1 몬스터와 보스 |
| `reference/STAGE_CATALOG.md` | Active Catalog | 최초 전투·스테이지 1·문 가격 |
| `reference/STAGE1_WAVE_BENCHMARK.md` | Active Benchmark | 15개 혼합 편성의 5웨이브 검증 |
| `reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | Active Benchmark | 첫 7,000 XP 도달 |
| `reference/STAT_TREE_CATALOG.md` | Active Catalog | 초기 코인 노드·좌표·가격 |

지역:

```text
1 초원·숲
2 사막
3 정글
4 설원
5 용암지대
```

---

## 밸런스 도구

| 경로 | 책임 |
|---|---|
| `../tools/balance/tower_baseline.py` | 최저급 6종 기여도 |
| `../tools/balance/stage1_wave_sim.py` | 스테이지 1 웨이브 1~5 |
| `../tools/balance/first_rebirth_economy.py` | 첫 환생 임계점 경제 |
| `../tools/balance/v1_probability_ladder.py` | 50슬롯·정확한 확률 합 |
| `../tools/balance/v1_luck_compression.py` | 초기 독립 행운 계수 기록 |
| `../tools/balance/v1_rebirth_xp_curve.py` | 스테이지 기준형 환생 XP와 횟수 |
| `../tools/balance/rebirth_stat_tokens.py` | XP 곡선·네 스탯·굴림·최고 타워 통합 검증 |
| `../tools/balance/v1_roster_power_distribution.py` | 20,000계정 보유 수량·무제한 Top-K 전투력 |
| `../tools/balance/v1_formation_slot_economy.py` | 슬롯 가격·해금 시각·역할 제한 실제 편성 전투력 |

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/STATE_LIFECYCLE.md` | Confirmed · Living | 프로필·XP 기준 상승·환생·토큰 재분배 원자성 |
| `technical/TOWER_MODELING.md` | Confirmed · Living | 3D 모델과 모션 견본 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 행동·전달·자원 문법 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | Confirmed · Living | 확장 모듈·훅 |
| `technical/MONSTER_MODELING.md` | Confirmed · Living | 몬스터 제작 규약 |

---

## 구현 전 권위 문서

```text
확률·행운
→ design/RNG_PROBABILITY.md
→ reference/V1_TOWER_PROBABILITY_LADDER.md
→ reference/V1_LUCK_COMPRESSION_BENCHMARK.md
→ reference/V1_ROSTER_POWER_DISTRIBUTION.md

편성 슬롯·역할 제한
→ design/FORMATION.md
→ reference/V1_FORMATION_SLOT_BENCHMARK.md

환생 XP·스탯
→ design/REBIRTH.md
→ design/STAT_TREE.md
→ reference/V1_REBIRTH_XP_BENCHMARK.md
→ reference/V1_REBIRTH_STAT_BENCHMARK.md

환생·저장
→ design/CURRENCY.md
→ design/WORLD_NAVIGATION.md
→ technical/STATE_LIFECYCLE.md

타워·몬스터·스테이지 수치
→ design/BALANCE_MODEL.md
→ reference 카탈로그와 벤치마크

완주 시간·완주 전력
→ design/V1_COMPLETION_PACING.md
→ reference/V1_FORMATION_SLOT_BENCHMARK.md

웨이브 시간
→ design/WAVE_PACING.md
```

---

## 현재 완료

```text
- 역할별 최저급 기준 타워 6종
- 스테이지 1 몬스터 3종·보스·5웨이브
- 전체 주기 56.28초, 혼합 편성 누수 0
- 첫 7,000 Defense XP 7.80~14.34분
- 코인·문·전투를 유지하는 환생
- 환생 1회당 스탯 토큰 4개
- 행운·성능·재화·주사위 속도 네 분야
- XP 기준 스테이지와 진행률 보존
- 두 번째 20분, 세 번째 35분, 4~50번째 50분 기준 환생 곡선
- 균형형 30시간 약 46회 환생
- 행운 0.0340/0.0040 Compression 계수
- 성능 최대 ×2.50, 재화 최대 ×4.00, 굴리기 최소 2.0초
- 환생 직후 무료 전체 재분배 1회
- V1 완주 12~15시간
- 최고 일반 타워 1 / 10^20, 기여도 약 6,309.57
- 정확한 합 1의 50자리 공식 확률 사다리
- 20,000계정 시간대별 보유·무제한 Top-K 전투력 분포
- 슬롯 5~12 가격과 균형형 11분→13시간 31분 해금 곡선
- 역할 상한 4~6슬롯 2개, 7~9슬롯 3개, 10~12슬롯 4개
- 균형형 15h 실제 Final EC P10/P50/P90 = 2,264/4,370/12,083
- 균형형 30h 실제 Final EC P10/P50/P90 = 12,115/23,067/38,181
```

---

## 다음 우선순위

```text
1. 코인 전투 스탯의 15시간·30시간 배율
2. 실제 슬롯·코인 성장·P10 전력을 합친 스테이지 15 권장 전투력 역산
3. 스테이지 2 실제 몬스터·웨이브·보스
4. 스테이지 2 진입·파밍 시간과 실제 XP율 검증
5. 중간 희귀도 실제 타워 작성
6. 변종·합체의 시간대별 전투력 기여
7. 실제 지원·제어 중첩과 자동 편성 평가
8. 환생 스탯 배분·재분배 UI 상세 명세
9. 지역 1 수직 슬라이스 구현
10. 실제 데이터로 계획 XP 주기 교체 후 50종·15스테이지 확장
```
