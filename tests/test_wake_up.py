"""Tests for smalltalk.wake_up — L1 context builder."""
from pathlib import Path

import pytest

from wake_up import build_wake_up_context


class TestWakeUpBasic:
    def test_empty_dir_returns_string(self, tmp_path):
        result = build_wake_up_context(tmp_path)
        assert isinstance(result, str)

    def test_includes_decision(self, tmp_path):
        (tmp_path / "d.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "deploy" in result
        assert "DECISION" in result

    def test_includes_hard_rule(self, tmp_path):
        (tmp_path / "r.st").write_text(
            "RULE: brand | no-purple | hard\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "brand" in result

    def test_includes_pattern(self, tmp_path):
        (tmp_path / "p.st").write_text(
            "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "jwt" in result

    def test_includes_repeatable_win(self, tmp_path):
        (tmp_path / "w.st").write_text(
            "WIN: palace | score-wing | 34pct-boost | repeat:y\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "palace" in result

    def test_excludes_ended_entry(self, tmp_path):
        (tmp_path / "x.st").write_text(
            "DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        # The ended decision should be excluded from the wake-up output
        assert "vercel>railway" not in result

    def test_permanent_stability_loads(self, tmp_path):
        (tmp_path / "x.st").write_text(
            "RULE: brand | core-truth | hard | stability:permanent\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "brand" in result

    def test_result_is_compact(self, tmp_path):
        """Wake-up output should be much shorter than raw prose."""
        lines = []
        for i in range(10):
            lines.append(f"DECISION: topic-{i} | choice-a>choice-b | reason-{i} | 2026-04\n")
        (tmp_path / "x.st").write_text("".join(lines), encoding="utf-8")
        result = build_wake_up_context(tmp_path)
        # Should contain all 10 decisions but be a manageable size
        assert result.count("DECISION") >= 10
        # Each entry is one line — no prose expansion
        assert len(result) < 5000

    def test_non_repeating_win_excluded(self, tmp_path):
        (tmp_path / "w.st").write_text(
            "WIN: one-off | technique | outcome | repeat:n\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "one-off" not in result

    def test_soft_rule_may_be_excluded(self, tmp_path):
        """Soft rules are lower priority — hard rules should always appear."""
        (tmp_path / "r.st").write_text(
            "RULE: important | must-do | hard\n"
            "RULE: optional | nice-to-do | soft\n",
            encoding="utf-8"
        )
        result = build_wake_up_context(tmp_path)
        assert "important" in result
