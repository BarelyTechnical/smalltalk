"""Tests for smalltalk.kg_viz — Knowledge Graph HTML visualizer."""
from pathlib import Path

import pytest

from kg_viz import visualize


class TestKGViz:
    def test_visualize_returns_path(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: kai | rel:works-on | nova | valid_from:2026-03 | stability:transient\n",
            encoding="utf-8"
        )
        out = tmp_path / "graph.html"
        result = visualize(directory=tmp_path, out=out, open_browser=False)
        assert isinstance(result, Path)

    def test_output_file_created(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: auth | rel:depends | billing | stability:stable\n",
            encoding="utf-8"
        )
        out = tmp_path / "graph.html"
        visualize(directory=tmp_path, out=out, open_browser=False)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_output_is_html(self, tmp_path):
        (tmp_path / "kg.st").write_text(
            "LINK: brand-color | rel:defined-as | indigo | stability:permanent\n",
            encoding="utf-8"
        )
        out = tmp_path / "graph.html"
        visualize(directory=tmp_path, out=out, open_browser=False)
        content = out.read_text(encoding="utf-8")
        assert "<html" in content.lower() or "<!doctype" in content.lower()

    def test_empty_dir_does_not_crash(self, tmp_path):
        out = tmp_path / "empty.html"
        result = visualize(directory=tmp_path, out=out, open_browser=False)
        assert isinstance(result, Path)

    def test_custom_out_path_respected(self, tmp_path):
        (tmp_path / "x.st").write_text(
            "LINK: a | rel:connects | b | stability:stable\n",
            encoding="utf-8"
        )
        custom_out = tmp_path / "custom" / "graph.html"
        custom_out.parent.mkdir()
        result = visualize(directory=tmp_path, out=custom_out, open_browser=False)
        assert result == custom_out
        assert custom_out.exists()

    def test_default_out_is_temp_file(self, tmp_path):
        (tmp_path / "x.st").write_text(
            "LINK: a | rel:connects | b | stability:stable\n",
            encoding="utf-8"
        )
        result = visualize(directory=tmp_path, out=None, open_browser=False)
        assert isinstance(result, Path)
        assert result.exists()

    def test_vis_js_referenced_in_output(self, tmp_path):
        """Graph should use vis.js for rendering."""
        (tmp_path / "x.st").write_text(
            "LINK: kai | rel:works-on | nova | stability:transient\n",
            encoding="utf-8"
        )
        out = tmp_path / "g.html"
        visualize(directory=tmp_path, out=out, open_browser=False)
        content = out.read_text(encoding="utf-8")
        assert "vis" in content.lower() or "network" in content.lower()

    def test_permanent_nodes_included(self, tmp_path):
        (tmp_path / "x.st").write_text(
            "LINK: brand-color | rel:defined-as | indigo | stability:permanent\n",
            encoding="utf-8"
        )
        out = tmp_path / "g.html"
        visualize(directory=tmp_path, out=out, open_browser=False)
        content = out.read_text(encoding="utf-8")
        assert "brand-color" in content or "indigo" in content
