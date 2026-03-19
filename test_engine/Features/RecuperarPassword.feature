Feature: Recuperar Password
  Como um utilizador
  Quero um link para recuperação de password
  Para poder recuperar a password caso esqueça

  Scenario: Recuperar password ao clicar no link
    Given the user navigates to "#/login"
    When the user clicks "Recuperar Password"
    Then the user should see "Recuperar Password"
    And the url should contain "#/recuperar-password"