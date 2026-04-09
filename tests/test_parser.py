"""Tests for parser.py — the .st file reader."""
import pytest
from pathlib import Path

from smalltalk.parser import parse_st_files, ST_LINE_PATTERN


# ── Helpers ───────────────────────────────────────────────────────────────────

def write(tmp_path, filename, content):
    f = tmp_path / filename
    f.write_text(content, encoding="utf-8")
    return f


# ── ST_LINE_PATTERN ───────────────────────────────────────────────────────────

class TestLinePattern:
    def test_matches_basic_entry(self):
        m = ST_LINE_PATTERN.match("RULE: auth | never-store-plaintext | hard")
        assert m is not None
        assert m.group(1) == "RULE"
        assert m.group(2) == "auth"

    def test_does_not_match_comment(self):
        assert ST_LINE_PATTERN.match("# this is a comment") is None

    def test_does_not_match_blank(self):
        assert ST_LINE_PATTERN.match("") is None

    def test_does_not_match_lowercase_type(self):
        assert ST_LINE_PATTERN.match("rule: auth | x | hard") is None


# ── parse_st_files — directory ────────────────────────────────────────────────

class TestParseStFilesDirectory:
    def test_reads_st_files(self, tmp_path):
        write(tmp_path, "a.st", "RULE: auth | no-plaintext | hard\n")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1
        assert entries[0]["type"] == "RULE"

    def test_ignores_non_st_files(self, tmp_path):
        write(tmp_path, "notes.md", "RULE: auth | no-plaintext | hard\n")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 0

    def test_ignores_blank_lines(self, tmp_path):
        write(tmp_path, "brain.st", "\nRULE: a | b | c\n\n")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1

    def test_ignores_comment_lines(self, tmp_path):
        write(tmp_path, "brain.st", "# comment\nRULE: a | b | c\n# another")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1

    def test_reads_multiple_files(self, tmp_path):
        write(tmp_path, "a.st", "RULE: x | y | hard\n")
        write(tmp_path, "b.st", "DECISION: db | pg>sqlite | scale | 2026-01\n")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 2

    def test_correct_line_numbers(self, tmp_path):
        write(tmp_path, "brain.st",
              "# comment\n"
              "RULE: a | b\n"
              "DECISION: x | y>z | reason | 2026-01\n")
        entries = parse_st_files(tmp_path)
        assert entries[0]["line_no"] == 2
        assert entries[1]["line_no"] == 3

    def test_multiple_entry_types(self, tmp_path):
        write(tmp_path, "brain.st",
              "DECISION: db | pg>sqlite | scale | 2026-01\n"
              "RULE: api | no-raw-sql | hard\n"
              "PATTERN: auth | broke:timeout | cause:missing-exp | fix:add-exp | reuse:y\n"
              "WIN: schema-first | no-surprises | repeat:y\n"
              "LINK: app | rel:depends | auth | stability:stable\n")
        entries = parse_st_files(tmp_path)
        types = {e["type"] for e in entries}
        assert {"DECISION", "RULE", "PATTERN", "WIN", "LINK"} == types

    def test_raw_field_preserved(self, tmp_path):
        line = "RULE: auth | never-store-plaintext | hard"
        write(tmp_path, "brain.st", line + "\n")
        entries = parse_st_files(tmp_path)
        assert entries[0]["raw"] == line

    def test_fields_stripped(self, tmp_path):
        write(tmp_path, "brain.st", "RULE: auth |  has-spaces  |  hard  ")
        entries = parse_st_files(tmp_path)
        assert entries[0]["fields"][0] == "has-spaces"
        assert entries[0]["fields"][1] == "hard"

    def test_file_path_set_correctly(self, tmp_path):
        write(tmp_path, "brain.st", "RULE: x | y | hard\n")
        entries = parse_st_files(tmp_path)
        assert Path(entries[0]["file"]).name == "brain.st"

    def test_reads_recursive(self, tmp_path):
        subdir = tmp_path / "sub"
        subdir.mkdir()
        write(subdir, "deep.st", "RULE: x | y | hard\n")
        entries = parse_st_files(tmp_path)
        assert len(entries) == 1


# ── parse_st_files — single file ─────────────────────────────────────────────

class TestParseStFilesSingleFile:
    def test_accepts_file_path_directly(self, tmp_path):
        f = write(tmp_path, "single.st", "RULE: a | b | hard\n")
        entries = parse_st_files(f)
        assert len(entries) == 1

    def test_rejects_non_st_file(self, tmp_path):
        f = write(tmp_path, "notes.md", "RULE: a | b | hard\n")
        entries = parse_st_files(f)
        assert len(entries) == 0

    def test_returns_empty_for_nonexistent_path(self, tmp_path):
        entries = parse_st_files(tmp_path / "ghost.st")
        assert entries == []
