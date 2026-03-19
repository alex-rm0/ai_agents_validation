# Vocabulário de Steps — test_engine

Este ficheiro define o vocabulário **completo e fixo** de step definitions disponíveis no `test_engine`.

Qualquer `.feature` colocado em `Features/generated/` que use **exclusivamente** os steps da
[Secção Genérica](#steps-genéricos) corre sem necessidade de implementação C# adicional.

---

## Steps Genéricos (GenericStepDefinitions.cs) — Vocabulário controlado para geração automática

> **Nota para o LLM:** Usa **apenas** os steps desta secção. Não inventes steps novos.
> A sintaxe das aspas e maiúsculas/minúsculas é obrigatória tal como mostrado.

### Given — Pré-condições

```gherkin
Given the user navigates to "<route>"
```
- Navega para uma rota relativa à BASE_URL ou URL absoluta.
- **Exemplos:**
  ```gherkin
  Given the user navigates to "login"
  Given the user navigates to "#/dashboard"
  Given the user navigates to "https://exemplo.pt/page"
  ```

```gherkin
Given the user is logged in
```
- Realiza login com as credenciais de TestConfig/appsettings.json. Aguarda redireccionamento.
- **Exemplo:**
  ```gherkin
  Given the user is logged in
  ```

---

### When — Acções do utilizador

```gherkin
When the user fills "<field>" with "<value>"
```
- Preenche um campo identificado por: placeholder, label, data-testid, data-cy, ou CSS selector.
- **Exemplos:**
  ```gherkin
  When the user fills "Email" with "teste@exemplo.pt"
  When the user fills "input[name='search']" with "consulta"
  When the user fills "input[type='text']" with "sandrodev"
  ```

```gherkin
When the user clears "<field>"
```
- Limpa um campo de formulário. Mesma identificação que `fills`.
- **Exemplo:**
  ```gherkin
  When the user clears "Search"
  ```

```gherkin
When the user clicks "<element>"
```
- Clica num elemento (botão, link, etc.) identificado por: texto, data-testid, data-cy, ou CSS selector.
- **Exemplos:**
  ```gherkin
  When the user clicks "Iniciar Sessão"
  When the user clicks "Submit"
  When the user clicks "[data-testid='save-btn']"
  ```

```gherkin
When the user submits the form
```
- Clica no primeiro `button[type=submit]` ou `input[type=submit]` visível.

```gherkin
When the user waits <N> seconds
```
- Aguarda N segundos inteiros (sem aspas).
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
- Verifica que o texto está visível (pesquisa via placeholder, label, texto, data-testid, data-cy, CSS).
- **Exemplos:**
  ```gherkin
  Then the user should see "Dashboard"
  Then the user should see "Bem-vindo"
  ```

```gherkin
Then the user should not see "<text>"
```
- Verifica que o texto NÃO está visível.
- **Exemplo:**
  ```gherkin
  Then the user should not see "Erro de autenticação"
  ```

```gherkin
Then the url should contain "<fragment>"
```
- Aguarda e verifica que a URL contém o fragmento (case-insensitive).
- **Exemplos:**
  ```gherkin
  Then the url should contain "dashboard"
  Then the url should contain "#/home"
  ```

```gherkin
Then the url should be "<url>"
```
- Aguarda e verifica que a URL é exactamente a especificada.
- **Exemplo:**
  ```gherkin
  Then the url should be "https://app.exemplo.pt/#/dashboard"
  ```

```gherkin
Then the element "<selector>" should be visible
```
- Verifica que um elemento está visível (placeholder, label, texto, data-testid, data-cy, CSS selector).
- **Exemplos:**
  ```gherkin
  Then the element ".sidebar" should be visible
  Then the element "[data-testid='user-menu']" should be visible
  ```

```gherkin
Then the element "<selector>" should not be visible
```
- Verifica que um elemento NÃO está visível.
- **Exemplo:**
  ```gherkin
  Then the element ".loading-spinner" should not be visible
  ```

```gherkin
Then the field "<field>" should contain "<value>"
```
- Verifica que o valor de um campo de formulário contém o texto esperado.
- **Exemplo:**
  ```gherkin
  Then the field "input[type='text']" should contain "sandrodev"
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

1. **Cada cenário começa com `Given`** seguido de `When` e `Then`.
2. **`And`** pode substituir Given/When/Then para melhor legibilidade.
3. **`Background:`** pode conter steps `Given` comuns a todos os cenários.
4. **Scenario Outline + Examples** suportado para múltiplos conjuntos de dados.
5. **Nunca** uses steps fora deste vocabulário — causarão falha na execução.
6. Valores dos parâmetros podem ser em Português (`"Iniciar Sessão"`).
7. Keywords Gherkin são sempre em Inglês (Feature, Scenario, Given, When, Then, And, But).

---

## Exemplo de feature completo (gerado automaticamente)

```gherkin
Feature: Login de Utilizador
  Como utilizador registado
  Quero poder autenticar-me na aplicação
  Para aceder às funcionalidades protegidas

  Scenario: Login com credenciais válidas
    Given the user navigates to "#/login"
    When the user fills "input[type='text']" with "sandrodev"
    And the user fills "input[type='password']" with "Sandrodev-123"
    And the user clicks "Iniciar Sessão"
    Then the url should contain "dashboard"
    And the user should see "Dashboard"

  Scenario: Login com password incorrecta
    Given the user navigates to "#/login"
    When the user fills "input[type='text']" with "sandrodev"
    And the user fills "input[type='password']" with "wrong-password"
    And the user clicks "Iniciar Sessão"
    Then the user should not see "Dashboard"

  Scenario: Aceder à aplicação após login automático
    Given the user is logged in
    Then the url should contain "dashboard"
```

---

## Steps legados (LoginStepDefinitions / NavigationStepDefinitions)

Estes steps existem no codebase mas **não devem ser usados em features geradas automaticamente**.
São mantidos para compatibilidade com os testes manuais existentes.

```gherkin
Given the application base url is configured
Given a user is on the login page
When the user logs in with valid credentials
When I navigate to the home page
Then the user should be authenticated
Then the browser should be at the base url
```
