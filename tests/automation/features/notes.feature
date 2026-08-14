# Feature: Notes Management
# Test note creation, reading, updating, and deletion

Feature: Notes Management

  Background:
    Given I am logged in as "testuser@example.com" with password "TestPassword123"
    And I am on the home page

  Scenario: Create a new note
    When I click the Create Note button
    And I enter the title "My First Note"
    And I enter the content "This is the content of my note"
    And I click the Save button
    Then I should see a success message "Note created successfully"
    And I should be redirected to the home page
    And the note "My First Note" should appear in my notes list

  Scenario: View list of notes
    Given I have created 3 notes
    When I navigate to the home page
    Then I should see all 3 notes displayed
    And each note should show the title and preview of content

  Scenario: View empty notes state
    When I navigate to the home page
    Then I should see the message "You don't have any notes"
    And the Create Note button should not be visible

  Scenario: View note detail
    Given I have created a note titled "Test Note"
    When I click on the note "Test Note"
    Then I should see the full note title
    And I should see the full note content

  Scenario: Update an existing note
    Given I have created a note titled "Original Title"
    And I navigate to this note
    When I click the Edit button
    And I change the title to "Updated Title"
    And I change the content to "Updated content"
    And I click the Save button
    Then I should see a success message "Note updated successfully"
    And the note should now display "Updated Title"

  Scenario: Delete a note
    Given I have created a note titled "Note to Delete"
    And I navigate to this note
    When I click the Delete button
    And I confirm the deletion
    Then I should see a success message "Note deleted successfully"
    And I should be redirected to the home page
    And the note should no longer appear in my notes list

  Scenario: Notes are private to user
    Given I am logged in as "user1@example.com"
    And I have created a note titled "My Private Note"
    When I log out
    And I log in as "user2@example.com"
    And I navigate to the home page
    Then I should not see the note "My Private Note"
    And the notes list should be empty
