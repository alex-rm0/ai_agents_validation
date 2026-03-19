from typing import List
import re

from agent.utils import get_env
from agent.agent_planner import generate_plan
from agent.agent_validator import validate_plan
from agent.agent_outputs import (
    create_run_folder,
    save_plan_json,
    save_requirements_summary,
    save_issues_preview,
    save_validation_report,
    save_frontend_generation,
    save_test_generation,
    print_plan,
    clear_frontend_preview_generated,
    copy_component_to_frontend_preview,
)
from agent.agent_github import build_issue_body, create_github_issue
from agent.agent_frontend_generator import generate_frontend_component
from agent.agent_test_generator import generate_functional_tests


def issue_title_to_component_filename(title: str) -> str:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", title)

    if not words:
        return "GeneratedComponent.tsx"

    ignored_words = {
        "de",
        "da",
        "do",
        "das",
        "dos",
        "e",
        "a",
        "o",
        "para",
        "com",
        "sem",
        "em",
        "na",
        "no",
        "nas",
        "nos",
    }

    filtered_words = [word for word in words if word.lower() not in ignored_words]

    if not filtered_words:
        filtered_words = words

    pascal_case = "".join(word.capitalize() for word in filtered_words)

    if not pascal_case.endswith("Component"):
        pascal_case += "Component"

    return f"{pascal_case}.tsx"


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

    frontend_issues = [
        issue for issue in plan["issues"]
        if "frontend" in issue.get("labels", [])
    ]

    if frontend_issues:
        clear_frontend_preview_generated()
        
        print("\n=== ISSUES FRONTEND DISPONÍVEIS ===")
        for i, issue in enumerate(frontend_issues, start=1):
            print(f"{i}. {issue['title']}")

        frontend_mode = input(
            "\nQueres gerar frontend para (1) uma issue, (2) todas as issues frontend, ou (3) ignorar? "
        ).strip()

        if frontend_mode == "1":
            selected = input("Escolhe o número da issue frontend: ").strip()

            if selected.isdigit():
                selected_index = int(selected) - 1

                if 0 <= selected_index < len(frontend_issues):
                    selected_issue = frontend_issues[selected_index]
                    file_name = issue_title_to_component_filename(selected_issue["title"])

                    print("\nA gerar componente frontend...")
                    frontend_result = generate_frontend_component(selected_issue)

                    saved_file = save_frontend_generation(frontend_result, run_dir, file_name=file_name)

                    print("\nComponente frontend gerado com sucesso.")
                    print(f"Ficheiro guardado em: {saved_file}")
                    print(f"Componente copiado para: frontend_preview/src/generated/{file_name}")
                else:
                    print("Número inválido. Geração frontend ignorada.")
            else:
                print("Valor inválido. Geração frontend ignorada.")

        elif frontend_mode == "2":
            print("\nA gerar componentes frontend para todas as issues...")

            for issue in frontend_issues:
                file_name = issue_title_to_component_filename(issue["title"])
                frontend_result = generate_frontend_component(issue)
                saved_file = save_frontend_generation(frontend_result, run_dir, file_name=file_name)

                print(f"Gerado: {saved_file}")
                print(f"Copiado para: frontend_preview/src/generated/{file_name}")

            print("\nTodos os componentes frontend foram gerados com sucesso.")

        elif frontend_mode == "3":
            print("Geração frontend ignorada.")

        else:
            print("Opção inválida. Geração frontend ignorada.")

    generate_tests = input(
        "\nQueres gerar ficheiros de teste Gherkin (.feature)? (s/n): "
    ).strip().lower()

    if generate_tests == "s":
        print("\nA gerar ficheiros .feature...")

        try:
            test_result = generate_functional_tests(
                user_prompt=user_prompt,
                requirements=plan["requirements"],
                issues=plan["issues"],
            )

            tests_dir = save_test_generation(test_result, run_dir)

            print(f"\nFicheiros .feature gerados com sucesso ({test_result['manifest']['total']} ficheiro(s)):")
            for entry in test_result["manifest"]["features"]:
                print(f"  - {entry['filename']}  (issue: {entry['issue_ref']})")

            print(f"\nGuardados em: {tests_dir}")
            print(
                "\nPara correr os testes: copia os .feature para "
                "test_engine/Features/generated/ e executa bash test_engine/run_tests.sh"
            )

        except RuntimeError as e:
            print(f"\nErro na geração de testes: {e}")

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