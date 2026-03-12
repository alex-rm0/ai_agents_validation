import requests
from typing import Dict, Any, List


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


def create_github_issue(
    owner: str,
    repo: str,
    token: str,
    title: str,
    body: str,
    labels: List[str] | None = None,
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

    if labels:
        payload["labels"] = labels

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code >= 300:
        raise RuntimeError(
            f"Erro ao criar issue no GitHub ({response.status_code}): {response.text}"
        )

    return response.json()["html_url"]