# 타워 카탈로그

- 계층: 참조 데이터
- 상태: **Active Catalog**
- 필수 참고: `../../AGENTS.md`
- 상위 문서: `../design/RNG_PROBABILITY.md`, `../design/BALANCE_MODEL.md`, `../design/TOWERS.md`, `../design/COMBAT.md`, `../design/TOWER_BEHAVIOR.md`, `../design/TOWER_VARIANTS.md`
- 관련 문서: `MONSTER_CATALOG.md`, `STAT_TREE_CATALOG.md`, `STAGE_CATALOG.md`
- 마지막 정리: 2026-08-02

## 목적

실제 타워의 ID, 공식 기본 확률, 전투 예산, 역할, 행동과 제작 자산을 기록합니다.

첫 출시 일반 굴리기 타워는 최소 50종, 역할별 약 8~10종입니다. 변종과 합체 전용 타워는 별도 추가합니다.

---

## 타워 작성 양식

```markdown
## 표시 이름

- TowerId:
- 상태: Proposed | Confirmed (Provisional Balance) | Confirmed | Implemented
- 획득 방식: 일반 굴리기 | 변종 판정 | 합체 | 이벤트 | 기타
- BaseOddsN: "10진수 문자열" | 없음
- 공식 기본 표시: 1 / N | 비굴리기
- ProbabilityTableVersion:
- CommonReserve 대상: 예 | 아니오
- 보조 등급:
- 주 역할:
- 보조 역할:
- FeedbackWeight: Micro | Standard | Heavy | Heroic

### 희귀도·전투 예산

- log10(BaseOddsN):
- RawPowerBudget:
- FinalPowerBudget:
- 동일 역할 희귀도 순위:
- 이전 타워 대비 최소 기여도 증가 검증:
- EquivalentContribution 기준값:
- 기준 전투 시나리오:

### 행동

- TargetPolicy:
- TargetLossPolicy:
- Movement:
- FacingPolicy:
- ActionRoutine:
- Delivery:
- DeliveryModifiers:
- ResourceProfile:
- Extensions:

### 기본 성능

- 기본 피해 또는 핵심 효과:
- 행동 주기:
- 대상 수:
- 역할별 기여 계산:
- 성능 강화 적용값:
- 치명타 적용 여부:
- 이동속도·교전거리:
- 큰 수 형식 사용 여부:

### 자동 편성

- 평가 기준:
- 동일 효과 중첩 규칙:
- 역할 슬롯 후보:
- 권장 타겟 정책:

### 타격감

- 준비 동작:
- 판정 순간:
- 공격자 반동:
- 대상 피격 반응:
- 효과·음향:
- 치명타 강화 표현:
- 카메라 흔들림: 없음 | 보스급 예외

### 제작 자산

- ModelKit:
- 주요 모션 견본:
- 효과·음향:
- 공격·효과 기준점:

### 성장과 수집

- 합체 결과:
- 합체 필요 수량:
- 변종 합체 규칙:
- 허용 변종 계열:
- 도감 설명:
- 제작 메모:
```

---

## 공식 확률 규칙

- 일반·변종 타워의 `BaseOddsN`은 10진수 문자열
- 공식 기본 확률만 UI에 표시
- 현재 행운 적용 확률은 카탈로그에 기록하지 않음
- 확률표 전체 합은 컴파일러가 임의 정밀도 유리수로 검증
- 신규 타워는 `CommonReserve`를 우선 사용
- 기존 중·고희귀 분모는 명시적 변경 없이는 유지

---

## 전투력 규칙

```text
RawPowerBudget(N) = (N / 10)^0.20
```

같은 역할 내 최종 예산:

```text
Final[i]
= max(Raw[i], Final[i-1] × 1.001)
```

점검:

- 분모가 큰 타워가 반드시 더 높은 기여도
- 정수 반올림 뒤에도 차이 유지
- 서로 다른 역할은 EquivalentContribution으로 비교
- 지원·제어를 표시 DPS만으로 평가하지 않음

---

## 최저급 기준 전투 시나리오

아래 여섯 타워는 역할별 희귀도 사다리의 시작점입니다. 이름과 역할 정체성은 확정하고, 세부 수치는 첫 전투 시뮬레이션 전까지 임시 밸런스 값으로 취급합니다.

공통 조건:

```text
공식 기본 확률: 각 1 / 10
RawPowerBudget: 1.000
FinalPowerBudget: 1.000
목표 EquivalentContribution: 1.000
스테이지 1 표준 일반 몬스터 HP: 5
표준 몬스터 목표 이동시간: 10초
초기 편성 기준: 4슬롯
일반 웨이브 4 : 보스 웨이브 1 비중
```

안전 조건:

- 여섯 타워 모두 혼자서 스테이지 1 표준 일반 몬스터를 처치할 수 있음
- 지원·제어 타워를 첫 굴림으로 얻어도 튜토리얼이 막히지 않음
- 모든 타워의 일반 공격은 카메라 흔들림 없이 모델 움직임·피격 반응·음향으로 타격감을 만듦
- 현재 여섯 타워의 공식 확률 합은 60%이며 나머지 40%는 이후 타워 카탈로그 작성에서 정확히 채움
- 전체 출시 확률표가 완성되기 전에는 정식 확률 컴파일 대상으로 사용하지 않음

---

# 역할별 최저급 기준 타워

## 견습 궁수

- TowerId: `TWR_APPRENTICE_ARCHER`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 단일 화력
- 보조 역할: 없음
- FeedbackWeight: Standard

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 스테이지 1 표준 일반 몬스터 단일 대상

### 행동

- TargetPolicy: 선두
- TargetLossPolicy: Retarget
- Movement: Formation
- FacingPolicy: TrackTarget
- ActionRoutine: Impact
- Delivery: Projectile
- DeliveryModifiers: 없음
- ResourceProfile: 없음
- Extensions: 없음

### 기본 성능

- 기본 피해 또는 핵심 효과: 화살 피해 1.00
- 행동 주기: 1.00초
- 대상 수: 1
- 역할별 기여 계산: 기준 단일 DPS 1.00
- 성능 강화 적용값: 화살 피해
- 치명타 적용 여부: 예
- 이동속도·교전거리: 편대 유지, 별도 교전거리 없음
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 안정적인 단일 대상 지속 피해
- 동일 효과 중첩 규칙: 별도 제한 없음
- 역할 슬롯 후보: 단일 화력
- 권장 타겟 정책: 선두 또는 균형

### 타격감

- 준비 동작: 상체를 크게 뒤로 젖히며 활시위를 끝까지 당김
- 판정 순간: 활시위가 빠르게 수축하며 화살 발사
- 공격자 반동: 활과 상체가 짧게 뒤로 튕김
- 대상 피격 반응: 작은 뒤틀림과 화살 방향의 짧은 밀림 표현
- 효과·음향: 선명한 시위음, 짧은 바람 Trail, 목재·살점 명중음
- 치명타 강화 표현: 더 굵은 Trail과 날카로운 명중음
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `ApprenticeArcher`
- 주요 모션 견본: `Aim`, `FullDraw`, `Release`, `Recoil`
- 효과·음향: 기본 화살 Trail, 시위·명중음
- 공격·효과 기준점: 활시위 중앙, 화살촉

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 아직 정식 군복도 받지 못했지만, 화살 한 발만큼은 정확히 쏘려 노력하는 궁수입니다.
- 제작 메모: 단일 화력 역할의 모든 후속 타워를 비교하는 기준점

---

## 돌팔매꾼

- TowerId: `TWR_STONE_SLINGER`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 광역 화력
- 보조 역할: 없음
- FeedbackWeight: Standard

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 평균 1.67마리가 폭발 반경에 포함되는 군집

### 행동

- TargetPolicy: 가장 밀집된 집단
- TargetLossPolicy: FinishAtPosition
- Movement: Formation
- FacingPolicy: FaceTargetOnce
- ActionRoutine: Impact
- Delivery: Projectile
- DeliveryModifiers: Splash
- ResourceProfile: 없음
- Extensions: 없음

### 기본 성능

- 기본 피해 또는 핵심 효과: 충돌 지점 주변 최대 3대상에게 각각 피해 0.60
- 행동 주기: 1.00초
- 대상 수: 최대 3
- 역할별 기여 계산: 평균 1.67대상 × 0.60 = 유효 DPS 약 1.00
- 성능 강화 적용값: 충돌·범위 피해
- 치명타 적용 여부: 예, 대상별 판정
- 이동속도·교전거리: 편대 유지
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 스테이지 후보의 평균 군집도와 예상 동시 명중 수
- 동일 효과 중첩 규칙: 별도 제한 없음
- 역할 슬롯 후보: 광역 화력
- 권장 타겟 정책: 밀집 집단

### 타격감

- 준비 동작: 팔 전체로 투석구를 크게 두 번 회전
- 판정 순간: 몸을 앞으로 비틀며 돌을 힘껏 방출
- 공격자 반동: 회전 관성으로 상체가 한 바퀴 가까이 따라감
- 대상 피격 반응: 중심 대상은 눌리고 주변 대상은 바깥으로 흔들림
- 효과·음향: 돌의 휘파람음, 충돌 먼지와 작은 파편 고리
- 치명타 강화 표현: 큰 파편과 무거운 파쇄음
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `StoneSlinger`
- 주요 모션 견본: `WindupLoop`, `Release`, `FollowThrough`
- 효과·음향: 돌 투사체, 먼지 Splash, 파쇄음
- 공격·효과 기준점: 투석구 주머니, 충돌 중심

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 좋은 무기가 없어도 주변에 돌은 많습니다. 여러 적이 모였을 때는 의외로 쓸 만합니다.
- 제작 메모: 광역 역할의 평균 대상 수 환산 기준점

---

## 서리 견습생

- TowerId: `TWR_FROST_NOVICE`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 제어
- 보조 역할: 단일 화력
- FeedbackWeight: Standard

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 스테이지 1 표준 경로에서 선두 적을 지속 감속

### 행동

- TargetPolicy: 선두
- TargetLossPolicy: Retarget
- Movement: Formation
- FacingPolicy: TrackTarget
- ActionRoutine: Impact
- Delivery: Projectile
- DeliveryModifiers: 없음
- ResourceProfile: 없음
- Extensions: `ApplySlow`

### 기본 성능

- 기본 피해 또는 핵심 효과: 냉기 피해 0.55, 이동속도 15% 감소
- 행동 주기: 1.00초
- 대상 수: 1
- 역할별 기여 계산: 직접 DPS 0.55 + 경로 지연 환산 0.45
- 감속 지속시간: 1.25초, 재명중 시 갱신
- 성능 강화 적용값: 피해와 지정된 제어 기여도
- 치명타 적용 여부: 피해만 적용, 감속 수치에는 미적용
- 이동속도·교전거리: 편대 유지
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 실제로 추가 확보한 경로 시간과 그 시간 동안 편성이 가한 기대 피해
- 동일 효과 중첩 규칙: 같은 감속은 가장 강한 값 사용, 지속시간 갱신
- 역할 슬롯 후보: 제어
- 권장 타겟 정책: 선두

### 타격감

- 준비 동작: 지팡이를 뒤로 당기며 끝의 서리 결정이 압축됨
- 판정 순간: 짧고 날카로운 냉기 탄환 발사
- 공격자 반동: 손목과 지팡이가 위로 튕김
- 대상 피격 반응: 몸이 순간 수축하고 발밑에 얼음 테두리 생성
- 효과·음향: 얇은 얼음 파열음, 푸른 냉기 잔상
- 치명타 강화 표현: 결정 파편이 크게 갈라지고 높은 파열음 재생
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `FrostNovice`
- 주요 모션 견본: `GatherCold`, `Cast`, `WandRecoil`
- 효과·음향: 냉기 탄환, 발밑 감속 테두리, 얼음 파열음
- 공격·효과 기준점: 지팡이 끝, 대상 발밑

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 얼릴 수 있는 것은 아직 발끝 정도지만, 느려진 적은 그만큼 오래 공격받습니다.
- 제작 메모: 제어 효과를 EquivalentContribution으로 환산하는 기준점

---

## 골목 도적

- TowerId: `TWR_ALLEY_CUTPURSE`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 마무리
- 보조 역할: 단일 화력
- FeedbackWeight: Standard

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 체력이 고르게 깎이는 표준 몬스터 집단

### 행동

- TargetPolicy: 마무리
- TargetLossPolicy: Retarget
- Movement: Engage
- FacingPolicy: 이동 중 FaceMovement, 공격 중 FaceTargetOnce
- ActionRoutine: Impact
- Delivery: Contact
- DeliveryModifiers: 없음
- ResourceProfile: 없음
- Extensions: `LowHealthMultiplier`

### 기본 성능

- 기본 피해 또는 핵심 효과: 단검 피해 0.80
- 행동 주기: 1.00초
- 대상 수: 1
- 마무리 효과: 현재 체력 30% 이하 대상에게 피해 ×2.00
- 역할별 기여 계산: 기본 피해 + 마무리 구간 추가 피해 - Engage 접근 손실
- 성능 강화 적용값: 기본·마무리 피해
- 치명타 적용 여부: 예
- 이동속도·교전거리: 임시 이동속도 14 studs/s, 교전거리 3.5 studs
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 마무리 구간 진입 빈도와 실제 오버킬 감소량
- 동일 효과 중첩 규칙: 별도 제한 없음
- 역할 슬롯 후보: 마무리
- 권장 타겟 정책: 현재 체력이 가장 낮은 적

### 타격감

- 준비 동작: 몸을 낮추고 단검을 허리 뒤까지 크게 당김
- 판정 순간: 대상 옆으로 짧게 파고들며 가로 베기
- 공격자 반동: 타격 뒤 한 발 미끄러지며 자세 회수
- 대상 피격 반응: 베기 방향으로 상체가 크게 꺾임
- 효과·음향: 짧은 금속 긁힘, 얇은 베기 Trail, 낮은 체력 대상은 날카로운 강조음
- 치명타 강화 표현: 두꺼운 베기 Trail과 짧은 정지감의 로컬 모델 포즈
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `AlleyCutpurse`
- 주요 모션 견본: `CrouchReady`, `DashIn`, `Slash`, `Recover`
- 효과·음향: 단검 Trail, 천·금속 마찰음, 마무리 강조음
- 공격·효과 기준점: 단검 끝, 대상 몸통

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 정면 승부보다는 이미 비틀거리는 적을 골라 빠르게 끝내는 데 익숙합니다.
- 제작 메모: Engage 이동 손실과 마무리 보너스 환산 기준점

---

## 신참 북잡이

- TowerId: `TWR_ROOKIE_DRUMMER`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 지원
- 보조 역할: 단일 화력
- FeedbackWeight: Standard

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 자신 외 기준 타워 3개가 편성된 4슬롯 편대

### 행동

- TargetPolicy: 균형
- TargetLossPolicy: Retarget
- Movement: Formation
- FacingPolicy: FaceTargetOnce
- ActionRoutine: Impact
- Delivery: Hitscan
- DeliveryModifiers: 없음
- ResourceProfile: 없음
- Extensions: `PassiveFormationAura`

### 기본 성능

- 기본 피해 또는 핵심 효과: 음파 피해 0.55
- 행동 주기: 1.00초
- 대상 수: 1
- 지원 효과: 자신을 제외한 편성 타워의 핵심 성능 +15%
- 역할별 기여 계산: 직접 DPS 0.55 + 기준 타워 3개의 추가 기여 0.45
- 성능 강화 적용값: 음파 피해와 지원 효과의 지정 성장값
- 치명타 적용 여부: 음파 피해만 적용, 지원 효과에는 미적용
- 이동속도·교전거리: 편대 유지
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 현재 편성에 실제로 더한 추가 EquivalentContribution
- 동일 효과 중첩 규칙: 같은 `TWR_ROOKIE_DRUMMER`의 지원 효과는 중첩하지 않고 가장 높은 값만 적용
- 역할 슬롯 후보: 지원
- 권장 타겟 정책: 균형

### 타격감

- 준비 동작: 북채를 머리 위까지 크게 들어 올림
- 판정 순간: 북 표면이 과장되게 눌렸다 펴지며 원형 음파 방출
- 공격자 반동: 양팔과 북이 아래로 크게 처졌다 복원
- 대상 피격 반응: 음파 방향으로 몸이 한 번 크게 출렁임
- 효과·음향: 짧고 두꺼운 북소리, 투명한 원형 파동, 강화된 아군에 작은 박자 광택
- 치명타 강화 표현: 더 깊은 북소리와 굵은 파동 테두리
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `RookieDrummer`
- 주요 모션 견본: `RaiseSticks`, `DrumImpact`, `DrumRebound`
- 효과·음향: 원형 음파, 북소리, 지원 광택
- 공격·효과 기준점: 북 중앙, 타겟 방향 파동 중심

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 박자가 자주 흔들리지만, 동료들은 그 소리를 들으면 조금 더 힘을 냅니다.
- 제작 메모: 지원 타워가 첫 굴림으로 나와도 전투를 진행할 수 있는 최소 공격력 보유

---

## 멧돼지 사냥꾼

- TowerId: `TWR_BOAR_HUNTER`
- 상태: **Confirmed (Provisional Balance)**
- 획득 방식: 일반 굴리기
- BaseOddsN: `"10"`
- 공식 기본 표시: `1 / 10`
- ProbabilityTableVersion: `PRELAUNCH-BENCHMARK-001`
- CommonReserve 대상: 아니오
- 보조 등급: 최저급
- 주 역할: 대형 사냥
- 보조 역할: 단일 화력
- FeedbackWeight: Heavy

### 희귀도·전투 예산

- log10(BaseOddsN): 1.000
- RawPowerBudget: 1.000
- FinalPowerBudget: 1.000
- 동일 역할 희귀도 순위: 1
- 이전 타워 대비 최소 기여도 증가 검증: 역할 시작점
- EquivalentContribution 기준값: 1.000
- 기준 전투 시나리오: 일반 웨이브 4회와 보스 웨이브 1회의 가중 평균

### 행동

- TargetPolicy: 강적
- TargetLossPolicy: FinishAtPosition
- Movement: Formation
- FacingPolicy: FaceTargetOnce
- ActionRoutine: ChargeRelease
- Delivery: Projectile
- DeliveryModifiers: 없음
- ResourceProfile: 없음
- Extensions: `LargeTargetMultiplier`

### 기본 성능

- 기본 피해 또는 핵심 효과: 투창 피해 1.60
- 행동 주기: 2.00초
- 대상 수: 1
- 대형 사냥 효과: 정예·보스 대상 피해 +125%, 최종 3.60
- 역할별 기여 계산: 일반 DPS 0.80 × 4웨이브 + 보스 DPS 1.80 × 1웨이브의 평균 = 1.00
- 성능 강화 적용값: 일반·대형 대상 피해
- 치명타 적용 여부: 예
- 이동속도·교전거리: 편대 유지
- 큰 수 형식 사용 여부: 기본값은 일반 수치, 최종 계산은 공통 수치 모듈

### 자동 편성

- 평가 기준: 스테이지 내 정예·보스 체력 비중과 대형 대상 기대 피해
- 동일 효과 중첩 규칙: 별도 제한 없음
- 역할 슬롯 후보: 대형 사냥
- 권장 타겟 정책: 최대 체력이 가장 높은 적

### 타격감

- 준비 동작: 창을 등 뒤까지 크게 젖히고 한 발을 깊게 디딤
- 판정 순간: 전신을 앞으로 던지듯 창을 투척
- 공격자 반동: 투척 뒤 상체가 아래로 크게 쏠렸다 회복
- 대상 피격 반응: 일반 적은 뒤로 크게 젖고, 보스는 무거운 표면 충격파 발생
- 효과·음향: 굵은 바람 가르기, 묵직한 창 명중음, 보스 명중 시 저음 강조
- 치명타 강화 표현: 창 궤적이 굵어지고 명중 지점에 짧은 방사형 파편
- 카메라 흔들림: 없음

### 제작 자산

- ModelKit: `BoarHunter`
- 주요 모션 견본: `Brace`, `FullDrawSpear`, `Throw`, `Recover`
- 효과·음향: 창 Trail, 일반·보스 명중음 분리
- 공격·효과 기준점: 손의 창 그립, 창촉

### 성장과 수집

- 합체 결과: 미정
- 합체 필요 수량: 3 예정
- 변종 합체 규칙: 같은 변종끼리만
- 허용 변종 계열: 미정
- 도감 설명: 마을 주변의 큰 짐승을 쫓아내던 사냥꾼입니다. 작은 적보다 커다란 목표에 창을 꽂는 데 익숙합니다.
- 제작 메모: 일반 웨이브와 보스 웨이브 가중 평균을 사용하는 대형 사냥 기준점

---

## 출시 목표

| 역할 | 목표 수량 | Confirmed | Implemented |
|---|---:|---:|---:|
| 단일 화력 | 8~10 | 1 | 0 |
| 광역 화력 | 8~10 | 1 | 0 |
| 제어 | 8~10 | 1 | 0 |
| 마무리 | 8~10 | 1 | 0 |
| 지원 | 8~10 | 1 | 0 |
| 대형 사냥 | 8~10 | 1 | 0 |

복합 역할은 한 종류로만 계산합니다.

---

## 다양성 점검

현재 기준 타워 분포:

- Movement: Formation 5, Engage 1
- ActionRoutine: Impact 5, ChargeRelease 1
- Delivery: Projectile 4, Contact 1, Hitscan 1
- FeedbackWeight: Standard 5, Heavy 1
- 모든 역할에 최저급 기준점 1종 존재

출시 목록 점검:

- 이동 방식 분포
- 행동 루틴 분포
- 전달 방식 분포
- 실루엣 분포
- 피드백 무게 분포
- 단순 타워와 고유 확장 타워 비율
- 공식 분모 범위: 1/10부터 수십억·수조 이상
- 같은 역할의 희귀도별 단계가 비어 있지 않은가

---

## 현재 작성 상태

역할별 최저급 기준 타워 6종을 등록했습니다.

```text
단일 화력: 견습 궁수
광역 화력: 돌팔매꾼
제어: 서리 견습생
마무리: 골목 도적
지원: 신참 북잡이
대형 사냥: 멧돼지 사냥꾼
```

다음 검증 단계는 이 여섯 타워를 스테이지 1 표준 몬스터와 4슬롯 편성 시나리오에서 시뮬레이션해 `EquivalentContribution = 1.000`에 맞추는 것입니다.