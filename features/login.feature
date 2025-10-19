Feature: User Login
  As a user
  I want to log in to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @smoke @login
  Scenario: Successful login with valid credentials
    When I enter username "valid_user"
    And I enter password "valid_password"
    And I click the login button
    Then I should be logged in successfully
    And I should see the dashboard

  @login @negative
  Scenario: Failed login with invalid credentials
    When I enter username "invalid_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see an error message
    And I should remain on the login page

  @login
  Scenario Outline: Login with different credentials
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then the login should "<result>"

    Examples:
      | username      | password      | result  |
      | valid_user    | valid_pass    | succeed |
      | invalid_user  | wrong_pass    | fail    |
      | empty         | valid_pass    | fail    |
      | valid_user    | empty         | fail    |

  @login @security
  Scenario: Account lockout after multiple failed attempts
    When I attempt to login with wrong credentials 3 times
    Then the account should be locked
    And I should see a lockout message

