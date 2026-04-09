"""Tests for kg.py — temporal validity, graph building, entity queries, invalidate."""
import pytest
from pathlib import Path
from datetime import datetime

from smalltalk.kg import (
    is_currently_valid,
    get_stability,
    build_graph,
    query_entity,
    get_timeline,
    invalidate_entry,
    format_entity_query,
    format_timeline,
    format_invalidate_result,
    _today,
    _is_valid_date,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_entry(fields, entry_type="DECISION", subject="test", file="test.st", line=1):
    return {
        "type": entry_type,
        "subject": subject,
        "fields": fields,
        "raw": f"{entry_type}: {subject} | ...",
        "file": file,
        "line_no": line,
    }


def write(tmp_path, filename, content):
    (tmp_path / filename).write_text(content, encoding="utf-8")
    return tmp_path / filename


# ── _is_valid_date ────────────────────────────────────────────────────────────

class TestIsValidDate:
    def test_valid_yyyy_mm(self):
        assert _is_valid_date("2026-04") is True

    def test_valid_yyyy_mm_dd(self):
        assert _is_valid_date("2026-04-09") is True

    def test_invalid_word(self):
        assert _is_valid_date("soon") is False

    def test_invalid_short(self):
        assert _is_valid_date("26-04") is False

    def test_invalid_empty(self):
        assert _is_valid_date("") is False

    def test_invalid_tbd(self):
        assert _is_valid_date("TBD") is False


# ── is_currently_valid ────────────────────────────────────────────────────────

class TestIsCurrentlyValid:
    def test_no_temporal_fields(self):
        assert is_currently_valid(make_entry([])) is True

    def test_past_ended(self):
        assert is_currently_valid(make_entry(["ended:2020-01"])) is False

    def test_future_ended(self):
        assert is_currently_valid(make_entry(["ended:2099-01"])) is True

    def test_past_valid_from(self):
        assert is_currently_valid(make_entry(["valid_from:2020-01"])) is True

    def test_future_valid_from(self):
        assert is_currently_valid(make_entry(["valid_from:2099-01"])) is False

    def test_permanent_no_ended(self):
        assert is_currently_valid(make_entry(["stability:permanent"])) is True

    def test_permanent_with_past_ended(self):
        assert is_currently_valid(
            make_entry(["stability:permanent", "ended:2020-01"])
        ) is False

    def test_malformed_date_ignored(self):
        # 'soon' is not a valid date — should be treated as if the field isn't there
        assert is_currently_valid(make_entry(["ended:soon"])) is True

    def test_as_of_override(self):
        # Entry started 2026-03. With as_of=2026-02 it should not yet be valid.
        e = make_entry(["valid_from:2026-03"])
        assert is_currently_valid(e, as_of="2026-02") is False
        assert is_currently_valid(e, as_of="2026-04") is True


# ── get_stability ─────────────────────────────────────────────────────────────

class TestGetStability:
    def test_default_stable(self):
        assert get_stability(make_entry([])) == "stable"

    def test_permanent(self):
        assert get_stability(make_entry(["stability:permanent"])) == "permanent"

    def test_transient(self):
        assert get_stability(make_entry(["stability:transient"])) == "transient"


# ── build_graph + query_entity ────────────────────────────────────────────────

class TestBuildGraph:
    def test_empty_directory(self, tmp_path):
        graph = build_graph(tmp_path)
        assert graph == {}

    def test_basic_link(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | nova | valid_from:2026-03 | stability:transient\n")
        graph = build_graph(tmp_path)
        assert "kai" in graph
        assert graph["kai"][0]["target"] == "nova"

    def test_historical_link_appears_in_graph(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n")
        graph = build_graph(tmp_path)
        # Historical entries still appear in graph — just marked as not active
        assert "kai" in graph
        assert graph["kai"][0]["ended"] == "2026-03"

    def test_as_of_filters_correctly(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n"
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n")
        # At 2026-02, kai works-on orion (nova hasn't started yet)
        graph_past = build_graph(tmp_path, as_of="2026-02")
        targets = {edge["target"] for edge in graph_past.get("kai", [])}
        assert "orion" in targets
        assert "nova" not in targets


class TestQueryEntity:
    def test_returns_direct_edges(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03 | stability:transient\n"
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03 | stability:transient\n"
              "LINK: kai | rel:member-of | team  | valid_from:2025-06 | stability:stable\n")
        result = query_entity(tmp_path, "kai")
        # direct includes all edges in build_graph (historical too, since as_of=None scans all)
        assert "direct" in result
        assert "extended" in result
        assert result["entity"] == "kai"

    def test_unknown_entity_returns_empty(self, tmp_path):
        write(tmp_path, "brain.st", "LINK: kai | rel:works-on | nova\n")
        result = query_entity(tmp_path, "nobody")
        assert result["direct"] == []
        assert result["extended"] == []

    def test_format_entity_query_no_crash(self, tmp_path):
        write(tmp_path, "brain.st", "LINK: kai | rel:works-on | nova\n")
        result = query_entity(tmp_path, "kai")
        output = format_entity_query(result)
        assert "kai" in output


# ── get_timeline ──────────────────────────────────────────────────────────────

class TestGetTimeline:
    def test_chronological_order(self, tmp_path):
        write(tmp_path, "brain.st",
              "LINK: kai | rel:works-on | nova  | valid_from:2026-03\n"
              "LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03\n")
        events = get_timeline(tmp_path, "kai")
        dates = [e["date"] for e in events if e["date"] != "0000-00"]
        assert dates == sorted(dates)

    def test_empty_for_unknown_entity(self, tmp_path):
        write(tmp_path, "brain.st", "LINK: kai | rel:works-on | nova\n")
        assert get_timeline(tmp_path, "nobody") == []

    def test_format_timeline_no_crash(self, tmp_path):
        write(tmp_path, "brain.st", "LINK: kai | rel:works-on | nova | valid_from:2026-03\n")
        events = get_timeline(tmp_path, "kai")
        output = format_timeline(events, "kai")
        assert "kai" in output


# ── invalidate_entry ──────────────────────────────────────────────────────────

class TestInvalidateEntry:
    def test_appends_ended(self, tmp_path):
        f = write(tmp_path, "brain.st",
                  "DECISION: deploy | vercel>railway | cost | 2026-01\n")
        result = invalidate_entry(str(f), 1, ended="2026-04")
        assert result["action"] == "appended"
        assert "ended:2026-04" in f.read_text(encoding="utf-8")

    def test_replaces_existing_ended(self, tmp_path):
        f = write(tmp_path, "brain.st",
                  "DECISION: deploy | vercel>railway | cost | ended:2025-01\n")
        result = invalidate_entry(str(f), 1, ended="2026-04")
        assert result["action"] == "updated"
        content = f.read_text(encoding="utf-8")
        assert "ended:2026-04" in content
        assert "ended:2025-01" not in content

    def test_defaults_to_current_month(self, tmp_path):
        f = write(tmp_path, "brain.st",
                  "DECISION: deploy | vercel>railway | cost | 2026-01\n")
        invalidate_entry(str(f), 1)
        content = f.read_text(encoding="utf-8")
        assert f"ended:{_today()}" in content

    def test_raises_on_missing_file(self, tmp_path):
        with pytest.raises(ValueError, match="not found"):
            invalidate_entry(str(tmp_path / "ghost.st"), 1)

    def test_raises_on_wrong_extension(self, tmp_path):
        f = write(tmp_path, "notes.md", "some markdown\n")
        with pytest.raises(ValueError, match=".st file"):
            invalidate_entry(str(f), 1)

    def test_raises_on_out_of_range_line(self, tmp_path):
        f = write(tmp_path, "brain.st", "RULE: auth | no-plaintext | hard\n")
        with pytest.raises(ValueError, match="out of range"):
            invalidate_entry(str(f), 99)

    def test_raises_on_comment_line(self, tmp_path):
        f = write(tmp_path, "brain.st", "# just a comment\n")
        with pytest.raises(ValueError, match="comment"):
            invalidate_entry(str(f), 1)

    def test_raises_on_malformed_ended_date(self, tmp_path):
        f = write(tmp_path, "brain.st", "RULE: auth | no-plaintext | hard\n")
        with pytest.raises(ValueError, match="Invalid ended date"):
            invalidate_entry(str(f), 1, ended="not-a-date")

    def test_format_result_no_crash(self, tmp_path):
        f = write(tmp_path, "brain.st",
                  "RULE: auth | no-plaintext | hard\n")
        result = invalidate_entry(str(f), 1, ended="2026-04")
        output = format_invalidate_result(result)
        assert "brain.st" in output
        assert "ended:2026-04" in output
