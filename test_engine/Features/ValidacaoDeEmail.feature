Feature: Validação de Email
  Como um utilizador
  Quero uma validação de email em tempo real
  Para garantir que a entrada de dados seja válida

  Scenario: Validar email em tempo real
    Given the user navigates to "#/login"
    When the user fills "input[type='email']" with "invalid_email"
    Then the user should not see "Email válido"
    When the user fills "input[type='email']" with "sandrodev@example.com"
    Then the user should see "Email válido"