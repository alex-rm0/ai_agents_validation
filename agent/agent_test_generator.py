import os
import re
from typing import Dict, Any, List

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

STEP_VOCABULARY = """
## Vocabulário controlado — ÚNICOS steps permitidos

### Given (pré-condições)
Given the user navigates to "<route>"
Given the user is logged in

### When (acções)
When the user fills "<field>" with "<value>"
When the user clears "<field>"
When the user clicks "<element>"
When the user submits the form
When the user waits <N> seconds

### Then (verificações)
Then the user should see "<text>"
Then the user should not see "<text>"
Then the url should contain "<fragment>"
Then the url should be "<url>"
Then the element "<selector>" should be visible
Then the element "<selector>" should not be visible
Then the field "<field>" should contain "<value>"
Then the page title should be "<title>"

### Notas de sintaxe
- "And" pode substituir qualquer keyword (Given/When/Then)
- <route>: rota relativa ("login", "#/dashboard") ou URL absoluta
- <field> e <element>: identificados por placeholder, label, texto visível, data-testid, data-cy, ou CSS selector
- <N> em "waits <N> seconds": inteiro positivo, SEM aspas
- Parâmetros em "<...>": SEMPRE entre aspas duplas no .feature
"""

SYSTEM_PROMPT = f"""
És um QA Test Generator Agent especialista em BDD e Gherkin.

Recebes um pedido de produto, a lista de requisitos, e as issues com acceptance criteria.
Para cada issue, gera um ficheiro .feature Gherkin usando EXCLUSIVAMENTE o vocabulário abaixo.
Nunca inventes steps que não estejam nessa lista.

{STEP_VOCABULARY}

FORMATO DE OUTPUT OBRIGATÓRIO:
Para cada issue, produz um bloco exactamente assim (substitui os campos entre <> pelos valores reais):

--- BEGIN: <NomeFeature.feature> | Issue: <título da issue> ---
Feature: <Nome da Funcionalidade em Português>
  <Como|Quero|Para — descrição em português>

  Scenario: <nome do cenário>
    <steps usando APENAS o vocabulário acima>

--- END ---

Regras:
- Gera 1 a 3 cenários por feature
- Cada cenário cobre um acceptance criterion distinto
- O nome do ficheiro usa PascalCase sem espaços (ex: LoginUtilizador.feature)
- Feature name e descriptions em Português de Portugal
- Keywords Gherkin em Inglês (Feature, Scenario, Given, When, Then, And, But)
- Não escrevas nada fora dos blocos --- BEGIN --- / --- END ---
- Não uses markdown, blocos de código, ou formatação extra
""".strip()


def _build_issues_text(issues: List[Dict[str, Any]]) -> str:
    lines = []
    for i, issue in enumerate(issues, start=1):
        title = issue.get("title", "").strip()
        body = issue.get("body", "").strip()
        criteria = issue.get("acceptance_criteria", [])

        lines.append(f"Issue {i}: {title}")
        lines.append(f"  Descrição: {body}")

        if criteria:
            lines.append("  Acceptance Criteria:")
            for criterion in criteria:
                lines.append(f"    - {criterion}")

        lines.append("")

    return "\n".join(lines)


def build_test_prompt(
    user_prompt: str,
    requirements: List[str],
    issues: List[Dict[str, Any]],
) -> str:
    req_text = "\n".join(f"- {r}" for r in requirements)
    issues_text = _build_issues_text(issues)

    return f"""Pedido de produto:
{user_prompt.strip()}

Requisitos:
{req_text}

Issues com acceptance criteria:
{issues_text}

Gera um ficheiro .feature para cada issue, usando EXCLUSIVAMENTE o vocabulário controlado do system prompt."""


def _parse_features(raw: str) -> List[Dict[str, str]]:
    pattern = re.compile(
        r"---\s*BEGIN:\s*(.+?)\s*\|\s*Issue:\s*(.+?)\s*---\n(.*?)---\s*END\s*---",
        re.DOTALL,
    )

    features = []
    for match in pattern.finditer(raw):
        filename = match.group(1).strip()
        issue_ref = match.group(2).strip()
        content = match.group(3).strip()

        if not filename.endswith(".feature"):
            filename += ".feature"

        if content.startswith("Feature:"):
            features.append({
                "filename": filename,
                "issue_ref": issue_ref,
                "content": content,
            })

    return features


def generate_functional_tests(
    user_prompt: str,
    requirements: List[str],
    issues: List[Dict[str, Any]],
) -> Dict[str, Any]:
    prompt = build_test_prompt(user_prompt, requirements, issues)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content or ""

    if not raw.strip():
        raise RuntimeError("O modelo devolveu uma resposta vazia na geração de testes.")

    features = _parse_features(raw)

    if not features:
        raise RuntimeError(
            "Não foi possível extrair nenhum bloco .feature da resposta do modelo.\n"
            f"Resposta recebida:\n{raw[:500]}"
        )

    manifest = {
        "total": len(features),
        "features": [
            {"filename": f["filename"], "issue_ref": f["issue_ref"]}
            for f in features
        ],
        "instructions": (
            "Copia os ficheiros .feature para test_engine/Features/generated/ "
            "e executa: bash test_engine/run_tests.sh"
        ),
    }

    return {"features": features, "manifest": manifest}
