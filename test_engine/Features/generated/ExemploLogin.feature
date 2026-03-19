Feature: Login de Utilizador — Exemplo de Steps Genéricos
  Como utilizador registado
  Quero poder autenticar-me na aplicação
  Para aceder às funcionalidades protegidas

  Scenario: Login com credenciais válidas usando steps genéricos
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
