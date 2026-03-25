import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional


TestPriority = Literal["low", "medium", "high"]
FlowType = Literal["happy_path", "error_path", "edge_case", "unknown"]
AuthRequirement = Literal["none", "optional", "required", "unknown"]


@dataclass(frozen=True)
class TestStep:
    text: str


@dataclass(frozen=True)
class TestScenario:
    name: str
    given: List[TestStep]
    when: List[TestStep]
    then: List[TestStep]
    priority: TestPriority = "medium"
    flow_type: FlowType = "unknown"
    auth: AuthRequirement = "unknown"


@dataclass(frozen=True)
class TestFeature:
    name: str
    scenarios: List[TestScenario]


@dataclass(frozen=True)
class TestSpec:
    schema_version: str
    generated_at_utc: str
    features: List[TestFeature]
    meta: Dict[str, Any]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_test_spec_from_plan(
    *,
    user_prompt: str,
    plan: Dict[str, Any],
    run_dir: Path,
) -> Dict[str, Any]:
    """
    Constrói uma especificação intermédia estável (`test_spec.json`) a partir de um plano.

    Nota:
    - Nesta fase é um "builder" conservador e genérico.
    - Não tenta inferir passos reais de UI/API a partir de markdown livre.
    - O objetivo é definir o contrato e permitir evolução incremental.
    """
    issues = plan.get("issues", []) or []

    scenarios: List[TestScenario] = []

    for issue in issues:
        title = (issue.get("title") or "").strip() or "Cenário sem título"
        priority = issue.get("priority", "medium")
        if priority not in ("low", "medium", "high"):
            priority = "medium"

        labels = set(issue.get("labels", []) or [])
        auth: AuthRequirement = "unknown"
        if "authentication" in labels:
            auth = "required"

        given_steps = [TestStep("the application base url is configured")]

        # Heurística mínima:
        # - mantemos apenas passos suportados pelo motor genérico (para evitar cenários "undefined").
        # - os critérios de aceitação seguem no contrato (meta) para futuras fases.
        then_steps = [TestStep("the browser should be at the base url")]

        scenarios.append(
            TestScenario(
                name=title,
                given=given_steps,
                when=[TestStep("I navigate to the home page")],
                then=then_steps,
                priority=priority,  # type: ignore[assignment]
                flow_type="unknown",
                auth=auth,
            )
        )

    feature_name = "Generated functional scenarios"
    features = [TestFeature(name=feature_name, scenarios=scenarios)]

    spec = TestSpec(
        schema_version="1.0",
        generated_at_utc=_utc_now_iso(),
        features=features,
        meta={
            "source": "agent.test_generation.test_spec_builder",
            "user_prompt": user_prompt,
            "run_dir": str(run_dir),
            "acceptance_criteria_by_issue": [
                {
                    "title": (i.get("title") or "").strip(),
                    "acceptance_criteria": i.get("acceptance_criteria", []) or [],
                }
                for i in issues
            ],
        },
    )

    # dataclasses -> dict (garantindo JSON estável)
    data = asdict(spec)
    return data


def save_test_spec_json(*, test_spec: Dict[str, Any], run_dir: Path) -> Path:
    tests_dir = run_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    path = tests_dir / "test_spec.json"
    path.write_text(json.dumps(test_spec, indent=2, ensure_ascii=False), encoding="utf-8")
    return path

