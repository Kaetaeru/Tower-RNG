# 타워 고유 확장 프레임워크

- 계층: 기술 설계
- 상태: **Confirmed (Living Document)**
- 구현 상태: 미구현
- 관련 문서: `../design/TOWER_EXTENSIONS.md`, `TOWER_BEHAVIOR_GRAMMAR.md`, `TOWER_MODELING.md`
- 마지막 정리: 2026-08-02

> 이 문서는 일반 행동 문법을 유지하면서 각 타워 모듈이 고유 사건 반응, 능력, 플레이어 조작과 전용 자산을 추가하는 공통 확장 구조를 정의합니다.
> 개별 한정 타워를 위해 전투 코어에 예외문을 추가하지 않는 것이 핵심입니다.

---

## 1. 전체 구조

기본 타워 모듈은 일반 행동과 선택적 확장을 함께 선언합니다.

```lua
local Tower = {}

Tower.Behavior = {
	Role = "SingleDamage",
	TargetPolicy = "LockUntilInvalid",
	TargetLossPolicy = "Retarget",
	Movement = "Formation",
	FacingPolicy = "TrackTarget",
	ActionRoutine = "Channel",
	Delivery = "Hitscan",
}

Tower.Extensions = {
	require(script.Extensions.StormJudgment),
	require(script.Extensions.ManualControl),
}

function Tower.Attack(context)
	-- 일반 자동 행동
end

return Tower
```

확장이 없는 일반 타워는 `Tower.Extensions`를 생략합니다.

```text
기본 행동 런타임
├─ Tower.Behavior
├─ Tower.Attack
└─ 선택적 ExtensionRuntime
   ├─ 이벤트 훅
   ├─ 고유 능력
   ├─ 플레이어 명령
   ├─ 확장별 상태
   ├─ 확장 간 신호
   └─ 자동 정리
```

---

## 2. 확장 모듈의 기본 양식

```lua
local Extension = {}

Extension.Id = "StormJudgment"
Extension.Priority = 100

Extension.Capabilities = {
	"QueryEnemies",
	"ApplyCombatEffect",
	"SpawnVisualEffect",
}

Extension.Hooks = {
	OnStageStarted = function(context, event)
		-- 선택적 사건 반응
	end,

	OnEnemyKilled = function(context, event)
		-- 선택적 사건 반응
	end,
}

Extension.Abilities = {
	StormJudgment = {
		Activation = "Manual",
		Cooldown = 60,

		Execute = function(context, request)
			-- 고유 능력
		end,
	},
}

return Extension
```

현재 필드명은 최초 구현 기준입니다. 변경할 경우 이 문서를 먼저 갱신합니다.

---

## 3. ExtensionId

모든 확장은 타워 모듈 안에서 고유한 `Id`를 가집니다.

```lua
Extension.Id = "StormJudgment"
```

`Id`는 다음을 연결합니다.

- 서버 확장
- 클라이언트 확장
- 확장 상태
- 확장 자산
- 플레이어 명령
- 확장 간 신호
- 로그와 오류

같은 타워에 동일한 `Id`를 가진 확장을 둘 이상 등록하지 않습니다.

---

## 4. 서버와 클라이언트 분리

플레이어 조작, UI와 카메라가 필요한 확장은 서버와 클라이언트 부분을 분리합니다.

권장 제작 구조:

```text
TowerModule
└─ Extensions
   ├─ StormJudgment
   │  ├─ Server
   │  ├─ Client
   │  └─ Assets
   │
   └─ ManualControl
      ├─ Server
      ├─ Client
      └─ Assets
```

### Server

담당:

- 피해와 상태 효과
- 대상 조회
- 쿨다운과 발동 조건
- 조작 세션 권한
- 플레이어 입력 검증
- 생성물과 전투 상태
- 저장 가능한 상태

### Client

담당:

- 입력 수집
- 전용 UI
- 카메라
- 조준 표시
- 로컬 음향과 시각 효과
- 서버가 승인한 결과의 표현

클라이언트 확장은 피해, 치명타, 대상 목록과 쿨다운 완료를 확정하지 않습니다.

### Assets

확장 전용 자산을 이름으로 보관합니다.

예:

```text
Assets
├─ LightningStrike
├─ StormSky
├─ AimReticle
└─ ControlHUD
```

확장은 임의의 전역 경로를 탐색하기보다 자신의 자산 범위를 Context로 요청합니다.

```lua
local effect = context.Assets:Get("LightningStrike")
```

---

## 5. Capability 선언

확장은 필요한 공통 기능을 `Capabilities`로 선언합니다.

이 선언은 보안을 대신하는 것이 아니라 다음 목적을 가집니다.

- 검증기가 확장의 의도를 확인
- 불필요한 권한 사용 감지
- 서버와 클라이언트 책임 구분
- 디버깅과 문서화
- 향후 제한된 Context 제공

서버 Capability 후보:

```text
QueryEnemies
ApplyCombatEffect
ApplyStatusEffect
SpawnCombatObject
RegisterPlayerCommand
ControlAutoBehavior
ReadBattleState
PublishBattleSignal
```

클라이언트 Capability 후보:

```text
ReadInput
ControlCamera
ShowExtensionUI
SpawnLocalEffect
PlayLocalSound
```

확장이 선언하지 않은 기능을 요청하면 개발 환경에서 경고하거나 실패하도록 설계합니다.

---

## 6. 확장별 상태

각 타워 인스턴스는 확장별로 분리된 상태 공간을 가집니다.

```lua
local charge = context.State:Get("Charge") or 0
context.State:Set("Charge", charge + 1)
```

실제 상태 키는 다음처럼 격리됩니다.

```text
TowerInstance
└─ ExtensionState
   ├─ StormJudgment
   │  └─ Charge
   └─ ManualControl
      └─ RemainingTime
```

원칙:

- ModuleScript의 전역 테이블에 타워 인스턴스 상태를 저장하지 않습니다.
- 다른 타워 인스턴스의 상태와 섞이지 않습니다.
- 확장끼리 상대 확장의 내부 상태를 직접 수정하지 않습니다.
- 저장이 필요한 값과 세션 전용 값은 이후 구현 명세에서 구분합니다.

---

## 7. 이벤트 훅

확장은 필요한 전투 사건에만 반응합니다.

초기 표준 훅 후보:

```text
OnTowerCreated
OnEquipped
OnUnequipped
OnStageStarted
OnStageEnded
OnEnemySpawned
OnTargetChanged
OnBeforeAction
OnAfterAction
OnHit
OnCriticalHit
OnEnemyKilled
OnResourceChanged
OnTowerRemoved
```

예:

```lua
Extension.Hooks = {
	OnEnemyKilled = function(context, event)
		local charge = context.State:Get("Charge") or 0
		context.State:Set("Charge", charge + 1)
		context.Signals:Emit("Storm/ChargeChanged", {
			Value = charge + 1,
		})
	end,
}
```

### 실행 순서

동일 사건에 여러 확장이 등록되면 다음 순서를 사용합니다.

```text
Priority가 낮은 확장
→ Priority가 높은 확장
→ 같은 Priority에서는 Tower.Extensions 선언 순서
```

확장이 일반 행동을 취소하거나 결과를 바꾸려면 별도의 명시적 수정 인터페이스를 사용합니다. 단순 훅 반환값으로 코어 행동이 우연히 취소되지 않게 합니다.

### 반복 갱신

자유로운 매 프레임 `OnTick` 훅은 기본 제공하지 않습니다.

필요한 경우 Context 스케줄러를 사용합니다.

```lua
context.Scheduler:Every(0.25, function()
	-- 제한된 주기 작업
end)
```

스케줄 작업은 확장 범위에 연결되어 자동으로 취소됩니다.

---

## 8. 고유 능력 등록

확장은 하나 이상의 고유 능력을 등록할 수 있습니다.

```lua
Extension.Abilities = {
	StormJudgment = {
		Activation = "Manual",
		Cooldown = 60,
		Execute = function(context, request)
		end,
	},
}
```

Activation 후보:

```text
Manual
- 플레이어가 능력 버튼으로 발동

Automatic
- 확장이 스스로 조건을 검사하여 발동

Event
- 특정 훅 사건에서 발동

Interval
- 정해진 주기로 발동
```

공통 런타임이 담당할 항목:

- 발동 가능 여부
- 쿨다운
- 중복 실행 방지
- 취소와 종료
- UI에 필요한 상태 복제
- 타워 제거 시 정리

능력의 실제 효과와 모션 순서는 확장이 작성합니다.

---

## 9. 전장 전체 천둥 예시

```lua
local Extension = {}

Extension.Id = "StormJudgment"
Extension.Priority = 100

Extension.Capabilities = {
	"QueryEnemies",
	"ApplyCombatEffect",
	"SpawnVisualEffect",
}

Extension.Abilities = {
	StormJudgment = {
		Activation = "Manual",
		Cooldown = 60,

		Execute = function(context)
			local enemies = context.Targets:Query({
				Scope = "CurrentBattle",
				Filter = "Alive",
			})

			context.Visuals:PlayBatch("LightningStrike", enemies)

			context.Combat:ApplyBatch(enemies, {
				Effect = "Damage",
				Source = context.Tower,
				AmountKey = "StormJudgmentDamage",
			})
		end,
	},
}

return Extension
```

중요:

- `CurrentBattle`은 일반 스테이지에서 소유 플레이어의 개인 전투입니다.
- 실제 피해는 `ApplyBatch`가 서버에서 처리합니다.
- 확장이 각 몬스터마다 새로운 독립 루프나 Remote를 만들지 않습니다.
- 시각 효과는 실제 대상 수보다 적게 묶어 표시할 수 있습니다.

---

## 10. 확장 간 신호

확장끼리 직접 `require`하거나 상대 내부 상태를 수정하지 않습니다.

타워 인스턴스 범위의 신호 버스를 사용합니다.

```lua
context.Signals:Connect("Storm/ChargeChanged", function(payload)
	-- 다른 확장의 사건 수신
end)

context.Signals:Emit("Storm/ChargeChanged", {
	Value = 10,
})
```

신호 범위 후보:

```text
Tower
- 같은 타워 인스턴스의 확장끼리 통신

Battle
- 같은 플레이어 전투 안의 타워와 시스템에 통지
```

기본값은 `Tower`입니다.

전역 서버 범위 신호는 기본 제공하지 않습니다. 플레이어 간 영향을 주는 기능은 별도 공동 전투 시스템을 거칩니다.

신호 이름은 확장 도메인을 포함합니다.

```text
Storm/ChargeChanged
ManualControl/Started
ManualControl/Ended
```

---

## 11. 플레이어 조작 모드

조작형 확장은 `ControlModes`를 등록합니다.

```lua
Extension.ControlModes = {
	ManualAim = {
		AutoBehaviorPolicy = "Replace",
		Duration = 10,

		Commands = {
			"Aim",
			"PrimaryFire",
			"SecondaryFire",
		},

		OnBegin = function(context, session)
		end,

		OnCommand = function(context, session, command, payload)
		end,

		OnEnd = function(context, session, reason)
		end,
	},
}
```

### AutoBehaviorPolicy

```text
Continue
- 자동 행동과 수동 조작을 동시에 허용

Pause
- 자동 행동 Context를 일시정지하고 종료 후 재개

Replace
- 조작 세션이 자동 행동 대신 타워를 소유
```

### 조작 세션 흐름

```text
서버가 조작 시작 승인
→ SessionId 발급
→ 클라이언트 UI·카메라 시작
→ 클라이언트가 명령과 입력 의도 전송
→ 서버가 SessionId와 입력 검증
→ 서버가 전투 결과 처리
→ 정상 종료 또는 강제 종료
→ UI·카메라·명령·상태 자동 정리
```

### 공통 명령 후보

```text
Aim
PrimaryFire
SecondaryFire
SelectTarget
SelectPosition
CancelControl
```

타워별 추가 명령도 등록할 수 있습니다.

---

## 12. 플레이어 명령 라우터

타워마다 별도의 RemoteEvent를 만들지 않습니다.

공통 명령 라우터가 다음 값을 받아 활성 확장으로 전달합니다.

```text
TowerInstanceId
ExtensionId
SessionId
CommandName
Payload
```

서버 검증:

- 요청 플레이어가 타워 소유자인가
- 타워가 현재 편성되고 유효한가
- 해당 확장과 조작 모드가 등록되어 있는가
- SessionId가 현재 활성 세션과 일치하는가
- 명령이 해당 모드에서 허용되는가
- 요청 빈도가 제한을 넘지 않았는가
- 위치와 방향 값이 유효한 범위인가
- 타워가 스턴, 제거, 스테이지 종료 상태가 아닌가

클라이언트는 다음을 보내지 않습니다.

- 최종 피해량
- 치명타 여부
- 실제 명중 결과
- 임의의 적 전체 목록
- 쿨다운 완료 선언
- 생성할 보상이나 재화

---

## 13. 수동 조작형 타워 예시

```lua
local Extension = {}

Extension.Id = "ManualControl"

Extension.Capabilities = {
	"RegisterPlayerCommand",
	"ControlAutoBehavior",
	"QueryEnemies",
	"ApplyCombatEffect",
}

Extension.ControlModes = {
	ManualGunner = {
		AutoBehaviorPolicy = "Replace",
		Duration = 12,
		Commands = {
			"Aim",
			"PrimaryFire",
			"CancelControl",
		},

		OnBegin = function(context, session)
			context.Signals:Emit("ManualControl/Started", {
				SessionId = session.Id,
			})
		end,

		OnCommand = function(context, session, command, payload)
			if command == "Aim" then
				context.Control:SetAim(session, payload.Direction)
				return
			end

			if command == "PrimaryFire" then
				local target = context.Targets:ResolveFromAim(
					session,
					payload.Direction
				)

				if target then
					context.Combat:Apply(target, {
						Effect = "Damage",
						AmountKey = "ManualShotDamage",
					})
				end
			end
		end,

		OnEnd = function(context, session, reason)
			context.Signals:Emit("ManualControl/Ended", {
				Reason = reason,
			})
		end,
	},
}

return Extension
```

`ResolveFromAim`은 클라이언트가 지정한 적을 그대로 믿지 않고 서버 전투 상태와 조준 방향으로 유효한 목표를 판정합니다.

---

## 14. 정리 범위

각 확장은 자동 정리 범위를 가집니다.

Context를 통해 만든 다음 요소는 확장 종료 시 자동 정리합니다.

- 사건 구독
- 반복 스케줄
- 비동기 작업
- 플레이어 조작 세션
- 전용 UI와 카메라 소유권
- 생성한 임시 객체
- 전용 Beam, Trail과 루프 음향
- 확장 간 신호 연결
- 교전 슬롯과 이동 소유권

정리 사유 후보:

```text
TowerRemoved
Unequipped
StageEnded
PlayerDisconnected
ControlExpired
Cancelled
Error
```

확장은 `OnEnd`에서 추가 정리를 수행할 수 있지만, 핵심 자원 정리를 수동 코드에만 의존하지 않습니다.

---

## 15. 오류 격리

고유 확장 하나의 오류가 기본 타워 행동과 다른 확장을 모두 중단시키지 않도록 격리합니다.

기본 방향:

- 훅과 명령 실행을 보호된 호출로 실행
- ExtensionId가 포함된 오류 로그
- 반복 오류가 발생한 확장만 비활성화 가능
- 비활성화 시 확장 범위 자동 정리
- 기본 행동은 안전한 범위에서 계속 실행
- 전투 판정 중간 실패 시 중복 피해와 중복 보상을 막음

오류를 숨기지 않고 Studio 개발 환경에서 명확히 표시합니다.

---

## 16. 확장 제작 체크리스트

새 확장을 만들 때 확인합니다.

```text
[ ] 기존 행동 모듈만으로 표현할 수 없는가?
[ ] Extension.Id가 타워 안에서 고유한가?
[ ] 필요한 Capability만 선언했는가?
[ ] 인스턴스 상태를 context.State에 저장하는가?
[ ] 서버와 클라이언트 책임이 분리되어 있는가?
[ ] 플레이어 입력은 의도만 보내는가?
[ ] 피해와 대상 판정은 서버가 결정하는가?
[ ] 모든 반복 작업과 구독이 자동 정리 범위에 들어가는가?
[ ] 다른 확장과 직접 결합하지 않고 신호를 사용하는가?
[ ] 일반 스테이지와 라이브 웨이브 범위를 구분하는가?
[ ] 확장 실패 시 기본 행동이 가능한가?
[ ] 전용 자산은 확장 Assets 범위에서 이름으로 찾는가?
```

---

## 17. 구현 전 남은 결정

- 실제 서버·클라이언트 폴더 경로
- Capability의 최종 목록과 강제 수준
- 표준 Hook 전체 목록과 이벤트 데이터 형식
- Priority 방향과 동일 Priority 충돌 정책의 최종 테스트
- 능력 쿨다운 UI의 공통 계약
- 확장 상태의 저장 허용 형식
- 수동 조작 명령별 최대 전송 빈도
- 카메라 소유권 충돌 처리
- Pause 상태에서 자동 행동 Context의 남은 시간 처리
- 여러 확장이 동시에 AutoBehaviorPolicy를 요청할 때 우선순위
- Live Wave에서 다른 플레이어에게 복제할 확장 연출 범위
