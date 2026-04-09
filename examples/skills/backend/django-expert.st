SKILL:   django-expert | django+orm+auth+deployment | python+django | v1.0.0
USE:     django-expert | when:web-app+admin+auth+database-heavy
STACK:   django-expert | framework | django5 | batteries-included+admin+auth
STACK:   django-expert | orm | django-orm | querysets+migrations+relations
STACK:   django-expert | api | drf+drf-spectacular | serializers+viewsets+schema
STACK:   django-expert | tasks | celery+redis | async-jobs+scheduling
STACK:   django-expert | deploy | gunicorn+whitenoise | production-ready
RULE:    django-expert | fat-models-thin-views | hard
RULE:    django-expert | use-class-based-views | soft
RULE:    django-expert | migrations-every-model-change | hard
RULE:    django-expert | select-related-prefetch-related | hard
RULE:    django-expert | settings-split-dev-prod | hard
RULE:    django-expert | custom-user-model-from-start | hard
STEP:    django-expert | setup | 1 | custom-user-model-before-first-migrate | required
STEP:    django-expert | build | 2 | define-models-and-migrate | required
STEP:    django-expert | build | 3 | build-serializers-and-views | required
STEP:    django-expert | deploy | 4 | configure-static-and-gunicorn | required
CHECK:   django-expert | no-n-plus-one-queries | required
CHECK:   django-expert | debug-false-in-prod | required
AVOID:   django-expert | fat-views+raw-sql-without-reason+missing-prefetch+debug-on-in-prod
