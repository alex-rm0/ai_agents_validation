Feature: Login
  A generic example feature to test login page.

  Background:
    Given the application base url is configured

  Scenario: User logs in with valid credentials
    Given a user is on the login page
    When the user logs in with valid credentials
    Then the user should be authenticated