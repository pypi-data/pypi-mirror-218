Feature: Create a client

  Scenario: Log in successfully

    Given that I have a valid username and password for a given environment
    When the client is created
    Then it logs in successfully
