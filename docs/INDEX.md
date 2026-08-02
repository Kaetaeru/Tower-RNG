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
| `design/PROGRESSION.md` | Confirmed · Living | 최초 25초, 첫 15분, 영구 문과 XP→토큰 환생 |
| `design/V1_COMPLETION_PACING.md` | Confirmed · Living | 스테이지 15 12~15시간, 숙련 20~30시간 |
| `design/RNG_PROBABILITY.md` | Confirmed · Living | 임의 정밀도 `1/N`, 로그 압축과 잠정 행운 계수 |
| `design/ROLLING.md` | Confirmed · Living | 4.0→3.6초, 황금·다이아몬드와 누적 굴림 |
| `design/BALANCE_MODEL.md` | Confirmed · Living | PowerBudget, StageScale, SpawnCost, 보상 |
| `design/ECONOMY_PACING.md` | Confirmed · Living | 영구 코인·문, 첫 환생과 토큰 경제 |
| `design/CURRENCY.md` | Confirmed · Living | 코인·정수·Defense XP·환생 스탯 토큰 |
| `design/REBIRTH.md` | Confirmed · Living | Defense XP만 초기화하고 스탯 토큰 지급 |
| `design/STAT_TREE.md` | Confirmed · Living | 코인 기반 거대 스탯 트리 |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 |
| `design/POTIONS.md` | Confirmed · Living | 포션 효과·시간·중첩 |

### 타워·전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/TOWERS.md` | Confirmed · Living | 최소 50종, 역할·희귀도 성능 순서 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투와 역할 |
| `design/FORMATION.md` | Confirmed · Living | 빈 슬롯·자동 편성·퀵 HUD |
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
| `design/UI_FLOW.md` | Confirmed · Living | HUD·인벤토리·합체·설정 흐름 |
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
| `reference/V1_TOWER_PROBABILITY_LADDER.md` | Active Benchmark | 50자리 공식 분모와 정확한 합 1 |
| `reference/V1_TOP_TOWER_BENCHMARK.md` | Active Benchmark | 최고 일반 타워 `1/10^20`, 기여도 약 6,310 |
| `reference/V1_LUCK_COMPRESSION_BENCHMARK.md` | Active Benchmark | 스테이지·행운 토큰·특수 굴림 계수와 누적 획득률 |
| `reference/TOWER_BALANCE_BENCHMARK.md` | Active Benchmark | 최저급 6역할 기여도 |
| `reference/MONSTER_CATALOG.md` | Active Catalog | 스테이지 1 몬스터와 보스 |
| `reference/STAGE_CATALOG.md` | Active Catalog | 최초 전투·스테이지 1·문 가격 |
| `reference/STAGE1_WAVE_BENCHMARK.md` | Active Benchmark | 15개 혼합 편성의 5웨이브 검증 |
| `reference/FIRST_REBIRTH_ECONOMY_BENCHMARK.md` | Active Benchmark | 첫 7,000 XP 도달; 이후 리셋 가정 폐기 |
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
| `../tools/balance/v1_luck_compression.py` | 누적 굴림·행운 압축·최고 타워 획득률 |

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/STATE_LIFECYCLE.md` | Confirmed · Living | 프로필·영구 문·XP→토큰 환생·원자성 |
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

환생·저장
→ design/REBIRTH.md
→ design/CURRENCY.md
→ design/WORLD_NAVIGATION.md
→ technical/STATE_LIFECYCLE.md

타워·몬스터·스테이지 수치
→ design/BALANCE_MODEL.md
→ reference 카탈로그와 벤치마크

완주 시간
→ design/V1_COMPLETION_PACING.md

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
- 코인과 문을 유지하는 XP→스탯 토큰 환생
- V1 완주 12~15시간
- 최고 일반 타워 1 / 10^20, 기여도 약 6,309.57
- 정확한 합 1의 50자리 공식 확률 사다리
- 스테이지 계수 0.245, 행운 토큰 계수 0.040
- 일반·황금·다이아몬드 압축 상한 5.40·5.65·6.05
- 균형 배분 최고 타워 누적 13.5h 3.012%, 15h 4.661%, 25h 17.062%, 30h 22.705%
```

---

## 다음 우선순위

```text
1. 환생당 스탯 토큰 지급량과 배분 스탯 목록
2. 행운 없음·균형·집중 계정의 전체 50종 최고 보유·편성 전투력 분포
3. 스테이지 15 권장 편성·계정 성장 배율 역산
4. 코인·문 유지 상태의 두 번째 이후 환생 요구량
5. 스테이지 2 실제 몬스터·웨이브·보스
6. 스테이지 2 진입·파밍 시간 검증
7. 중간 희귀도 실제 타워 작성
8. 후속 굴리기 속도와 행운 곡선 재검증
9. 지역 1 수직 슬라이스 구현
10. 검증 후 50종·15스테이지 확장
```
