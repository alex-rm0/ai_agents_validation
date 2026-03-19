# test_engine (motor genérico de testes funcionais)

Este diretório contém um **motor reutilizável** de testes funcionais em **.NET 8** usando:

- Playwright
- Reqnroll (Gherkin)
- NUnit

O objetivo é **receber ficheiros `.feature` gerados automaticamente** (por exemplo por agentes de IA) e executá-los de forma consistente, sem depender de um domínio/projeto específico.

## Como corre

Na raiz de `test_engine/`:

```bash
dotnet build
dotnet test
```

## Configuração (sem URLs hardcoded)

A configuração está centralizada em `Config/TestConfig.cs` e lê por ordem:

- variáveis de ambiente
- `appsettings.json`

Variáveis suportadas:

- `BASE_URL`: URL base da aplicação sob teste (ex.: `https://localhost:5173`)
- `HEADLESS`: `true`/`false`

Por defeito, `appsettings.json` usa `about:blank` para permitir que o projeto execute em modo “standalone”.

## Estrutura

- `Features/`: ficheiros `.feature` (inclui `generated/` para conteúdos sincronizados a partir de `outputs/*`)
- `StepDefinitions/`: step definitions genéricos reutilizáveis
- `Pages/`: page objects (padrão POM)
- `Hooks/`: setup/teardown de Playwright e DI do Reqnroll
- `Config/`: configuração do motor (env + json)
- `TestData/`: modelos simples de dados de teste
- `Helpers/`: compatibilidade/auxiliares (manter mínimo)

## Integração com o pipeline de agentes

O fluxo previsto é:

`outputs/<timestamp>/tests/test_spec.json` → geração de `.feature` → copiar para `test_engine/Features/generated/` → `dotnet test`
