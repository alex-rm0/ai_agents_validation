import os
import json
import requests
from typing import Dict, Any, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ----------------------------
# LLM CONFIG (OpenRouter)
# ----------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1"

MODEL = "meta-llama/llama-3.1-8b-instruct"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)

# ----------------------------
# ENV HELPER
# ----------------------------

def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta a variável de ambiente: {name}")
    return value


# ----------------------------
# FORMAT ISSUE BODY
# ----------------------------

def build_issue_body(issue: Dict[str, Any]) -> str:
    body = issue.get("body", "").strip()
    priority = issue.get("priority", "medium")
    acceptance_criteria = issue.get("acceptance_criteria", [])

    formatted = f"Descrição:\n{body}\n\n"
    formatted += f"Prioridade: {priority}\n\n"

    if acceptance_criteria:
        formatted += "Critérios de aceitação:\n"
        for criterion in acceptance_criteria:
            formatted += f"- {criterion}\n"

    return formatted.strip()


# ----------------------------
# GENERATE PLAN WITH LLM
# ----------------------------

def generate_plan(client, user_prompt: str) -> Dict[str, Any]:

    system_prompt = """
És um Project Manager Agent.

Recebes um pedido de funcionalidade e deves decompor esse pedido em tarefas realistas para um projeto de software.

Devolve APENAS JSON válido neste formato:

{
  "summary": "resumo curto",
  "requirements": [
    "requisito 1",
    "requisito 2"
  ],
  "issues": [
    {
      "title": "título curto da tarefa",
      "body": "descrição clara da tarefa",
      "labels": ["frontend", "ui"],
      "priority": "medium",
      "acceptance_criteria": [
        "critério 1",
        "critério 2"
      ]
    }
  ]
}

Regras:
- escreve em português de Portugal
- cria entre 3 e 6 issues
- cada issue deve representar uma tarefa distinta e executável
- não criar issues redundantes, repetidas ou semanticamente sobrepostas
- evitar títulos muito semelhantes
- não inventar backend se o pedido for apenas frontend
- garantir que as tarefas cobrem o pedido completo
- usar granularidade realista para uma equipa de desenvolvimento
- não criar uma issue separada para algo que já esteja implicitamente incluído noutra
- usar labels adequadas de entre: frontend, backend, ui, validation, authentication, documentation, testing
- usar priority com um destes valores: low, medium, high
- o campo body deve ser curto mas útil
- os acceptance_criteria devem ser concretos e verificáveis
- não escrever texto fora do JSON
- não usar markdown
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    text = response.choices[0].message.content

    if not text or not text.strip():
        raise RuntimeError("O modelo devolveu uma resposta vazia.")

    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise RuntimeError(
            f"O modelo não devolveu JSON reconhecível.\n\nResposta recebida:\n{text}"
        )

    json_text = text[start:end + 1]

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Falha ao interpretar JSON.\n\nResposta recebida:\n{text}"
        ) from e

    if "summary" not in data or "requirements" not in data or "issues" not in data:
        raise RuntimeError(
            f"JSON incompleto recebido do modelo:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        )

    if not isinstance(data["issues"], list) or len(data["issues"]) == 0:
        raise RuntimeError("O modelo não devolveu nenhuma issue.")

    for issue in data["issues"]:
        if "title" not in issue or "body" not in issue:
            raise RuntimeError(
                f"Issue inválida recebida do modelo:\n{json.dumps(issue, indent=2, ensure_ascii=False)}"
            )

        if "labels" not in issue or not isinstance(issue["labels"], list):
            raise RuntimeError(
                f"Issue sem labels válidas:\n{json.dumps(issue, indent=2, ensure_ascii=False)}"
            )

        if "priority" not in issue or issue["priority"] not in ["low", "medium", "high"]:
            raise RuntimeError(
                f"Issue com prioridade inválida:\n{json.dumps(issue, indent=2, ensure_ascii=False)}"
            )

        if "acceptance_criteria" not in issue or not isinstance(issue["acceptance_criteria"], list):
            raise RuntimeError(
                f"Issue sem critérios de aceitação válidos:\n{json.dumps(issue, indent=2, ensure_ascii=False)}"
            )

    return data


# ----------------------------
# CREATE GITHUB ISSUE
# ----------------------------

def create_github_issue(
    owner: str,
    repo: str,
    token: str,
    title: str,
    body: str,
) -> str:

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload = {
        "title": title,
        "body": body,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code >= 300:
        raise RuntimeError(
            f"Erro ao criar issue no GitHub ({response.status_code}): {response.text}"
        )

    return response.json()["html_url"]


# ----------------------------
# PRINT PLAN
# ----------------------------

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


# ----------------------------
# MAIN
# ----------------------------

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

    plan = generate_plan(client, user_prompt)

    print_plan(plan)

    confirm = input("\nQueres criar estas issues no GitHub? (s/n): ").strip().lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    print("\nA criar issues no GitHub...")

    created_urls: List[str] = []

    formatted_body = build_issue_body(issue)

    for issue in plan["issues"]:
        url = create_github_issue(
            owner=github_owner,
            repo=github_repo,
            token=github_token,
            title=issue["title"],
            body=formatted_body,
        )

        created_urls.append(url)

    print("\n=== ISSUES CRIADAS ===")

    for url in created_urls:
        print(url)

    print("\nConcluído.")


if __name__ == "__main__":
    main()