import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "meta-llama/llama-3.1-8b-instruct"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)


def generate_plan(user_prompt: str) -> Dict[str, Any]:
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