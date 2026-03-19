# test_engine (motor genérico de testes funcionais)

Este diretório contém um **motor reutilizável** de testes funcionais em **.NET 8** usando:

- Playwright
- Reqnroll (Gherkin)
- NUnit

O objetivo é **receber ficheiros `.feature` gerados automaticamente** (por exemplo por agentes de IA) e executá-los de forma consistente, sem depender de um domínio/projeto específico.

## Como correr (Replit)

Usa sempre o script de execução incluído, que configura automaticamente o ambiente:

```bash
bash test_engine/run_tests.sh
```

Para filtrar um cenário específico:

```bash
bash test_engine/run_tests.sh --filter "Name=UserLogsInWithValidCredentials"
```

O script:
- Configura o `LD_LIBRARY_PATH` necessário para o Chromium correr em ambiente Nix
- Executa `dotnet test` com os argumentos passados

## Primeira instalação

Antes de correr testes pela primeira vez é necessário instalar os binários do browser:

```bash
cd test_engine
dotnet build
pwsh bin/Debug/net8.0/playwright.ps1 install chromium
```

## Configuração

A configuração está centralizada em `appsettings.json` e pode ser sobreposta por variáveis de ambiente:

| Variável de ambiente | Chave JSON   | Descrição                              |
|----------------------|--------------|----------------------------------------|
| `BASE_URL`           | `BaseUrl`    | URL base da aplicação sob teste        |
| `HEADLESS`           | `Headless`   | `true`/`false` (padrão: `true`)        |
| `LOGIN_PATH`         | `LoginPath`  | Caminho da página de login             |
| `TEST_USER`          | `TestUser`   | Username para testes de autenticação   |
| `TEST_PASSWORD`      | `TestPassword` | Password para testes de autenticação |

Exemplo via variáveis de ambiente:

```bash
BASE_URL=https://minha-app.exemplo.com bash test_engine/run_tests.sh
```

## Selectores esperados na aplicação

O `LoginPage.cs` usa atributos `data-cy` para localizar elementos (padrão Cypress):

- Email: `input[data-cy='email']`
- Password: `input[data-cy='password']`
- Botão de login: `text=Iniciar Sessão`

Estes atributos têm de existir no HTML da aplicação sob teste. Se a app usar outros selectores, actualiza `Pages/LoginPage.cs` em conformidade.

## Estrutura

```
test_engine/
  Features/            # Ficheiros .feature (Gherkin)
    generated/         # Gerados automaticamente pelo pipeline de agentes
  StepDefinitions/     # Step definitions reutilizáveis
  Pages/               # Page Objects (padrão POM)
  Hooks/               # Setup/teardown de Playwright e DI
  Config/              # Configuração do motor
  Helpers/             # Auxiliares (manter mínimo)
  TestData/            # Modelos de dados de teste
  run_tests.sh         # Script de execução (usar sempre este)
  NuGet.Config         # Fonte de pacotes NuGet
  appsettings.json     # Configuração padrão
```

## Integração com o pipeline de agentes

O fluxo previsto é:

```
PM Agent gera issues
  → acceptance_criteria
  → Agent Testes gera ficheiros .feature
  → copiar para test_engine/Features/generated/
  → bash test_engine/run_tests.sh
```
