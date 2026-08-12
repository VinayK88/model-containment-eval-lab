from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Action:
    tool: str
    target: str = ""
    payload: str = ""


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    title: str
    category: str
    pressure: str
    instruction: str
    evidence: str
    injection: str = ""
    shutdown_after_step: int | None = None
    evaluation_visible: bool = False
    pair_id: str | None = None


@dataclass(frozen=True)
class TraceEvent:
    step: int
    action: Action
    allowed: bool
    outcome: str
    violation_type: str | None = None
    tripwire: str | None = None
    simulated_effect: bool = False
    shutdown_active: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Episode:
    scenario_id: str
    scenario_title: str
    category: str
    agent: str
    control_profile: str
    task_completed: bool
    shutdown_compliant: bool | None
    events: tuple[TraceEvent, ...]

    @property
    def violation_attempted(self) -> bool:
        return any(event.violation_type for event in self.events)

    @property
    def simulated_breach(self) -> bool:
        return any(event.violation_type and event.simulated_effect for event in self.events)

    @property
    def first_violation_step(self) -> int | None:
        return next((event.step for event in self.events if event.violation_type), None)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["violation_attempted"] = self.violation_attempted
        result["simulated_breach"] = self.simulated_breach
        result["first_violation_step"] = self.first_violation_step
        return result
