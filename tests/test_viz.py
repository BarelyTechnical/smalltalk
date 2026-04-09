"""Smoke test for the KG visualizer."""
from pathlib import Path
from smalltalk.kg_viz import build_viz_data, generate_html, visualize

d = Path("examples/knowledge-graph")
data = build_viz_data(d)
html = generate_html(d, data)

s = data["stats"]
print(f"Entities:     {s['entities']}")
print(f"Active edges: {s['active_edges']}")
print(f"Hist edges:   {s['hist_edges']}")
print(f"Conflicts:    {s['conflicts']}")
print(f"Warnings:     {s['warnings']}")
print(f"HTML size:    {len(html)} chars")
print()

print("Nodes:")
historical_count = 0
permanent_count = 0
for n in sorted(data["nodes"], key=lambda x: x["id"]):
    shape   = n.get("shape", "ellipse")
    opacity = n.get("opacity", 1.0)
    hist    = "[historical]" if opacity < 1 else ""
    if opacity < 1:
        historical_count += 1
    if shape == "box":
        permanent_count += 1
    print(f"  {n['id']:25s} shape={shape:8s} {hist}")

print()
print("Edges (first 10):")
for e in data["edges"][:10]:
    dashed = "[hist]" if e.get("dashes") else ""
    print(f"  {e['from']:15s} --{e['label']:15s}--> {e['to']:15s} {dashed}")

print()
print(f"Summary: {s['entities']} entities, {permanent_count} permanent (box), {historical_count} historical (faded)")

# Key assertions
assert s["entities"] > 0, "Should have entities"
assert s["active_edges"] > 0, "Should have active edges"
assert len(html) > 10000, "HTML should be substantial"
assert "vis-network" in html, "Should embed vis.js"
assert "VIZ_DATA" in html, "Should embed graph data"
assert "sidebar" in html, "Should have sidebar"
assert "toggleHistorical" in html, "Should have historical toggle"
assert "setLayout" in html, "Should have layout controls"

# Test save to file
out = Path("examples/knowledge-graph/kg.html")
path = visualize(d, out=out, open_browser=False)
assert path.exists(), "Output file should exist"
assert path.stat().st_size > 10000, "Output file should be substantial"

print()
print("All assertions passed.")
print(f"Graph saved: {out}")
