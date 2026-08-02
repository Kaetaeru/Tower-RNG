# 타워 모델링·모션 규약

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 구현 상태: 미구현
- 관련 문서: `../design/TOWER_BEHAVIOR.md`, `../design/PRESENTATION_FEEL.md`, `TOWER_BEHAVIOR_GRAMMAR.md`
- 마지막 정리: 2026-08-02

> 이 문서는 타워 3D 모델과 모션 견본을 제작하는 현재 확정 기준입니다.
> 새 요구가 생기면 문서를 먼저 갱신한 뒤 구현과 제작 규약을 함께 수정합니다.

---

## 1. 기본 전제

타워는 3D `Model`로 제작합니다.

BillboardGui 기반 타워를 기본 모델링 방식으로 사용하지 않습니다.

인간형 구조는 필수가 아닙니다.

허용 예:

- 인간형 검사
- 총기형 기계
- 부유하는 수정과 무기
- 하나의 거대한 MeshPart
- 여러 파츠가 분리된 추상 오브젝트
- 석판, 토템, 눈, 고리

관절, 팔, 다리, Motor6D와 일반 캐릭터 리그는 필수가 아닙니다.

모델과 모션은 단순히 판정을 표시하는 수단이 아니라 타격감의 핵심입니다. 실루엣 변화가 거의 없는 작은 움직임보다 멀리서도 읽히는 과장된 준비·공격·반동을 우선합니다.

---

## 2. 키트 구조

키트 하나는 기본 모델, 자유 이름의 모션 견본과 행동 모듈을 포함합니다.

```text
SwordsmanKit
├─ Basic
├─ SwordUp
├─ HeavySlash
├─ Spin
├─ Victory
└─ SwordsmanModule
```

### 예약 이름

현재 예약된 모델 이름은 `Basic` 하나입니다.

- `Basic`: 게임에서 실제로 복제되어 움직이는 기본 3D 모델
- 그 외 같은 키트의 Model: 이름으로 호출할 수 있는 모션 상태 견본

`BeforeAttack`, `Attack`, `Recover`는 고정 이름이 아닙니다.

모션 이름은 자유롭게 정합니다.

```text
SwordUp
HeavySlash
Charge
발도준비
발도
Pose17
```

---

## 3. 모션 호출

행동 모듈은 모션 견본 이름을 문자열로 호출합니다.

```lua
context:PlayPose("SwordUp", 0.3)
context:Wait(0.1)
context:PlayPose("HeavySlash", 0.12)
```

새 모션 제작 순서:

```text
1. Basic을 복제한다.
2. 자유로운 모션 이름을 붙인다.
3. Studio에서 해당 순간의 3D 상태를 만든다.
4. 행동 모듈에서 PlayPose("이름", 시간)을 호출한다.
```

공통 시스템은 모션 이름의 의미를 판단하지 않습니다.

---

## 4. 런타임 재생 방식

모션 견본 Model 자체를 게임 중 교체하지 않습니다.

런타임에는 `Basic` 복제본 하나가 존재합니다.

`PlayPose`는 지정된 모션 견본의 상태를 읽고 런타임 모델에 적용합니다.

```text
Basic 복제본
    ↓
PlayPose("HeavySlash", 0.12)
    ↓
HeavySlash 견본의 시각 상태로 변화
```

모션 견본들은 Studio에서 비교하기 편하게 서로 떨어뜨려 놓을 수 있습니다.

월드 절대 좌표가 아니라 각 견본 Model의 Pivot 기준 상대 상태를 사용합니다.

---

## 5. 구성요소 대응 방식

Attribute, PartId, CollectionService 태그와 별도 등록표를 사용하지 않습니다.

구성요소는 **이름과 모델 내부 상대 경로**로 대응합니다.

```text
Basic/Weapon/Blade
HeavySlash/Weapon/Blade
```

두 인스턴스의 상대 경로는 다음과 같습니다.

```text
Weapon/Blade
```

따라서 같은 요소로 취급합니다.

서로 다른 부모 아래에서는 같은 이름을 사용할 수 있습니다.

```text
Left/Gem
Right/Gem
```

같은 부모 아래에서는 이름을 중복하지 않습니다.

대응 경로의 클래스가 다르면 적용하지 않고 검증 경고를 출력합니다.

---

## 6. 전체 모션과 부분 모션

### 전체 모션

`Basic` 전체를 복제해 모든 요소의 상태를 작성합니다.

```text
HeavySlash
├─ Core
├─ Weapon
├─ Cape
└─ Floating
```

### 부분 모션

바뀌는 요소만 남길 수 있습니다.

```text
SwordShake
└─ Weapon
```

부분 모션 규칙:

- 모션 견본에 존재하는 대응 요소만 변화합니다.
- `Basic`에는 있지만 견본에 없는 요소는 현재 상태를 유지합니다.
- 견본에만 있고 `Basic`에는 없는 요소는 일반 포즈 변형 대상에서 제외합니다.
- 순간 생성되는 검기, 폭발, 투사체는 효과 또는 전달 시스템에서 생성합니다.

---

## 7. 모션은 전체 시각 상태 견본이다

모션 견본은 위치와 회전만 저장하지 않습니다.

각 견본은 해당 순간의 전체 3D 시각 상태를 표현합니다.

지원 대상 방향:

### BasePart 계열

- CFrame
- Size
- Color
- Transparency
- Reflectance
- Material
- CastShadow

### Attachment

- CFrame
- Visible

Attachment는 공격, 발사체와 효과의 기준점으로도 사용합니다.

```text
Basic/Weapon/ProjectileOrigin
Basic/Weapon/SlashOrigin
```

### Light

- Brightness
- Color
- Range
- Angle
- Shadows
- Enabled

### ParticleEmitter

- Enabled
- Rate
- Brightness
- LightEmission
- LightInfluence
- Color
- Transparency
- Size
- Speed
- Lifetime
- Rotation
- RotSpeed
- SpreadAngle
- Acceleration
- Drag

### Trail과 Beam

- Enabled
- Color
- Transparency
- Brightness
- LightEmission
- LightInfluence
- WidthScale
- TextureLength
- TextureSpeed
- Width0
- Width1
- CurveSize0
- CurveSize1

### Highlight

- Enabled
- FillColor
- FillTransparency
- OutlineColor
- OutlineTransparency
- DepthMode

정확한 지원 속성은 중앙 시각 속성 레지스트리에서 관리합니다.

---

## 8. 속성 적용 방식

### 연속 보간

중간값이 존재하는 속성은 `PlayPose` 시간 동안 부드럽게 변화합니다.

예:

- CFrame
- Size
- Color
- Transparency
- Reflectance
- Brightness
- Range
- 일부 수치형 속성

### 단계 전환

중간값이 없는 속성은 시작 또는 종료 시점에 전환합니다.

예:

- Material
- CastShadow
- Enabled
- DepthMode
- MeshId
- TextureId

기본 전환 시점과 개별 재정의 방식은 구현 명세에서 확정합니다.

---

## 9. 복사하지 않는 속성

모션 견본은 시각 상태를 제어합니다.

다음 실행 구조와 물리 상태는 복사하지 않습니다.

- Name
- Parent
- Anchored
- CanCollide
- CanTouch
- CanQuery
- CollisionGroup
- Massless
- Archivable
- 서버 권한과 전투 판정 값

---

## 10. 이동·포즈·오버레이 레이어

타워 전체 이동과 개별 파츠 포즈가 같은 CFrame을 직접 덮어쓰지 않도록 세 레이어를 분리합니다.

```text
Root Movement
- 타워 전체의 월드 위치와 방향
- Engage 이동
- 편대 복귀
- 대상 추적과 바라보기

Pose
- 모션 견본에 따른 파츠의 기준 상태
- 위치, 회전, 크기, 색상, 투명도 등

Overlay
- 짧은 반동
- 흔들림
- 피격 반짝임
- 순간 확대와 축소
- 명중 순간 강조
```

개념적으로 최종 상태는 다음 세 레이어의 합성 결과입니다.

```text
최종 파츠 상태
= Root Movement × Pose × Overlay
```

`RunToTarget`과 `PlayPose`는 동시에 실행할 수 있어야 합니다.

---

## 11. 과장된 움직임 제작 원칙

### 준비 동작

강한 공격일수록 판정 전에 힘이 모이는 방향과 실루엣이 보여야 합니다.

- 무기를 크게 뒤로 당김
- 몸체를 압축하거나 낮춤
- 부유 파츠를 중심으로 모음
- 빛과 파티클을 발사점으로 집중

### 판정 동작

판정 순간에는 가장 큰 속도 변화와 실루엣 변화를 둡니다.

- 빠른 위치·회전 변화
- 순간적인 크기 변화
- 강한 Trail·Beam·Light 전환
- 발사 반대 방향의 반동

### 마무리 동작

공격 후 힘이 빠지는 반동과 복원을 짧게 제공합니다.

- 오버슈트 후 복귀
- 무기·총열의 짧은 흔들림
- 파츠가 원위치보다 약간 지나쳤다가 돌아옴

모든 공격을 현실적인 작은 관절 움직임만으로 표현하지 않습니다.

---

## 12. 공격 무게 등급 지원

모션 키트는 같은 기본 행동 안에서도 표현 무게를 구분할 수 있어야 합니다.

후보 등급:

- Light
- Medium
- Heavy
- Finisher

등급은 피해를 자동으로 결정하지 않습니다. 카메라·음향·Overlay·파티클의 기본 강도를 선택하는 표현 정보입니다.

정확한 데이터 위치와 명칭은 명세에서 정합니다.

---

## 13. 모션 반복

달리기, 반동과 총열 진동처럼 반복되는 모션은 자유 이름의 견본을 순환 재생합니다.

```lua
context:StartPoseLoop({"RunLeft", "RunRight"}, 0.1)
context:RunToTarget(target, options)
context:StopPoseLoop()
```

`Run`, `Idle`, `Attack` 같은 고정 이름을 강제하지 않습니다.

인간형이 아닌 타워도 동일한 기능을 사용합니다.

```lua
context:StartPoseLoop({"Stretch", "Contract"}, 0.08)
```

---

## 14. 기준점

공격, 효과와 발사 위치는 이름 기반 Attachment로 찾습니다.

```text
Basic
├─ Core
│  └─ EffectOrigin
└─ Weapon
   ├─ ProjectileOrigin
   └─ SlashOrigin
```

호출 예:

```lua
context:GetPoint("Weapon/ProjectileOrigin")
```

이름이 전체 모델에서 유일하면 간단한 이름 검색도 허용할 수 있지만, 중복 가능성이 있으면 상대 경로를 사용합니다.

---

## 15. 검증기

Attribute를 강제하는 대신 검증기가 경고를 제공합니다.

검증 항목:

- 같은 부모 아래 중복 이름
- 모션 견본과 Basic 사이의 클래스 불일치
- Basic에는 없고 견본에만 있는 요소
- 참조한 모션 이름이 키트에 없음
- 참조한 Attachment, 효과와 소리 이름이 없음
- Pivot 기준이 비정상적으로 다른 견본
- 강한 공격인데 준비·판정 견본의 실루엣 차이가 지나치게 작은 경우의 품질 경고 가능성

경고는 제작을 차단하지 않지만 Preview 전에 확인할 수 있어야 합니다.

---

## 16. 사용자 제작 흐름

```text
1. TemplateKit 복제
2. 키트 이름 변경
3. Basic 3D 모델 제작
4. Basic 복제로 자유 이름 모션 견본 제작
5. 준비·판정·반동이 읽히는 과장된 시각 상태 편집
6. 행동 모듈에서 이동과 행동 함수 조합
7. Preview 실행
8. 판정 시점과 명중 체감 확인
9. 검증 경고와 실제 움직임 확인
10. 모델, 모션 시간과 행동 순서 수정
```

---

## 17. 변경 원칙

이 문서는 현재 확정 기준이며 계속 수정합니다.

새 시각 속성이나 Instance 클래스 지원이 필요할 때는 개별 타워 코드에 임시 복사를 추가하지 않고 중앙 레지스트리와 이 문서를 갱신합니다.

타격감을 위해 추가한 장식이 서버 판정이나 행동 시간 규칙을 조용히 변경해서는 안 됩니다.
