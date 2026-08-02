# Tower RNG 콘텐츠 카탈로그 인덱스

- 상태: **Active Catalog Index**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 계산·검증: `../balance/INDEX.md`

## 책임

```text
balance에서 계산
→ 사용자 승인
→ catalog에서 영구 ID·값·콘텐츠 채택
→ spec·implementation에서 같은 데이터 사용
→ Roblox 런타임 검증
```

계산 문서가 변경돼도 카탈로그는 자동으로 바뀌지 않습니다.

---

# 상태

```text
Confirmed
- V1 ID·수치·전투 정체성 채택

Confirmed Values · Content Pending
- 수치는 채택됐지만 좌표·자산·개별 콘텐츠 일부 미작성

Implemented
- Roblox 데이터와 동작에 반영되고 검증됨
```

---

# 현재 권위 문서

| 영역 | 권위 문서 | 상태 |
|---|---|---|
| 영구 스테이지 문 | `STAGE_GATE_CATALOG.md` | Confirmed · Not Implemented |
| 지역·스테이지·웨이브 | `STAGE_CATALOG.md` | Confirmed Combat Data · Map Pending |
| 몬스터·보스 | `MONSTER_CATALOG.md` | Confirmed Gameplay Identity · Visuals Replaceable |
| 코인 스탯 트리 | `STAT_TREE_CATALOG.md` | Confirmed Values · Layout Pending |
| 변종·합체 공통 규칙 | `TOWER_SYSTEM_CATALOG.md` | Confirmed System Values · Individual Content Pending |

기술 구조:

```text
../technical/MONSTER_CONTENT_ARCHITECTURE.md
```

---

# 채택 현황

## 스테이지·몬스터

```text
RegionId: 5 / 5
StageId: 15 / 15
WaveSetId: 15 / 15
영구 문: 14 / 14
몬스터·보스 안정 MonsterId: 39
스테이지 웨이브 전투 데이터: 15 / 15
실제 맵·모델·애니메이션: 미구현
```

모델은 `VisualProfileId`로 분리했습니다. 제작 난도가 높으면 전투 데이터와 웨이브를 유지하고 VisualProfile만 교체합니다.

## 스탯 트리·경제

```text
편성 슬롯 5~12          2,790,686,200
공통 전투 I~XI         32,303,644,750
변종 가지              25,018,500,000
합체 가지               2,750,250,000
오프라인 가지           3,120,100,000
숙련 제어실            25,200,000,000
```

## 변종·합체

```text
인화성 1/5,000 · ×5.4928
독성   1/10,000 · ×6.3096
공허   1/20,000 · ×7.2478
거대   1/50,000 · ×8.7055

같은 TowerId 3개 → 1단계 ×1.45
같은 1단계 3개 → 2단계 ×2.1025
V1 최대 2단계
```

---

# 기존 reference 호환 문서

다음 파일은 과거 링크 호환을 위해 남겨둡니다.

```text
../reference/TOWER_CATALOG.md
../reference/MONSTER_CATALOG.md
../reference/STAGE_CATALOG.md
../reference/STAT_TREE_CATALOG.md
```

충돌 시 `docs/catalog`의 권위 문서를 사용합니다. 내부 링크 이전이 끝나기 전에는 기존 파일을 삭제하지 않습니다.

---

# 아직 필요한 카탈로그

## 타워

- 일반 굴리기 타워 50종의 최종 이름과 `TowerId`
- 50종 역할·행동·희귀도 순서
- 지원·제어 타워의 개별 수치
- 타워별 `AllowedVariantFamilies`
- 개별 변종 `TowerId`, 이름과 행동
- 기본형·변종 합체 계보와 결과 `TowerId`
- 타워 모델·애니메이션·VFX·SFX 요구사항

현재:

```text
공식 확률 슬롯 50 / 50
기준 정체성 6 / 최소 50
```

## 스테이지 표시 자산

- 실제 맵 경로와 좌표
- 랜드마크와 코인 수집 동선
- 몬스터 VisualProfile과 LOD
- 문·베이스 모델과 연출
- 지역 조명·음향

## 스탯 트리 표시 콘텐츠

- 전체 좌표와 연결선
- 가지 입구 부모 노드
- 일부 최소 환생 조건
- 아이콘·분야 색상·구매 연출

---

# 작성 규칙

- 같은 영구 ID를 여러 권위 파일에서 독립 정의하지 않습니다.
- 수치와 시각 자산의 상태를 분리합니다.
- 모델 교체가 전투 판정을 바꾸지 않게 합니다.
- 실제 런타임 효율은 Roblox 측정 전까지 Confirmed로 표시하지 않습니다.
- MonsterId를 AssetId나 모델 파일명에 종속시키지 않습니다.

---

# 다음 카탈로그 작업

```text
CAT-NEXT-003
일반 타워 50종 정체성·역할·행동 채택
```

그 다음:

```text
CAT-NEXT-004 타워별 변종 허용 계열과 개별 변종
CAT-NEXT-005 기본형·변종 합체 계보
CAT-NEXT-006 스탯 트리 좌표·아이콘·연결선
```
