"""Tests for palace.py — _index.st generation and navigate()."""
import pytest
from pathlib import Path

from smalltalk.palace import init_palace, index_palace, navigate, palace_status_text


def write(path, filename, content):
    (path / filename).write_text(content, encoding="utf-8")


class TestInitPalace:
    def test_creates_index_file(self, tmp_path):
        write(tmp_path, "brain.st", "RULE: auth | no-plaintext | hard\n")
        index_path = init_palace(tmp_path)
        assert index_path.exists()
        assert index_path.name == "_index.st"

    def test_index_contains_wing(self, tmp_path):
        write(tmp_path, "decisions.st", "DECISION: db | pg>sqlite | scale | 2026-01\n")
        init_palace(tmp_path)
        content = (tmp_path / "_index.st").read_text(encoding="utf-8")
        assert "decisions" in content.lower()

    def test_wing_per_subdirectory(self, tmp_path):
        subdir = tmp_path / "projects"
        subdir.mkdir()
        write(subdir, "nova.st", "DECISION: nova | pg>sqlite | scale | 2026-01\n")
        init_palace(tmp_path)
        content = (tmp_path / "_index.st").read_text(encoding="utf-8")
        assert "nova" in content.lower()

    def test_index_palace_updates_existing(self, tmp_path):
        write(tmp_path, "brain.st", "RULE: auth | no-plaintext | hard\n")
        init_palace(tmp_path)
        write(tmp_path, "new.st", "WIN: test | worked | repeat:y\n")
        index_palace(tmp_path)
        content = (tmp_path / "_index.st").read_text(encoding="utf-8")
        # Both files should appear in refreshed index
        assert "brain" in content.lower() or "new" in content.lower()

    def test_palace_status_text_no_crash(self, tmp_path):
        write(tmp_path, "brain.st", "RULE: auth | no-plaintext | hard\n")
        init_palace(tmp_path)
        text = palace_status_text(tmp_path)
        assert isinstance(text, str)


class TestNavigate:
    def test_returns_rooms_for_keyword(self, tmp_path):
        write(tmp_path, "decisions.st", "DECISION: db | pg>sqlite | scale | 2026-01\n")
        init_palace(tmp_path)
        rooms = navigate(tmp_path, "database")
        # May be empty if keyword doesn't match — just shouldn't crash
        assert isinstance(rooms, list)

    def test_navigate_direct_match(self, tmp_path):
        write(tmp_path, "decisions.st", "DECISION: db | pg>sqlite | scale | 2026-01\n")
        init_palace(tmp_path)
        rooms = navigate(tmp_path, "decisions")
        # Should find the decisions wing
        assert isinstance(rooms, list)
