# 타워 모델링·모션 규약 임시 초안

- 상태: **Working Draft**
- 확정 수준: **임시 합의**
- 구현 가능 상태: **아님**
- 최종 규약 여부: **아님**
- 마지막 정리: 2026-08-02

> 이 문서는 현재까지 합의한 모델링 및 모션 제작 방향을 잊지 않기 위한 임시 기록입니다.
> 타워의 전투 방식과 애니메이션 하위클래스 분류를 더 논의한 뒤 반드시 수정합니다.

---

## 1. 문서 범위

이 문서는 다음만 임시로 정리합니다.

- 사용자가 Roblox Studio에서 직접 타워 3D 모델을 제작하는 방식
- 하나의 기본 모델과 여러 모션 견본 모델을 구성하는 방식
- 모션 견본을 이름으로 호출하는 방식
- 실제 모델과 모션 견본의 구성요소를 이름과 상대 경로로 대응하는 방식
- 위치뿐 아니라 전체 시각 상태를 모션에 반영하는 방향

다음 항목은 아직 확정하지 않습니다.

- 타워 애니메이션 하위클래스의 종류와 명칭
- 각 하위클래스가 제공할 기본 모션과 함수
- 공격 주기, 타격 시점, 발사체와 연속 사격의 정확한 계약
- 서버와 클라이언트의 애니메이션 책임
- 성능 최적화와 네트워크 복제 방식
- 실제 ModuleScript와 폴더의 최종 경로

---

## 2. 전제

타워는 **3D Model**로 제작합니다.

BillboardGui 기반 타워를 기본 모델링 방식으로 사용하지 않습니다.

하지만 타워를 인간형 캐릭터처럼 만들 필요는 없습니다. 다음은 모두 허용합니다.

- 인간형 검사
- 총기형 기계
- 부유하는 수정과 무기
- 하나의 거대한 MeshPart
- 여러 파츠가 분리된 추상 오브젝트
- 석판, 토템, 눈, 고리와 같은 비인간형 형태

관절, 팔, 다리, Motor6D와 일반 캐릭터 리그는 필수가 아닙니다.

---

## 3. 키트의 기본 구조

키트 하나는 기본 3D 모델, 자유롭게 이름 붙인 모션 견본 모델들, 행동 모듈을 포함합니다.

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

현재 예약된 모델 이름은 `Basic` 하나뿐입니다.

- `Basic`: 실제 게임에서 복제되어 움직이는 기본 3D 모델
- 그 외 같은 키트의 3D Model: 이름으로 호출할 수 있는 모션 상태 견본

`BeforeAttack`, `Attack`, `Recover` 같은 이름은 고정 분류가 아닙니다. 단순한 예시에 불과합니다.

모션 이름은 자유롭게 정할 수 있습니다.

```text
SwordUp
HeavySlash
Charge
발도준비
발도
Pose17
```

---

## 4. 모션 호출

행동 모듈은 모션 모델의 이름을 문자열로 호출합니다.

```lua
context:PlayPose("SwordUp", 0.3)
context:Wait(0.1)
context:PlayPose("HeavySlash", 0.12)
```

새 모션을 추가하는 기본 절차는 다음과 같습니다.

```text
1. Basic을 복제한다.
2. 복제 모델에 원하는 모션 이름을 붙인다.
3. Studio에서 해당 순간의 3D 상태를 직접 만든다.
4. 행동 모듈에서 PlayPose("모션 이름", 시간)을 호출한다.
```

모션의 의미를 공통 시스템이 판단하지 않습니다.

`SwordUp`이 공격 준비인지, 승리 자세인지, 스킬 중간 동작인지는 행동 모듈이 결정합니다.

---

## 5. 모션 재생 방식

모션 모델 자체를 게임 중 교체하지 않습니다.

실제 런타임 모델은 `Basic`을 복제한 모델 하나이며, `PlayPose`는 모션 견본의 상태를 읽어 런타임 모델에 적용합니다.

```text
Basic 복제본
    ↓
PlayPose("HeavySlash", 0.12)
    ↓
HeavySlash 견본과 같은 시각 상태로 변화
```

모션 모델들은 Studio에서 비교하기 편하도록 서로 떨어뜨려 배치할 수 있습니다.

월드 절대 좌표를 그대로 복사하지 않고, 각 모션 Model의 Pivot을 기준으로 한 상대 상태를 사용합니다.

---

## 6. 구성요소 대응 방식

Attribute, PartId, CollectionService 태그와 별도의 등록표는 사용하지 않습니다.

구성요소는 **이름과 모델 내부 상대 경로**로 대응합니다.

```text
Basic/Weapon/Blade
HeavySlash/Weapon/Blade
```

두 인스턴스는 각각 자신의 모델 루트를 기준으로 다음 상대 경로를 가집니다.

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

---

## 7. 전체 모션과 부분 모션

### 전체 모션

`Basic` 전체를 복제하여 모든 요소의 상태를 작성할 수 있습니다.

```text
HeavySlash
├─ Core
├─ Weapon
├─ Cape
└─ Floating
```

### 부분 모션

움직이거나 바뀌는 요소만 남긴 모션도 허용합니다.

```text
SwordShake
└─ Weapon
```

이 경우 `Weapon` 경로에 대응하는 요소만 변화하고, 나머지는 현재 상태를 유지합니다.

`Basic`에는 있지만 모션 견본에 없는 요소는 오류로 처리하지 않습니다.

모션 견본에만 있고 `Basic`에는 대응 경로가 없는 요소는 기본 포즈 변형 대상에서 제외합니다. 순간적으로 새로 생성되는 검기, 폭발과 투사체는 별도의 효과 또는 발사체 시스템에서 다룹니다.

---

## 8. 모션은 전체 시각 상태 견본이다

모션 견본은 위치와 회전만 저장하는 포즈가 아닙니다.

각 모션 Model은 해당 순간의 **전체 3D 시각 상태**를 표현합니다.

예를 들어 `Charge` 견본에서 사용자가 다음을 바꿀 수 있습니다.

- 코어 위치와 회전
- 코어 크기
- 색상
- 투명도
- 반사도
- 재질
- 조명 색상과 밝기
- 파티클 활성 여부와 방출량
- Trail과 Beam 상태
- Highlight 상태

호출은 여전히 단순해야 합니다.

```lua
context:PlayPose("Charge", 0.4)
```

사용자는 코드에 색상이나 파티클 수치를 반복해서 작성하지 않고 Studio의 `Charge` 견본을 직접 수정합니다.

---

## 9. 이름과 경로로 추적할 시각 요소

초기 후보는 다음과 같습니다.

### BasePart 계열

- Part
- MeshPart
- UnionOperation

주요 시각 속성 후보:

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

Attachment는 공격, 발사체와 효과의 기준점으로도 사용할 수 있습니다.

```text
Basic/Weapon/ProjectileOrigin
Basic/Weapon/SlashOrigin
```

### Light

- PointLight
- SpotLight
- SurfaceLight

주요 시각 속성 후보:

- Brightness
- Color
- Range
- Angle
- Shadows
- Enabled

### ParticleEmitter

주요 시각 속성 후보:

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

주요 시각 속성 후보:

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

주요 시각 속성 후보:

- Enabled
- FillColor
- FillTransparency
- OutlineColor
- OutlineTransparency
- DepthMode

이 목록은 최종 구현 계약이 아닙니다. 실제 지원 범위는 후속 기술 설계에서 확정합니다.

---

## 10. 속성 적용 방식

속성은 성격에 따라 두 종류로 나눕니다.

### 연속적으로 보간할 수 있는 속성

예:

- CFrame
- Size
- Color
- Transparency
- Reflectance
- Brightness
- Range
- 일부 수치형 속성

이 값들은 `PlayPose`에 전달한 시간 동안 부드럽게 변화합니다.

### 즉시 전환해야 하는 속성

예:

- Material
- CastShadow
- Enabled
- DepthMode
- MeshId
- TextureId

이 값들은 중간값이 없으므로 모션 시작 또는 종료 시점에 전환합니다.

기본 전환 시점과 선택 옵션은 아직 확정하지 않습니다.

---

## 11. 복사하지 않을 속성

모션은 시각 상태를 제어하며, 실행 구조와 물리 상태를 무작정 복사하지 않습니다.

기본적으로 다음은 모션 견본에서 가져오지 않습니다.

- Name
- Parent
- Anchored
- CanCollide
- CanTouch
- CanQuery
- CollisionGroup
- Massless
- Archivable
- 서버 권한과 게임 판정에 관련된 값

지원 속성은 중앙의 시각 속성 레지스트리에서 관리하는 방향으로 검토합니다.

사용자는 이 레지스트리를 직접 수정하지 않고 Studio에서 모션 견본만 편집할 수 있어야 합니다.

---

## 12. 행동 모듈의 목표 형태

사용자가 직접 수정하는 행동 모듈은 복잡한 애니메이터 내부 구현을 노출하지 않습니다.

```lua
local Swordsman = {}

function Swordsman.Attack(context)
	context:PlayPose("SwordUp", 0.3)
	context:Wait(0.1)

	context:PlayPose("HeavySlash", 0.12)
	context:PlaySound("Swing")
	context:DamageTarget()

	context:PlayPose("Basic", 0.2)
end

return Swordsman
```

`context:Wait()`를 사용하는 이유는 공격 속도, 일시정지, 스턴, 취소와 타워 제거를 공통 시스템에서 통제하기 위해서입니다.

함수의 정확한 이름과 계약은 아직 확정하지 않습니다.

---

## 13. 전투 역할과 애니메이션 하위클래스는 별개다

`단일 공격`, `광역 공격`, `제어`, `마무리`, `지원`, `보스 사냥`은 타워의 전투 역할입니다.

하지만 같은 전투 역할 안에서도 움직임의 구조는 크게 다를 수 있습니다.

예:

```text
단일 공격
├─ 검투사: 접근 또는 전진, 준비, 한 번의 강한 베기, 복귀
└─ 미니거너: 총열 준비, 지속 사격, 반동 반복, 사격 종료
```

둘은 같은 대상을 집중 공격할 수 있지만 다음이 다릅니다.

- 공격을 준비하는 방식
- 피해가 발생하는 횟수와 시점
- 모션이 반복되는 방식
- 발사체 사용 여부
- 공격 도중 방향을 유지하거나 변경하는 방식
- 반동, 충전, 채널링과 복귀 방식
- 필요한 효과, 소리와 기준점

따라서 전투 역할만으로 애니메이션 실행 구조를 결정하지 않습니다.

향후 별도의 **애니메이션 하위클래스 또는 행동 문법 분류**가 필요합니다.

현재는 분류를 확정하지 않습니다. 검토할 질문은 다음과 같습니다.

- 검투사와 같은 단발 근접형을 별도 하위클래스로 둘 것인가?
- 미니거너와 같은 지속 사격형을 채널링 공격으로 분류할 것인가?
- 궁수, 총잡이와 마법 발사체 타워가 같은 발사 문법을 공유할 수 있는가?
- 다단 공격과 지속 공격을 같은 반복 실행기로 처리할 것인가?
- 공격 도중 타깃이 사라지거나 바뀔 때 각 하위클래스는 어떻게 반응하는가?
- 하위클래스가 기본 행동 모듈을 제공하고 개별 타워가 이를 수정하는 구조가 적합한가?

이 분류가 정해지기 전에는 모델링 규약과 `PlayPose` 계약을 최종 확정하지 않습니다.

---

## 14. 현재 임시 합의

```text
1. 타워는 3D Model로 제작한다.
2. Basic만 예약된 기본 모델 이름이다.
3. 같은 키트의 다른 3D Model은 자유 이름의 모션 견본이다.
4. PlayPose("모션 이름", 시간)으로 견본을 호출한다.
5. 실제 런타임 모델은 Basic의 복제본 하나다.
6. 모션 모델 자체를 교체하지 않고 런타임 모델의 상태를 변화시킨다.
7. 대응은 Attribute 없이 이름과 상대 경로로 처리한다.
8. 전체 모션과 부분 모션을 모두 허용한다.
9. 모션은 위치뿐 아니라 전체 시각 상태를 표현한다.
10. 물리, 계층과 게임 판정 속성은 모션에서 복사하지 않는다.
11. 인간형, 관절, 리그와 Motor6D를 필수로 요구하지 않는다.
12. 전투 역할과 애니메이션 하위클래스는 별도로 분류한다.
13. 애니메이션 하위클래스가 정해진 뒤 이 규약을 반드시 수정한다.
```

---

## 15. 다음 논의

다음 단계에서는 모델링 규약을 더 확정하지 않고 먼저 아래를 논의합니다.

1. 타워의 공격 행동을 어떤 애니메이션 문법으로 분류할 것인가?
2. 검투사, 궁수, 미니거너, 마법사와 소환형 타워의 행동 차이는 무엇인가?
3. 각 하위클래스가 공통으로 제공해야 하는 함수는 무엇인가?
4. 피해 시점, 발사체 생성, 지속 공격과 취소를 모션과 어떻게 연결할 것인가?
5. 개별 타워가 하위클래스 기본 동작을 어느 수준까지 덮어쓸 수 있어야 하는가?

이 질문에 답한 후 이 문서를 `design`, `spec`, `technical`, `implementation` 계층으로 분리하거나 승격합니다.
