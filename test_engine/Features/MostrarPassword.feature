Feature: Mostrar Password
  Como um utilizador
  Quero um botão para mostrar a password
  Para poder visualizar a password ao clicar no botão

  Scenario: Mostrar password ao clicar no botão
    Given the user navigates to "#/login"
    When the user clicks "Mostrar Password"
    Then the user should see "Password visível"
    When the user clicks "Mostrar Password"
    Then the user should see "Password oculto"