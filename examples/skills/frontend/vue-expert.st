SKILL:   vue-expert | vue3+composition+pinia+routing | vue3+typescript | v1.0.0
USE:     vue-expert | when:vue-app+spa+component-library+state-management
STACK:   vue-expert | view | vue3 | composition-api+script-setup
STACK:   vue-expert | state | pinia | type-safe+devtools+composable
STACK:   vue-expert | routing | vue-router | file-based+guards+meta
STACK:   vue-expert | build | vite | fast+esm+hmr
RULE:    vue-expert | script-setup-always | hard
RULE:    vue-expert | composables-for-reusable-logic | hard
RULE:    vue-expert | pinia-for-shared-state-not-provide-inject | soft
RULE:    vue-expert | defineprops-defineemits-always-typed | hard
RULE:    vue-expert | v-key-required-on-lists | hard
STEP:    vue-expert | build | 1 | define-props-and-emits-interface | required
STEP:    vue-expert | build | 2 | implement-template | required
STEP:    vue-expert | build | 3 | add-composable-logic | required
STEP:    vue-expert | build | 4 | connect-pinia-if-shared-state | optional
CHECK:   vue-expert | no-this-in-script-setup | required
CHECK:   vue-expert | no-mutate-props | required
AVOID:   vue-expert | options-api+vuex+v-html-without-sanitize+deeply-nested-provide-inject
