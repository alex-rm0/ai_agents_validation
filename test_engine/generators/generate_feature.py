#!/usr/bin/env python3
"""
Test Generator — Gerador de ficheiros .feature
===============================================
Converte acceptance criteria em texto (ou ficheiro) num ficheiro Gherkin
(.feature) pronto a correr com o test_engine.

Usa OpenRouter (Llama 3.1 8b por defeito) para gerar os cenários.
O LLM é restringido ao vocabulário controlado definido em docs/step-vocabulary.md.

Uso:
    # A partir de texto directo:
    python3 test_engine/generators/generate_feature.py \\
        --criteria "O utilizador deve conseguir fazer login com email e password válidos" \\
        --name "Login"

    # A partir de ficheiro:
    python3 test_engine/generators/generate_feature.py \\
        --file criterios.txt \\
        --name "Login"

    # Especificar output diferente:
    python3 test_engine/generators/generate_feature.py \\
        --criteria "..." \\
        --name "Checkout" \\
        --output test_engine/Features/generated/Checkout.feature

Variáveis de ambiente:
    OPENROUTER_API_KEY   Obrigatória. Chave da API OpenRouter.
    OPENROUTER_MODEL     Opcional. Modelo a usar (default: meta-llama/llama-3.1-8b-instruct)

Requisitos:
    pip install -r test_engine/generators/requirements.txt
"""

import argparse
import os
import sys
from pathlib import Path


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct"

# Vocabulário genérico de steps disponíveis no test_engine (GenericStepDefinitions).
# Este bloco é injetado directamente no system prompt do LLM.
# NÃO inclui steps legados (a user is on the login page, etc.) — usa apenas o vocabulário genérico.
STEP_VOCABULARY = """
## Steps disponíveis — vocabulário genérico controlado (GenericStepDefinitions)

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
- "And" pode substituir qualquer keyword (Given/When/Then) para melhor legibilidade.
- "Background:" pode conter steps Given comuns a todos os cenários.
- Parâmetros entre aspas duplas (<field>, <value>, etc.) são obrigatórios tal como mostrado.
- N em "waits <N> seconds" é um inteiro positivo sem aspas.
- <route> pode ser relativa ("login", "#/dashboard") ou URL absoluta.
- <field> e <element> identificam elementos por: placeholder, label, texto visível, data-testid, data-cy, ou CSS selector.
"""

SYSTEM_PROMPT = f"""
És um engenheiro de QA especialista em Behaviour-Driven Development (BDD) e Gherkin.

Recebes acceptance criteria de uma funcionalidade de software e deves gerar um ficheiro .feature Gherkin válido.

REGRA CRÍTICA — VOCABULÁRIO CONTROLADO:
Usa EXCLUSIVAMENTE os steps da lista abaixo. Nunca inventes steps novos.
Se um critério de aceitação não puder ser coberto pelos steps disponíveis, approxima ao step mais próximo.
O motor de testes só reconhece estes steps — qualquer step fora da lista causará falha na execução.

{STEP_VOCABULARY}

REGRAS DE FORMATO:
- Escreve APENAS o conteúdo do ficheiro .feature, sem texto antes ou depois
- Começa com: Feature: <nome da funcionalidade>
- Inclui 2-3 linhas de descrição após o Feature (Como/Quero/Para — em português)
- Cria entre 1 e 4 cenários (Scenario ou Scenario Outline)
- Cada cenário deve cobrir um critério de aceitação distinto
- Usa Background: para steps Given comuns a todos os cenários (se aplicável)
- A linguagem dos valores dos parâmetros pode ser Português (ex: "Iniciar Sessão")
- A linguagem dos keywords Gherkin é sempre Inglês (Feature, Scenario, Given, When, Then, And, But)
- Não uses markdown, blocos de código, ou qualquer formatação extra
- Não escreves texto fora do .feature

EXEMPLO DE OUTPUT CORRECTO (para um critério de login):

Feature: Login de Utilizador
  Como utilizador registado
  Quero poder autenticar-me na aplicação
  Para aceder às funcionalidades protegidas

  Background:
    Given the application base url is configured

  Scenario: Login com credenciais válidas
    Given the user navigates to "login"
    When the user fills "Username" with "sandrodev"
    And the user fills "Password" with "Sandrodev-123"
    And the user clicks "Iniciar Sessão"
    Then the url should contain "dashboard"
    And the user should see "Dashboard"

  Scenario: Login com password incorrecta
    Given the user navigates to "login"
    When the user fills "Username" with "sandrodev"
    And the user fills "Password" with "wrong-password"
    And the user clicks "Iniciar Sessão"
    Then the user should see "credenciais inválidas"
"""


def load_api_key() -> str:
    try:
        from dotenv import load_dotenv
        env_file = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(dotenv_path=env_file, override=False)
    except ImportError:
        pass

    key = os.environ.get("OPENROUTER_API_KEY", "").strip()

    if not key:
        print("Erro: OPENROUTER_API_KEY não definida.")
        print("Define a variável de ambiente ou cria um ficheiro .env na raiz do projecto.")
        sys.exit(1)

    return key


def generate(criteria: str, feature_name: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        print("Erro: openai não está instalado.")
        print("Corre: pip install -r test_engine/generators/requirements.txt")
        sys.exit(1)

    api_key = load_api_key()
    model = os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)

    client = OpenAI(api_key=api_key, base_url=OPENROUTER_BASE_URL)

    user_message = (
        f"Feature: {feature_name}\n\n"
        f"Acceptance Criteria:\n{criteria.strip()}\n\n"
        f"Gera o ficheiro .feature usando EXCLUSIVAMENTE os steps do vocabulário controlado fornecido."
    )

    print(f"A gerar .feature para: {feature_name}")
    print(f"Modelo: {model}")
    print()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content or ""
    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()
        lines = [l for l in lines if not l.strip().startswith("```")]
        content = "\n".join(lines).strip()

    return content


def save_feature(content: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content + "\n", encoding="utf-8")
    print(f"Ficheiro gerado: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera um ficheiro .feature Gherkin a partir de acceptance criteria."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--criteria",
        help="Acceptance criteria em texto directo.",
    )
    group.add_argument(
        "--file",
        help="Caminho para ficheiro de texto com acceptance criteria.",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Nome da funcionalidade (ex: Login, Checkout, RegistoUtilizador).",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Caminho de output (default: test_engine/Features/generated/<name>.feature).",
    )

    args = parser.parse_args()

    if args.file:
        criteria_path = Path(args.file)
        if not criteria_path.exists():
            print(f"Erro: ficheiro não encontrado: {args.file}")
            sys.exit(1)
        criteria = criteria_path.read_text(encoding="utf-8")
    else:
        criteria = args.criteria

    output_path = (
        Path(args.output)
        if args.output
        else Path(__file__).parent.parent / "Features" / "generated" / f"{args.name}.feature"
    )

    content = generate(criteria=criteria, feature_name=args.name)

    if not content.startswith("Feature:"):
        print("Aviso: o modelo não devolveu um .feature válido. Output:")
        print(content)
        sys.exit(1)

    save_feature(content, output_path)

    print()
    print("--- Conteúdo gerado ---")
    print(content)


if __name__ == "__main__":
    main()
