# 타워 행동 문법·제작 양식

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 구현 상태: 미구현
- 관련 문서: `../design/TOWER_BEHAVIOR.md`, `TOWER_MODELING.md`, `../design/COMBAT.md`, `../design/TARGETING.md`, `../design/FORMATION.md`
- 마지막 정리: 2026-08-02

> 이 문서는 새 타워를 만들 때 이동, 타겟, 행동 루틴, 전달 방식과 모션을 조합하는 현재 기준입니다.
> 현재 적힌 함수명은 최초 구현 기준으로 사용하되, 변경 시 이 문서를 먼저 갱신합니다.

---

## 1. 핵심 구조

타워 행동은 거대한 상속 트리보다 조합 가능한 행동 문법으로 구성합니다.

```text
전투 역할
+ TargetPolicy
+ TargetLossPolicy
+ Movement
+ FacingPolicy
+ ActionRoutine
+ Delivery
+ DeliveryModifiers
+ SpawnPolicy
+ ResourceProfile
+ 자유 이름 3D 모션
```

메타데이터는 제작자, 검증기와 런타임이 타워 구조를 이해하도록 돕습니다.

실제 행동 순서는 ModuleScript 함수 안의 호출 순서가 결정합니다.

---

## 2. 공통 ModuleScript 양식

```lua
local Tower = {}

Tower.Behavior = {
	Role = "SingleDamage",
	TargetPolicy = "LockUntilInvalid",
	TargetLossPolicy = "Retarget",
	Movement = "Engage",
	FacingPolicy = "FaceTargetOnce",
	ActionRoutine = "Impact",
	Delivery = "Contact",
	DeliveryModifiers = {},
	ResourceProfile = nil,
}

function Tower.Attack(context)
	-- 이동, 포즈, 판정, 효과와 종료 순서를 작성합니다.
end

return Tower
```

모든 필드를 반드시 직접 작성해야 하는지는 구현 명세에서 정합니다. 현재 기준은 각 타워의 의도를 명시적으로 확인할 수 있게 만드는 것입니다.

---

## 3. 공통 Context 함수

현재 제작 기준 함수:

```lua
context:PlayPose("모션이름", 시간, options?)
context:PlayPoseAsync("모션이름", 시간, options?)
context:StartPoseLoop({"모션A", "모션B"}, 각모션시간, options?)
context:StopPoseLoop()

context:Wait(시간)
context:CancelPoint()
context:IsCancelled()

context:GetPriorityTarget()
context:IsTargetValid(target)
context:GetTargetPosition(target)

context:FaceTarget(target, 시간?)
context:TrackTarget(target)
context:StopTrackingTarget()
context:FaceMovement()

context:PlaySound("소리이름")
context:EmitEffect("효과이름", options?)
context:GetPoint("상대경로또는이름")

context:DamageTarget(target, options?)
context:DamageArea(position, radius, options?)
context:FireProjectile("투사체이름", target, options?)
context:FireHitscan(target, options?)
context:StartBeam(target, options?)
context:StopBeam()
```

### 공통 원칙

- 일반 `task.wait()` 대신 `context:Wait()`를 사용합니다.
- 모든 장시간 동작은 취소, 일시정지, 타워 제거와 전투 종료를 처리할 수 있어야 합니다.
- 포즈 이름은 자유롭게 정합니다.
- 피해 판정 시점은 각 타워 모듈이 명시합니다.
- 모션 완료 자체가 자동으로 피해를 발생시키지 않습니다.

---

# TargetPolicy

## 4. LockUntilInvalid

현재 대상이 죽거나 무효가 될 때까지 유지합니다.

```lua
local target = context:GetOrKeepTarget("LockUntilInvalid")
```

적합한 예:

- 검투사
- 미니거너
- 지속 광선
- 보스 사냥 타워

---

## 5. RetargetEachAction

새 행동 사이클이 시작될 때마다 우선순위 대상을 다시 선택합니다.

```lua
local target = context:GetPriorityTarget()
```

적합한 예:

- 느린 단발 저격수
- 공격마다 선두 적을 다시 고르는 대포

---

## 6. RetargetEachHit

다단 공격의 각 판정 전에 대상을 다시 선택합니다.

```lua
for _ = 1, 3 do
	local target = context:GetPriorityTarget()
	if not target then
		break
	end
	context:DamageTarget(target)
end
```

적합한 예:

- 연쇄 검격
- 여러 수정이 각자 대상을 찾는 공격

---

## 7. SnapshotPosition

공격 시작 시점의 대상 위치를 저장하고 이후에는 해당 위치를 사용합니다.

```lua
local target = context:GetPriorityTarget()
if not target then
	return
end

local position = context:GetTargetPosition(target)
context:PlayPose("Charge", 0.4)
context:DamageArea(position, 8)
```

---

## 8. NoTarget

특정 적 없이 타워 또는 지정 위치를 중심으로 행동합니다.

적합한 예:

- 오라
- 자기 중심 충격파
- 주기적 지원 효과

---

# TargetLossPolicy

## 9. 대상 상실 처리 양식

```lua
local target = context:GetPriorityTarget()
if not target then
	return
end

context:PlayPose("Ready", 0.2)

if not context:IsTargetValid(target) then
	target = context:ResolveTargetLoss("Retarget", target)
	if not target then
		return
	end
end
```

지원 값:

```text
Cancel
Retarget
FinishAtPosition
FinishWithoutTarget
```

---

# Movement

## 10. Formation

편대 위치를 유지하며 공격합니다.

```lua
function Tower.Attack(context)
	local target = context:GetPriorityTarget()
	if not target then
		return
	end

	context:FaceTarget(target, 0.08)
	-- 행동 루틴
end
```

---

## 11. Engage

우선순위 적에게 실제로 달려가 교전합니다.

이동 시간은 실제 공격 시작 시점과 타겟 변경 후 다음 공격 시점에 영향을 줍니다.

### 기본 양식

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget("LockUntilInvalid")
	if not target then
		context:ReturnToFormation({
			Speed = 16,
		})
		return
	end

	local slot = context:ReserveEngageSlot(target, {
		Distance = 2.5,
	})

	context:StartPoseLoop({"RunLeft", "RunRight"}, 0.1)

	local result = context:RunToTarget(target, {
		Speed = 18,
		StopDistance = 2.5,
		Destination = slot and slot.Position or nil,
		FacingPolicy = "FaceMovement",
	})

	context:StopPoseLoop()

	if result ~= "Reached" then
		context:ReleaseEngageSlot()
		return
	end

	context:FaceTarget(target, 0.08)
	-- 행동 루틴
end
```

### Engage 함수

```lua
context:RunToPriorityTarget(options)
context:RunToTarget(target, options)
context:EnsureTargetDistance(target, distance, options)
context:ReserveEngageSlot(target, options)
context:ReleaseEngageSlot()
context:ReturnToFormation(options)
```

### Engage 원칙

- 호출 순간 위치가 아니라 이동 중인 적의 현재 위치를 추적합니다.
- 이동 시간 동안 공격은 시작되지 않습니다.
- 공격마다 편대로 돌아가지 않습니다.
- 대상이 살아 있고 교전 거리 안에 있으면 바로 다음 행동을 수행합니다.
- 대상이 멀어지면 다시 접근합니다.
- 새 타겟을 얻으면 새 교전 위치로 이동합니다.
- 적이 없을 때만 편대로 복귀합니다.

---

## 12. ChargeThrough

대상을 통과하거나 지나치며 공격합니다.

```lua
local target = context:GetPriorityTarget()
if not target then
	return
end

context:PlayPose("ChargeReady", 0.15)

local hit = context:ChargeThroughTarget(target, {
	Speed = 30,
	PassDistance = 4,
	Motion = "Charge",
})

if hit then
	context:DamageTarget(target)
end
```

---

## 13. Orbit

대상 주변을 주회하며 행동합니다.

```lua
context:OrbitTarget(target, {
	Radius = 5,
	AngularSpeed = 180,
	Duration = 1.2,
	FacingPolicy = "TrackTarget",
})
```

---

## 14. DeployPosition

전개 위치로 이동한 뒤 고정 상태로 행동합니다.

```lua
local position = context:ChooseDeployPosition()
if not position then
	return
end

context:MoveToPosition(position, {
	Speed = 12,
	Motion = {"MoveA", "MoveB"},
})

context:PlayPose("Deployed", 0.3)
```

---

## 15. Independent

편대 이동 규칙을 사용하지 않고 개별 이동 컨트롤러를 사용합니다.

소환체와 자율 드론에 적합합니다.

---

## 16. Blink

```lua
context:BlinkToTarget(target, {
	OffsetDistance = 2,
	DisappearPose = "FadeOut",
	AppearPose = "FadeIn",
})
```

---

## 17. Tether

```lua
context:TetherToTarget(target, {
	Offset = Vector3.new(0, 4, -2),
	FollowSpeed = 20,
	FacingPolicy = "TrackTarget",
})
```

---

# FacingPolicy

## 18. 방향 처리

지원 값:

```text
FaceTargetOnce
TrackTarget
FaceMovement
Fixed
None
```

사용 예:

```lua
context:FaceMovement()
context:FaceTarget(target, 0.08)
context:TrackTarget(target)
-- 공격 종료
context:StopTrackingTarget()
```

---

# ActionRoutine

## 19. Impact

한 번의 핵심 판정을 발생시킵니다.

```lua
function Tower.PerformImpact(context, target)
	context:PlayPose("Ready", 0.2)
	context:Wait(0.05)
	context:PlayPose("Strike", 0.1)
	context:DamageTarget(target)
	context:PlayPose("Basic", 0.18)
end
```

---

## 20. Sequence

서로 다른 타격을 순서대로 실행합니다.

```lua
function Tower.PerformSequence(context, target)
	context:PlayPose("SlashLeft", 0.1)
	context:DamageTarget(target)

	context:PlayPose("SlashRight", 0.1)
	context:DamageTarget(target)

	context:PlayPose("FinalStrike", 0.16)
	context:DamageTarget(target)

	context:PlayPose("Basic", 0.2)
end
```

각 타격 전 TargetPolicy에 따라 대상을 다시 선택할 수 있습니다.

---

## 21. Burst

같은 공격 단위를 정해진 횟수만큼 반복합니다.

```lua
function Tower.PerformBurst(context, target)
	context:PlayPose("Aim", 0.15)

	context:RunBurst(3, 0.08, function(index)
		context:PlayPose("Kick", 0.03)
		context:FireProjectile("Bullet", target)
		context:PlaySound("Shot")
	end)

	context:PlayPose("Basic", 0.15)
end
```

---

## 22. Channel

일정 시간 동안 반복 판정을 수행합니다.

```lua
function Tower.PerformChannel(context, target)
	context:PlayPose("SpinUp", 0.3)
	context:TrackTarget(target)

	context:RunChannel(1.5, 0.08, function()
		if not context:IsTargetValid(target) then
			target = context:ResolveTargetLoss("Retarget", target)
			if not target then
				return false
			end
		end

		context:PlayPoseAsync("BarrelKick", 0.04)
		context:FireHitscan(target)
		return true
	end)

	context:StopTrackingTarget()
	context:PlayPose("SpinDown", 0.25)
	context:PlayPose("Basic", 0.15)
end
```

---

## 23. ChargeRelease

```lua
function Tower.PerformChargeRelease(context, target)
	context:PlayPose("ChargeStart", 0.2)
	context:PlayPose("FullCharge", 0.6)
	context:CancelPoint()
	context:PlayPose("Release", 0.08)
	context:FireHitscan(target)
	context:PlayPose("Basic", 0.3)
end
```

---

## 24. Pulse

```lua
function Tower.PerformPulse(context)
	context:PlayPose("Expand", 0.2)
	context:DamageArea(context:GetTowerPosition(), 8)
	context:PlayPose("Basic", 0.25)
end
```

지원 효과라면 `DamageArea` 대신 해당 효과 함수를 호출합니다.

---

## 25. Deploy

```lua
function Tower.PerformDeploy(context, target)
	local position = context:GetTargetPosition(target)
	context:PlayPose("Throw", 0.15)
	context:SpawnObject("Mine", position, {
		Behavior = "WorldPersistent",
		OwnerLossPolicy = "FinishLifetime",
	})
	context:PlayPose("Basic", 0.2)
end
```

---

## 26. Summon

```lua
function Tower.PerformSummon(context)
	context:PlayPose("OpenGate", 0.4)
	context:SpawnUnit("Wolf", {
		Behavior = "Independent",
		OwnerLossPolicy = "DestroyWithOwner",
	})
	context:PlayPose("Basic", 0.25)
end
```

---

## 27. Passive

```lua
function Tower.Start(context)
	context:ApplyAura("AttackSpeedAura")
end

function Tower.Stop(context)
	context:RemoveAura("AttackSpeedAura")
end
```

---

## 28. Reactive

```lua
function Tower.OnEnemyKilled(context, enemy)
	context:PlayPose("Trigger", 0.12)
	context:DamageArea(context:GetTargetPosition(enemy), 6)
	context:PlayPose("Basic", 0.15)
end
```

이벤트 종류와 중복 실행 제한은 구현 명세에서 확정합니다.

---

## 29. ModeShift

```lua
function Tower.EnterMode(context, modeName)
	context:SetMode(modeName)
	context:PlayPose("Transform", 0.5)
end

function Tower.ExitMode(context)
	context:SetMode("Basic")
	context:PlayPose("Basic", 0.4)
end
```

ModeShift는 다른 Movement와 ActionRoutine을 상태별로 바꿀 수 있습니다.

---

# Delivery

## 30. Contact

```lua
context:DamageTarget(target)
```

타워가 대상 근처에 있어야 하는지는 Movement가 결정합니다.

---

## 31. Projectile

```lua
context:FireProjectile("Arrow", target, {
	Origin = context:GetPoint("Weapon/ProjectileOrigin"),
	Modifiers = {"Homing"},
})
```

---

## 32. Hitscan

```lua
context:FireHitscan(target, {
	Origin = context:GetPoint("Weapon/Muzzle"),
	Modifiers = {"Pierce"},
})
```

---

## 33. Beam

```lua
context:StartBeam(target, {
	Origin = context:GetPoint("Core/BeamOrigin"),
})

context:RunChannel(1.0, 0.1, function()
	context:DamageTarget(target)
end)

context:StopBeam()
```

---

## 34. TargetArea와 SelfArea

```lua
context:DamageArea(context:GetTargetPosition(target), 8)
context:DamageArea(context:GetTowerPosition(), 8)
```

---

## 35. SpawnedObject와 SummonedUnit

생성물은 생성물 정책을 함께 지정합니다.

```lua
context:SpawnObject("StormField", position, {
	Behavior = "WorldPersistent",
	OwnerLossPolicy = "FinishLifetime",
})
```

```lua
context:SpawnUnit("Drone", {
	Behavior = "Independent",
	OwnerLossPolicy = "DestroyWithOwner",
})
```

---

# DeliveryModifiers

## 36. 지원 Modifier

```text
Pierce
Chain
Bounce
Splash
Return
Attach
Homing
Split
```

Modifier는 조합 가능한 목록으로 전달합니다.

```lua
context:FireProjectile("Blade", target, {
	Modifiers = {"Homing", "Return", "Pierce"},
})
```

조합이 충돌할 경우 검증기가 경고해야 합니다.

---

# SpawnPolicy

## 37. 생성물 행동 형태

```text
Attached
WorldPersistent
Independent
Returnable
```

## 38. 소유자·대상 상실 정책

```text
DestroyWithOwner
FinishLifetime
TransferOwnership
ReturnToOwner
DestroyWithTarget
```

생성물 최대 수, 수명과 중복 제한은 개별 타워 데이터 또는 생성물 명세에 둡니다.

---

# ResourceProfile

## 39. Ammo

```lua
if not context:ConsumeAmmo(1) then
	context:PlayPose("Reload", 0.8)
	context:ReloadAmmo()
	return
end
```

## 40. Heat

```lua
if context:IsOverheated() then
	context:PlayPose("CoolDown", 0.8)
	context:CoolHeat()
	return
end

context:AddHeat(1)
```

## 41. Charge

```lua
context:AddCharge(1)
if context:GetCharge() >= 5 then
	context:ConsumeCharge(5)
	-- 강화 행동
end
```

## 42. Stack

```lua
context:AddStack("Rage", 1)
if context:GetStack("Rage") >= 3 then
	context:ConsumeStack("Rage", 3)
	-- 방출 행동
end
```

---

# 조합 예시

## 43. 검투사 — Engage + Impact + Contact

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget("LockUntilInvalid")
	if not target then
		context:ReturnToFormation({Speed = 16})
		return
	end

	context:StartPoseLoop({"RunA", "RunB"}, 0.1)
	local result = context:RunToTarget(target, {
		Speed = 18,
		StopDistance = 2.5,
	})
	context:StopPoseLoop()

	if result ~= "Reached" then
		return
	end

	context:FaceTarget(target, 0.08)
	context:PlayPose("SwordRaise", 0.18)
	context:PlayPose("HeavySlash", 0.1)
	context:DamageTarget(target)
	context:PlayPose("Basic", 0.18)
end
```

---

## 44. 전기톱 전사 — Engage + Channel + Contact

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget("LockUntilInvalid")
	if not target then
		context:ReturnToFormation({Speed = 14})
		return
	end

	context:EnsureTargetDistance(target, 2.2, {Speed = 16})
	context:PlayPose("SawStart", 0.2)

	context:RunChannel(1.0, 0.12, function()
		if not context:IsTargetValid(target) then
			target = context:ResolveTargetLoss("Retarget", target)
			if not target then
				return false
			end
			context:EnsureTargetDistance(target, 2.2, {Speed = 16})
		end

		context:PlayPoseAsync("SawKick", 0.05)
		context:DamageTarget(target)
		return true
	end)

	context:PlayPose("Basic", 0.2)
end
```

---

## 45. 미니거너 — Formation + Channel + Hitscan + Heat

```lua
function Tower.Attack(context)
	local target = context:GetOrKeepTarget("LockUntilInvalid")
	if not target then
		return
	end

	if context:IsOverheated() then
		context:PlayPose("CoolDown", 0.8)
		context:CoolHeat()
		return
	end

	context:FaceTarget(target, 0.08)
	context:TrackTarget(target)
	context:PlayPose("BarrelWake", 0.3)

	context:RunChannel(1.5, 0.08, function()
		if not context:IsTargetValid(target) then
			target = context:ResolveTargetLoss("Retarget", target)
			if not target then
				return false
			end
		end

		context:PlayPoseAsync("Kick", 0.04)
		context:FireHitscan(target)
		context:AddHeat(1)
		return not context:IsOverheated()
	end)

	context:StopTrackingTarget()
	context:PlayPose("BarrelSleep", 0.25)
	context:PlayPose("Basic", 0.15)
end
```

---

# 제작 순서

## 46. 새 타워 제작 체크리스트

```text
1. 전투 역할 선택
2. TargetPolicy 선택
3. TargetLossPolicy 선택
4. Movement 선택
5. FacingPolicy 선택
6. ActionRoutine 선택
7. Delivery 선택
8. 필요한 Modifier 선택
9. 생성물이 있으면 SpawnPolicy 선택
10. 자원 순환이 있으면 ResourceProfile 선택
11. Basic 3D 모델 제작
12. 자유 이름 모션 견본 제작
13. 행동 ModuleScript에서 함수 순서 작성
14. Preview와 검증기 실행
```

### Preview 검증 항목

- Engage 이동 시간이 실제 공격 시점에 반영되는가
- 타겟 사망 시 정책대로 처리되는가
- Root Movement와 Pose가 서로 덮어쓰지 않는가
- 여러 Engage 타워가 같은 위치에 완전히 겹치지 않는가
- 취소 후 Beam, Trail, 포즈 반복과 교전 슬롯이 정리되는가
- 생성물이 소유권과 수명 정책대로 제거되는가
- ResourceProfile 상태가 행동과 일치하는가

---

## 47. 변경 원칙

이 문서는 현재 확정된 제작 기준이며 계속 수정합니다.

새 타워가 기존 문법으로 표현되지 않을 때는 새 상속 클래스를 먼저 만들지 않습니다.

검토 순서:

```text
기존 축 조합
→ 새 Modifier
→ 새 ResourceProfile 또는 SpawnPolicy
→ 기존 ActionRoutine의 옵션 확장
→ 마지막 수단으로 새 Movement 또는 ActionRoutine 추가
```

새 공개 함수나 메타데이터를 코드에 먼저 추가하지 않고 이 문서를 먼저 갱신합니다.
