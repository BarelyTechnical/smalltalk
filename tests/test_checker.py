"""Tests for checker.py — contradiction detection across all entry types."""
import pytest
from pathlib import Path

from smalltalk.checker import check_contradictions, format_check_results


# ── Helpers ───────────────────────────────────────────────────────────────────

def write(tmp_path, filename, content):
    (tmp_path / filename).write_text(content, encoding="utf-8")
    return tmp_path / filename


# ── No-conflict baseline ──────────────────────────────────────────────────────

class TestNoConflicts:
    def test_empty_dir(self, tmp_path):
        assert check_contradictions(tmp_path) == []

    def test_single_active_decision(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01\n")
        assert check_contradictions(tmp_path) == []

    def test_historical_entry_not_flagged(self, tmp_path):
        # ended: entry should NOT be compared against the active one
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04\n"
              "DECISION: deploy | railway>vercel | scale | 2026-04\n")
        assert check_contradictions(tmp_path, as_of="2026-04") == []

    def test_format_clean(self, tmp_path):
        output = format_check_results([], tmp_path)
        assert "No active contradictions" in output


# ── DECISION contradictions ───────────────────────────────────────────────────

class TestDecisionConflicts:
    def test_two_active_decisions(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01\n"
              "DECISION: deploy | railway>vercel | scale | 2026-04\n")
        conflicts = check_contradictions(tmp_path)
        assert len(conflicts) == 1
        assert conflicts[0]["type"] == "DECISION"
        assert conflicts[0]["conflict_type"] == "diverging-choices"

    def test_same_choice_no_conflict(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01\n"
              "DECISION: deploy | vercel>railway | also | 2026-02\n")
        assert check_contradictions(tmp_path) == []

    def test_severity_is_warning_by_default(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: db | pg>sqlite | scale | 2026-01\n"
              "DECISION: db | sqlite>pg | simple | 2026-02\n")
        conflicts = check_contradictions(tmp_path)
        assert conflicts[0]["severity"] == "WARNING"

    def test_permanent_decision_is_critical(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: brand | mono>multi | cost | 2026-01 | stability:permanent\n"
              "DECISION: brand | multi>mono | growth | 2026-04\n")
        conflicts = check_contradictions(tmp_path)
        assert conflicts[0]["severity"] == "CRITICAL"

    def test_older_newer_correctly_identified(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01\n"
              "DECISION: deploy | railway>vercel | scale | 2026-04\n")
        conflicts = check_contradictions(tmp_path)
        # older = vercel>railway (2026-01), newer = railway>vercel (2026-04)
        assert "vercel>railway" in conflicts[0]["older"]["raw"]
        assert "railway>vercel" in conflicts[0]["newer"]["raw"]


# ── RULE contradictions ───────────────────────────────────────────────────────

class TestRuleConflicts:
    def test_hard_vs_soft(self, tmp_path):
        write(tmp_path, "brain.st",
              "RULE: deploy | no-friday-deploys | hard\n"
              "RULE: deploy | no-friday-deploys | soft\n")
        conflicts = check_contradictions(tmp_path)
        assert len(conflicts) == 1
        assert conflicts[0]["conflict_type"] == "strength-conflict"

    def test_two_hard_no_conflict(self, tmp_path):
        write(tmp_path, "brain.st",
              "RULE: deploy | no-friday-deploys | hard\n"
              "RULE: deploy | run-tests-first   | hard\n")
        # Different rule descriptions — same subject but no strength conflict
        assert check_contradictions(tmp_path) == []

    def test_two_soft_no_conflict(self, tmp_path):
        write(tmp_path, "brain.st",
              "RULE: api | prefer-rest | soft\n"
              "RULE: api | prefer-graphql | soft\n")
        # Both soft — no strength conflict (content conflict is handled manually)
        assert check_contradictions(tmp_path) == []


# ── PATTERN contradictions ────────────────────────────────────────────────────

class TestPatternConflicts:
    def test_same_cause_different_fixes(self, tmp_path):
        write(tmp_path, "brain.st",
              "PATTERN: auth | broke:timeout | cause:missing-exp | fix:add-exp | reuse:y\n"
              "PATTERN: auth | broke:timeout | cause:missing-exp | fix:refresh-token | reuse:y\n")
        conflicts = check_contradictions(tmp_path)
        assert len(conflicts) == 1
        assert conflicts[0]["conflict_type"] == "conflicting-fixes"

    def test_different_causes_no_conflict(self, tmp_path):
        write(tmp_path, "brain.st",
              "PATTERN: auth | broke:timeout | cause:missing-exp | fix:add-exp | reuse:y\n"
              "PATTERN: auth | broke:crash   | cause:null-ref     | fix:null-check | reuse:y\n")
        assert check_contradictions(tmp_path) == []


# ── WIN contradictions ────────────────────────────────────────────────────────

class TestWinConflicts:
    def test_repeat_y_and_n(self, tmp_path):
        write(tmp_path, "brain.st",
              "WIN: dry-run | preview-first | no-prod-accidents | repeat:y\n"
              "WIN: dry-run | preview-first | slow-workflow | repeat:n\n")
        conflicts = check_contradictions(tmp_path)
        assert len(conflicts) == 1
        assert conflicts[0]["conflict_type"] == "repeat-conflict"

    def test_two_repeat_y_no_conflict(self, tmp_path):
        write(tmp_path, "brain.st",
              "WIN: dry-run | approach-a | result-a | repeat:y\n"
              "WIN: dry-run | approach-b | result-b | repeat:y\n")
        assert check_contradictions(tmp_path) == []


# ── LINK overlap detection ────────────────────────────────────────────────────

class TestLinkConflicts:
    def test_simultaneous_exclusive_rel(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01\n"
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n")
        conflicts = check_contradictions(tmp_path)
        assert any(c["type"] == "LINK" for c in conflicts)

    def test_exclusive_rel_is_critical(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01\n"
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n")
        conflicts = check_contradictions(tmp_path)
        link_conflicts = [c for c in conflicts if c["type"] == "LINK"]
        assert link_conflicts[0]["severity"] == "CRITICAL"

    def test_non_exclusive_rel_not_flagged(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:member-of | team   | valid_from:2025-06\n"
              "LINK: kai | rel:member-of | guild  | valid_from:2025-09\n")
        conflicts = check_contradictions(tmp_path)
        assert all(c["type"] != "LINK" for c in conflicts)

    def test_properly_split_with_ended_not_flagged(self, tmp_path):
        # orion has ended: — kai correctly moved to nova. Not a conflict.
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n"
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n")
        conflicts = check_contradictions(tmp_path)
        assert all(c["type"] != "LINK" for c in conflicts)


# ── Full resolution cycle ─────────────────────────────────────────────────────

class TestResolutionCycle:
    def test_detect_resolve_confirm(self, tmp_path):
        from smalltalk.kg import invalidate_entry

        f = write(tmp_path, "brain.st",
                  "DECISION: deploy | vercel>railway | cost | 2026-01\n"
                  "DECISION: deploy | railway>vercel | scale | 2026-04\n")

        # Step 1: detect
        before = check_contradictions(tmp_path)
        assert len(before) == 1
        older = before[0]["older"]
        assert older["line_no"] == 1

        # Step 2: resolve
        invalidate_entry(str(f), older["line_no"], ended="2026-04")

        # Step 3: confirm
        after = check_contradictions(tmp_path)
        assert len(after) == 0

    def test_link_resolve_cycle(self, tmp_path):
        from smalltalk.kg import invalidate_entry

        f = write(tmp_path, "brain.st",
                  "LINK: kai | rel:works-on | orion | valid_from:2026-01\n"
                  "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n")

        before = check_contradictions(tmp_path)
        link_conflicts = [c for c in before if c["type"] == "LINK"]
        assert len(link_conflicts) == 1

        invalidate_entry(str(f), link_conflicts[0]["older"]["line_no"], ended="2026-04")

        after = check_contradictions(tmp_path)
        assert all(c["type"] != "LINK" for c in after)


# ── format_check_results ──────────────────────────────────────────────────────

class TestFormatCheckResults:
    def test_critical_before_warning(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: x | a>b | r | 2026-01 | stability:permanent\n"
              "DECISION: x | b>a | r | 2026-04\n"
              "RULE: y | rule-a | hard\n"
              "RULE: y | rule-a | soft\n")
        conflicts = check_contradictions(tmp_path)
        output = format_check_results(conflicts, tmp_path)
        crit_pos = output.find("CRITICAL")
        warn_pos = output.find("WARNING")
        assert crit_pos < warn_pos

    def test_shows_file_and_line(self, tmp_path):
        write(tmp_path, "data.st",
              "DECISION: db | pg>sqlite | scale | 2026-01\n"
              "DECISION: db | sqlite>pg | simple | 2026-02\n")
        conflicts = check_contradictions(tmp_path)
        output = format_check_results(conflicts, tmp_path)
        assert "data.st" in output
