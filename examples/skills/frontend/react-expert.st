SKILL:   react-expert | react+hooks+state+components | react+typescript | v1.0.0
USE:     react-expert | when:component-building+state-management+ui-development
USE:     react-expert | when:frontend-react+hooks+performance+rendering
STACK:   react-expert | view | react | component-model+virtual-dom
STACK:   react-expert | state | useState+useReducer+context | local-and-shared-state
STACK:   react-expert | effects | useEffect+useCallback+useMemo | side-effects+memoization
STACK:   react-expert | data | react-query+swr | server-state+caching
RULE:    react-expert | prefer-composition-over-inheritance | hard
RULE:    react-expert | single-responsibility-per-component | hard
RULE:    react-expert | lift-state-only-as-high-as-needed | hard
RULE:    react-expert | memo-and-callback-only-when-profiled | soft
RULE:    react-expert | key-prop-required-on-lists | hard
RULE:    react-expert | no-direct-state-mutation | hard
RULE:    react-expert | collocate-state-with-component-that-uses-it | hard
STEP:    react-expert | build | 1 | define-component-interface-first | required
STEP:    react-expert | build | 2 | implement-base-render | required
STEP:    react-expert | build | 3 | add-state-and-effects | required
STEP:    react-expert | build | 4 | extract-hooks-if-logic-reusable | optional
STEP:    react-expert | build | 5 | add-error-boundaries | optional
CHECK:   react-expert | no-stale-closure-in-useeffect | required
CHECK:   react-expert | deps-array-complete | required
CHECK:   react-expert | no-conditional-hooks | required
AVOID:   react-expert | prop-drilling-beyond-2-levels+index-as-key+useeffect-for-derived-state
