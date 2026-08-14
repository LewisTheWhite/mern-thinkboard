# Test Case Template

## Test Case ID
- **ID:** TC-XXX (e.g., TC-001)
- **Title:** [Clear, concise test case title]
- **Module:** [Auth / Notes / UI / API]
- **Feature:** [Feature name being tested]
- **Created Date:** YYYY-MM-DD
- **Created By:** [Tester Name]
- **Last Updated:** YYYY-MM-DD
- **Status:** [Draft / Active / Deprecated]
- **Automation Status:** [Manual / Automated / In Progress]

---

## Test Case Description
**Purpose:** What is this test case validating?

Example: "Verify that users can successfully create a new note with valid title and content"

---

## Pre-conditions
List all conditions that must be met before test execution:
1. Application is running and accessible
2. User is logged in with valid credentials
3. Browser cache is cleared
4. Test data is available (user account, sample data)
5. Backend API is responding normally
6. (Add more as needed)

---

## Test Data
Specify any data needed for this test:

| Field | Value | Notes |
|-------|-------|-------|
| Email | testuser@example.com | Valid registered user |
| Password | TestPassword123 | 8+ characters |
| Note Title | "Test Note" | Text input |
| Note Content | "This is test content" | Long text |

---

## Test Steps
Step-by-step instructions for executing the test case:

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|-----------------|-----------|-------|
| 1 | Navigate to home page | Page loads successfully, user is logged in | ☐ | - |
| 2 | Click "Create Note" button | Redirected to note creation page | ☐ | - |
| 3 | Enter title "Test Note" | Title field displays entered text | ☐ | - |
| 4 | Enter content in text area | Content field displays entered text | ☐ | - |
| 5 | Click "Save" button | Success toast appears, page redirects to home | ☐ | - |
| 6 | Verify note in list | "Test Note" appears in notes list | ☐ | - |

---

## Expected Result
**Summary of successful test execution:**

The user should be able to create and view a new note. The note should persist in the database and be retrievable on subsequent logins.

---

## Post-conditions
State of the application after test execution:
1. New note appears in user's notes list
2. Note data is saved in database
3. User remains logged in
4. No error messages or console logs

---

## Pass Criteria
Conditions that must be met for test to pass:
- ✓ All steps complete without errors
- ✓ No unexpected console errors
- ✓ Note appears in the list with correct data
- ✓ Success message displayed
- ✓ Page redirects correctly

---

## Fail Criteria
Conditions that result in test failure:
- ✗ Application crashes or throws unhandled error
- ✗ Note not created or saved
- ✗ Wrong/corrupted data displayed
- ✗ Error message appears instead of success message
- ✗ User is logged out unexpectedly

---

## Regression Potential
**Risk Level:** [High / Medium / Low]
**Impact:** Brief description of potential impact if regression occurs

---

## Related Documentation
- User Story: US-XXX (If applicable)
- Bug ID: #XXX (If bug fix related)
- API Endpoint: POST /api/notes
- Feature Requirements: Link to requirements document

---

## Screenshots/Attachments
- [ ] Initial state screenshot
- [ ] During execution screenshot
- [ ] Final expected state screenshot
- [ ] Screen recording of test
- [ ] Browser console log

---

## Execution History
| Date | Tester | Result | Notes | Build |
|------|--------|--------|-------|-------|
| 2026-04-19 | [QA Name] | Pass | All steps successful | v1.0.1 |
| | | | | |

---

## Notes for Trainee QA
When creating test cases:
1. **Clarity is key** - Steps should be clear enough for anyone to follow
2. **Positive & Negative** - Create both happy path and error scenarios
3. **Repeatability** - Test case must be repeatable with consistent results
4. **Independence** - Test should not depend on other test results
5. **Data Management** - Use consistent test data or fixtures
6. **Maintenance** - Update test case when app requirements change
7. **Coverage** - Ensure all features have corresponding test cases
8. **Organization** - Group related test cases by module/feature

---

## Test Case Types to Create
- **Smoke Tests:** Quick validation of core functionality
- **Sanity Tests:** Verify specific bug fixes
- **Regression Tests:** Ensure no new bugs after updates
- **Functional Tests:** Full feature testing
- **Boundary Tests:** Test limits and edge cases
- **Negative Tests:** Invalid input handling
- **Performance Tests:** Load and response time validation
