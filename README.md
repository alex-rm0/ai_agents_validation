# Fluxo de Agentes IA — Validação

Prova de conceito de um pipeline multi-agente capaz de percorrer um ciclo completo de desenvolvimento de software: da interpretação de um requisito de produto até ao produto final testado e documentado.

## Visão geral do pipeline

```
Pedido de produto (texto livre)
  │
  ▼
[PM Agent]  ──────────── interpreta requisitos, decompõe em issues com acceptance criteria
  │
  ▼
[GitHub Agent]  ────────── cria issues no repositório GitHub
  │
  ▼
[Frontend Generator]  ───── gera componentes React TSX a partir de cada issue
  │
  ▼
[Test Generator Agent]  ──── converte acceptance criteria em ficheiros .feature (Gherkin)  ← a construir
  │
  ▼
[Test Engine]  ─────────── corre testes BDD funcionais (Playwright + Reqnroll + NUnit)
```

## Estrutura do repositório

```
/
├── main.py                   # Orquestrador do pipeline de agentes
├── requirements.txt          # Dependências Python
│
├── agents/                   # Agentes de IA (Python + OpenRouter / Llama 3.1)
│   ├── agent_planner.py      # PM Agent: interpreta requisitos e gera issues
│   ├── agent_validator.py    # Valida o plano antes de avançar
│   ├── agent_github.py       # Cria issues no GitHub via API
│   ├── agent_frontend_generator.py  # Gera componentes React TSX
│   ├── agent_outputs.py      # Gestão de outputs (ficheiros, pastas de run)
│   └── utils.py              # Utilitários partilhados
│
├── frontend_preview/         # App React/Vite para pré-visualizar componentes gerados
│   └── src/
│       └── generated/        # Componentes TSX gerados pelo pipeline (auto-populado)
│
├── test_engine/              # Motor de testes funcionais (.NET 8)
│   ├── Features/             # Cenários Gherkin (.feature)
│   │   └── generated/        # Gerados automaticamente pelo Test Generator Agent
│   ├── StepDefinitions/      # Implementação dos steps Gherkin
│   ├── Pages/                # Page Objects (padrão POM)
│   ├── Hooks/                # Setup/teardown do Playwright
│   ├── Config/               # Configuração do motor
│   ├── Helpers/              # Utilitários de teste
│   ├── TestData/             # Modelos de dados de teste
│   ├── appsettings.json      # Configuração (URL, credenciais, headless)
│   └── run_tests.sh          # Script de execução (usar sempre este no Replit)
│
└── docs/                     # Notas e decisões de design
    └── notas.md
```

> **Nota:** a pasta `agent/` no código-fonte chama-se `agent/` (não `agents/`) — os imports Python usam esse nome.

## Como correr

### Pipeline de agentes

```bash
pip install -r requirements.txt
python main.py
```

Variáveis de ambiente necessárias:

| Variável           | Descrição                          |
|--------------------|------------------------------------|
| `OPENROUTER_API_KEY` | Chave OpenRouter (Llama 3.1 8b)  |
| `GITHUB_TOKEN`     | Token de acesso ao GitHub          |
| `GITHUB_OWNER`     | Username ou organização no GitHub  |
| `GITHUB_REPO`      | Nome do repositório GitHub         |

### Testes funcionais

```bash
# No Replit (headless automático):
bash test_engine/run_tests.sh

# Localmente (abre o browser para poderes ver):
cd test_engine && dotnet test
```

Configuração dos testes em `test_engine/appsettings.json`.  
Ver `test_engine/README.md` para mais detalhes.

## Estado actual

| Componente           | Estado       |
|----------------------|--------------|
| PM Agent             | ✅ Funcional |
| GitHub Agent         | ✅ Funcional |
| Frontend Generator   | ✅ Funcional |
| Test Engine          | ✅ Funcional |
| Test Generator Agent | 🔧 A construir |
