SKILL:   tailwind-expert | tailwind+responsive+dark-mode+design-system | tailwind | v1.0.0
USE:     tailwind-expert | when:utility-css+responsive-design+design-tokens
STACK:   tailwind-expert | styling | tailwind | jit+purge+config
STACK:   tailwind-expert | theming | tailwind.config | custom-tokens+dark-mode
STACK:   tailwind-expert | components | @apply | reusable-patterns-only
RULE:    tailwind-expert | mobile-first-always | hard
RULE:    tailwind-expert | no-dynamic-class-construction | hard
RULE:    tailwind-expert | extract-to-component-not-apply | hard
RULE:    tailwind-expert | direct-utility-over-custom-css | hard
RULE:    tailwind-expert | design-tokens-in-config-not-inline | soft
STEP:    tailwind-expert | setup | 1 | npx-tailwindcss-init | required
STEP:    tailwind-expert | setup | 2 | configure-content-paths | required
STEP:    tailwind-expert | build | 3 | define-custom-tokens-in-config | optional
STEP:    tailwind-expert | build | 4 | mobile-first-then-sm-md-lg | required
CHECK:   tailwind-expert | no-purged-dynamic-classes | required
CHECK:   tailwind-expert | dark-mode-class-not-media | required
AVOID:   tailwind-expert | @apply-overuse+important-modifier+inline-style+desktop-first-media
