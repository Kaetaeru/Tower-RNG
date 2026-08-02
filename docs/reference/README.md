# `docs/reference` 호환 영역

- 상태: **Legacy Compatibility Area**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 콘텐츠 카탈로그: `../catalog/INDEX.md`
- 계산·검증: `../balance/INDEX.md`

## 규칙

이 폴더는 과거에 카탈로그와 계산 문서를 함께 보관했습니다.

2026-08-03부터 책임을 다음과 같이 분리합니다.

```text
실제 콘텐츠 ID·이름·채택 수치
→ docs/catalog

수식·가정·시뮬레이션·수용 조건
→ docs/balance
```

이 폴더에는 **새 문서를 추가하지 않습니다.**

기존 파일은 상대 링크와 상위 문서가 모두 새 경로로 교체될 때까지 호환을 위해 유지합니다.

---

## 카탈로그로 분류되는 기존 파일

```text
TOWER_CATALOG.md
MONSTER_CATALOG.md
STAGE_CATALOG.md
STAT_TREE_CATALOG.md
```

목표 경로:

```text
docs/catalog/<same filename>
```

---

## 계산·검증으로 분류되는 기존 파일

```text
V1_TOWER_PROBABILITY_LADDER.md
V1_TOP_TOWER_BENCHMARK.md
V1_LUCK_COMPRESSION_BENCHMARK.md
V1_REBIRTH_STAT_BENCHMARK.md
V1_REBIRTH_XP_BENCHMARK.md
V1_ROSTER_POWER_DISTRIBUTION.md
V1_FORMATION_SLOT_BENCHMARK.md
V1_COIN_COMBAT_BENCHMARK.md
TOWER_BALANCE_BENCHMARK.md
FIRST_REBIRTH_ECONOMY_BENCHMARK.md
STAGE1_WAVE_BENCHMARK.md
STAGE2_WAVE_BENCHMARK.md
STAGE3_WAVE_BENCHMARK.md
STAGE4_5_LIGHT_BENCHMARK.md
STAGE6_WAVE_BENCHMARK.md
STAGE15_WAVE_BENCHMARK.md
```

목표 경로:

```text
docs/balance/<same filename>
```

---

## 이전 완료 조건

- [ ] 새 경로에 문서 생성
- [ ] 문서 내부 상대 링크 수정
- [ ] `docs/INDEX.md` 경로 수정
- [ ] design·technical·implementation 문서 링크 수정
- [ ] 기존 경로를 호환 안내문으로 교체
- [ ] 전체 링크 검사
- [ ] 호환 안내문 제거 여부 결정

이전 중에는 동일 문서를 양쪽에서 독립 수정하지 않습니다. 현재 원본은 기존 경로에 있고, 논리적 분류와 신규 작성 위치는 `catalog` 또는 `balance`입니다.
