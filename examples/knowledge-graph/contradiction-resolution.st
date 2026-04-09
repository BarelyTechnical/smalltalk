# Smalltalk v3.0.0 — KG example: contradiction resolution
# A worked example of the detect → resolve → confirm cycle.
#
# BEFORE resolution (run `smalltalk check` on this file — it will flag two conflicts):
#
#   [CRITICAL] LINK: brand-color | simultaneous-defined-as  |  purple | indigo
#   [WARNING]  DECISION: deploy | diverging-choices  |  railway>vercel | vercel>railway
#
# AFTER resolution (this file shows the resolved state):
#
#   Run:  smalltalk kg invalidate contradiction-example.st 23
#   Run:  smalltalk kg invalidate contradiction-example.st 27
#   Then: smalltalk check .  →  OK  No active contradictions detected.

# ── Brand color — resolved correctly ─────────────────────────────────────────
# Old value had ended: added via: smalltalk kg invalidate <file> <line>
LINK: brand-color | rel:defined-as | purple | stability:permanent | ended:2026-04
# New value — the active truth
LINK: brand-color | rel:defined-as | indigo | stability:permanent | valid_from:2026-04

# ── Deploy target — resolved correctly ───────────────────────────────────────
# Old decision was closed via: smalltalk kg invalidate <file> <line>
DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04
# New decision — the active truth
DECISION: deploy | railway>vercel | scale | 2026-04

# ── These are still active (background context, no conflict) ─────────────────
LINK: kai | rel:works-on  | nova  | valid_from:2026-03 | stability:transient
LINK: kai | rel:member-of | team  | valid_from:2025-06 | stability:stable
RULE: brand-name | never-change-without-legal-review | hard | stability:permanent
