SKILL:   typescript-pro | typescript+types+generics+safety | typescript | v1.0.0
USE:     typescript-pro | when:typed-javascript+api-contracts+large-codebases
STACK:   typescript-pro | compiler | strict-mode | all-strict-flags-enabled
STACK:   typescript-pro | patterns | generics+discriminated-unions+type-guards | safety
STACK:   typescript-pro | tooling | tsconfig+eslint | strict+consistent
RULE:    typescript-pro | strict-mode-always | hard
RULE:    typescript-pro | no-any-use-unknown | hard
RULE:    typescript-pro | prefer-interface-for-object-shapes | soft
RULE:    typescript-pro | prefer-type-for-unions-and-intersections | soft
RULE:    typescript-pro | never-cast-without-type-guard | hard
RULE:    typescript-pro | exhaustive-switch-with-never | hard
RULE:    typescript-pro | readonly-for-immutable-data | soft
RULE:    typescript-pro | infer-dont-annotate-obvious-types | soft
STEP:    typescript-pro | setup | 1 | enable-strict-in-tsconfig | required
STEP:    typescript-pro | type | 2 | define-domain-types-first | required
STEP:    typescript-pro | type | 3 | use-discriminated-unions-for-state | required
STEP:    typescript-pro | validate | 4 | add-type-guards-at-boundaries | required
CHECK:   typescript-pro | no-implicit-any-in-strict | required
CHECK:   typescript-pro | no-ts-ignore-comments | required
AVOID:   typescript-pro | any+type-assertion-over-guard+enum-prefer-const-union+as-any
