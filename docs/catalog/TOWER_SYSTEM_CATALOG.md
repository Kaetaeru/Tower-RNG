# V1 변종·합체 시스템 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed System Values · Individual Content Pending**
- 카탈로그 버전: `V1-2026-08-03`
- 계산 근거: `../balance/V1_TOWER_VARIANT_BENCHMARK.md`, `../balance/V1_FUSION_BENCHMARK.md`, `../balance/FINAL_RECOMMENDATION.md`
- 상위 기획: `../design/TOWER_VARIANTS.md`, `../design/FUSION.md`
- 관련 카탈로그: `STAT_TREE_CATALOG.md`
- 구현 상태: **Not Implemented**
- 마지막 정리: 2026-08-03

## 책임

이 문서는 변종 계열의 공식 티켓 확률·전투력 예산과 수동 합체의 공통 조합 규칙을 소유합니다.

아직 소유하지 않는 항목:

- 개별 변종 `TowerId`
- 타워별 허용 계열
- 개별 합체 결과 `TowerId`
- 개별 행동·모델·애니메이션·VFX·SFX

공통 수치를 바꾸려면 관련 밸런스 계산과 전체 계정 경로를 다시 검증해야 합니다.

---

# 1. 변종 계열

| VariantFamilyId | 표시 이름 | 공식 티켓 | PowerBudget 배율 | 상태 |
|---|---|---:|---:|---|
| `VARIANT_FAMILY_FIRE` | 인화성 | `1 / 5,000` | `×5.4928` | Confirmed |
| `VARIANT_FAMILY_TOXIC` | 독성 | `1 / 10,000` | `×6.3096` | Confirmed |
| `VARIANT_FAMILY_VOID` | 공허 | `1 / 20,000` | `×7.2478` | Confirmed |
| `VARIANT_FAMILY_GIANT` | 거대 | `1 / 50,000` | `×8.7055` | Confirmed |

모든 계열이 해금되고 선택된 기본 타워가 모든 계열을 허용할 때 원시 합계:

```text
1/5,000 + 1/10,000 + 1/20,000 + 1/50,000
= 0.00037
≈ 1 / 2,702.70
```

---

# 2. 변종 판정 계약

```text
1. 기존 일반 확률표와 현재 Compression으로 기본 타워 선택
2. 하나의 고정 변종 티켓에서 계열 구간 판정
3. 계열이 해금되고 기본 타워가 해당 계열을 허용하며 허용 범위 안이면 변종 지급
4. 조건이 맞지 않으면 원래 기본형 지급
```

불변 규칙:

- 한 굴림에서 타워는 하나만 지급합니다.
- 한 굴림에서 변종은 최대 하나입니다.
- 일반 행운·황금 주사위·다이아몬드 주사위는 기본 타워 선택에만 적용합니다.
- 변종 티켓에 일반 행운을 두 번째로 적용하지 않습니다.
- 잠긴 계열 구간은 다른 계열로 재분배하지 않습니다.
- 새 계열을 해금해도 기존 계열의 티켓 확률은 변하지 않습니다.
- 허용되지 않은 계열이 나오면 기본형을 지급합니다.
- 변종 해금은 환생 후 유지합니다.
- Robux로 특정 변종 결과를 직접 구매하지 않습니다.

최종 공식 기본 분모:

```text
VariantBaseOddsN
= BaseTowerOddsN × FamilyOddsN
```

예:

```text
기본 타워 1 / 10
인화성 티켓 1 / 5,000
→ 인화성 변종 1 / 50,000
```

---

# 3. 변종 PowerBudget

```text
VariantPowerMultiplier
= FamilyOddsN ^ 0.20

VariantPowerBudget
= BaseTowerPowerBudget × VariantPowerMultiplier
```

이는 일반 희귀도 공식과 동일한 순서를 유지합니다.

```text
RawPowerBudget(BaseN × FamilyN)
= RawPowerBudget(BaseN) × FamilyN^0.20
```

PowerBudget 전체를 직접 피해에 넣지 않습니다. 개별 변종 카탈로그는 예산을 다음 요소에 나눠 배정합니다.

- 기본 행동 강화
- 지속 피해·폭발·전염·연쇄
- 범위·대상 수·타겟 전환
- 역할 고유 지원·제어 기여
- 템포·조건·제약

같은 최종 분모의 일반 타워보다 임의로 더 높은 총 기여도를 주지 않습니다.

---

# 4. 변종 허용 범위

각 계열은 `STAT_TREE_CATALOG.md`의 독립 가지를 사용합니다.

| 단계 | 허용 기본 타워 |
|---|---:|
| 계열 해금 | 공식 확률표 1~12번 |
| 확장 I | 공식 확률표 1~31번 |
| 확장 II | 공식 확률표 1~50번 |

타워별 `AllowedVariantFamilies`는 개별 타워 카탈로그에서 작성합니다. 모든 타워에 모든 계열을 강제하지 않습니다.

---

# 5. 변종 개체 계약

각 변종은 별도 `TowerId`입니다.

최소 필드:

```text
TowerId
BaseTowerId
VariantFamilyId
BaseOddsN
PowerBudget
Role
AllowedFusionLineageId
ModelAssetId
AnimationProfileId
VfxProfileId
SfxProfileId
BalanceStatus
ImplementationStatus
```

불변 규칙:

- 동일 변종은 항상 같은 성능과 외형을 사용합니다.
- 개체별 무작위 옵션을 사용하지 않습니다.
- 기본형과 수량을 합산하지 않습니다.
- 환생으로 변종 수량이 사라지지 않습니다.
- 거래는 지원하지 않습니다.

---

# 6. 기본형 합체

## 1단계

| FusionRecipeId | 재료 | 결과 | PowerBudget | 상태 |
|---|---|---|---:|---|
| `FUSION_TIER_1` | 같은 기본 `TowerId` 3개 | 해당 계보 1단계 `TowerId` 1개 | 기본형 `×1.45` | Confirmed |

등가 분모 증가:

```text
1.45^5 ≈ 6.4097배
```

## 2단계

| FusionRecipeId | 재료 | 결과 | PowerBudget | 상태 |
|---|---|---|---:|---|
| `FUSION_TIER_2` | 같은 1단계 결과 `TowerId` 3개 | 해당 계보 2단계 `TowerId` 1개 | 기본형 `×2.1025` | Confirmed |

총 기본형 재료:

```text
9개
```

등가 분모 증가:

```text
2.1025^5 ≈ 41.0847배
```

V1 최대 합체 단계는 2단계입니다.

---

# 7. 합체 허용 범위

| 구매 노드 | 허용 범위 |
|---|---|
| `NODE_FUSION_CORE` | 확률표 1~31번 기본형의 1단계 |
| `NODE_FUSION_ADVANCED` | 허용 계보의 2단계 |
| `NODE_FUSION_RARE_LINEAGE` | 확률표 32~50번 계보 포함 |

개별 타워는 다음 중 하나를 명시합니다.

```text
기본형 합체 계보
변종 대응 계보
변종 전용 계보
합체 불가
```

개별 결과 `TowerId`와 고유 행동은 향후 타워 카탈로그에서 확정합니다.

---

# 8. 변종 합체

```text
같은 BaseTowerId
AND 같은 VariantFamilyId
AND 같은 변종 TowerId
AND 대응 계보 존재
```

위 조건을 모두 만족할 때만 1단계 변종 합체를 허용합니다.

금지:

- 기본형 + 변종
- 서로 다른 변종 계열
- 서로 다른 변종 `TowerId`
- 계보가 없는 변종

V1에서 변종 2단계 합체는 핵심 진행으로 요구하지 않습니다. 대응 계보가 작성되지 않은 변종은 합체할 수 없습니다.

---

# 9. 실행 계약

합체 가능 수량:

```text
AvailableForFusion
= OwnedCount
- ProtectedCount
- EquippedCount
```

실행 순서:

```text
TransactionId 검증
→ 계보·재료·보호·편성 수량 검증
→ 재료 차감
→ 고정 결과 지급
→ 합체 누적·도감 갱신
→ 중요 저장 예약
```

불변 규칙:

- 성공률은 100%입니다.
- 실행 코인 비용은 0입니다.
- 실행 정수 비용은 0입니다.
- 대기시간과 합체권을 사용하지 않습니다.
- 자동 합체를 사용하지 않습니다.
- 플레이어가 승인한 수동 일괄 실행은 허용할 수 있습니다.
- 클라이언트가 결과 `TowerId`를 결정할 수 없습니다.
- 편성 중이거나 보호된 수량을 자동 소비하지 않습니다.

---

# 10. 아직 미작성인 콘텐츠

- 50개 기본 타워의 `AllowedVariantFamilies`
- 각 변종의 실제 `TowerId`와 이름
- 변종별 예산 배분과 공격 행동
- 기본형·변종 합체 계보
- 합체 결과의 실제 `TowerId`, 이름과 행동
- 모델·애니메이션·VFX·SFX 자산
- 도감 정렬과 획득 연출

이 항목들은 공통 티켓 확률과 합체 배율을 변경하지 않는 범위에서 후속 카탈로그 작업으로 작성합니다.
