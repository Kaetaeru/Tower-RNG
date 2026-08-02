# V1 최종 밸런스 계산 배치

- 계층: 계산·검증
- 상태: **Calculations Complete · Catalog Adopted · Runtime Measurement Pending**
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 최종 권고값: `FINAL_RECOMMENDATION.md`
- 채택 카탈로그: `../catalog/STAGE_GATE_CATALOG.md`, `../catalog/STAT_TREE_CATALOG.md`, `../catalog/TOWER_SYSTEM_CATALOG.md`
- 마지막 정리: 2026-08-03

## 목적

남은 계산을 의존성 순서에 따라 처리하고, 통과한 값을 실제 카탈로그에 채택했습니다.

```text
개별 공식·스크립트 유지
→ 단계별 수용 조건 검사
→ 최종 권고값 작성
→ 사용자 승인
→ 카탈로그 채택
→ Roblox 구현·실측
```

---

# 최종 단계 상태

| 단계 | 상태 | 결과 |
|---|---|---|
| `BAL-FINAL-001` 수동 합체 | 완료 | 3→1, 최대 2단계, `×1.45 / ×2.1025` |
| `BAL-FINAL-002` 런타임 손실 | 조건부 | 계산 예산 완료, Roblox 실측 대기 |
| `BAL-FINAL-003` 오프라인 코인 | 완료 | 25→40%, 8→24h |
| `BAL-FINAL-004` 후반 코인 싱크 | 완료 | 숙련 제어실 포함 30h 잔여 5B 이하 |
| `BAL-FINAL-005` 전체 계정 경로 | 완료 | 빠른·중앙·느린 목표 통과 |
| `BAL-FINAL-006` 최종 권고값 | 완료 | 권고값 정리 및 카탈로그 채택 |

```text
계산 수행: 6 / 6
수학 계산 완료: 6 / 6
카탈로그 채택: 완료
실제 런타임 측정: 대기
```

---

# 채택된 주요 결과

## 완주 시간

```text
빠른 완주 9.5~10h
중앙 완주 12.5~15h
느린 완주 18~21.5h
중앙 안정 파밍 약 13.5h
```

## Stage 15

```text
FirstClearEC = 10,050
StableFarmEC = 12,200
```

## 최종 영구 코인 싱크

```text
문·슬롯·전투  36.3968252B
변종           25.0185B
합체            2.75025B
오프라인        3.1201B
숙련 제어실    25.2000B
합계           92.4856752B
```

## 30시간 잔여

```text
문 우선        4.870B
균형형         0.034B
전투 우선      0.648B
슬롯 우선      0.648B
코인 실현 70%  3.798B
```

---

# 채택 위치

| 채택 범위 | 권위 카탈로그 |
|---|---|
| 스테이지 2~15 문 | `../catalog/STAGE_GATE_CATALOG.md` |
| 초기 노드·슬롯·전투 | `../catalog/STAT_TREE_CATALOG.md` |
| 변종·합체 해금 노드 | `../catalog/STAT_TREE_CATALOG.md` |
| 오프라인·숙련 제어실 노드 | `../catalog/STAT_TREE_CATALOG.md` |
| 변종 티켓·PowerBudget | `../catalog/TOWER_SYSTEM_CATALOG.md` |
| 합체 조합 규칙 | `../catalog/TOWER_SYSTEM_CATALOG.md` |

계산 문서는 수치의 근거를 소유하고, 카탈로그 문서는 실제 채택값을 소유합니다.

---

# 런타임 실측 대기

현재 구현 목표:

```text
Stage1  RuntimeEfficiency >= 0.992
Stage9  RuntimeEfficiency >= 0.990
Stage12 RuntimeEfficiency >= 0.988
Stage15 RuntimeEfficiency >= 0.986
```

지원 규칙 교체와 계산 예산을 적용한 Stage 15 15시간 P10 예상:

```text
113.20초 → 118.75초
```

저장소에 플레이 가능한 Roblox 수직 슬라이스가 없으므로 실제 통과를 주장하지 않습니다.

---

# 재계산 규칙

| 변경 | 다시 실행할 단계 |
|---|---|
| 합체 배율·재료 | 001, 004, 005, 006 |
| 런타임 실측 | 002, 005, 006 |
| 오프라인 효율·가격 | 003, 004, 005, 006 |
| 변종 확률·가격 | 001, 004, 005, 006 |
| 문·슬롯·전투 가격 | 004, 005, 006 |
| 숙련 제어실 가격 | 004, 006 |
| 일반 확률표 | 001~006 전체 |

재계산 결과가 기존 카탈로그와 달라지면 사용자 승인 뒤 카탈로그를 별도로 갱신해야 합니다.

---

# 다음 단계

```text
CAT-NEXT-002
스테이지 1~15 계산용 웨이브를 최종 StageId·MonsterId 카탈로그로 채택
```

별도 실측:

```text
RUN-NEXT-001
지역 1 Roblox 수직 슬라이스에서 RuntimeEfficiency 측정
```
