"""
Smalltalk Knowledge Graph Visualizer

Reads .st files from a directory, builds the KG, and opens an interactive
graph visualization in the browser. No extra dependencies — uses vis.js via CDN.

Usage:
    python -m smalltalk.kg_viz <directory>
    python -m smalltalk.kg_viz _brain/
    python -m smalltalk.kg_viz _brain/ --out graph.html   # save without opening

CLI:
    smalltalk kg visualize <dir>
"""
from __future__ import annotations

import json
import webbrowser
import tempfile
import http.server
import threading
from pathlib import Path
from typing import Optional

from smalltalk.kg import build_graph, _today
from smalltalk.checker import check_contradictions


# ── Colour / shape palette ────────────────────────────────────────────────────

_STABILITY_COLOURS = {
    "permanent": {"background": "#7c3aed", "border": "#5b21b6", "highlight": "#8b5cf6"},
    "stable":    {"background": "#2563eb", "border": "#1d4ed8", "highlight": "#3b82f6"},
    "transient": {"background": "#0891b2", "border": "#0e7490", "highlight": "#06b6d4"},
}

_HISTORICAL_COLOUR = {"background": "#374151", "border": "#1f2937", "highlight": "#4b5563"}
_CONFLICT_COLOUR   = {"background": "#dc2626", "border": "#991b1b", "highlight": "#ef4444"}
_WARNING_COLOUR    = {"background": "#d97706", "border": "#b45309", "highlight": "#f59e0b"}

_EDGE_COLOURS = {
    "works-on":     "#f59e0b",
    "depends":      "#3b82f6",
    "defined-as":   "#8b5cf6",
    "member-of":    "#10b981",
    "reports-to":   "#ec4899",
    "replaced-by":  "#ef4444",
    "caused-by":    "#f97316",
    "assigned-to":  "#a3e635",
    "deployed-to":  "#06b6d4",
    "blocks":       "#dc2626",
}
_DEFAULT_EDGE_COLOUR = "#6b7280"


def build_viz_data(directory: Path) -> dict:
    """
    Build nodes + edges dicts for vis.js from a directory of .st files.
    Returns dict with keys: nodes, edges, stats, conflicts.
    """
    graph      = build_graph(directory)
    conflicts  = check_contradictions(directory)
    today      = _today()

    conflict_entities: set[str] = set()
    warning_entities:  set[str] = set()
    for c in conflicts:
        if c.get("severity") == "CRITICAL":
            for e in [c.get("older", {}), c.get("newer", {})]:
                src = e.get("subject", "")
                if src:
                    conflict_entities.add(src)
        else:
            for e in [c.get("older", {}), c.get("newer", {})]:
                src = e.get("subject", "")
                if src:
                    warning_entities.add(src)

    # Collect all entity names
    all_entities: set[str] = set()
    for src, edges in graph.items():
        all_entities.add(src)
        for edge in edges:
            all_entities.add(edge["target"])

    nodes = []
    for entity in sorted(all_entities):
        edges_from = graph.get(entity, [])
        active_edges = [e for e in edges_from if e.get("active", True)]
        hist_edges   = [e for e in edges_from if not e.get("active", True)]
        is_historical = not active_edges and bool(hist_edges)

        stability = "stable"
        for e in edges_from:
            s = e.get("stability", "stable")
            if s == "permanent":
                stability = "permanent"
                break
            if s == "transient" and stability != "permanent":
                stability = "transient"

        if entity in conflict_entities:
            colour = _CONFLICT_COLOUR
            border_width = 3
        elif entity in warning_entities:
            colour = _WARNING_COLOUR
            border_width = 2
        elif is_historical:
            colour = _HISTORICAL_COLOUR
            border_width = 1
        else:
            colour = _STABILITY_COLOURS.get(stability, _STABILITY_COLOURS["stable"])
            border_width = 2 if stability == "permanent" else 1

        node = {
            "id":    entity,
            "label": entity,
            "title": _node_tooltip(entity, edges_from, conflicts),
            "color": colour,
            "borderWidth": border_width,
            "font":  {"color": "#f9fafb", "size": 14},
            "shape": "ellipse" if stability != "permanent" else "box",
        }
        if is_historical:
            node["opacity"] = 0.5
            node["font"]["color"] = "#9ca3af"
        nodes.append(node)

    edges = []
    edge_id = 0
    seen_edges: set[tuple] = set()
    for src, src_edges in graph.items():
        for edge in src_edges:
            key = (src, edge["rel"], edge["target"])
            if key in seen_edges:
                continue
            seen_edges.add(key)

            is_active  = edge.get("active", True)
            rel_name   = edge["rel"]
            ec         = _EDGE_COLOURS.get(rel_name, _DEFAULT_EDGE_COLOUR)

            edges.append({
                "id":     edge_id,
                "from":   src,
                "to":     edge["target"],
                "label":  rel_name,
                "title":  _edge_tooltip(edge),
                "color":  {
                    "color":     ec if is_active else "#374151",
                    "highlight": ec,
                    "opacity":   1.0 if is_active else 0.35,
                },
                "dashes":    not is_active,
                "arrows":    "to",
                "font":      {"size": 11, "color": "#d1d5db", "strokeWidth": 0},
                "width":     2 if is_active else 1,
                "smooth":    {"type": "curvedCW", "roundness": 0.1},
            })
            edge_id += 1

    # Stats
    active_nodes = sum(1 for n in nodes if n.get("opacity", 1.0) == 1.0 or "opacity" not in n)
    hist_edges_count   = sum(1 for _, se in graph.items() for e in se if not e.get("active", True))
    active_edges_count = sum(1 for _, se in graph.items() for e in se if e.get("active", True))

    return {
        "nodes":     nodes,
        "edges":     edges,
        "conflicts": conflicts,
        "stats": {
            "entities":      len(all_entities),
            "active_edges":  active_edges_count,
            "hist_edges":    hist_edges_count,
            "conflicts":     len([c for c in conflicts if c.get("severity") == "CRITICAL"]),
            "warnings":      len([c for c in conflicts if c.get("severity") == "WARNING"]),
            "as_of":         today,
        },
    }


def _node_tooltip(entity: str, edges: list, conflicts: list) -> str:
    active  = [e for e in edges if e.get("active", True)]
    hist    = [e for e in edges if not e.get("active", True)]
    lines   = [f"<b>{entity}</b>"]
    if active:
        lines.append(f"Active edges: {len(active)}")
        for e in active[:5]:
            since = f"  since {e['valid_from']}" if e.get("valid_from") else ""
            lines.append(f"  → {e['rel']} → {e['target']}{since}")
    if hist:
        lines.append(f"Historical: {len(hist)}")
    for c in conflicts:
        if c.get("older", {}).get("subject") == entity or c.get("newer", {}).get("subject") == entity:
            lines.append(f"⚠ {c['conflict_type']}")
    return "<br>".join(lines)


def _edge_tooltip(edge: dict) -> str:
    lines = [f"<b>{edge['rel']}</b>"]
    if edge.get("valid_from"):
        lines.append(f"Since: {edge['valid_from']}")
    if edge.get("ended"):
        lines.append(f"Ended: {edge['ended']}")
    lines.append(f"Stability: {edge.get('stability', 'stable')}")
    if not edge.get("active", True):
        lines.append("<i>Historical</i>")
    return "<br>".join(lines)


_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smalltalk Knowledge Graph — {directory}</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
    background: #0f1117;
    color: #f9fafb;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  /* ── Header ─────────────────────────────────────────────────────── */
  .header {{
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 20px;
    background: #1a1d27;
    border-bottom: 1px solid #2d3148;
    flex-shrink: 0;
  }}
  .logo {{
    font-size: 15px;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: #f9fafb;
  }}
  .logo span {{ color: #7c3aed; }}
  .dir-badge {{
    font-size: 12px;
    color: #9ca3af;
    background: #0f1117;
    border: 1px solid #2d3148;
    border-radius: 6px;
    padding: 3px 10px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
  }}
  .stats {{
    margin-left: auto;
    display: flex;
    gap: 12px;
    align-items: center;
  }}
  .stat {{
    font-size: 12px;
    color: #6b7280;
    display: flex;
    gap: 4px;
    align-items: center;
  }}
  .stat strong {{ color: #9ca3af; font-weight: 600; }}
  .stat.conflict {{ color: #ef4444; }}
  .stat.conflict strong {{ color: #f87171; }}
  .stat.warning {{ color: #f59e0b; }}
  .stat.warning strong {{ color: #fbbf24; }}

  /* ── Controls ────────────────────────────────────────────────────── */
  .controls {{
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 8px 20px;
    background: #13151f;
    border-bottom: 1px solid #2d3148;
    flex-shrink: 0;
  }}
  .control-btn {{
    font-size: 12px;
    padding: 5px 12px;
    border-radius: 6px;
    border: 1px solid #2d3148;
    background: #1a1d27;
    color: #d1d5db;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .control-btn:hover {{ background: #22263a; border-color: #7c3aed; color: #f9fafb; }}
  .control-btn.active {{ background: #7c3aed; border-color: #7c3aed; color: #fff; }}
  .search-box {{
    margin-left: 8px;
    padding: 5px 12px;
    border-radius: 6px;
    border: 1px solid #2d3148;
    background: #1a1d27;
    color: #f9fafb;
    font-size: 12px;
    width: 200px;
    outline: none;
    transition: border-color 0.15s;
  }}
  .search-box:focus {{ border-color: #7c3aed; }}
  .search-box::placeholder {{ color: #4b5563; }}
  .spacer {{ flex: 1; }}
  .legend {{
    display: flex;
    gap: 10px;
    align-items: center;
    margin-left: auto;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    color: #6b7280;
  }}
  .legend-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 1.5px solid transparent;
  }}

  /* ── Graph ───────────────────────────────────────────────────────── */
  .body {{
    display: flex;
    flex: 1;
    overflow: hidden;
  }}
  #network {{
    flex: 1;
    background: radial-gradient(ellipse at 50% 50%, #13151f 0%, #0f1117 100%);
  }}

  /* ── Sidebar ─────────────────────────────────────────────────────── */
  .sidebar {{
    width: 300px;
    background: #1a1d27;
    border-left: 1px solid #2d3148;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .sidebar-head {{
    padding: 14px 16px 10px;
    border-bottom: 1px solid #2d3148;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #6b7280;
  }}
  .sidebar-body {{
    flex: 1;
    overflow-y: auto;
    padding: 12px 0;
  }}
  .sidebar-body::-webkit-scrollbar {{ width: 4px; }}
  .sidebar-body::-webkit-scrollbar-track {{ background: transparent; }}
  .sidebar-body::-webkit-scrollbar-thumb {{ background: #2d3148; border-radius: 2px; }}
  .entity-card {{
    padding: 10px 16px;
    border-bottom: 1px solid #13151f;
    cursor: pointer;
    transition: background 0.1s;
  }}
  .entity-card:hover {{ background: #22263a; }}
  .entity-card.selected {{ background: #2d2150; border-left: 2px solid #7c3aed; }}
  .entity-name {{
    font-size: 13px;
    font-weight: 600;
    color: #f9fafb;
    margin-bottom: 4px;
  }}
  .entity-meta {{
    font-size: 11px;
    color: #6b7280;
    display: flex;
    gap: 8px;
  }}
  .tag {{
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 4px;
    border: 1px solid;
  }}
  .tag-permanent {{ color: #a78bfa; border-color: #5b21b6; background: #1e1230; }}
  .tag-transient  {{ color: #67e8f9; border-color: #0e7490; background: #0c1f26; }}
  .tag-conflict   {{ color: #f87171; border-color: #991b1b; background: #2c0f0f; }}
  .tag-warning    {{ color: #fbbf24; border-color: #b45309; background: #2c1c06; }}
  .tag-historical {{ color: #9ca3af; border-color: #374151; background: #111827; }}

  /* Conflict panel */
  .conflict-panel {{
    margin: 0;
    padding: 0;
  }}
  .conflict-item {{
    padding: 10px 16px;
    border-bottom: 1px solid #13151f;
    border-left: 2px solid transparent;
  }}
  .conflict-item.critical {{ border-left-color: #ef4444; }}
  .conflict-item.warning  {{ border-left-color: #f59e0b; }}
  .conflict-type {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}
  .conflict-type.critical {{ color: #f87171; }}
  .conflict-type.warning  {{ color: #fbbf24; }}
  .conflict-desc {{
    font-size: 11px;
    color: #9ca3af;
    line-height: 1.5;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
  }}
  .conflict-resolution {{
    margin-top: 6px;
    font-size: 10px;
    color: #6b7280;
    background: #0f1117;
    border-radius: 4px;
    padding: 4px 8px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
  }}

  /* Tab system */
  .tabs {{
    display: flex;
    border-bottom: 1px solid #2d3148;
  }}
  .tab {{
    flex: 1;
    padding: 8px;
    font-size: 11px;
    text-align: center;
    cursor: pointer;
    color: #6b7280;
    border-bottom: 2px solid transparent;
    transition: all 0.15s;
  }}
  .tab.active {{ color: #7c3aed; border-bottom-color: #7c3aed; }}
  .tab:hover {{ color: #a78bfa; }}
  .tab-content {{ display: none; flex: 1; overflow: hidden; flex-direction: column; }}
  .tab-content.active {{ display: flex; }}

  .empty-state {{
    padding: 24px 16px;
    text-align: center;
    color: #4b5563;
    font-size: 12px;
    line-height: 1.8;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="logo">small<span>talk</span> KG</div>
  <div class="dir-badge">{directory}</div>
  <div class="stats">
    <div class="stat"><strong>{entities}</strong> entities</div>
    <div class="stat"><strong>{active_edges}</strong> active edges</div>
    <div class="stat"><strong>{hist_edges}</strong> historical</div>
    {conflict_stat}
    {warning_stat}
    <div class="stat">as of <strong>{as_of}</strong></div>
  </div>
</div>

<div class="controls">
  <button class="control-btn active" onclick="setLayout('physics')" id="btn-physics">Physics</button>
  <button class="control-btn" onclick="setLayout('hierarchical')" id="btn-hier">Hierarchical</button>
  <button class="control-btn" onclick="resetView()">Reset view</button>
  <button class="control-btn" onclick="toggleHistorical(this)">Show historical</button>
  <input class="search-box" id="search" type="text" placeholder="Filter entities..." oninput="filterNodes(this.value)">
  <div class="spacer"></div>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#7c3aed;border-color:#5b21b6"></div>permanent</div>
    <div class="legend-item"><div class="legend-dot" style="background:#2563eb;border-color:#1d4ed8"></div>stable</div>
    <div class="legend-item"><div class="legend-dot" style="background:#0891b2;border-color:#0e7490"></div>transient</div>
    <div class="legend-item"><div class="legend-dot" style="background:#374151;border-color:#1f2937;opacity:0.6"></div>historical</div>
    <div class="legend-item"><div class="legend-dot" style="background:#dc2626;border-color:#991b1b"></div>conflict</div>
    <div class="legend-item"><div class="legend-dot" style="background:#d97706;border-color:#b45309"></div>warning</div>
  </div>
</div>

<div class="body">
  <div id="network"></div>

  <div class="sidebar">
    <div class="tabs">
      <div class="tab active" onclick="switchTab('entities')">Entities ({entities})</div>
      <div class="tab" onclick="switchTab('conflicts')" id="tab-conflicts">
        {conflicts_tab_label}
      </div>
    </div>

    <div class="tab-content active" id="tab-entities">
      <div class="sidebar-body" id="entities-list">
        <!-- populated by JS -->
      </div>
    </div>

    <div class="tab-content" id="tab-conflicts">
      <div class="sidebar-body">
        {conflicts_html}
      </div>
    </div>
  </div>
</div>

<script>
const VIZ_DATA = {viz_data_json};
const allNodes = new vis.DataSet(VIZ_DATA.nodes);
const allEdges = new vis.DataSet(VIZ_DATA.edges);
let showHistorical = false;
let selectedNode   = null;

const container = document.getElementById('network');
const options = {{
  nodes: {{
    borderWidth: 1,
    size: 26,
    font: {{ face: 'Inter, -apple-system, sans-serif', size: 14 }},
    shadow: {{ enabled: true, color: '#00000088', size: 6, x: 2, y: 2 }},
  }},
  edges: {{
    font: {{ face: 'Inter, sans-serif', size: 11, strokeWidth: 0 }},
    length: 220,
    shadow: {{ enabled: false }},
    selectionWidth: 2,
  }},
  physics: {{
    enabled: true,
    barnesHut: {{
      gravitationalConstant: -3000,
      centralGravity: 0.25,
      springLength: 200,
      springConstant: 0.04,
      damping: 0.12,
    }},
    stabilization: {{ iterations: 200, fit: true }},
  }},
  interaction: {{
    hover: true,
    tooltipDelay: 100,
    hideEdgesOnDrag: true,
  }},
}};

const network = new vis.Network(container, {{ nodes: allNodes, edges: allEdges }}, options);

// ── Sidebar entity list ───────────────────────────────────────────
const entityList = document.getElementById('entities-list');

function buildEntityList(filter) {{
  entityList.innerHTML = '';
  const nodes = VIZ_DATA.nodes
    .filter(n => !filter || n.id.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => a.id.localeCompare(b.id));

  if (!nodes.length) {{
    entityList.innerHTML = '<div class="empty-state">No entities match filter.</div>';
    return;
  }}

  nodes.forEach(n => {{
    const edges_from = VIZ_DATA.edges.filter(e => e.from === n.id && !e.dashes);
    const edges_hist = VIZ_DATA.edges.filter(e => e.from === n.id &&  e.dashes);
    const isHistorical = n.opacity && n.opacity < 1;
    const conflictInfo = VIZ_DATA.conflicts.find(c =>
      (c.older && c.older.subject === n.id) || (c.newer && c.newer.subject === n.id)
    );

    const card = document.createElement('div');
    card.className = 'entity-card' + (n.id === selectedNode ? ' selected' : '');
    card.onclick = () => selectNode(n.id, card);

    let tags = '';
    if (conflictInfo)  tags += `<span class="tag ${{conflictInfo.severity === 'CRITICAL' ? 'tag-conflict' : 'tag-warning'}}">${{conflictInfo.severity.toLowerCase()}}</span>`;
    if (isHistorical)  tags += '<span class="tag tag-historical">historical</span>';
    const stability = (VIZ_DATA.edges.find(e => e.from === n.id) || {{}}).title?.includes('permanent') ? 'permanent' : '';
    if (stability)     tags += '<span class="tag tag-permanent">permanent</span>';

    card.innerHTML = `
      <div class="entity-name">${{n.id}}</div>
      <div class="entity-meta">
        <span>${{edges_from.length}} active · ${{edges_hist.length}} hist</span>
        ${{tags}}
      </div>`;
    entityList.appendChild(card);
  }});
}}

buildEntityList('');

function selectNode(id, cardEl) {{
  selectedNode = id;
  document.querySelectorAll('.entity-card').forEach(c => c.classList.remove('selected'));
  if (cardEl) cardEl.classList.add('selected');
  network.selectNodes([id]);
  network.focus(id, {{ scale: 1.2, animation: {{ duration: 400, easingFunction: 'easeInOutQuad' }} }});
}}

network.on('selectNode', params => {{
  if (params.nodes.length) {{
    selectedNode = params.nodes[0];
    buildEntityList(document.getElementById('search').value);
  }}
}});

// ── Layout controls ────────────────────────────────────────────────
function setLayout(type) {{
  document.getElementById('btn-physics').classList.remove('active');
  document.getElementById('btn-hier').classList.remove('active');
  if (type === 'hierarchical') {{
    document.getElementById('btn-hier').classList.add('active');
    network.setOptions({{ layout: {{ hierarchical: {{ enabled: true, direction: 'LR', levelSeparation: 180 }} }} }});
  }} else {{
    document.getElementById('btn-physics').classList.add('active');
    network.setOptions({{ layout: {{ hierarchical: {{ enabled: false }} }} }});
  }}
}}

function resetView() {{ network.fit({{ animation: {{ duration: 400 }} }}); }}

function toggleHistorical(btn) {{
  showHistorical = !showHistorical;
  btn.classList.toggle('active', showHistorical);
  const edgeUpdate = VIZ_DATA.edges.map(e => ({{
    id: e.id,
    hidden: !showHistorical && e.dashes,
  }}));
  const nodeUpdate = VIZ_DATA.nodes
    .filter(n => n.opacity && n.opacity < 1)
    .map(n => ({{ id: n.id, hidden: !showHistorical }}));
  allEdges.update(edgeUpdate);
  allNodes.update(nodeUpdate);
}}

function filterNodes(val) {{
  buildEntityList(val);
  if (!val) {{
    allNodes.update(VIZ_DATA.nodes.map(n => ({{ id: n.id, hidden: false }})));
    return;
  }}
  const matched = new Set(VIZ_DATA.nodes.filter(n => n.id.toLowerCase().includes(val.toLowerCase())).map(n => n.id));
  allNodes.update(VIZ_DATA.nodes.map(n => ({{ id: n.id, hidden: !matched.has(n.id) }})));
}}

// ── Tab system ─────────────────────────────────────────────────────
function switchTab(name) {{
  document.querySelectorAll('.tab').forEach((t, i) => {{
    const names = ['entities', 'conflicts'];
    t.classList.toggle('active', names[i] === name);
  }});
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
}}
</script>
</body>
</html>
"""


def _conflicts_html(conflicts: list) -> str:
    if not conflicts:
        return '<div class="empty-state">✓ No active contradictions detected.</div>'
    items = []
    for c in conflicts:
        sev   = c.get("severity", "WARNING")
        ctype = c.get("conflict_type", "")
        older = c.get("older", {})
        newer = c.get("newer", {})
        res   = c.get("resolution", "")
        items.append(f"""
        <div class="conflict-item {sev.lower()}">
          <div class="conflict-type {sev.lower()}">{sev} — {ctype}</div>
          <div class="conflict-desc">
            {older.get('file', '')}:{older.get('line_no', '')}&nbsp;&nbsp;&lt;&lt; older<br>
            {newer.get('file', '')}:{newer.get('line_no', '')}&nbsp;&nbsp;&lt;&lt; newer
          </div>
          {f'<div class="conflict-resolution">{res}</div>' if res else ''}
        </div>""")
    return '<div class="conflict-panel">' + "\n".join(items) + '</div>'


def generate_html(directory: Path, viz_data: dict) -> str:
    stats    = viz_data["stats"]
    confl    = viz_data["conflicts"]
    n_crit   = stats["conflicts"]
    n_warn   = stats["warnings"]

    conflict_stat = (
        f'<div class="stat conflict"><strong>{n_crit}</strong> critical</div>' if n_crit else ""
    )
    warning_stat = (
        f'<div class="stat warning"><strong>{n_warn}</strong> warnings</div>' if n_warn else ""
    )

    if n_crit or n_warn:
        conflicts_tab_label = f'Issues ({n_crit + n_warn})'
    else:
        conflicts_tab_label = 'Issues'

    # Sanitise conflicts for JSON (remove non-serialisable items if any)
    safe_conflicts = []
    for c in confl:
        safe_conflicts.append({k: v for k, v in c.items() if isinstance(v, (str, int, float, bool, dict, list, type(None)))})

    return _HTML_TEMPLATE.format(
        directory            = str(directory),
        entities             = stats["entities"],
        active_edges         = stats["active_edges"],
        hist_edges           = stats["hist_edges"],
        as_of                = stats["as_of"],
        conflict_stat        = conflict_stat,
        warning_stat         = warning_stat,
        conflicts_tab_label  = conflicts_tab_label,
        conflicts_html       = _conflicts_html(confl),
        viz_data_json        = json.dumps({
            "nodes":     viz_data["nodes"],
            "edges":     viz_data["edges"],
            "conflicts": safe_conflicts,
        }),
    )


def visualize(
    directory: Path,
    out: Optional[Path] = None,
    open_browser: bool = True,
) -> Path:
    """
    Build and open the KG visualization.

    Args:
        directory:    Directory containing .st files
        out:          Optional path to save the HTML file (default: temp file)
        open_browser: Open the file in the default browser (default: True)

    Returns:
        Path to the generated HTML file
    """
    directory = Path(directory).resolve()

    if not directory.exists():
        raise ValueError(f"Directory not found: {directory}")

    viz_data = build_viz_data(directory)
    html     = generate_html(directory, viz_data)

    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        target = out
    else:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        )
        tmp.write(html)
        tmp.flush()
        target = Path(tmp.name)

    if open_browser:
        webbrowser.open(target.as_uri())

    return target


# ── CLI entry point ────────────────────────────────────────────────────────────

def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Smalltalk KG visualizer — opens an interactive graph in the browser."
    )
    parser.add_argument("directory", help="Directory containing .st files")
    parser.add_argument("--out", help="Save HTML to this path instead of a temp file")
    parser.add_argument("--no-browser", action="store_true", help="Don't open a browser window")
    args = parser.parse_args()

    path = visualize(
        directory    = Path(args.directory),
        out          = Path(args.out) if args.out else None,
        open_browser = not args.no_browser,
    )
    print(f"Graph: {path}")
    if args.no_browser:
        print("Open the file in any browser to view the visualization.")


if __name__ == "__main__":
    main()
