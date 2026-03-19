# test_engine — Motor de Testes Funcionais

Motor de testes funcionais em **.NET 8** com:

- **Playwright** — automação de browser
- **Reqnroll** — testes BDD em sintaxe Gherkin
- **NUnit** — runner de testes

Desenhado para ser **portátil e auto-suficiente**: podes copiar esta pasta para qualquer projecto e estar a correr testes em minutos, sem modificar código C#.

---

## Usar este motor num projecto novo (passo a passo)

```
1. Copia a pasta test_engine/ para o teu projecto

2. Corre o script de descoberta de selectores:
   python3 test_engine/tools/discover_selectors.py --url https://tua-app.com --login-path "#/login"

3. Copia os selectores sugeridos para appsettings.json

4. Preenche o resto do appsettings.json (credenciais, URL base)

5. Gera os ficheiros .feature a partir dos teus acceptance criteria:
   python3 test_engine/generators/generate_feature.py --criteria "..." --name "Login"

6. Corre os testes:
   cd test_engine && dotnet test
```

---

## Como correr

**Localmente** (abre o browser para ver o teste a executar):

```bash
cd test_engine
dotnet test
```

**No Replit / servidor** (headless automático, sem janela):

```bash
bash test_engine/run_tests.sh
```

Filtrar um cenário específico:

```bash
bash test_engine/run_tests.sh --filter "Name=UserLogsInWithValidCredentials"
```

---

## Primeira instalação

Só é necessário fazer uma vez após clonar o repositório:

```bash
cd test_engine
dotnet build
pwsh bin/Debug/net8.0/playwright.ps1 install chromium
```

---

## Configuração

Toda a configuração está em `appsettings.json`. Pode ser sobreposta por variáveis de ambiente:

| Variável de ambiente    | Chave JSON            | Descrição                                         |
|-------------------------|-----------------------|---------------------------------------------------|
| `BASE_URL`              | `BaseUrl`             | URL base da aplicação sob teste                   |
| `HEADLESS`              | `Headless`            | `true` = sem janela / `false` = browser visível   |
| `LOGIN_PATH`            | `LoginPath`           | Caminho da página de login (ex: `#/login`)        |
| `TEST_USER`             | `TestUser`            | Username para testes de autenticação              |
| `TEST_PASSWORD`         | `TestPassword`        | Password para testes de autenticação              |
| `USERNAME_SELECTOR`     | `UsernameSelector`    | Selector do campo de username/email               |
| `PASSWORD_SELECTOR`     | `PasswordSelector`    | Selector do campo de password                     |
| `LOGIN_BUTTON_SELECTOR` | `LoginButtonSelector` | Selector do botão de login                        |

Exemplo — apontar para outro ambiente sem alterar o ficheiro:

```bash
BASE_URL=https://staging.exemplo.com bash test_engine/run_tests.sh
```

---

## Tools incluídos

### 1. Descoberta de selectores (`tools/discover_selectors.py`)

Inspeciona automaticamente a página de login de qualquer app e sugere os selectores a usar:

```bash
# Instalar dependências (só uma vez):
pip install -r test_engine/tools/requirements.txt

# Correr (lê BaseUrl e LoginPath do appsettings.json por defeito):
python3 test_engine/tools/discover_selectors.py

# Apontar para outro URL:
python3 test_engine/tools/discover_selectors.py --url https://outra-app.com --login-path "#/login"

# Ver o browser a trabalhar:
python3 test_engine/tools/discover_selectors.py --no-headless
```

Output exemplo:
```json
{
  "UsernameSelector": "input[type='text']",
  "PasswordSelector": "input[type='password']",
  "LoginButtonSelector": "text=Iniciar Sessão"
}
```

Copia estes valores para o `appsettings.json`.

> **Nota Replit/NixOS:** define `PLAYWRIGHT_BROWSERS_PATH` para reutilizar os browsers já instalados:
> ```bash
> PLAYWRIGHT_BROWSERS_PATH=/home/runner/workspace/.cache/ms-playwright python3 test_engine/tools/discover_selectors.py
> ```

### 2. Gerador de .feature (`generators/generate_feature.py`)

Converte acceptance criteria em texto num ficheiro `.feature` Gherkin pronto a correr:

```bash
# Instalar dependências (só uma vez):
pip install -r test_engine/generators/requirements.txt

# A partir de texto directo:
python3 test_engine/generators/generate_feature.py \
  --criteria "O utilizador deve conseguir fazer login com credenciais válidas" \
  --name "Login"

# A partir de ficheiro de texto:
python3 test_engine/generators/generate_feature.py \
  --file meus_criterios.txt \
  --name "Checkout"

# Especificar output:
python3 test_engine/generators/generate_feature.py \
  --criteria "..." \
  --name "Registo" \
  --output test_engine/Features/generated/Registo.feature
```

O ficheiro é gerado em `test_engine/Features/generated/` e fica pronto a correr com `dotnet test`.

**Variáveis de ambiente necessárias:**

| Variável            | Descrição                                      |
|---------------------|------------------------------------------------|
| `OPENROUTER_API_KEY` | Chave OpenRouter (obrigatória)                |
| `OPENROUTER_MODEL`   | Modelo a usar (default: llama-3.1-8b-instruct)|

---

## Estrutura

```
test_engine/
├── Features/                     # Cenários Gherkin
│   ├── Login.feature             # Cenário de autenticação (exemplo)
│   ├── Navigation.feature        # Cenário de navegação (exemplo)
│   └── generated/                # Gerados por generate_feature.py
├── StepDefinitions/              # Implementação dos steps Gherkin
│   ├── LoginStepDefinitions.cs
│   └── NavigationStepDefinitions.cs
├── Pages/                        # Page Objects (padrão POM)
│   ├── BasePage.cs               # Classe base com navegação
│   ├── LoginPage.cs              # Login (selectores via config)
│   └── SimplePage.cs             # Páginas genéricas
├── Hooks/
│   └── CommonHooks.cs            # Setup/teardown do browser
├── Config/
│   └── TestConfig.cs             # Leitura de appsettings.json + env vars
├── Helpers/
│   └── ConfigurationHelper.cs   # Helpers de acesso à configuração
├── TestData/
│   └── GenericUser.cs            # Modelo de dados de utilizador
├── tools/
│   ├── discover_selectors.py     # Descobre selectores de qualquer app
│   └── requirements.txt          # playwright
├── generators/
│   ├── generate_feature.py       # Gera .feature a partir de acceptance criteria
│   └── requirements.txt          # openai, python-dotenv
├── appsettings.json              # Configuração (editar para cada projecto)
├── run_tests.sh                  # Script de execução Replit/servidor
├── NuGet.Config                  # Fonte de pacotes NuGet
├── GlobalUsings.cs               # Using directives globais
└── FunctionalTests.csproj        # Projecto .NET
```

---

## Integração com pipeline de agentes

```
PM Agent gera issues com acceptance_criteria
  → generate_feature.py converte em ficheiros .feature
  → ficheiros vão para Features/generated/
  → bash test_engine/run_tests.sh
```

Os ficheiros em `Features/generated/` são gerados dinamicamente e não são versionados (apenas o `.gitkeep` é mantido no git).
