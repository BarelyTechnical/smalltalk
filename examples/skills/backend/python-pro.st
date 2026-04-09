SKILL:   python-pro | python+async+typing+testing | python3.10+ | v1.0.0
USE:     python-pro | when:python-scripting+apis+automation+data-processing
STACK:   python-pro | runtime | python3.10+ | match-statements+type-hints
STACK:   python-pro | async | asyncio+httpx | concurrent+non-blocking
STACK:   python-pro | types | pydantic+mypy | validation+type-checking
STACK:   python-pro | testing | pytest+pytest-asyncio | coverage+fixtures
STACK:   python-pro | packaging | uv+pyproject.toml | fast+standard
RULE:    python-pro | type-hints-always | hard
RULE:    python-pro | prefer-dataclass-or-pydantic-over-dict | hard
RULE:    python-pro | early-return-reduce-nesting | soft
RULE:    python-pro | explicit-over-implicit | hard
RULE:    python-pro | context-managers-for-resources | hard
RULE:    python-pro | no-bare-except | hard
RULE:    python-pro | f-strings-over-format | soft
STEP:    python-pro | setup | 1 | uv-init-project | required
STEP:    python-pro | setup | 2 | add-pyproject-toml | required
STEP:    python-pro | code | 3 | type-annotate-all-functions | required
STEP:    python-pro | test | 4 | pytest-with-fixtures | required
CHECK:   python-pro | mypy-passes-strict | required
CHECK:   python-pro | no-mutable-default-arguments | required
AVOID:   python-pro | bare-except+global-state+mutable-defaults+wildcard-imports+nested-3-deep
