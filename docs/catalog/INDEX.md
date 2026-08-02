# Tower RNG 콘텐츠 카탈로그 인덱스

- 상태: **Active Catalog Index**
- 마지막 정리: 2026-08-03
- 프로젝트 현황: `../PROJECT_STATUS.md`
- 계산·검증: `../balance/INDEX.md`

## 책임

카탈로그는 게임에 실제로 채택되는 콘텐츠를 소유합니다.

포함:

- 영구 ID
- 플레이어에게 보이는 이름과 설명
- 최종 채택 능력치
- 역할·태그·행동 계약
- 스테이지·웨이브 구성
- 모델·애니메이션·VFX·SFX 요구사항
- Proposed·Confirmed·Implemented 상태

포함하지 않음:

- 수치 역산 과정
- 몬테카를로 결과
- 가정별 비교표
- 민감도 분석
- 임시 계정 프로필
- 검증 로그 전체

계산 근거는 `docs/balance`가 소유합니다. 카탈로그는 채택한 최종값과 해당 계산 문서의 경로만 기록합니다.

---

## 채택 규칙

카탈로그의 수치 항목은 가능하면 다음 필드를 가집니다.

```text
BalanceSource
- 값을 채택한 계산·검증 문서

BalanceStatus
- Proposed
- Confirmed (Provisional Balance)
- Confirmed
- Implemented
```

계산 문서의 값이 바뀌어도 카탈로그가 자동으로 바뀌지는 않습니다.

```text
계산 완료
→ 수용 조건 통과
→ 카탈로그 채택 여부 확인
→ 카탈로그 갱신
→ 구현 데이터 갱신
```

임시 계산용 이름은 카탈로그의 최종 이름으로 간주하지 않습니다.

---

## 현재 카탈로그

기존 문서는 링크 호환을 위해 잠시 `docs/reference`에 남아 있습니다. 새 카탈로그 문서는 이 폴더에만 작성합니다.

| 영역 | 현재 권위 문서 | 상태 |
|---|---|---|
| 타워 | `../reference/TOWER_CATALOG.md` | Active · 경로 이전 예정 |
| 몬스터·보스 | `../reference/MONSTER_CATALOG.md` | Active · 경로 이전 예정 |
| 지역·스테이지 | `../reference/STAGE_CATALOG.md` | Active · 경로 이전 예정 |
| 코인 스탯 트리 | `../reference/STAT_TREE_CATALOG.md` | Active · 경로 이전 예정 |

물리 이전 목표:

```text
docs/reference/TOWER_CATALOG.md
→ docs/catalog/TOWER_CATALOG.md

docs/reference/MONSTER_CATALOG.md
→ docs/catalog/MONSTER_CATALOG.md

docs/reference/STAGE_CATALOG.md
→ docs/catalog/STAGE_CATALOG.md

docs/reference/STAT_TREE_CATALOG.md
→ docs/catalog/STAT_TREE_CATALOG.md
```

이전이 끝날 때까지 기존 파일을 직접 삭제하지 않습니다. 내부 링크를 모두 교체한 뒤 호환 문서를 제거합니다.

---

## 현재 콘텐츠 진행

### 타워

```text
공식 확률 슬롯: 50 / 50
기준 정체성: 6 / 최소 50
최종 모델·행동·자산: 대부분 미작성
```

### 몬스터·보스

```text
스테이지 1: 카탈로그 채택
스테이지 2~6·15: 계산 문서의 임시 콘텐츠
스테이지 7~14: 대부분 미작성
```

### 스테이지

```text
지역 테마: 5 / 5
상세 카탈로그: 스테이지 1 중심
전투 계산: 스테이지 1~6·15
최종 맵·경로·랜드마크: 미작성
```

### 스탯 트리

```text
초기 노드: 작성됨
슬롯·전투 성장 곡선: 계산 완료
전체 V1 노드·좌표·표시 자산: 미완료
```

---

## 다음 카탈로그 작업

카탈로그는 다음 계산이 잠긴 뒤 확장합니다.

```text
1. 스테이지 4~15 문 가격과 전체 코인 경제
2. 스테이지 7~14 전투 검증
3. 지원·제어 중첩
4. 변종·합체 기여
```

그 뒤의 채택 순서:

```text
1. 15스테이지 최종 데이터
2. 스테이지별 몬스터·보스
3. 50타워 최종 정체성·행동
4. 전체 스탯 트리
5. 변종·합체 결과
```

---

## 작성 금지

- 계산 결과 전체를 카탈로그에 복사
- 검증 전 수치를 `Confirmed`로 표시
- 계산용 임시 이름을 자동으로 최종 이름으로 승격
- 같은 ID를 여러 파일에서 독립 정의
- 카탈로그 수치와 구현 수치를 별도로 관리
