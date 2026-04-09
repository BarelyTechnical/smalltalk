SKILL:   golang-pro | golang+concurrency+errors+testing | go | v1.0.0
USE:     golang-pro | when:cli+microservice+system-tool+performance-critical
STACK:   golang-pro | runtime | go1.22+ | builtins+stdlib-first
STACK:   golang-pro | http | net/http+chi | standard+routing
STACK:   golang-pro | errors | errors.Is+fmt.Errorf | wrap+sentinel
STACK:   golang-pro | testing | testing+testify | table-driven
RULE:    golang-pro | errors-as-values-not-exceptions | hard
RULE:    golang-pro | interfaces-should-be-small | hard
RULE:    golang-pro | accept-interfaces-return-structs | hard
RULE:    golang-pro | goroutines-need-cancel-context | hard
RULE:    golang-pro | no-naked-returns | hard
RULE:    golang-pro | stdlib-first-third-party-last | hard
RULE:    golang-pro | wrap-errors-with-context | hard
STEP:    golang-pro | build | 1 | define-interfaces-first | required
STEP:    golang-pro | build | 2 | implement-and-inject | required
STEP:    golang-pro | test | 3 | table-driven-tests | required
STEP:    golang-pro | error | 4 | wrap-at-call-boundary | required
CHECK:   golang-pro | go-vet-passes | required
CHECK:   golang-pro | no-goroutine-leaks | required
AVOID:   golang-pro | global-state+panic+init-functions+large-interfaces+fmt-errorf-without-wrap
