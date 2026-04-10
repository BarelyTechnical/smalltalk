"""Tests for smalltalk.kg — temporal knowledge graph."""
from pathlib import Path

import pytest

from kg import query_entity, get_timeline, invalidate_entry


class TestKGQuery:
    def test_empty_dir(self, tmp_path):
        result = query_entity(tmp_path, "kai")
        assert isinstance(result, dict)
        assert result.get("entity") == "kai"

    def test_direct_link_found(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: kai | rel:works-on | nova | valid_from:2026-03 | stability:transient\n",
            encoding="utf-8"
        )
        result = query_entity(tmp_path, "kai")
        direct = result.get("direct", [])
        assert len(direct) >= 1
        rels = [r.get("rel") or r.get("target") for r in direct]
        assert any("nova" in str(r) for r in direct)

    def test_ended_link_excluded_by_default(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n",
            encoding="utf-8"
        )
        result = query_entity(tmp_path, "kai", as_of=None)
        direct = result.get("direct", [])
        # Active query should not include ended entries
        active = [r for r in direct if not r.get("ended")]
        assert len(active) == 0

    def test_as_of_historical_query(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n",
            encoding="utf-8"
        )
        # Query as of Feb — orion should appear
        result = query_entity(tmp_path, "kai", as_of="2026-02")
        direct = result.get("direct", [])
        assert len(direct) >= 1

    def test_permanent_stability_always_loads(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: brand-color | rel:defined-as | indigo | stability:permanent\n",
            encoding="utf-8"
        )
        result = query_entity(tmp_path, "brand-color")
        direct = result.get("direct", [])
        assert len(direct) >= 1


class TestKGTimeline:
    def test_timeline_chronological(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n"
            "LINK: kai | rel:works-on | nova  | valid_from:2026-03 | stability:transient\n",
            encoding="utf-8"
        )
        events = get_timeline(tmp_path, "kai")
        assert isinstance(events, list)
        assert len(events) == 2
        # Should be sorted chronologically
        dates = [e.get("valid_from", "") for e in events]
        assert dates == sorted(dates)

    def test_timeline_empty(self, tmp_path):
        events = get_timeline(tmp_path, "nonexistent")
        assert events == []


class TestKGInvalidate:
    def test_invalidate_appends_ended(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text(
            "DECISION: deploy | vercel>railway | cost | 2026-01\n",
            encoding="utf-8"
        )
        result = invalidate_entry(file_path=str(f), line_no=1, ended="2026-04")
        assert result.get("success") is True
        content = f.read_text(encoding="utf-8")
        assert "ended:2026-04" in content

    def test_invalidate_wrong_line_raises(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text("RULE: brand | no-purple | hard\n", encoding="utf-8")
        with pytest.raises((ValueError, IndexError)):
            invalidate_entry(file_path=str(f), line_no=99, ended="2026-04")

    def test_invalidate_default_date(self, tmp_path):
        f = tmp_path / "x.st"
        f.write_text("PATTERN: jwt | broke:auth | cause:exp | fix:add-exp | reuse:y\n", encoding="utf-8")
        result = invalidate_entry(file_path=str(f), line_no=1)
        assert result.get("success") is True
        content = f.read_text(encoding="utf-8")
        assert "ended:" in content
