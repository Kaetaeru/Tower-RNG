# Tower RNG 문서 인덱스

- 상태: Active
- 필수 참고: `../AGENTS.md`
- 마지막 정리: 2026-08-02

## 문서 사용 순서

```text
AGENTS.md
→ README.md / docs/INDEX.md
→ 관련 design 문서
→ 관련 reference 데이터
→ 관련 spec 문서
→ 관련 technical 문서
→ 관련 implementation 문서
→ 실제 코드
```

하위 계층의 공개 규칙이 변경되면 영향을 받는 상위 문서도 같은 작업에서 함께 갱신합니다.

---

## 프로젝트 진입 문서

| 문서 | 상태 | 책임 |
|---|---|---|
| `../README.md` | Active | 최신 핵심 루프, 지역, 웨이브, 콘텐츠 규모, 과금과 타격감 개요 |
| `../AGENTS.md` | Required | 승인, 문서 계층, 상하위 동기화와 감각 품질 원칙 |
| `INDEX.md` | Active | 전체 문서 위치와 상태 |

---

## 게임 기획 문서

### 전체 진행과 획득

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/PROGRESSION.md` | Confirmed · Living | 전역 타워 풀, 첫 10분, 환생 주기와 출시 범위 |
| `design/ECONOMY_PACING.md` | Confirmed · Living | 초·분·환생 단위 목표와 가격·보상 곡선 원칙 |
| `design/ROLLING.md` | Confirmed · Living | 무료 굴리기, 전역 일반 타워 풀과 특수 주사위 |
| `design/TOWERS.md` | Confirmed · Living | 최소 50종 타워, 역할 분포, 고정 데이터와 자동 편성 연동 |
| `design/STAT_TREE.md` | Confirmed · Living | 하나의 거대한 트리, 분야 해금과 영구 성장 |
| `design/REBIRTH.md` | Confirmed · Living | 짧은 반복 환생과 완만한 영구 배율 |
| `design/TUTORIAL.md` | Confirmed · Living | 첫 굴리기, 코인 수집과 기능 안내 |
| `design/FUSION.md` | Confirmed · Living | 중후반 합체와 영구 누적 진행 |
| `design/TOWER_VARIANTS.md` | Confirmed · Living | 인화성·독성·공허·거대 변종과 자산 재사용 |

### 월드와 전투

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/WORLD_NAVIGATION.md` | Confirmed · Living | 로비, 선형 스테이지, 문, 웨이브 초기화와 텔레포터 |
| `design/LEVEL_DESIGN.md` | Confirmed · Living | 10초 웨이브, 비율 예산, 15개 스테이지와 3초 과부하 |
| `design/STAGE_BOSSES.md` | Confirmed · Living | 지역별 초·중반·최종 보스와 5웨이브 비율 구성 |
| `design/COMBAT.md` | Confirmed · Living | 추종 자동 전투, 역할, Engage와 전투 타격감 |
| `design/PRESENTATION_FEEL.md` | Confirmed · Living | UI·굴리기·전투의 과장된 움직임과 피드백 완료 기준 |
| `design/TOWER_BEHAVIOR.md` | Confirmed · Living | 타겟, 이동, 행동 루틴과 전달 방식 |
| `design/TOWER_EXTENSIONS.md` | Confirmed · Living | 고유 능력, 사건 반응과 플레이어 조작 |
| `design/FORMATION.md` | Confirmed · Living | 전체·역할 슬롯, 자동 편성과 퀵 편성 HUD |
| `design/TARGETING.md` | Confirmed | 경로 진행도, 실제 거리와 예약 피해 타겟팅 |
| `design/MONSTERS.md` | Confirmed · Living | 몬스터 유형, 생성 비용, 웨이브 배치와 변종 |

### 경제·UI·운영

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/CURRENCY.md` | Confirmed · Living | 코인 드롭·수집, 문 구매와 연금 정수 |
| `design/OFFLINE_PROGRESS.md` | Confirmed · Living | 제한된 오프라인 코인 효율과 시간 상한 |
| `design/POTIONS.md` | Confirmed · Living | 포션 효과, 지속시간과 중첩 |
| `design/UI_FLOW.md` | Confirmed · Living | HUD, 퀵 편성, 인벤토리와 즉각적인 클릭 피드백 |
| `design/SOCIAL.md` | Confirmed · Living | 현재 보유 희귀 타워 `1 / N` 리더보드와 공개 프로필 |
| `design/MONETIZATION.md` | Confirmed · Living | RNG 게임 조사 기반 상품 방향과 무료 핵심 기능 보호 |

### 추가 콘텐츠

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/LIVE_WAVE.md` | Draft | 로비에서 진입하는 서버 공동 전투 |

### 호환 별칭

| 문서 | 상태 | 책임 |
|---|---|---|
| `design/FEEL_AND_FEEDBACK.md` | Deprecated Alias | `PRESENTATION_FEEL.md`로 연결하는 이전 문서명 |

---

## 콘텐츠 참조 문서

공통 시스템 규칙은 design에 두고 실제 콘텐츠 목록과 수치는 reference에 기록합니다.

| 문서 | 상태 | 책임 |
|---|---|---|
| `reference/TOWER_CATALOG.md` | Active Template | 최소 50종 타워의 확률·행동·수치·타격감 작성 양식 |
| `reference/MONSTER_CATALOG.md` | Active Template | 몬스터·보스 ID, 생성 비용, 능력치와 행동 |
| `reference/STAT_TREE_CATALOG.md` | Active Template | 거대 트리 노드 좌표, 연결, 가격과 환생 조건 |
| `reference/STAGE_CATALOG.md` | Active Template | 맵, Min/Base/Max 예산, 비율 구성과 보스 데이터 |

현재 확정된 지역 테마:

```text
지역 1: 초원·숲
지역 2: 사막
지역 3: 정글
지역 4: 설원
지역 5: 용암지대
```

스테이지 구성과 디자인은 `STAGE_CATALOG.md` 양식을 복제해 사용자가 직접 작성합니다.

---

## 시스템 명세 예정

```text
spec/PROGRESSION.md
spec/ECONOMY_PACING.md
spec/ROLLING.md
spec/TOWERS.md
spec/STAT_TREE.md
spec/REBIRTH.md
spec/TUTORIAL.md
spec/FUSION.md
spec/TOWER_VARIANTS.md
spec/WORLD_NAVIGATION.md
spec/LEVEL_DESIGN.md
spec/STAGE_BOSSES.md
spec/COMBAT.md
spec/PRESENTATION_FEEL.md
spec/TOWER_BEHAVIOR.md
spec/TOWER_EXTENSIONS.md
spec/FORMATION.md
spec/TARGETING.md
spec/MONSTERS.md
spec/CURRENCY.md
spec/OFFLINE_PROGRESS.md
spec/POTIONS.md
spec/UI_FLOW.md
spec/SOCIAL.md
spec/MONETIZATION.md
spec/LIVE_WAVE.md
```

---

## 기술 설계

| 문서 | 상태 | 책임 |
|---|---|---|
| `technical/TOWER_MODELING.md` | Confirmed · Living | Basic 모델, 자유 이름 모션, 과장된 준비·공격·반동 규약 |
| `technical/TOWER_BEHAVIOR_GRAMMAR.md` | Confirmed · Living | 이동, 행동 루틴, 전달과 자원 프로필 |
| `technical/TOWER_EXTENSION_FRAMEWORK.md` | Confirmed · Living | 확장 모듈, 훅, 고유 능력과 조작 세션 |
| `technical/MONSTER_MODELING.md` | Confirmed · Living | 공유 모션 엔진을 사용하는 몬스터 제작 규약 |

---

## 구현 명세

기술 설계가 확정된 뒤 `implementation/<SYSTEM>.md`에 실제 파일, 공개 타입, 함수, Remote, 저장 스키마와 테스트 대상을 기록합니다.

---

## 현재 우선순위

```text
1. STAGE_CATALOG에서 지역 1의 3개 스테이지 작성
2. MONSTER_CATALOG에서 지역 1 몬스터와 두 보스 계열 작성
3. TOWER_CATALOG에서 최소 50종의 초기 목록과 역할 분포 작성
4. STAT_TREE_CATALOG에서 중심부와 첫 환생 전 노드 배치
5. 웨이브·문·스탯·환생 경제 시뮬레이션
6. UI·전투 공통 피드백 토큰과 Preview 기준 정의
7. 과금 상품의 정확한 배율은 무료 수직 슬라이스 측정 후 결정
8. 핵심 시스템 명세 작성
9. 지역 1 수직 슬라이스 구현
```
