# QA Regression Testing

This folder contains regression test suites and documentation.

## Purpose
Regression testing verifies that:
- New features don't break existing functionality
- Bug fixes don't introduce new issues
- Updated code maintains backward compatibility
- System remains stable after changes

## Contents
- Regression test suite definitions
- Regression test cases
- Regression test results
- Smoke test definitions
- Critical path test cases

## Regression Test Strategy
1. **Scope:** Identify areas most likely affected by changes
2. **Frequency:** Run after every build/deployment
3. **Priority:** Focus on critical and high-risk areas
4. **Automation:** Automate repetitive regression tests
5. **Maintenance:** Update regression suite as features change

## Test Categories

### Smoke Tests (Quick validation)
- Login/Logout functionality
- Create note
- View notes list
- Delete note
- Update profile

### Critical Path Tests
- End-to-end user journeys
- Payment flows (if applicable)
- Data persistence
- User data isolation

### API Regression Tests
- Authentication endpoints
- Notes CRUD operations
- Rate limiting
- Error handling

## Folder Structure
```
├── smoke_tests/
│   ├── smoke_test_suite.md
│   └── critical_features.md
├── critical_path_tests/
│   ├── user_journey_1.md
│   ├── user_journey_2.md
│   └── ...
└── regression_results/
    ├── 2026-04-19_post_build.md
    └── 2026-04-20_pre_release.md
```

## Regression Execution
**When to run:**
- After each development build
- Before UAT release
- Before production release
- After hotfix deployment

**Expected Duration:**
- Smoke tests: 15-30 minutes
- Full regression: 2-4 hours
- Automated regression: 10-20 minutes

## Pass Criteria
- All smoke tests pass
- No new defects introduced
- No critical issues unresolved
- All critical path scenarios work

## Documents to Create
- [ ] Regression Test Suite Definition.md
- [ ] Smoke Test Checklist.md
- [ ] Critical Path Test Cases.md
- [ ] Regression Test Results (per run).md

## Links to Other Phases
→ Related to: [Execution](../execution/)
→ Reported in: [Reporting](../reporting/)

## Notes for Trainee QA
- Keep regression tests up to date with code changes
- Regularly review and optimize regression suite
- Document test results for trend analysis
- Identify patterns in regression failures
- Automate high-impact regression tests first
