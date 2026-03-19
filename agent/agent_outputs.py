import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def create_run_folder(base_dir: str = "outputs") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(base_dir) / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_plan_json(plan: Dict[str, Any], run_dir: Path) -> None:
    file_path = run_dir / "plan.json"
    file_path.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def save_requirements_summary(plan: Dict[str, Any], run_dir: Path) -> None:
    file_path = run_dir / "requirements_summary.md"

    content = "# Resumo dos Requisitos\n\n"
    content += "## Resumo\n\n"
    content += f"{plan['summary']}\n\n"
    content += "## Requisitos\n\n"

    for i, req in enumerate(plan["requirements"], start=1):
        content += f"{i}. {req}\n"

    file_path.write_text(content, encoding="utf-8")


def save_issues_preview(plan: Dict[str, Any], run_dir: Path) -> None:
    file_path = run_dir / "issues_preview.md"

    content = "# Issues a Criar\n\n"

    for i, issue in enumerate(plan["issues"], start=1):
        content += f"## {i}. {issue['title']}\n\n"
        content += f"**Prioridade:** {issue.get('priority', 'medium')}\n\n"
        content += f"**Labels:** {', '.join(issue.get('labels', []))}\n\n"
        content += f"**Descrição:** {issue.get('body', '')}\n\n"

        criteria = issue.get("acceptance_criteria", [])
        if criteria:
            content += "**Critérios de aceitação:**\n\n"
            for criterion in criteria:
                content += f"- {criterion}\n"
            content += "\n"

    file_path.write_text(content, encoding="utf-8")


def save_validation_report(errors: List[str], run_dir: Path) -> None:
    file_path = run_dir / "validation_report.md"

    if not errors:
        content = "# Relatório de Validação\n\nPlano validado sem erros.\n"
    else:
        content = "# Relatório de Validação\n\nForam encontrados os seguintes problemas:\n\n"
        for error in errors:
            content += f"- {error}\n"

    file_path.write_text(content, encoding="utf-8")


def print_plan(plan: Dict[str, Any]) -> None:
    print("\n=== RESUMO ===")
    print(plan["summary"])

    print("\n=== REQUISITOS ===")
    for i, req in enumerate(plan["requirements"], start=1):
        print(f"{i}. {req}")

    print("\n=== ISSUES A CRIAR ===")
    for i, issue in enumerate(plan["issues"], start=1):
        print(f"\n{i}. {issue['title']}")
        print(f"   Prioridade: {issue.get('priority', 'medium')}")
        print(f"   Labels: {', '.join(issue.get('labels', []))}")
        print(f"   Descrição: {issue.get('body', '')}")

        criteria = issue.get("acceptance_criteria", [])
        if criteria:
            print("   Critérios de aceitação:")
            for criterion in criteria:
                print(f"   - {criterion}")


def save_frontend_generation(
    result: Dict[str, str],
    run_dir: Path,
    file_name: str,
    preview_base_dir: str = "frontend_preview",
) -> Path:
    frontend_dir = run_dir / "frontend"
    frontend_dir.mkdir(parents=True, exist_ok=True)

    safe_stem = Path(file_name).stem

    prompt_file = frontend_dir / f"{safe_stem}_prompt.txt"
    raw_file = frontend_dir / f"{safe_stem}_raw_response.txt"
    code_file = frontend_dir / file_name

    prompt_file.write_text(result["prompt"], encoding="utf-8")
    raw_file.write_text(result["raw_response"], encoding="utf-8")
    code_file.write_text(result["code"], encoding="utf-8")

    copy_component_to_frontend_preview(code_file, preview_base_dir=preview_base_dir)

    return code_file


def copy_component_to_frontend_preview(
    source_file: Path,
    preview_base_dir: str = "frontend_preview",
) -> Path | None:
    preview_generated_dir = Path(preview_base_dir) / "src" / "generated"

    if not preview_generated_dir.parent.parent.exists():
        return None

    preview_generated_dir.mkdir(parents=True, exist_ok=True)

    destination_file = preview_generated_dir / source_file.name
    shutil.copy2(source_file, destination_file)

    return destination_file


def clear_frontend_preview_generated(preview_base_dir: str = "frontend_preview"):
    preview_generated_dir = Path(preview_base_dir) / "src" / "generated"

    if not preview_generated_dir.exists():
        return

    for file in preview_generated_dir.glob("*.tsx"):
        file.unlink()


def save_test_generation(result: Dict[str, Any], run_dir: Path) -> Path:
    tests_dir = run_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    for feature in result["features"]:
        feature_file = tests_dir / feature["filename"]
        feature_file.write_text(feature["content"], encoding="utf-8")

    manifest_file = tests_dir / "manifest.json"
    manifest_file.write_text(
        json.dumps(result["manifest"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return tests_dir