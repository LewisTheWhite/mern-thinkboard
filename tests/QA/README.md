# QA Folder Structure Overview

This folder contains all Quality Assurance artifacts and documentation for the MERN-ThinkBoard project.

## Folder Organization by STLC Phase

### 🔵 Planning Phase
**[planning/](./planning/)**
- Test strategy documents
- Test plan
- Requirements traceability matrix
- Risk assessment
- Resource allocation
- Testing schedule

### 🟢 Design Phase
**[design/](./design/)**
- Test case specifications
- Test scenarios
- Test data design
- Environment setup documentation
- Test execution checklists

### 🟡 Execution Phase
**[execution/](./execution/)**
- Test execution logs
- Bug reports with findings
- Test run summaries
- Screenshots and evidence
- Execution metrics

### 🔴 Reporting Phase
**[reporting/](./reporting/)**
- Test summary reports
- Defect analysis reports
- Test metrics and statistics
- Coverage analysis
- Release readiness assessment

### 🟠 Regression Phase
**[regression/](./regression/)**
- Regression test suites
- Smoke test definitions
- Critical path test cases
- Regression test results

### 🟣 Exploratory Phase
**[exploratory/](./exploratory/)**
- Exploratory test charters
- Session-based test logs
- Edge case findings
- Interesting behavior discoveries
- Improvement recommendations

### 📋 Templates
**[templates/](./templates/)**
- Bug Report Template
- Test Case Template
- Template guidance and best practices

---

## Quick Navigation

| Phase | Lead Activities | Key Deliverables |
|-------|-----------------|------------------|
| Planning | Scope definition, resource allocation | Test Plan, RTM |
| Design | Test design, data preparation | Test Cases, Test Data |
| Execution | Test running, bug reporting | Test Results, Bug Reports |
| Reporting | Analysis, metrics compilation | Reports, Recommendations |
| Regression | Repeated testing of key paths | Regression Results |
| Exploratory | Unscripted investigation | Findings, Improvements |

---

## For Trainee QA

### Getting Started
1. Review [planning/README.md](./planning/) to understand testing strategy
2. Study test cases in [design/](./design/) to see test format
3. Use templates in [templates/](./templates/) for creating artifacts
4. Review sample bugs in [execution/](./execution/) to learn bug reporting
5. Check [exploratory/](./exploratory/) for testing techniques

### Key Workflows

**Running Tests:**
1. Go to [execution/](./execution/) phase folder
2. Follow test cases from [design/](./design/)
3. Document results and any bugs found
4. Use [templates/bug_report_template.md](./templates/bug_report_template.md) for issues

**Creating Test Cases:**
1. Use [templates/test_case_template.md](./templates/test_case_template.md)
2. Save in appropriate [design/](./design/) subfolder
3. Follow naming convention: `TC-XXX_feature_scenario.md`
4. Include all required sections from template

**Reporting Bugs:**
1. Use [templates/bug_report_template.md](./templates/bug_report_template.md)
2. Save in [execution/bugs_found/](./execution/) folder
3. Include clear steps to reproduce
4. Attach screenshots/logs as evidence
5. Mark severity and priority

---

## Testing Workflow

```
Plan → Design → Execute → Report
         ↓         ↓
      Regression & Exploratory (parallel with other phases)
```

1. **Plan:** Define what to test
2. **Design:** Create how to test
3. **Execute:** Run the tests
4. **Report:** Analyze and communicate results
5. **Regression:** Re-test critical paths
6. **Exploratory:** Discover edge cases

---

## Key Documents Structure

```
qa/
├── planning/
│   ├── README.md (Guidance for Planning phase)
│   ├── Test Strategy.md
│   ├── Test Plan.md
│   └── Risk Assessment.md
│
├── design/
│   ├── README.md (Guidance for Design phase)
│   ├── auth/
│   │   ├── TC-001_signup.md
│   │   ├── TC-002_login.md
│   │   └── ...
│   ├── notes/
│   │   ├── TC-010_create_note.md
│   │   └── ...
│   └── ...
│
├── execution/
│   ├── README.md (Guidance for Execution phase)
│   ├── test_runs/
│   │   └── 2026-04-19_run_1/
│   ├── bugs_found/
│   │   ├── BUG-001_issue_title.md
│   │   └── ...
│   └── ...
│
├── reporting/
│   ├── README.md (Guidance for Reporting phase)
│   ├── Test Summary Report.md
│   ├── Defect Summary Report.md
│   └── ...
│
├── regression/
│   ├── README.md (Guidance for Regression phase)
│   ├── smoke_tests/
│   ├── critical_path_tests/
│   └── ...
│
├── exploratory/
│   ├── README.md (Guidance for Exploratory phase)
│   ├── test_charters/
│   ├── session_logs/
│   └── ...
│
└── templates/
    ├── README.md (How to use templates)
    ├── bug_report_template.md
    └── test_case_template.md
```

---

## Best Practices

### Documentation
✅ Keep documentation current with code changes
✅ Use clear, consistent terminology
✅ Include examples and context
✅ Version control all QA artifacts

### Quality
✅ Create comprehensive test coverage
✅ Prioritize critical paths
✅ Document evidence (screenshots, logs)
✅ Review and peer-check test cases

### Communication
✅ Use templates for consistency
✅ Report issues promptly
✅ Provide clear reproduction steps
✅ Share learnings with team

---

## Useful Links

- **Automation Tests:** [../automation/](../automation/) (Python/Pytest)
- **Backend API:** http://localhost:5001/api
- **Frontend App:** http://localhost:5173
- **Project Docs:** [../../README.md](../../README.md)

---

## Contacts and Roles

| Role | Owner | Contact |
|------|-------|---------|
| QA Lead | [Lead Name] | [Email/Slack] |
| Test Automation | [Name] | [Email/Slack] |
| Manual Testing Lead | [Name] | [Email/Slack] |

---

## Questions?

Refer to the README.md in each phase folder for phase-specific guidance.

**Last Updated:** 2026-04-19
**Version:** 1.0
