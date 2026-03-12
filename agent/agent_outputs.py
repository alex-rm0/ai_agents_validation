import json
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