import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _safe_filename(name: str) -> str:
    name = name.strip() or "generated"
    name = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE)
    name = re.sub(r"\s+", "_", name)
    return name[:80] or "generated"


def _to_tags(scenario: Dict[str, Any]) -> List[str]:
    tags: List[str] = []
    priority = scenario.get("priority")
    if priority in ("low", "medium", "high"):
        tags.append(f"priority_{priority}")

    flow_type = scenario.get("flow_type")
    if isinstance(flow_type, str) and flow_type:
        tags.append(f"flow_{_safe_filename(flow_type).lower()}")

    auth = scenario.get("auth")
    if auth in ("none", "optional", "required", "unknown"):
        tags.append(f"auth_{auth}")

    return tags


def generate_feature_files_from_test_spec(
    *,
    test_spec: Dict[str, Any],
    output_dir: Path,
) -> List[Path]:
    """
    Gera ficheiros `.feature` a partir de `test_spec.json`.

    Nota:
    - Os passos são gravados "como texto" (contrato estável).
    - A compatibilidade com step definitions concretos é responsabilidade do `test_engine`.
    """
    generated_dir = output_dir / "generated_features"
    generated_dir.mkdir(parents=True, exist_ok=True)

    created: List[Path] = []

    for feature in test_spec.get("features", []) or []:
        feature_name = (feature.get("name") or "Generated Feature").strip()
        feature_file = generated_dir / f"{_safe_filename(feature_name)}.feature"

        lines: List[str] = []
        lines.append("@ignore")
        lines.append(f"Feature: {feature_name}")
        lines.append("  Generated from test_spec.json (contract-first).")
        lines.append("")

        for scenario in feature.get("scenarios", []) or []:
            scenario_name = (scenario.get("name") or "Generated Scenario").strip()
            tags = _to_tags(scenario)
            if tags:
                lines.append("@" + " @".join(tags))

            lines.append(f"  Scenario: {scenario_name}")

            for step in scenario.get("given", []) or []:
                lines.append(f"    Given {step.get('text')}")
            for step in scenario.get("when", []) or []:
                lines.append(f"    When {step.get('text')}")
            for step in scenario.get("then", []) or []:
                lines.append(f"    Then {step.get('text')}")

            lines.append("")

        feature_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        created.append(feature_file)

    return created


def load_test_spec_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

