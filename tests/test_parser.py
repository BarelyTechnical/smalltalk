"""Tests for smalltalk.parser — .st file parsing."""
import textwrap
from pathlib import Path

import pytest

from parser import parse_st_files


@pytest.fixture
def tmp_st(tmp_path):
    """Helper: write a .st file and return its path."""
    def _write(name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(textwrap.dedent(content), encoding="utf-8")
        return p
    return _write


class TestParseBasicTypes:
    def test_parse_rule(self, tmp_st):
        tmp_st("test.st", """\
            RULE: brand | no-purple-gradient | hard
        """)
        entries = parse_st_files(tmp_st.__self__.tmp_path if hasattr(tmp_st, '__self__') else Path(tmp_st("x.st", "").parent))
        # Use direct path
        p = Path(tmp_st("basic.st", "RULE: brand | no-purple-gradient | hard\n").parent)
        entries = parse_st_files(p)
        rules = [e for e in entries if e["type"] == "RULE"]
        assert len(rules) >= 1
        assert rules[-1]["subject"] == "brand"

    def test_parse_decision(self, tmp_path):
        f = tmp_path / "decisions.st"
        f.write_text("DECISION: deploy | railway>vercel | scale | 2026-04\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        decisions = [e for e in entries if e["type"] == "DECISION"]
        assert len(decisions) == 1
        assert decisions[0]["subject"] == "deploy"
        assert "railway>vercel" in decisions[0]["fields"]

    def test_parse_pattern(self, tmp_path):
        f = tmp_path / "p.st"
        f.write_text("PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        patterns = [e for e in entries if e["type"] == "PATTERN"]
        assert len(patterns) == 1
        assert patterns[0]["subject"] == "jwt"

    def test_parse_win(self, tmp_path):
        f = tmp_path / "w.st"
        f.write_text("WIN: palace | score-wing-room | 34pct-boost | repeat:y\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        wins = [e for e in entries if e["type"] == "WIN"]
        assert len(wins) == 1

    def test_parse_link(self, tmp_path):
        f = tmp_path / "kg.st"
        f.write_text(
            "LINK: kai | rel:works-on | nova | valid_from:2026-03 | stability:transient\n",
            encoding="utf-8"
        )
        entries = parse_st_files(tmp_path)
        links = [e for e in entries if e["type"] == "LINK"]
        assert len(links) == 1
        assert links[0]["subject"] == "kai"

    def test_parse_skill(self, tmp_path):
        f = tmp_path / "skills.st"
        f.write_text("SKILL: hunt | when:bug+error | stack:root-cause | version:1\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        skills = [e for e in entries if e["type"] == "SKILL"]
        assert len(skills) == 1
        assert skills[0]["subject"] == "hunt"

    def test_ignore_comments(self, tmp_path):
        f = tmp_path / "c.st"
        f.write_text("# this is a comment\nRULE: x | y | hard\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert all(e["type"] != "#" for e in entries)
        assert len(entries) == 1

    def test_ignore_blank_lines(self, tmp_path):
        f = tmp_path / "b.st"
        f.write_text("\n\nRULE: x | y | hard\n\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1

    def test_multiple_files(self, tmp_path):
        (tmp_path / "a.st").write_text("RULE: a | desc | hard\n", encoding="utf-8")
        (tmp_path / "b.st").write_text("DECISION: b | x>y | reason | 2026-01\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 2
        types = {e["type"] for e in entries}
        assert types == {"RULE", "DECISION"}

    def test_entry_has_file_field(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text("NOTE: tip | something useful\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert "file" in entries[0]
        assert entries[0]["file"] == str(f)

    def test_recursive_subdirs(self, tmp_path):
        sub = tmp_path / "subdir"
        sub.mkdir()
        (sub / "nested.st").write_text("WIN: x | technique | outcome | repeat:y\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1

    def test_skip_non_st_files(self, tmp_path):
        (tmp_path / "notes.md").write_text("RULE: this | should | be-ignored\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 0

    def test_ended_field_parsed(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text("DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04\n", encoding="utf-8")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1
        # ended field should be accessible
        fields_str = " ".join(entries[0].get("fields", []))
        assert "ended:2026-04" in fields_str
