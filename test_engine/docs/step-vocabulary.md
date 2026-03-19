# Vocabulário de Steps — test_engine

Este ficheiro define o vocabulário **completo e fixo** de step definitions disponíveis no `test_engine`.

Qualquer `.feature` colocado em `Features/generated/` que use **exclusivamente** estes steps
corre sem necessidade de implementação C# adicional.

> **Nota para o LLM:** Usa **apenas** os steps desta lista. Não inventes steps novos.
> Sintaxe: as aspas `"` à volta de parâmetros são obrigatórias tal como mostrado.

---

## Contexto de base (pre-existentes)

Estes steps já existem em `NavigationStepDefinitions.cs` e `LoginStepDefinitions.cs`:

```gherkin
Given the application base url is configured
Given a user is on the login page
When the user logs in with valid credentials
Then the user should be authenticated
When I navigate to the home page
Then the browser should be at the base url
```

---

## Steps Genéricos (GenericStepDefinitions.cs)

### Given — Pré-condições

```gherkin
Given the user navigates to "<route>"
```
- Navega para uma rota relativa à BASE_URL.
- `<route>` pode ser: `"login"`, `"dashboard"`, `"#/settings"`, `"/"`, ou URL absoluta.
- **Exemplos:**
  ```gherkin
  Given the user navigates to "login"
  Given the user navigates to "admin/users"
  Given the user navigates to "#/dashboard"
  ```

```gherkin
Given the user is logged in
```
- Realiza o login com as credenciais configuradas no `appsettings.json` (TestUser / TestPassword).
- Navega para LoginPath, preenche os campos e aguarda o redireccionamento.
- **Exemplo:**
  ```gherkin
  Given the user is logged in
  ```

---

### When — Acções do utilizador

```gherkin
When the user fills "<field>" with "<value>"
```
- Preenche um campo de formulário com um valor.
- `<field>` pode ser: texto da label, placeholder, valor de `data-testid`, valor de `data-cy`, ou CSS selector.
- **Exemplos:**
  ```gherkin
  When the user fills "Username" with "sandrodev"
  When the user fills "Password" with "Sandrodev-123"
  When the user fills "Email" with "teste@exemplo.pt"
  When the user fills "input[name='search']" with "consulta"
  ```

```gherkin
When the user clears "<field>"
```
- Limpa o conteúdo de um campo de formulário.
- `<field>`: mesmo critério que `fills`.
- **Exemplo:**
  ```gherkin
  When the user clears "Search"
  ```

```gherkin
When the user clicks "<element>"
```
- Clica num elemento (botão, link, checkbox, tab, etc.).
- `<element>` pode ser: texto do botão/link, valor de `data-testid`, valor de `data-cy`, ou CSS selector.
- **Exemplos:**
  ```gherkin
  When the user clicks "Iniciar Sessão"
  When the user clicks "Submit"
  When the user clicks "Guardar"
  When the user clicks "button.btn-primary"
  When the user clicks "[data-testid='save-btn']"
  ```

```gherkin
When the user submits the form
```
- Clica no primeiro `button[type=submit]` ou `input[type=submit]` visível.
- **Exemplo:**
  ```gherkin
  When the user submits the form
  ```

```gherkin
When the user waits <N> seconds
```
- Aguarda N segundos (inteiro positivo).
- Usa apenas quando estritamente necessário (animações, polling).
- **Exemplos:**
  ```gherkin
  When the user waits 2 seconds
  When the user waits 1 second
  ```

---

### Then — Verificações / Asserções

```gherkin
Then the user should see "<text>"
```
- Verifica que o texto está visível na página (pesquisa parcial, case-insensitive).
- **Exemplos:**
  ```gherkin
  Then the user should see "Dashboard"
  Then the user should see "Bem-vindo"
  Then the user should see "Erro de autenticação"
  ```

```gherkin
Then the user should not see "<text>"
```
- Verifica que o texto NÃO está visível na página.
- **Exemplos:**
  ```gherkin
  Then the user should not see "Iniciar Sessão"
  Then the user should not see "Error"
  ```

```gherkin
Then the url should contain "<fragment>"
```
- Verifica que a URL actual contém o fragmento especificado (case-insensitive).
- **Exemplos:**
  ```gherkin
  Then the url should contain "dashboard"
  Then the url should contain "#/home"
  Then the url should contain "/admin"
  ```

```gherkin
Then the url should be "<url>"
```
- Verifica que a URL actual é exactamente a URL especificada.
- **Exemplo:**
  ```gherkin
  Then the url should be "https://app.exemplo.pt/#/dashboard"
  ```

```gherkin
Then the element "<selector>" should be visible
```
- Verifica que um elemento identificado por CSS selector está visível.
- **Exemplos:**
  ```gherkin
  Then the element ".sidebar" should be visible
  Then the element "[data-testid='user-menu']" should be visible
  Then the element "#main-content" should be visible
  ```

```gherkin
Then the element "<selector>" should not be visible
```
- Verifica que um elemento identificado por CSS selector NÃO está visível.
- **Exemplo:**
  ```gherkin
  Then the element ".loading-spinner" should not be visible
  ```

```gherkin
Then the field "<field>" should contain "<value>"
```
- Verifica que o valor de um campo de formulário contém o texto esperado.
- `<field>`: mesmo critério que `fills`.
- **Exemplo:**
  ```gherkin
  Then the field "Username" should contain "sandrodev"
  ```

```gherkin
Then the page title should be "<title>"
```
- Verifica que o título da página (tag `<title>`) é exactamente o especificado.
- **Exemplo:**
  ```gherkin
  Then the page title should be "Shipperform — Dashboard"
  ```

---

## Regras de construção de cenários

1. **Cada cenário começa com `Given`** (pré-condição) seguido de `When` (acção) e `Then` (asserção).
2. **`And`** pode substituir qualquer keyword (Given/When/Then) para melhor legibilidade.
3. **`Background`** pode conter steps `Given` comuns a todos os cenários da feature.
4. **Scenario Outline + Examples** pode ser usado para testar múltiplos conjuntos de dados.
5. **Nunca** uses steps fora deste vocabulário — o motor não os reconhecerá.
6. A linguagem dos **valores** dos parâmetros pode ser Português (ex: `"Iniciar Sessão"`).
7. A linguagem dos **keywords Gherkin** é sempre Inglês (Given, When, Then, And, But, Feature, Scenario).

---

## Exemplo de feature completo

```gherkin
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

  Scenario: Aceder a área protegida após login
    Given the user is logged in
    Then the url should contain "dashboard"
    And the element ".sidebar" should be visible
```
