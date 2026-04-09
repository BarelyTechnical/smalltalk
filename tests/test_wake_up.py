"""Tests for wake_up.py — L1 context builder."""
import pytest
from pathlib import Path

from smalltalk.wake_up import build_wake_up_context


def write(tmp_path, filename, content):
    (tmp_path / filename).write_text(content, encoding="utf-8")


class TestWakeUp:
    def test_empty_dir(self, tmp_path):
        ctx = build_wake_up_context(tmp_path)
        # Empty dir returns a helpful message — just shouldn't crash or return None
        assert isinstance(ctx, str)

    def test_loads_active_decision(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | 2026-01\n")
        ctx = build_wake_up_context(tmp_path)
        assert "DECISION" in ctx
        assert "deploy" in ctx

    def test_excludes_ended_entry(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | ended:2020-01\n")
        ctx = build_wake_up_context(tmp_path)
        assert "vercel>railway" not in ctx

    def test_excludes_future_valid_from(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: deploy | vercel>railway | cost | valid_from:2099-01\n")
        ctx = build_wake_up_context(tmp_path)
        assert "vercel>railway" not in ctx

    def test_permanent_entries_appear_first(self, tmp_path):
        write(tmp_path, "brain.st",
              "RULE: brand | never-change | hard\n"
              "RULE: brand | never-change | hard | stability:permanent\n"
              "DECISION: db | pg>sqlite | scale | 2026-01\n")
        ctx = build_wake_up_context(tmp_path)
        perm_pos = ctx.find("permanent")
        dec_pos = ctx.find("DECISION")
        assert perm_pos < dec_pos

    def test_only_loads_hard_rules(self, tmp_path):
        write(tmp_path, "brain.st",
              "RULE: style | prefer-tabs   | soft\n"
              "RULE: style | no-raw-sql    | hard\n")
        ctx = build_wake_up_context(tmp_path)
        assert "no-raw-sql" in ctx
        assert "prefer-tabs" not in ctx

    def test_only_repeat_y_wins(self, tmp_path):
        write(tmp_path, "brain.st",
              "WIN: dry-run | preview | no-accidents | repeat:y\n"
              "WIN: other   | thing   | result       | repeat:n\n")
        ctx = build_wake_up_context(tmp_path)
        assert "dry-run" in ctx
        assert "other" not in ctx
