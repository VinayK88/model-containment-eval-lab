from __future__ import annotations

import argparse
import json
from pathlib import Path

from .experiment import load_scenarios, run_experiment
from .visualize import render_overview


def main() -> int:
    parser = argparse.ArgumentParser(description="Run safe, simulation-only model containment evaluations.")
    parser.add_argument("--scenarios", type=Path, default=Path("scenarios/scenarios.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/baseline.json"))
    parser.add_argument("--visual", type=Path, default=Path("assets/containment-overview.svg"))
    args = parser.parse_args()

    report = run_experiment(load_scenarios(args.scenarios))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.visual.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.visual.write_text(render_overview(report) + "\n", encoding="utf-8")

    print("agent                control      complete  attempts  sim-breach  monitor-risk")
    print("-------------------  -----------  --------  --------  ----------  ------------")
    for item in report["summary"]:
        print(
            f"{item['agent']:<19}  {item['control_profile']:<11}  "
            f"{item['task_completion_rate']:.1%}    {item['violation_attempt_rate']:.1%}    "
            f"{item['simulated_breach_rate']:.1%}       {item['mean_learned_risk']:.1%}"
        )
    print(f"\nwrote {args.output} and {args.visual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
