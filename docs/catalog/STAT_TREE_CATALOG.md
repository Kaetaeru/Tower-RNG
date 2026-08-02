# V1 코인 스탯 트리 카탈로그

- 계층: 콘텐츠 카탈로그
- 상태: **Confirmed Values · Layout Pending**
- 카탈로그 버전: `V1-2026-08-03`
- 계산 근거: `../balance/FINAL_RECOMMENDATION.md`, `../balance/V1_GATE_ECONOMY_BENCHMARK.md`, `../balance/V1_TOWER_VARIANT_BENCHMARK.md`, `../balance/V1_FUSION_BENCHMARK.md`, `../balance/OFFLINE_COIN_BENCHMARK.md`, `../balance/MASTERY_UTILITY_SINK_BENCHMARK.md`
- 상위 기획: `../design/STAT_TREE.md`
- 구현 상태: **Not Implemented**
- 마지막 정리: 2026-08-03

## 책임

이 문서는 V1 코인 스탯 트리에 채택된 실제 `NodeId`, 가격과 효과를 소유합니다.

```text
가격·효과·최대 단계 = Confirmed
트리 좌표·아이콘·세부 연결선 = Pending
Roblox 구현 = Not Implemented
```

좌표와 아이콘이 미작성이어도 아래 값은 더 이상 계산용 임시값이 아닙니다. 가격 또는 효과를 바꾸려면 관련 밸런스 문서를 다시 실행하고 카탈로그를 명시적으로 갱신합니다.

---

# 1. 공통 구매 계약

- 모든 구매 결과는 계정에 영구 유지됩니다.
- 환생으로 노드가 초기화되지 않습니다.
- 클라이언트는 가격·효과·구매 결과를 결정할 수 없습니다.
- 서버가 `NodeId`, 선행 조건, 현재 단계와 코인을 다시 검증합니다.
- 코인 차감과 노드 단계 증가는 하나의 프로필 변경으로 처리합니다.
- 동일 구매 요청 재전송으로 중복 차감하지 않습니다.
- Robux로 핵심 전투·확률·문 진행을 직접 대체하지 않습니다.

최소 저장 데이터:

```text
PurchasedStatNodes[NodeId] = Level
```

---

# 2. 최초 중심부

| NodeId | 표시 이름 | 가격 | 효과 | 선행 노드 | 상태 |
|---|---|---:|---|---|---|
| `NODE_AUTO_ROLL` | 자동 굴리기 | 10 | 기본 4.0초 간격 자동 굴리기 ON/OFF | 없음 | Confirmed |
| `NODE_AUTO_FORMATION` | 자동 편성 | 30 | 자동 편성 ON/OFF와 역할 성향 | `NODE_AUTO_ROLL` | Confirmed |
| `NODE_MAGNET_RANGE_1` | 자석 범위 I | 50 | 코인 흡입 반경 `+4 studs` | `NODE_AUTO_ROLL` | Confirmed |
| `NODE_CORE_OUTPUT_1` | 핵심 성능 I | 100 | 공통 역할 기여도 누적 `×1.25` | `NODE_AUTO_ROLL` | Confirmed |
| `NODE_ROLL_SPEED_1` | 굴리기 속도 I | 160 | 기본 간격 `4.0초 → 3.6초` | `NODE_AUTO_ROLL` | Confirmed |
| `NODE_MAGNET_SPEED_1` | 자석 속도 I | 220 | 코인 흡입 이동속도 `+35%` | `NODE_MAGNET_RANGE_1` | Confirmed |
| `NODE_COMBAT_BRANCH` | 전투 분야 해금 | 450 | 후속 공통 전투 노드 공개 | `NODE_CORE_OUTPUT_1` | Confirmed |
| `NODE_COIN_YIELD_1` | 코인 획득 I | 550 | 온라인·오프라인 기준 코인 배율 `×1.15` | `NODE_MAGNET_SPEED_1` | Confirmed |
| `NODE_CORE_OUTPUT_2` | 핵심 성능 II | 650 | 공통 역할 기여도 누적 `×1.50` | `NODE_COMBAT_BRANCH` | Confirmed |
| `NODE_FORMATION_SLOT_5` | 편성 슬롯 5 | 1,200 | 전체 편성 슬롯 `4 → 5` | `NODE_AUTO_FORMATION` | Confirmed |

최초 중심부의 목표 시간은 밸런스 검증용이며 서버 데이터에는 저장하지 않습니다.

---

# 3. 편성 슬롯

| NodeId | 표시 이름 | 가격 | 구매 후 전체 슬롯 | 선행 노드 | 상태 |
|---|---|---:|---:|---|---|
| `NODE_FORMATION_SLOT_5` | 편성 슬롯 5 | 1,200 | 5 | `NODE_AUTO_FORMATION` | Confirmed |
| `NODE_FORMATION_SLOT_6` | 편성 슬롯 6 | 15,000 | 6 | `NODE_FORMATION_SLOT_5` | Confirmed |
| `NODE_FORMATION_SLOT_7` | 편성 슬롯 7 | 170,000 | 7 | `NODE_FORMATION_SLOT_6` | Confirmed |
| `NODE_FORMATION_SLOT_8` | 편성 슬롯 8 | 1,500,000 | 8 | `NODE_FORMATION_SLOT_7` | Confirmed |
| `NODE_FORMATION_SLOT_9` | 편성 슬롯 9 | 9,000,000 | 9 | `NODE_FORMATION_SLOT_8` | Confirmed |
| `NODE_FORMATION_SLOT_10` | 편성 슬롯 10 | 80,000,000 | 10 | `NODE_FORMATION_SLOT_9` | Confirmed |
| `NODE_FORMATION_SLOT_11` | 편성 슬롯 11 | 400,000,000 | 11 | `NODE_FORMATION_SLOT_10` | Confirmed |
| `NODE_FORMATION_SLOT_12` | 편성 슬롯 12 | 2,300,000,000 | 12 | `NODE_FORMATION_SLOT_11` | Confirmed |

누적 가격:

```text
2,790,686,200
```

역할별 배치 상한:

```text
RoleCap = max(2, ceil(TotalSlots / 3))

4~6슬롯   역할당 최대 2
7~9슬롯   역할당 최대 3
10~12슬롯 역할당 최대 4
```

별도의 역할 슬롯 구매는 사용하지 않습니다.

---

# 4. 공통 전투 성장

| NodeId | 표시 이름 | 가격 | 단계 증가 | 누적 배율 | 선행 노드 | 상태 |
|---|---|---:|---:|---:|---|---|
| `NODE_CORE_OUTPUT_1` | 핵심 성능 I | 100 | `+0.25` | `×1.25` | `NODE_AUTO_ROLL` | Confirmed |
| `NODE_CORE_OUTPUT_2` | 핵심 성능 II | 650 | `+0.25` | `×1.50` | `NODE_COMBAT_BRANCH` | Confirmed |
| `NODE_CORE_OUTPUT_3` | 핵심 성능 III | 12,000 | `+0.25` | `×1.75` | `NODE_CORE_OUTPUT_2` | Confirmed |
| `NODE_CORE_OUTPUT_4` | 핵심 성능 IV | 42,000 | `+0.25` | `×2.00` | `NODE_CORE_OUTPUT_3` | Confirmed |
| `NODE_CORE_OUTPUT_5` | 핵심 성능 V | 290,000 | `+0.30` | `×2.30` | `NODE_CORE_OUTPUT_4` | Confirmed |
| `NODE_CORE_OUTPUT_6` | 핵심 성능 VI | 3,300,000 | `+0.35` | `×2.65` | `NODE_CORE_OUTPUT_5` | Confirmed |
| `NODE_CORE_OUTPUT_7` | 핵심 성능 VII | 25,000,000 | `+0.40` | `×3.05` | `NODE_CORE_OUTPUT_6` | Confirmed |
| `NODE_CORE_OUTPUT_8` | 핵심 성능 VIII | 45,000,000 | `+0.45` | `×3.50` | `NODE_CORE_OUTPUT_7` | Confirmed |
| `NODE_CORE_OUTPUT_9` | 핵심 성능 IX | 280,000,000 | `+0.50` | `×4.00` | `NODE_CORE_OUTPUT_8` | Confirmed |
| `NODE_CORE_OUTPUT_10` | 핵심 성능 X | 1,950,000,000 | `+0.50` | `×4.50` | `NODE_CORE_OUTPUT_9` | Confirmed |
| `NODE_CORE_OUTPUT_11` | 핵심 성능 XI | 30,000,000,000 | `+0.50` | `×5.00` | `NODE_CORE_OUTPUT_10` | Confirmed |

전체 I~XI 누적 가격:

```text
32,303,644,750
```

적용 규칙:

- 모든 역할의 `EquivalentContribution`에 공통 적용합니다.
- 공격력·공격속도·치명타를 별도의 무제한 곱연산으로 다시 더하지 않습니다.
- V1 공통 코인 전투 성장 상한은 `×5.00`입니다.

---

# 5. 변종 가지

각 계열은 독립된 세 단계 가지입니다. 정확한 트리 좌표와 네 계열 입구의 공통 부모 노드는 아직 미작성입니다.

| NodeId | 표시 이름 | 가격 | 허용 기본 타워 범위 | 선행 노드 | 상태 |
|---|---|---:|---:|---|---|
| `NODE_VARIANT_FIRE_UNLOCK` | 인화성 변종 해금 | 3,500,000 | 확률표 1~12 | 특수 시스템 가지 입구 미작성 | Confirmed |
| `NODE_VARIANT_TOXIC_UNLOCK` | 독성 변종 해금 | 15,000,000 | 확률표 1~12 | 특수 시스템 가지 입구 미작성 | Confirmed |
| `NODE_VARIANT_VOID_UNLOCK` | 공허 변종 해금 | 50,000,000 | 확률표 1~12 | 특수 시스템 가지 입구 미작성 | Confirmed |
| `NODE_VARIANT_GIANT_UNLOCK` | 거대 변종 해금 | 150,000,000 | 확률표 1~12 | 특수 시스템 가지 입구 미작성 | Confirmed |
| `NODE_VARIANT_FIRE_EXPANSION_1` | 인화성 확장 I | 100,000,000 | 확률표 1~31 | `NODE_VARIANT_FIRE_UNLOCK` | Confirmed |
| `NODE_VARIANT_TOXIC_EXPANSION_1` | 독성 확장 I | 200,000,000 | 확률표 1~31 | `NODE_VARIANT_TOXIC_UNLOCK` | Confirmed |
| `NODE_VARIANT_VOID_EXPANSION_1` | 공허 확장 I | 500,000,000 | 확률표 1~31 | `NODE_VARIANT_VOID_UNLOCK` | Confirmed |
| `NODE_VARIANT_GIANT_EXPANSION_1` | 거대 확장 I | 1,000,000,000 | 확률표 1~31 | `NODE_VARIANT_GIANT_UNLOCK` | Confirmed |
| `NODE_VARIANT_FIRE_EXPANSION_2` | 인화성 확장 II | 1,000,000,000 | 확률표 1~50 | `NODE_VARIANT_FIRE_EXPANSION_1` | Confirmed |
| `NODE_VARIANT_TOXIC_EXPANSION_2` | 독성 확장 II | 2,000,000,000 | 확률표 1~50 | `NODE_VARIANT_TOXIC_EXPANSION_1` | Confirmed |
| `NODE_VARIANT_VOID_EXPANSION_2` | 공허 확장 II | 5,000,000,000 | 확률표 1~50 | `NODE_VARIANT_VOID_EXPANSION_1` | Confirmed |
| `NODE_VARIANT_GIANT_EXPANSION_2` | 거대 확장 II | 15,000,000,000 | 확률표 1~50 | `NODE_VARIANT_GIANT_EXPANSION_1` | Confirmed |

전체 가격:

```text
25,018,500,000
```

계열 해금 순서는 강제하지 않습니다. 한 계열을 추가 구매해도 다른 계열의 티켓 확률은 변하지 않습니다.

---

# 6. 수동 합체 가지

| NodeId | 표시 이름 | 가격 | 효과 | 선행 노드 | 상태 |
|---|---|---:|---|---|---|
| `NODE_FUSION_CORE` | 합체 핵심 해금 | 250,000 | 확률표 1~31 기본형의 1단계 합체 | 특수 시스템 가지 입구 미작성 | Confirmed |
| `NODE_FUSION_ADVANCED` | 고급 합체 | 750,000,000 | 2단계 합체 해금 | `NODE_FUSION_CORE` | Confirmed |
| `NODE_FUSION_RARE_LINEAGE` | 희귀 계보 확장 | 2,000,000,000 | 확률표 32~50 계보 허용 | `NODE_FUSION_ADVANCED` | Confirmed |

전체 가격:

```text
2,750,250,000
```

합체 실행 자체에는 코인·정수 비용이 없습니다. 실제 조합 규칙은 `TOWER_SYSTEM_CATALOG.md`가 소유합니다.

---

# 7. 오프라인 코인 가지

| NodeId | 표시 이름 | 가격 | 구매 후 효과 | 선행 노드 | 상태 |
|---|---|---:|---|---|---|
| `NODE_OFFLINE_UNLOCK` | 오프라인 코인 해금 | 100,000 | 효율 25%, 저장 8시간 | 수집·오프라인 가지 입구 미작성 | Confirmed |
| `NODE_OFFLINE_EFFICIENCY_2` | 오프라인 효율 II | 5,000,000 | 효율 30% | `NODE_OFFLINE_UNLOCK` | Confirmed |
| `NODE_OFFLINE_STORAGE_2` | 오프라인 저장 II | 15,000,000 | 저장 12시간 | `NODE_OFFLINE_EFFICIENCY_2` | Confirmed |
| `NODE_OFFLINE_EFFICIENCY_3` | 오프라인 효율 III | 100,000,000 | 효율 35% | `NODE_OFFLINE_STORAGE_2` | Confirmed |
| `NODE_OFFLINE_STORAGE_3` | 오프라인 저장 III | 500,000,000 | 저장 24시간 | `NODE_OFFLINE_EFFICIENCY_3` | Confirmed |
| `NODE_OFFLINE_EFFICIENCY_4` | 오프라인 효율 IV | 2,500,000,000 | 효율 40% | `NODE_OFFLINE_STORAGE_3` | Confirmed |

전체 가격:

```text
3,120,100,000
```

오프라인 기준:

```text
OfflineAnchorStage
= max(1, 3 × floor((HighestCompletedStage - 1) / 3))
```

| 최고 완주 스테이지 | 기준 스테이지 |
|---:|---:|
| 1~3 | 1 |
| 4~6 | 3 |
| 7~9 | 6 |
| 10~12 | 9 |
| 13~15 | 12 |

오프라인에서는 타워·변종·굴림·Defense XP·환생·스테이지 진행이 발생하지 않습니다.

---

# 8. 숙련 제어실 가지

해금 조건:

```text
변종 가지 완료
AND 합체 가지 완료
AND 오프라인 가지 완료
```

| NodeId | 표시 이름 | 가격 | 누적 | 효과 | 선행 노드 | 상태 |
|---|---|---:|---:|---|---|---|
| `NODE_MASTERY_TELEPORTER_CORE` | 텔레포터 코어 | 250,000,000 | 250,000,000 | 열린 스테이지 이동 | 숙련 제어실 해금 조건 | Confirmed |
| `NODE_MASTERY_STAGE_FAVORITES` | 스테이지 즐겨찾기 | 500,000,000 | 750,000,000 | 빠른 목적지 저장 | `NODE_MASTERY_TELEPORTER_CORE` | Confirmed |
| `NODE_MASTERY_ROLE_TARGETING` | 역할별 타겟 명령 | 750,000,000 | 1,500,000,000 | 역할 단위 타겟 설정 | `NODE_MASTERY_STAGE_FAVORITES` | Confirmed |
| `NODE_MASTERY_FORMATION_PRESET_2` | 편성 프리셋 II | 1,000,000,000 | 2,500,000,000 | 추가 편성 저장 | `NODE_MASTERY_ROLE_TARGETING` | Confirmed |
| `NODE_MASTERY_TOWER_TARGETING` | 개별 타워 타겟 명령 | 1,500,000,000 | 4,000,000,000 | TowerId 단위 타겟 설정 | `NODE_MASTERY_FORMATION_PRESET_2` | Confirmed |
| `NODE_MASTERY_FORMATION_PRESET_3` | 편성 프리셋 III | 2,000,000,000 | 6,000,000,000 | 추가 편성 저장 | `NODE_MASTERY_TOWER_TARGETING` | Confirmed |
| `NODE_MASTERY_TARGET_PROFILE` | 타겟 프로필 저장 | 2,500,000,000 | 8,500,000,000 | 타겟 설정 묶음 저장 | `NODE_MASTERY_FORMATION_PRESET_3` | Confirmed |
| `NODE_MASTERY_QUICK_HUD` | 퀵 HUD 확장 | 3,000,000,000 | 11,500,000,000 | 전투 중 빠른 전환 | `NODE_MASTERY_TARGET_PROFILE` | Confirmed |
| `NODE_MASTERY_COIN_DISPLAY_MERGE` | 코인 표시·병합 제어 | 4,000,000,000 | 15,500,000,000 | 표시량·병합 방식 편의 | `NODE_MASTERY_QUICK_HUD` | Confirmed |
| `NODE_MASTERY_COLLECTION_PRESENTATION` | 도감·획득 연출 프리셋 | 4,500,000,000 | 20,000,000,000 | 수집·표현 설정 저장 | `NODE_MASTERY_COIN_DISPLAY_MERGE` | Confirmed |
| `NODE_MASTERY_CONTROL_ROOM` | 숙련 제어실 완성 | 5,200,000,000 | 25,200,000,000 | 해금 편의 기능 통합 관리 | `NODE_MASTERY_COLLECTION_PRESENTATION` | Confirmed |

숙련 제어실은 다음 값을 증가시키지 않습니다.

- 타워 전투력과 편성 슬롯
- 일반 행운과 굴리기 속도
- 변종 티켓 확률과 합체 배율
- 코인 드롭량과 오프라인 효율
- Defense XP와 환생 속도

`코인 표시·병합 제어`는 획득 가능한 총 코인을 바꾸지 않습니다.

---

# 9. 채택된 영구 노드 합계

아래 합계는 첫 중심부의 비전투 편의 노드와 스테이지 문을 제외합니다.

```text
편성 슬롯       2,790,686,200
공통 전투      32,303,644,750
변종           25,018,500,000
합체            2,750,250,000
오프라인        3,120,100,000
숙련 제어실    25,200,000,000
```

---

# 10. 아직 미작성인 콘텐츠

- 전체 트리의 실제 X·Y 좌표
- 가지 입구 공통 부모 노드와 연결선
- 일부 노드의 최소 환생 횟수 조건
- 아이콘, 분야 색상과 구매 연출
- 모바일·PC 확대·이동 UI
- 각 노드의 Roblox 데이터 모듈 경로

이 항목들은 채택 가격과 효과를 바꾸지 않는 범위에서 기술 명세와 UI 카탈로그에서 확정합니다.
