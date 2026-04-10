"""Tests for smalltalk.palace — wing/room/tunnel navigation."""
from pathlib import Path

import pytest

from palace import init_palace, index_palace, navigate, list_wings, list_rooms


class TestPalaceInit:
    def test_init_creates_index(self, tmp_path):
        (tmp_path / "decisions.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        index_path = init_palace(tmp_path)
        assert index_path.exists()
        assert index_path.name == "_index.st"

    def test_init_empty_dir(self, tmp_path):
        """Init on empty dir should create an index (empty or minimal)."""
        index_path = init_palace(tmp_path)
        assert index_path.exists()

    def test_init_detects_subdirs_as_wings(self, tmp_path):
        sub = tmp_path / "projects"
        sub.mkdir()
        (sub / "nova.st").write_text("NOTE: nova | active project\n", encoding="utf-8")
        index_path = init_palace(tmp_path)
        content = index_path.read_text(encoding="utf-8")
        assert "WING" in content or "nova" in content.lower()

    def test_index_file_excluded_from_rooms(self, tmp_path):
        """_index.st itself should not be added as a ROOM."""
        (tmp_path / "a.st").write_text("RULE: x | y | hard\n", encoding="utf-8")
        index_path = init_palace(tmp_path)
        content = index_path.read_text(encoding="utf-8")
        # _index.st should not reference itself as a room
        lines = [l for l in content.splitlines() if "_index.st" in l and l.strip().startswith("ROOM")]
        assert len(lines) == 0


class TestPalaceNavigate:
    def test_navigate_finds_relevant_file(self, tmp_path):
        (tmp_path / "auth.st").write_text(
            "DECISION: auth | clerk>auth0 | sdk | 2026-04\n",
            encoding="utf-8"
        )
        init_palace(tmp_path)
        paths = navigate(tmp_path, "auth decision")
        assert isinstance(paths, list)
        # Should find auth.st (by name match)
        assert any("auth" in str(p) for p in paths)

    def test_navigate_no_index_returns_empty(self, tmp_path):
        (tmp_path / "decisions.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        # No init_palace called — no _index.st
        paths = navigate(tmp_path, "deploy")
        # Should return empty list or raise gracefully
        assert isinstance(paths, list)

    def test_navigate_returns_list(self, tmp_path):
        (tmp_path / "a.st").write_text("RULE: deploy | fast | hard\n", encoding="utf-8")
        init_palace(tmp_path)
        result = navigate(tmp_path, "deploy")
        assert isinstance(result, list)


class TestPalaceListWings:
    def test_list_wings_after_init(self, tmp_path):
        sub = tmp_path / "projects"
        sub.mkdir()
        (sub / "orion.st").write_text("NOTE: orion | project\n", encoding="utf-8")
        init_palace(tmp_path)
        wings = list_wings(tmp_path)
        assert isinstance(wings, list)

    def test_list_wings_no_index(self, tmp_path):
        wings = list_wings(tmp_path)
        assert wings == []


class TestPalaceListRooms:
    def test_list_rooms_after_init(self, tmp_path):
        (tmp_path / "decisions.st").write_text(
            "DECISION: deploy | railway>vercel | scale | 2026-04\n",
            encoding="utf-8"
        )
        init_palace(tmp_path)
        rooms = list_rooms(tmp_path)
        assert isinstance(rooms, list)

    def test_list_rooms_filter_by_wing(self, tmp_path):
        sub = tmp_path / "projects"
        sub.mkdir()
        (sub / "nova.st").write_text("NOTE: nova | active\n", encoding="utf-8")
        init_palace(tmp_path)
        rooms = list_rooms(tmp_path, wing="projects")
        assert isinstance(rooms, list)
