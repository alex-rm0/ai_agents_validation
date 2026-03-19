Feature: Estilos e Animações
  Como um utilizador
  Quero uma página de login com estilos e animações agradáveis
  Para uma experiência de usuário melhorada

  Scenario: Página de login com estilos e animações
    Given the user navigates to "#/login"
    Then the user should see "Estilos e animações agradáveis"
    And the page should have a responsive design
    And the page should have a clean and organized layout