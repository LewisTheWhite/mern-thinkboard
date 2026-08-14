# Feature: User Authentication
# Test user signup, login, and profile management

Feature: User Authentication

  Background:
    Given the application is running
    And I navigate to the signup page

  Scenario: Successful user signup
    When I enter a valid name "John Doe"
    And I enter a valid email "john@example.com"
    And I enter a valid password "SecurePassword123"
    And I confirm the password "SecurePassword123"
    And I click the Sign Up button
    Then I should see a success message
    And I should be redirected to the login page

  Scenario: Signup with invalid email
    When I enter a valid name "Jane Doe"
    And I enter an invalid email "invalidemail"
    And I enter a valid password "SecurePassword123"
    And I click the Sign Up button
    Then I should see an error message "Invalid email format"
    And I should remain on the signup page

  Scenario: Signup with short password
    When I enter a valid name "Bob Smith"
    And I enter a valid email "bob@example.com"
    And I enter a short password "pass"
    And I click the Sign Up button
    Then I should see an error message "Password must be at least 8 characters"
    And I should remain on the signup page

  Scenario: Successful user login
    Given I have a registered account with email "user@example.com" and password "TestPass123"
    And I navigate to the login page
    When I enter the email "user@example.com"
    And I enter the password "TestPass123"
    And I click the Login button
    Then I should be redirected to the home page
    And I should see my username in the navbar

  Scenario: Login with invalid credentials
    Given I navigate to the login page
    When I enter the email "wrong@example.com"
    And I enter the password "WrongPassword123"
    And I click the Login button
    Then I should see an error message "Invalid email or password"
    And I should remain on the login page
