Feature: Página de Login
  Como um utilizador
  Quero uma página de login com interface responsiva
  Para poder autenticar-me na aplicação

  Scenario: Página de login com estrutura responsiva
    Given the user navigates to "#/login"
    Then the page title should be "Página de Login"
    And the user should see "Login"
    And the user should see "Email"
    And the user should see "Password"
    And the user should see "Mostrar Password"
    And the user should see "Recuperar Password"
    And the url should contain "#/login"