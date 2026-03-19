# test_engine — Motor de Testes Funcionais

Motor de testes funcionais em **.NET 8** com:

- **Playwright** — automação de browser
- **Reqnroll** — testes BDD em sintaxe Gherkin
- **NUnit** — runner de testes

O objectivo é receber ficheiros `.feature` (gerados pelo Test Generator Agent) e executá-los de forma consistente contra qualquer ambiente.

---

## Como correr

**No Replit** (headless automático, sem janela):

```bash
bash test_engine/run_tests.sh
```

**Localmente** (abre o browser para ver o teste a executar):

```bash
cd test_engine
dotnet test
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

Centralizada em `appsettings.json`. Pode ser sobreposta por variáveis de ambiente:

| Variável de ambiente | Chave JSON     | Descrição                                         |
|----------------------|----------------|---------------------------------------------------|
| `BASE_URL`           | `BaseUrl`      | URL base da aplicação sob teste                   |
| `HEADLESS`           | `Headless`     | `true` = sem janela / `false` = browser visível   |
| `LOGIN_PATH`         | `LoginPath`    | Caminho da página de login (ex: `#/login`)        |
| `TEST_USER`          | `TestUser`     | Username para testes de autenticação              |
| `TEST_PASSWORD`      | `TestPassword` | Password para testes de autenticação              |

Exemplo — apontar para outro ambiente:

```bash
BASE_URL=https://staging.exemplo.com bash test_engine/run_tests.sh
```

O `run_tests.sh` força `HEADLESS=true` para o ambiente Replit. Localmente o valor de `appsettings.json` é usado (`false` por defeito — browser abre).

---

## Estrutura

```
test_engine/
├── Features/                   # Cenários Gherkin
│   ├── Login.feature           # Cenário de autenticação
│   ├── Navigation.feature      # Cenário de navegação básica
│   └── generated/              # Gerados pelo Test Generator Agent (pipeline)
├── StepDefinitions/            # Implementação dos steps Gherkin
│   ├── LoginStepDefinitions.cs
│   └── NavigationStepDefinitions.cs
├── Pages/                      # Page Objects (padrão POM)
│   ├── BasePage.cs             # Classe base com navegação e helpers
│   ├── LoginPage.cs            # Login: preencher form, verificar autenticação
│   └── SimplePage.cs           # Páginas genéricas (verificar URL, título)
├── Hooks/
│   └── CommonHooks.cs          # Setup/teardown do browser e injecção de dependências
├── Config/
│   └── TestConfig.cs           # Leitura de appsettings.json + env vars
├── Helpers/
│   └── ConfigurationHelper.cs  # Helpers de acesso à configuração
├── TestData/
│   └── GenericUser.cs          # Modelo de dados de utilizador de teste
├── appsettings.json            # Configuração padrão
├── run_tests.sh                # Script de execução (usar no Replit)
├── NuGet.Config                # Fonte de pacotes NuGet
├── GlobalUsings.cs             # Using directives globais
└── FunctionalTests.csproj      # Projecto .NET
```

---

## Selectores usados

O `LoginPage.cs` usa selectores baseados nos atributos HTML reais da aplicação em teste (`https://dev.nexus.shipperform.devlop.systems`):

| Campo          | Selector                  |
|----------------|---------------------------|
| Email          | `input[type='text']`      |
| Password       | `input[type='password']`  |
| Botão de login | `text=Iniciar Sessão`     |

Se a aplicação sob teste mudar ou for diferente, actualiza `Pages/LoginPage.cs`.

---

## Integração com o pipeline de agentes

```
PM Agent gera issues com acceptance_criteria
  → Test Generator Agent converte em ficheiros .feature
  → coloca em Features/generated/
  → bash test_engine/run_tests.sh
```

Os ficheiros em `Features/generated/` são ignorados pelo git (apenas o `.gitkeep` é versionado).
