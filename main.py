from typing import List

from agent.utils import get_env
from agent.agent_planner import generate_plan
from agent.agent_validator import validate_plan
from agent.agent_outputs import (
    create_run_folder,
    save_plan_json,
    save_requirements_summary,
    save_issues_preview,
    save_validation_report,
    print_plan,
)
from agent.agent_github import build_issue_body, create_github_issue


def main() -> None:
    github_token = get_env("GITHUB_TOKEN")
    github_owner = get_env("GITHUB_OWNER")
    github_repo = get_env("GITHUB_REPO")

    print("PM Agent - GitHub Issues")
    print("Escreve o pedido de produto/funcionalidade.")

    user_prompt = input("\nPedido: ").strip()

    if not user_prompt:
        print("Pedido vazio.")
        return

    print("\nA gerar plano...")
    plan = generate_plan(user_prompt)

    validation_errors = validate_plan(plan, user_prompt)

    run_dir = create_run_folder()
    save_plan_json(plan, run_dir)
    save_requirements_summary(plan, run_dir)
    save_issues_preview(plan, run_dir)
    save_validation_report(validation_errors, run_dir)

    print(f"\nOutputs guardados em: {run_dir}")

    if validation_errors:
        print("\nForam encontrados problemas no plano:")
        for error in validation_errors:
            print(f"- {error}")

        print("\nOperação cancelada devido a erros de validação.")
        return

    print_plan(plan)

    confirm = input("\nQueres criar estas issues no GitHub? (s/n): ").strip().lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    print("\nA criar issues no GitHub...")

    created_urls: List[str] = []

    for issue in plan["issues"]:
        formatted_body = build_issue_body(issue)

        url = create_github_issue(
            owner=github_owner,
            repo=github_repo,
            token=github_token,
            title=issue["title"],
            body=formatted_body,
            labels=issue.get("labels", []),
        )

        created_urls.append(url)

    print("\n=== ISSUES CRIADAS ===")
    for url in created_urls:
        print(url)

    print("\nConcluído.")


if __name__ == "__main__":
    main()