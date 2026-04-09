# Smalltalk v3.0.0 — KG example: team brain
# Demonstrates LINK entries, temporal validity, stability levels,
# and the contradiction → resolution cycle.

# ── Entity relationships ─────────────────────────────────────────────────────

LINK: kai         | rel:works-on    | nova     | valid_from:2026-03 | stability:transient
LINK: kai         | rel:member-of   | team     | valid_from:2025-06 | stability:stable
LINK: kai         | rel:reports-to  | priya    | valid_from:2025-06 | stability:stable

LINK: priya       | rel:leads       | team     | valid_from:2025-01 | stability:stable
LINK: priya       | rel:works-on    | nova     | valid_from:2026-01 | stability:transient
LINK: priya       | rel:works-on    | orion    | valid_from:2025-01 | ended:2026-01 | stability:transient

LINK: nova        | rel:depends     | auth     | stability:stable
LINK: nova        | rel:depends     | billing  | stability:stable
LINK: nova        | rel:deployed-to | vercel   | valid_from:2026-03 | stability:transient

LINK: orion       | rel:depends     | auth     | stability:stable
LINK: orion       | rel:archived    | true     | valid_from:2026-01 | stability:permanent

# ── Brand / permanent facts ───────────────────────────────────────────────────

LINK: brand-name  | rel:defined-as  | brainroot | stability:permanent
LINK: brand-color | rel:defined-as  | indigo    | stability:permanent

# ── Historical: kai worked on orion before nova ───────────────────────────────

LINK: kai | rel:works-on | orion | valid_from:2025-06 | ended:2026-03 | stability:transient

# ── Decisions with temporal fields ───────────────────────────────────────────

DECISION: deploy-target | vercel>railway | cost+dx | 2026-01 | stability:stable
DECISION: auth-provider | clerk>auth0    | sdk-simplicity | 2026-02 | stability:stable
DECISION: db             | postgres>sqlite | concurrent-writes | 2026-01 | stability:stable

# ── Rules ────────────────────────────────────────────────────────────────────

RULE: brand-name | never-change-without-legal-review | hard | stability:permanent
RULE: deploy     | never-push-breaking-changes-on-friday | hard
