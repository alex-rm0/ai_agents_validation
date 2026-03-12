import os
import re
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


def build_frontend_prompt(issue: Dict[str, Any]) -> str:
    title = issue.get("title", "").strip()
    body = issue.get("body", "").strip()
    labels = ", ".join(issue.get("labels", []))
    acceptance_criteria = issue.get("acceptance_criteria", [])

    criteria_text = "\n".join(
        f"- {criterion}" for criterion in acceptance_criteria
    ) if acceptance_criteria else "- Sem critérios de aceitação adicionais"

    prompt = f"""
És um Frontend Generator Agent.

Recebes uma issue de frontend já validada e deves gerar um único componente React em TypeScript (TSX), simples, funcional e bem estruturado.

Objetivo:
- implementar apenas o que é pedido na issue
- não inventar backend, base de dados, API, autenticação real ou integrações externas
- não usar bibliotecas externas além de React
- gerar apenas um componente TSX
- o componente deve ser autocontido
- usar estado local apenas se necessário
- respeitar os critérios de aceitação
- o código deve estar limpo e legível
- devolver apenas código TSX
- não usar markdown
- não escrever explicações fora do código
- não incluir múltiplos componentes exportados no mesmo ficheiro
- não duplicar imports
- não criar imports locais para ficheiros que não existam

Issue:
Título: {title}
Descrição: {body}
Labels: {labels}

Critérios de aceitação:
{criteria_text}
"""
    return prompt.strip()


def extract_code(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = (
            text.replace("```tsx", "")
            .replace("```typescript", "")
            .replace("```jsx", "")
            .replace("```ts", "")
            .replace("```", "")
            .strip()
        )

    return text


def sanitize_generated_code(code: str) -> str:
    lines = code.splitlines()

    cleaned_lines = []
    seen_imports = set()
    export_default_found = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("import "):
            if stripped in seen_imports:
                continue
            seen_imports.add(stripped)
            cleaned_lines.append(line)
            continue

        if stripped.startswith("export default "):
            if export_default_found:
                break
            export_default_found = True
            cleaned_lines.append(line)
            continue

        cleaned_lines.append(line)

    cleaned_code = "\n".join(cleaned_lines).strip()

    local_import_pattern = re.compile(
        r"""^\s*import\s+.+?\s+from\s+['"]\./.+?['"];?\s*$""",
        re.MULTILINE,
    )
    cleaned_code = re.sub(local_import_pattern, "", cleaned_code).strip()

    react_imports = re.findall(
        r"""^\s*import\s+React(?:\s*,\s*\{[^}]+\})?\s+from\s+['"]react['"];?\s*$""",
        cleaned_code,
        re.MULTILINE,
    )

    if len(react_imports) > 1:
        cleaned_code = re.sub(
            r"""^\s*import\s+React(?:\s*,\s*\{[^}]+\})?\s+from\s+['"]react['"];?\s*$""",
            "",
            cleaned_code,
            flags=re.MULTILINE,
        ).strip()

        if "useState" in cleaned_code:
            cleaned_code = f'import React, {{ useState }} from "react";\n\n{cleaned_code}'
        else:
            cleaned_code = f'import React from "react";\n\n{cleaned_code}'

    elif len(react_imports) == 0:
        if "useState" in cleaned_code:
            cleaned_code = f'import React, {{ useState }} from "react";\n\n{cleaned_code}'
        else:
            cleaned_code = f'import React from "react";\n\n{cleaned_code}'

    cleaned_code = re.sub(r"\n{3,}", "\n\n", cleaned_code).strip()

    return cleaned_code


def generate_frontend_component(issue: Dict[str, Any]) -> Dict[str, str]:
    prompt = build_frontend_prompt(issue)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "És um agente especializado em gerar componentes frontend React em TypeScript.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    raw_response = response.choices[0].message.content

    if not raw_response or not raw_response.strip():
        raise RuntimeError("O modelo devolveu uma resposta vazia na geração de frontend.")

    extracted_code = extract_code(raw_response)
    code = sanitize_generated_code(extracted_code)

    if not code.strip():
        raise RuntimeError("Não foi possível extrair código TSX da resposta do modelo.")

    return {
        "prompt": prompt,
        "raw_response": raw_response,
        "code": code,
    }