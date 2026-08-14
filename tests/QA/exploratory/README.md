# QA Exploratory Testing

This folder contains exploratory testing documentation and findings.

## Purpose
Exploratory testing is unscripted, investigative testing that:
- Discovers unexpected issues and edge cases
- Validates assumptions about system behavior
- Explores features not covered by scripted tests
- Identifies areas for focused testing
- Provides creative problem-solving approaches

## Contents
- Exploratory test charters
- Test tours and heuristics
- Findings and interesting behaviors
- Session-based testing logs
- Unexpected discoveries and insights

## Exploratory Testing Approach

### Test Charters
Define the mission for exploratory testing sessions:
- Time-boxed (typically 60-90 minutes)
- Clear objectives
- Specific focus area or feature
- Success criteria defined

### Testing Heuristics
Techniques to guide exploratory testing:
- **Boundary Value Analysis:** Test limits and edges
- **State Testing:** Invalid state transitions
- **Combination Testing:** Multiple fields together
- **Workflow Testing:** Real-world usage patterns
- **Load Testing:** Performance with typical data
- **Usability Testing:** User experience assessment

### Test Tours
Guided exploration of features:
- **Happy Path Tour:** Normal usage flows
- **Sad Path Tour:** Error and exception handling
- **Feature Tour:** Exploring all options
- **User Tour:** Different user roles
- **Data Tour:** Various data types and amounts

## Folder Structure
```
├── test_charters/
│   ├── charter_auth_forms.md
│   ├── charter_note_creation.md
│   └── ...
├── session_logs/
│   ├── 2026-04-19_session_1_auth_edge_cases.md
│   ├── 2026-04-19_session_2_note_limits.md
│   └── ...
└── findings/
    ├── interesting_behaviors.md
    ├── potential_improvements.md
    └── edge_cases_discovered.md
```

## Session-Based Test Log Template
```markdown
**Test Charter:** [Charter title]
**Tester:** [Name]
**Date & Time:** [Date] [Time]
**Duration:** [Minutes]
**Build/Version:** [Version tested]

### Objectives
- Objective 1
- Objective 2

### Activities Performed
1. Action 1
2. Action 2

### Findings
- Finding 1 (with severity)
- Finding 2 (with severity)

### Questions/Unknowns
- Question 1
- Question 2

### Recommendations
- Recommendation 1
- Recommendation 2
```

## Key Areas to Explore
- **Authentication:** Edge cases in login/signup
- **Input Validation:** Special characters, lengths, formats
- **Performance:** Behavior under load
- **Usability:** Navigation, error messages, guidance
- **Data Handling:** Large datasets, special characters
- **Browser Compatibility:** Different browsers/versions
- **Network Issues:** Slow connections, timeouts
- **Concurrency:** Multiple users, race conditions

## Documents to Create
- [ ] Exploratory Test Charters.md
- [ ] Session-Based Test Log (per session).md
- [ ] Discovered Edge Cases.md
- [ ] Improvement Recommendations.md

## Best Practices
1. **Document findings immediately** while testing
2. **Ask questions:** "What if...?" and "What happens if...?"
3. **Vary approach:** Don't test the same way twice
4. **Investigate thoroughly** before moving on
5. **Report with evidence:** Screenshots, steps to reproduce
6. **Share learnings:** Collaborate with team
7. **Update charters:** Refine based on findings

## Links to Other Phases
→ Informs: [Execution](../execution/)
→ May trigger: [Design](../design/) updates

## Notes for Trainee QA
- Exploratory testing requires creativity and critical thinking
- Document "why" you were testing something, not just "what"
- Interesting discoveries might not be bugs - they might be features
- Use exploratory testing to improve test case coverage
- Combine with scripted testing for comprehensive coverage
