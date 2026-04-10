"""Tests for smalltalk.checker — contradiction detection."""
from pathlib import Path

import pytest

from checker import check_contradictions


class TestDecisionContradictions:
    def test_no_contradiction_single_decision(self, tmp_path):
        (tmp_path / "a.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] == 0

    def test_decision_contradiction_detected(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "DECISION: deploy | vercel>railway | cost | 2026-01\n"
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] >= 1
        types = [c["type"] for c in results.get("contradictions", [])]
        assert "DECISION" in types

    def test_ended_entry_not_flagged(self, tmp_path):
        """An ended: entry should not trigger a contradiction."""
        f = tmp_path / "x.st"
        f.write_text(
            "DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04\n"
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] == 0

    def test_same_decision_same_value_no_conflict(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "DECISION: auth | clerk>auth0 | sdk | 2026-01\n"
            "DECISION: auth | clerk>auth0 | confirmed | 2026-04\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] == 0


class TestRuleContradictions:
    def test_rule_hardness_conflict(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "RULE: brand | no-purple | hard\n"
            "RULE: brand | no-purple | soft\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] >= 1

    def test_rule_no_conflict_same_hardness(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "RULE: brand | no-purple | hard\n"
            "RULE: brand | no-purple | hard\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] == 0


class TestPatternContradictions:
    def test_pattern_conflicting_fix(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp | reuse:y\n"
            "PATTERN: jwt | broke:auth | cause:missing-exp | fix:use-refresh | reuse:y\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] >= 1

    def test_pattern_no_conflict_different_cause(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp | reuse:y\n"
            "PATTERN: jwt | broke:auth | cause:wrong-secret | fix:rotate-secret | reuse:y\n",
            encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] == 0


class TestEmptyDir:
    def test_empty_directory(self, tmp_path):
        results = check_contradictions(tmp_path)
        assert results["total"] == 0

    def test_no_st_files(self, tmp_path):
        (tmp_path / "notes.md").write_text("some text\n", encoding="utf-8")
        results = check_contradictions(tmp_path)
        assert results["total"] == 0

    def test_cross_file_contradiction(self, tmp_path):
        (tmp_path / "a.st").write_text(
            "DECISION: deploy | vercel>railway | cost | 2026-01\n", encoding="utf-8"
        )
        (tmp_path / "b.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n", encoding="utf-8"
        )
        results = check_contradictions(tmp_path)
        assert results["total"] >= 1
