# 타워 행동 문법·제작 양식 임시 초안

- 상태: **Working Draft**
- 확정 수준: **임시 합의**
- 구현 가능 상태: **아님**
- 최종 API 여부: **아님**
- 관련 문서: `docs/drafts/TOWER_MODELING.md`, `docs/design/COMBAT.md`, `docs/design/TARGETING.md`, `docs/design/FORMATION.md`
- 마지막 정리: 2026-08-02

> 이 문서는 타워마다 다른 이동과 공격 움직임을 만들기 위한 제작 양식을 임시로 기록합니다.
> 현재 적힌 분류명, 함수명, 매개변수와 반환값은 구현 전에 변경될 수 있습니다.
> 새 타워를 단일 상속 클래스 하나에 억지로 넣지 않고, 여러 행동 축을 조합하는 방향을 우선합니다.

---

## 1. 핵심 구조

타워의 전투 특성과 움직임은 하나의 클래스 이름으로 결정하지 않습니다.

```text
전투 역할
+ 이동 방식
+ 행동 루틴
+ 공격 전달 방식
+ 자유 이름의 3D 모션 견본
```

각 축의 책임은 다음과 같습니다.

| 축 | 질문 | 예시 |
|---|---|---|
| 전투 역할 | 전투에서 무엇을 잘하는가? | 단일 화력, 광역 화력, 제어, 마무리, 지원, 대형 사냥 |
| 이동 방식 | 어디에서 어떻게 움직이는가? | Formation, Engage, ChargeThrough |
| 행동 루틴 | 한 행동 주기에서 판정이 어떻게 발생하는가? | Impact, Sequence, Burst, Channel |
| 공격 전달 방식 | 공격이 대상에게 어떤 모습으로 전달되는가? | Contact, Projectile, Hitscan, Beam |
| 모션 견본 | 실제 3D 모델이 어떤 상태로 변하는가? | SwordUp, HeavySlash, BarrelKick |

예:

```text
검투사
- 전투 역할: 단일 화력
- 이동 방식: Engage
- 행동 루틴: Impact
- 전달 방식: Contact

미니거너
- 전투 역할: 단일 화력
- 이동 방식: Formation
- 행동 루틴: Channel
- 전달 방식: Hitscan
```

같은 전투 역할을 사용해도 이동과 공격 실행 구조는 완전히 달라질 수 있습니다.

---

## 2. 분류는 상속 트리가 아니라 조합 가능한 행동 문법이다

현재 문서에서 `Engage`, `Impact`, `Channel` 등을 편의상 하위클래스라고 부를 수 있지만, 실제 구현을 반드시 객체지향 상속 구조로 만들지는 않습니다.

우선 목표는 다음입니다.

- 사용자가 타워 ModuleScript에서 필요한 공통 함수를 조합할 수 있음
- 포즈 이름을 공통 시스템이 강제하지 않음
- 새 행동을 추가하기 위해 거대한 상속 트리를 수정하지 않음
- 같은 이동 방식에 여러 공격 루틴을 결합할 수 있음
- 같은 공격 루틴에 여러 전달 방식을 결합할 수 있음

예:

```text
Engage + Impact + Contact
Engage + Sequence + Contact
Engage + Channel + Contact
Formation + Impact + Projectile
Formation + Channel + Beam
```

---

## 3. 공통 타워 ModuleScript 양식

다음은 현재 논의를 위한 최소 제작 양식입니다.

```lua
local Tower = {}

-- 분류 표기는 제작자와 검증기가 타워 구조를 이해하기 위한 임시 메타데이터입니다.
-- 실제 필드 이름과 필수 여부는 아직 확정하지 않습니다.
Tower.Behavior = {
	Movement = "Engage",
	Action = "Impact",
	Delivery = "Contact",
}

function Tower.Attack(context)
	-- 이 안에서 이동, 모션, 판정, 효과와 복귀 순서를 자유롭게 작성합니다.
end

return Tower
```

`Tower.Behavior`는 자동 실행을 강제하는 설정표가 아니라, 현재 타워가 어떤 행동 문법을 사용하는지 명시하기 위한 후보입니다.

실제 행동은 `Attack` 함수 안의 호출 순서가 결정합니다.

---

## 4. 모든 양식에서 사용할 공통 함수 후보

정확한 함수명과 반환 계약은 아직 확정하지 않습니다.

```lua
context:PlayPose("모션이름", 시간)
context:PlayPoseAsync("모션이름", 시간)
context:Wait(시간)
context:FaceTarget(target, 시간)
context:PlaySound("소리이름")
context:EmitEffect("효과이름")
context:GetPoint("기준점이름")
context:IsTargetValid(target)
context:CancelPoint()
```

### 공통 원칙

- 일반 `task.wait()`보다 `context:Wait()`를 사용합니다.
- 모션 이름은 자유롭게 정합니다.
- `Attack`, `BeforeAttack`, `Recover` 같은 고정 포즈 이름은 없습니다.
- 피해 판정은 시각 연출 완료에 불필요하게 종속되지 않습니다.
- 스턴, 제거, 전투 종료와 일시정지는 Context가 공통으로 통제해야 합니다.

---

# 이동 방식

## 5. Formation — 편대 유지형

타워가 플레이어 주변의 편대 위치를 유지하며 공격합니다.

적합한 예:

- 궁수
- 소총병
- 미니거너
- 마법사
- 지원 토템

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:FaceTarget(target, 0.08)

	-- 행동 루틴 작성
end
```

### 제작 기준

- 공격을 위해 목표까지 이동하지 않습니다.
- 목표 방향으로 회전하는 것은 허용합니다.
- 편대 자체가 움직이면 플레이어를 따라갑니다.
- 타워의 공격 사거리 판정과 시각적 위치는 분리할 수 있습니다.

---

## 6. Engage — 추격 교전형

우선순위 적에게 달려가 가까운 위치에서 계속 교전합니다.

대부분의 일반 근접 타워가 사용하는 기본 이동 방식입니다.

```text
편대 대기
→ 우선순위 적 선택
→ 대상 추격
→ 교전 거리 도달
→ 공격 반복
→ 대상 사망 시 다음 적 추격
→ 적이 없을 때만 편대 복귀
```

적합한 예:

- 검투사
- 쌍검사
- 전기톱 전사
- 근접 야수
- 망치병

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:RunToPriorityTarget({
		Speed = 18,
		StopDistance = 2.5,
		Motion = {
			{"RunLeft", 0.1},
			{"RunRight", 0.1},
		},
	})

	if not target then
		context:ReturnToFormation({
			Speed = 16,
		})
		return
	end

	context:FaceTarget(target)

	-- 행동 루틴 작성
end
```

### 필요한 함수 후보

```lua
context:RunToPriorityTarget(options)
context:RunToTarget(target, options)
context:EnsureTargetDistance(target, distance, options)
context:ReturnToFormation(options)
```

### 반환 결과 후보

```text
Reached
TargetLost
Cancelled
```

간편 함수인 `RunToPriorityTarget`은 성공 시 대상 자체를 반환하고, 실패 시 `nil`을 반환하는 형태도 검토합니다.

### 제작 기준

- 호출 순간의 적 위치가 아니라 움직이는 적의 현재 위치를 계속 추적합니다.
- 공격 한 번마다 편대로 복귀하지 않습니다.
- 기존 대상이 살아 있고 가까우면 다시 달려가지 않고 바로 공격합니다.
- 대상이 멀어졌다면 `EnsureTargetDistance`로 다시 접근합니다.
- 적이 전부 사라졌을 때만 편대 위치로 돌아갑니다.
- 달리기 모션은 `Run`이라는 이름으로 고정하지 않습니다.

### 인간형이 아닌 이동 모션 예

```lua
Motion = {
	{"Stretch", 0.08},
	{"Contract", 0.08},
}
```

또는:

```lua
Motion = {
	{"TiltForward", 0.12},
}
```

---

## 7. ChargeThrough — 관통 돌진형

목표 근처에 머무르지 않고 목표를 향해 돌진하거나 통과하며 공격합니다.

적합한 예:

- 기병
- 돌진하는 창병
- 베어 가르며 지나가는 암살자
- 굴러가는 톱날

### 기본 양식 후보

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		context:ReturnToFormation({Speed = 18})
		return
	end

	context:PlayPose("ChargeReady", 0.15)

	local result = context:ChargeThroughTarget(target, {
		Speed = 30,
		PassDistance = 4,
		Motion = {
			{"Charge", 0.08},
		},
	})

	if result == "HitWindow" then
		context:DamageTarget(target)
	end

	context:ReturnToFormation({Speed = 22})
end
```

정확한 충돌 시점, 지나간 뒤 위치와 복귀 규칙은 추가 논의가 필요합니다.

---

## 8. Orbit — 대상 주회형

대상 주변을 일정 반경으로 돌거나 위치를 바꾸며 공격합니다.

적합한 예:

- 비행 드론
- 회전하는 검
- 고속 정령
- 대상을 포위하는 소환체

### 기본 양식 후보

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:OrbitTarget(target, {
		Radius = 5,
		AngularSpeed = 180,
		Duration = 1.2,
		Motion = {
			{"OrbitTilt", 0.1},
		},
	})
end
```

주회 도중 공격 루틴을 병렬로 실행하는 방식은 후속 설계에서 정합니다.

---

## 9. DeployPosition — 전투 위치 전개형

지정된 위치로 이동한 뒤 일정 시간 고정되어 행동합니다.

적합한 예:

- 자리를 잡고 포를 전개하는 병기
- 땅에 뿌리내리는 토템
- 전개형 방벽
- 고정 사격 자세를 취하는 저격수

### 기본 양식 후보

```lua
function Tower.Attack(context)
	local position = context:ChooseDeployPosition()
	if not position then
		return
	end

	context:MoveToPosition(position, {
		Speed = 12,
		Motion = {
			{"Move", 0.12},
		},
	})

	context:PlayPose("Deployed", 0.3)

	-- 전개 상태 행동 루틴 작성
end
```

위치 선택 기준과 전개 해제 조건은 아직 미확정입니다.

---

## 10. Independent — 독립 이동형

공통 편대나 타워 이동 규칙 대신 자체 이동 규칙을 사용합니다.

적합한 예:

- 소환체
- 분신
- 자율 드론
- 맵을 돌아다니는 공격 개체

공통 양식으로 강제하지 않습니다.

```lua
function Tower.Attack(context)
	-- 해당 개체만의 이동과 행동을 직접 작성합니다.
end
```

---

# 행동 루틴

## 11. Impact — 단발 판정형

한 행동 사이클에서 핵심 공격 판정이 한 번 발생합니다.

```text
준비
→ 한 번의 판정
→ 마무리
```

적합한 예:

- 검투사의 베기
- 궁수의 화살 한 발
- 망치병의 내려찍기
- 저격수의 단발
- 즉발 번개

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget()
	if not target then
		return
	end

	context:PlayPose("Ready", 0.2)
	context:Wait(0.05)

	context:PlayPose("Strike", 0.1)
	context:DeliverAttack(target)

	context:PlayPose("Finish", 0.12)
	context:PlayPose("Basic", 0.15)
end
```

`DeliverAttack`은 실제로는 Contact, Projectile, Hitscan 등 전달 방식에 따라 다른 함수를 호출할 수 있습니다.

### Engage + Impact 양식

```lua
function Tower.Attack(context)
	local target = context:RunToPriorityTarget({
		Speed = 18,
		StopDistance = 2.5,
		Motion = {
			{"RunA", 0.1},
			{"RunB", 0.1},
		},
	})

	if not target then
		context:ReturnToFormation({Speed = 16})
		return
	end

	context:FaceTarget(target)
	context:PlayPose("SwordRaise", 0.18)
	context:PlayPose("HeavySlash", 0.1)
	context:DamageTarget(target)
	context:PlayPose("SlashEnd", 0.12)
	context:PlayPose("Basic", 0.15)
end
```

---

## 12. Sequence — 수동 다단 공격형

하나의 행동 사이클 안에 서로 다른 모션과 간격을 가진 판정이 여러 번 발생합니다.

```text
첫 동작과 판정
→ 두 번째 동작과 판정
→ 마무리 동작과 판정
```

적합한 예:

- 삼연검
- 좌우 쌍검 공격
- 서로 다른 수정이 차례대로 발사되는 마법
- 첫 두 타격과 강한 마무리가 다른 공격

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget()
	if not target then
		return
	end

	context:PlayPose("SlashLeft", 0.1)
	context:DamageTarget(target)

	context:Wait(0.04)
	context:PlayPose("SlashRight", 0.1)
	context:DamageTarget(target)

	context:Wait(0.06)
	context:PlayPose("FinalStrike", 0.16)
	context:DamageTarget(target)

	context:PlayPose("Basic", 0.18)
end
```

각 타격이 동일하지 않으므로 반복문이나 `RunBurst`로 숨기지 않고 직접 순서를 작성하는 것이 기본입니다.

---

## 13. Burst — 고정 횟수 반복형

같은 공격 단위를 정해진 횟수만큼 빠르게 반복합니다.

```text
사격 준비
→ 동일한 발사 단위 × N
→ 사격 종료
```

적합한 예:

- 3점사 소총
- 연발 석궁
- 동일한 마법탄 다섯 발
- 짧은 기관포 사격

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:PlayPose("Aim", 0.15)

	context:RunBurst(3, 0.08, function(index)
		context:PlayPose("Kick", 0.04)
		context:FireProjectile("Bullet", target)
		context:PlayPose("Aim", 0.04)
	end)

	context:PlayPose("Basic", 0.15)
end
```

### `RunBurst`가 담당할 후보

- 고정 반복 횟수
- 발사 간격
- 공격속도 적용
- 취소 검사
- 대상 사망 시 유지 또는 재지정
- 반복 종료 보장

각 발이 서로 다른 공격이라면 `Sequence`를 사용합니다.

---

## 14. Channel — 지속 판정형

행동을 시작한 뒤 일정 시간 동안 반복 판정이 발생합니다.

```text
시동
→ 일정 시간 반복 판정
→ 종료
```

적합한 예:

- 미니거너
- 화염방사기
- 지속 광선
- 전기톱 전사
- 지속 치유 광선

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:PlayPose("BarrelWake", 0.3)

	context:RunChannel(1.5, 0.08, function(tickIndex)
		if not context:IsTargetValid(target) then
			target = context:GetPriorityTarget()
		end

		if not target then
			return "Stop"
		end

		context:FaceTarget(target)
		context:PlayPose("KickA", 0.04)
		context:DamageTarget(target)
		context:PlayPose("KickB", 0.04)
	end)

	context:PlayPose("BarrelSleep", 0.22)
	context:PlayPose("Basic", 0.15)
end
```

### `RunChannel`이 담당할 후보

- 전체 지속시간
- 틱 간격
- 공격속도 적용 방식
- 스턴과 제거에 의한 중단
- 타겟 사망 처리
- 반복 종료 처리
- 종료 모션이 실행될 수 있도록 정리 단계 보장

### Engage + Channel 예

전기톱 전사는 적 근처에서 지속 공격할 수 있습니다.

```lua
function Tower.Attack(context)
	local target = context:RunToPriorityTarget({
		Speed = 17,
		StopDistance = 2,
		Motion = {
			{"RushA", 0.08},
			{"RushB", 0.08},
		},
	})

	if not target then
		context:ReturnToFormation({Speed = 15})
		return
	end

	context:PlayPose("SawStart", 0.2)

	context:RunChannel(1.0, 0.1, function()
		context:EnsureTargetDistance(target, 2, {Speed = 17})
		context:PlayPose("SawContact", 0.05)
		context:DamageTarget(target)
	end)

	context:PlayPose("SawStop", 0.18)
	context:PlayPose("Basic", 0.15)
end
```

---

## 15. ChargeRelease — 충전 방출형

공격 결과보다 충전 과정이 행동 구조의 핵심입니다.

```text
충전 시작
→ 충전 유지 또는 강화
→ 방출 판정
→ 냉각 또는 복귀
```

적합한 예:

- 레일건
- 거대 활
- 대포
- 힘을 모아 내려찍는 거인
- 거대 마법 구체

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:PlayPose("ChargeStart", 0.2)
	context:PlayPose("FullCharge", 0.8)
	context:Wait(0.05)

	context:PlayPose("Release", 0.08)
	context:FireHitscan("RailShot", target)

	context:PlayPose("Cooldown", 0.3)
	context:PlayPose("Basic", 0.2)
end
```

### 후속 결정이 필요한 항목

- 충전 도중 대상 사망 시 재지정 여부
- 충전 중단 시 공격을 잃는지
- 공격속도가 충전과 냉각에 적용되는 방식
- 부분 충전 발사 허용 여부

---

## 16. Pulse — 주기적 방출형

타워 자신이나 특정 위치를 중심으로 한 번의 파동 효과를 발생시킵니다.

적합한 예:

- 치유 토템
- 감속 수정
- 충격파 발생기
- 주기적 편대 강화
- 독기 방출체

### 기본 양식

```lua
function Tower.Attack(context)
	context:PlayPose("Expand", 0.2)
	context:EmitEffect("PulseRing")
	context:ApplySelfAreaEffect()
	context:PlayPose("Contract", 0.18)
	context:PlayPose("Basic", 0.15)
end
```

Pulse는 공격 주기마다 한 번 방출되는 형태와, `RunChannel` 내부에서 여러 번 맥동하는 형태를 모두 가질 수 있습니다.

---

## 17. Deploy — 설치물 생성형

타워 행동의 결과로 일정 시간 남아 있는 별도 오브젝트나 영역을 생성합니다.

적합한 예:

- 지뢰
- 화염 장판
- 자동 포탑
- 마법진
- 부착 폭탄
- 지속 회오리

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:PlayPose("PrepareDevice", 0.2)
	context:PlayPose("ThrowDevice", 0.1)

	context:SpawnDeployable("Mine", {
		Position = context:GetTargetPosition(target),
		Lifetime = 8,
	})

	context:PlayPose("Basic", 0.2)
end
```

### 공통 시스템이 담당할 후보

- 설치 가능한 최대 개수
- 수명
- 기존 설치물 교체 여부
- 설치물 자체 행동 주기
- 원본 타워 제거 시 처리

---

## 18. Summon — 소환체 생성형

독립적으로 움직이거나 공격하는 임시 개체를 생성합니다.

적합한 예:

- 해골 소환사
- 늑대 조련사
- 드론 운영자
- 작은 정령
- 분신 검사

### 기본 양식

```lua
function Tower.Attack(context)
	context:PlayPose("SummonGather", 0.3)
	context:PlayPose("SummonOpen", 0.15)

	context:SummonUnit("Wolf", {
		SpawnPoint = context:GetPoint("SummonOrigin"),
		Lifetime = 10,
	})

	context:PlayPose("Basic", 0.2)
end
```

소환체의 이동과 공격은 `Independent` 이동 방식과 별도 행동 모듈을 사용할 수 있습니다.

---

## 19. ModeShift — 상태전환형

일정 시간 동안 외형과 행동 루틴 자체가 다른 상태로 전환됩니다.

적합한 예:

- 인간에서 야수로 변신
- 검이 포신으로 재구성되는 기계
- 방어형에서 공격형으로 전개
- 일정 횟수 후 각성

다른 행동 루틴을 내부에 포함하는 복합 구조이므로 현재 초기 채용 대상에서는 제외합니다.

```text
Working Draft 후보
기본 상태
→ 전환 모션
→ 다른 이동·행동 루틴 사용
→ 해제 모션
→ 기본 상태 복귀
```

---

# 공격 전달 방식

## 20. 전달 방식 목록

| 이름 | 용도 | 대표 함수 후보 |
|---|---|---|
| Contact | 목표 근처의 직접 타격 | `DamageTarget(target)` |
| Projectile | 날아가는 투사체 | `FireProjectile(name, target)` |
| Hitscan | 즉시 명중 선형 공격 | `FireHitscan(name, target)` |
| Beam | 일정 시간 연결되는 광선 | `StartBeam(name, target)` |
| TargetArea | 목표 또는 목표 지점 범위 | `DamageTargetArea(target, radius)` |
| SelfArea | 타워 중심 범위 | `ApplySelfAreaEffect(radius)` |
| SpawnedObject | 설치물이나 공격 오브젝트 | `SpawnDeployable(name, options)` |
| SummonedUnit | 자율 행동 소환체 | `SummonUnit(name, options)` |

전달 방식은 행동 루틴과 독립적으로 조합합니다.

예:

```text
Impact + Contact
Impact + Projectile
Impact + Hitscan
Burst + Projectile
Channel + Beam
Channel + TargetArea
Deploy + SpawnedObject
Summon + SummonedUnit
```

---

# 새 타워 제작 절차

## 21. 제작 순서

### 1단계: 전투 역할 선택

```text
이 타워는 전투에서 무엇을 잘하는가?
```

예: 단일 화력

### 2단계: 이동 방식 선택

```text
어디에서 공격하는가?
```

예: Engage

### 3단계: 행동 루틴 선택

```text
한 행동 주기에서 판정이 몇 번, 어떤 간격으로 발생하는가?
```

예: Sequence

### 4단계: 전달 방식 선택

```text
타격이 목표에게 어떤 모습으로 전달되는가?
```

예: Contact

### 5단계: Basic 모델 제작

`docs/drafts/TOWER_MODELING.md`의 이름·상대 경로 규칙을 따릅니다.

### 6단계: 필요한 자유 이름 모션 제작

예:

```text
Basic
RunA
RunB
SlashLeft
SlashRight
FinalStrike
```

### 7단계: 가장 가까운 ModuleScript 양식 복제

```text
Engage + Sequence + Contact
```

조합에 맞는 예시를 복제한 뒤 포즈 이름, 시간과 효과를 수정합니다.

### 8단계: 프리뷰 검증

확인할 항목:

- 대상이 움직여도 올바르게 추적하는가
- 공격 후 불필요하게 복귀하지 않는가
- 피해 시점과 모션이 자연스럽게 맞는가
- 대상이 죽었을 때 다음 대상 처리가 올바른가
- 적이 없을 때 편대로 복귀하는가
- 색상, 투명도, 재질, 파티클 등의 모션 상태가 적용되는가
- 스턴과 타워 제거 시 행동이 안전하게 중단되는가

---

## 22. 조합 예시 표

| 타워 | 역할 | 이동 | 행동 | 전달 |
|---|---|---|---|---|
| 검투사 | 단일 화력 | Engage | Impact | Contact |
| 쌍검사 | 단일·마무리 | Engage | Sequence | Contact |
| 전기톱 전사 | 단일 화력 | Engage | Channel | Contact |
| 궁수 | 단일 화력 | Formation | Impact | Projectile |
| 돌격소총병 | 단일 화력 | Formation | Burst | Projectile |
| 미니거너 | 단일 화력 | Formation | Channel | Hitscan |
| 레일건 | 대형 사냥 | Formation | ChargeRelease | Hitscan |
| 화염방사기 | 광역·제어 | Formation | Channel | TargetArea |
| 치유 토템 | 지원 | Formation | Pulse | SelfArea |
| 지뢰공병 | 광역 화력 | Formation | Deploy | SpawnedObject |
| 강령술사 | 단일·광역 | Formation | Summon | SummonedUnit |
| 기병 | 단일·광역 | ChargeThrough | Impact | Contact |

---

## 23. 현재 임시 채용 범위

### 우선 채용할 이동 방식

```text
Formation
Engage
ChargeThrough
Orbit
DeployPosition
Independent
```

### 우선 채용할 행동 루틴

```text
Impact
Sequence
Burst
Channel
ChargeRelease
Pulse
Deploy
Summon
```

### 후순위

```text
ModeShift
```

### 전달 방식

```text
Contact
Projectile
Hitscan
Beam
TargetArea
SelfArea
SpawnedObject
SummonedUnit
```

---

## 24. 아직 결정하지 않은 사항

- 실제 상속 구조를 사용할지, 함수 조합 방식만 사용할지
- `Tower.Behavior` 메타데이터의 최종 형식과 필수 여부
- 공개 함수의 정확한 이름과 반환값
- 이동 속도와 교전 거리의 데이터 위치
- 이동 중 회전과 높이 보정 방식
- 몬스터와 타워 모델이 겹칠 때의 시각 처리
- 여러 근접 타워가 같은 적을 둘러싸는 배치 방식
- 대상 사망 시 Burst와 Channel의 재지정 규칙
- 공격속도가 준비, 이동, 반복 간격, 지속시간과 복귀에 적용되는 방식
- 서버 판정과 클라이언트 연출의 정확한 분리
- 다른 플레이어에게 보이는 비전투 모션과 자신의 전투 모션 구분
- 설치물과 소환체의 최대 수, 수명과 정리 규칙
- ModeShift의 상태 소유권과 중첩 규칙

이 항목들을 결정하기 전에는 문서를 시스템 명세나 구현 명세로 승격하지 않습니다.
