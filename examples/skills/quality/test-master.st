SKILL:   test-master | tdd+unit+integration+e2e | pytest+jest+playwright | v1.0.0
USE:     test-master | when:testing+tdd+coverage+quality-assurance
STACK:   test-master | unit | pytest+jest | fast+isolated
STACK:   test-master | integration | supertest+httpx | api-layer
STACK:   test-master | e2e | playwright+cypress | user-flows
STACK:   test-master | coverage | coverage.py+istanbul | 80pct-minimum
RULE:    test-master | test-behaviour-not-implementation | hard
RULE:    test-master | one-assertion-per-test | soft
RULE:    test-master | arrange-act-assert | hard
RULE:    test-master | no-logic-in-tests | hard
RULE:    test-master | mock-only-external-deps | soft
RULE:    test-master | deterministic-no-time-or-random | hard
STEP:    test-master | write | 1 | write-test-before-implementation | optional
STEP:    test-master | write | 2 | happy-path-first | required
STEP:    test-master | write | 3 | edge-cases-and-errors | required
STEP:    test-master | validate | 4 | coverage-report-review | required
CHECK:   test-master | 80pct-coverage-minimum | required
CHECK:   test-master | all-tests-deterministic | required
AVOID:   test-master | testing-internals+flaky-sleep-assertions+no-edge-cases+mocking-everything
