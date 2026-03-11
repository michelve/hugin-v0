#!/usr/bin/env python3
"""Generate an interactive HTML visualization of React component dependencies.

Scans src/client/components/ and src/client/routes/ for import relationships
between components. Outputs a standalone HTML file with an interactive force-directed
graph using embedded CSS and vanilla JS (no external dependencies).

Usage:
    python3 scripts/visualize-components.py [output_path]

If output_path is not provided, writes to ./component-graph.html
"""
import os
import re
import sys
import json
from pathlib import Path


def find_tsx_files(root_dir: str) -> list[str]:
    """Find all .tsx and .ts files in the given directory recursively."""
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(('.tsx', '.ts')) and not f.endswith('.d.ts'):
                files.append(os.path.join(dirpath, f))
    return files


def extract_imports(filepath: str, base_dir: str) -> list[dict]:
    """Extract import statements from a TypeScript/React file."""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return imports

    # Match: import { X } from "@/components/..." or from "../components/..."
    pattern = r'import\s+(?:type\s+)?(?:{[^}]*}|[^;{]*)\s+from\s+["\']([^"\']+)["\']'
    for match in re.finditer(pattern, content):
        source = match.group(1)
        # Resolve @/ alias
        if source.startswith('@/'):
            resolved = source.replace('@/', 'src/client/')
        elif source.startswith('.'):
            dir_of_file = os.path.dirname(filepath)
            resolved = os.path.normpath(os.path.join(dir_of_file, source))
            resolved = os.path.relpath(resolved, base_dir).replace('\\', '/')
        else:
            continue  # Skip node_modules imports

        imports.append({
            'source': source,
            'resolved': resolved
        })
    return imports


def build_graph(base_dir: str) -> dict:
    """Build a dependency graph from component files."""
    components_dir = os.path.join(base_dir, 'src', 'client', 'components')
    routes_dir = os.path.join(base_dir, 'src', 'client', 'routes')

    nodes = {}
    edges = []

    # Collect all component files
    all_files = []
    if os.path.isdir(components_dir):
        all_files.extend(find_tsx_files(components_dir))
    if os.path.isdir(routes_dir):
        all_files.extend(find_tsx_files(routes_dir))

    for filepath in all_files:
        rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
        name = Path(filepath).stem

        # Categorize
        if 'components/ui/' in rel_path:
            category = 'ui'
        elif 'components/' in rel_path:
            category = 'component'
        elif 'routes/' in rel_path:
            category = 'route'
        else:
            category = 'other'

        nodes[rel_path] = {
            'id': rel_path,
            'name': name,
            'category': category
        }

        imports = extract_imports(filepath, base_dir)
        for imp in imports:
            resolved = imp['resolved']
            # Try to find the actual file
            for ext in ['', '.tsx', '.ts', '/index.tsx', '/index.ts']:
                candidate = resolved + ext
                candidate_abs = os.path.join(base_dir, candidate)
                if os.path.isfile(candidate_abs):
                    target_rel = os.path.relpath(candidate_abs, base_dir).replace('\\', '/')
                    if target_rel.startswith('src/client/'):
                        edges.append({
                            'source': rel_path,
                            'target': target_rel
                        })
                    break

    return {
        'nodes': list(nodes.values()),
        'edges': edges
    }


def generate_html(graph: dict) -> str:
    """Generate standalone HTML with embedded visualization."""
    nodes_json = json.dumps(graph['nodes'])
    edges_json = json.dumps(graph['edges'])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Component Dependency Graph</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; overflow: hidden; }}
#canvas {{ width: 100vw; height: 100vh; }}
#legend {{ position: fixed; top: 16px; right: 16px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 16px; font-size: 13px; z-index: 10; }}
#legend h3 {{ margin-bottom: 8px; font-size: 14px; color: #f8fafc; }}
.legend-item {{ display: flex; align-items: center; gap: 8px; margin: 4px 0; }}
.legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
#info {{ position: fixed; bottom: 16px; left: 16px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; font-size: 13px; z-index: 10; }}
#stats {{ position: fixed; top: 16px; left: 16px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; font-size: 13px; z-index: 10; }}
#filter {{ position: fixed; top: 80px; left: 16px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; font-size: 13px; z-index: 10; }}
#filter label {{ display: block; margin: 4px 0; cursor: pointer; }}
#filter input {{ margin-right: 6px; }}
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<div id="stats"></div>
<div id="legend">
  <h3>Categories</h3>
  <div class="legend-item"><div class="legend-dot" style="background:#60a5fa"></div> Route</div>
  <div class="legend-item"><div class="legend-dot" style="background:#34d399"></div> Component</div>
  <div class="legend-item"><div class="legend-dot" style="background:#a78bfa"></div> UI (shadcn)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#94a3b8"></div> Other</div>
</div>
<div id="filter">
  <h3 style="margin-bottom:8px;font-size:14px;">Filter</h3>
  <label><input type="checkbox" checked data-cat="route"> Routes</label>
  <label><input type="checkbox" checked data-cat="component"> Components</label>
  <label><input type="checkbox" checked data-cat="ui"> UI (shadcn)</label>
  <label><input type="checkbox" checked data-cat="other"> Other</label>
</div>
<div id="info">Drag nodes to rearrange. Scroll to zoom. Click a node for details.</div>
<script>
const NODES = {nodes_json};
const EDGES = {edges_json};
const COLORS = {{ route: '#60a5fa', component: '#34d399', ui: '#a78bfa', other: '#94a3b8' }};

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let W, H, scale = 1, offsetX = 0, offsetY = 0;
let dragging = null, dragOffX = 0, dragOffY = 0;
let hoveredNode = null;
let visibleCats = new Set(['route', 'component', 'ui', 'other']);

function resize() {{ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }}
window.addEventListener('resize', resize);
resize();

// Initialize positions
NODES.forEach((n, i) => {{
  const angle = (i / NODES.length) * Math.PI * 2;
  const r = Math.min(W, H) * 0.3;
  n.x = W/2 + Math.cos(angle) * r * (0.5 + Math.random() * 0.5);
  n.y = H/2 + Math.sin(angle) * r * (0.5 + Math.random() * 0.5);
  n.vx = 0; n.vy = 0;
  n.radius = n.category === 'route' ? 8 : n.category === 'ui' ? 5 : 7;
}});

// Build edge index
const nodeMap = {{}};
NODES.forEach(n => nodeMap[n.id] = n);
const validEdges = EDGES.filter(e => nodeMap[e.source] && nodeMap[e.target]);

document.getElementById('stats').innerHTML =
  `<strong>${{NODES.length}}</strong> files &middot; <strong>${{validEdges.length}}</strong> dependencies`;

// Filter checkboxes
document.querySelectorAll('#filter input').forEach(cb => {{
  cb.addEventListener('change', () => {{
    if (cb.checked) visibleCats.add(cb.dataset.cat);
    else visibleCats.delete(cb.dataset.cat);
  }});
}});

function simulate() {{
  // Force simulation
  NODES.forEach(n => {{
    if (!visibleCats.has(n.category)) return;
    // Center gravity
    n.vx += (W/2 - n.x) * 0.0005;
    n.vy += (H/2 - n.y) * 0.0005;
    // Repulsion
    NODES.forEach(m => {{
      if (n === m || !visibleCats.has(m.category)) return;
      const dx = n.x - m.x, dy = n.y - m.y;
      const d2 = dx*dx + dy*dy + 1;
      const f = 800 / d2;
      n.vx += dx * f; n.vy += dy * f;
    }});
  }});
  // Attraction along edges
  validEdges.forEach(e => {{
    const s = nodeMap[e.source], t = nodeMap[e.target];
    if (!s || !t || !visibleCats.has(s.category) || !visibleCats.has(t.category)) return;
    const dx = t.x - s.x, dy = t.y - s.y;
    const d = Math.sqrt(dx*dx + dy*dy) + 1;
    const f = (d - 120) * 0.003;
    s.vx += dx/d * f; s.vy += dy/d * f;
    t.vx -= dx/d * f; t.vy -= dy/d * f;
  }});
  // Apply velocity with damping
  NODES.forEach(n => {{
    if (n === dragging) return;
    n.vx *= 0.85; n.vy *= 0.85;
    n.x += n.vx; n.y += n.vy;
  }});
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);
  ctx.save();
  ctx.translate(offsetX, offsetY);
  ctx.scale(scale, scale);

  // Draw edges
  ctx.lineWidth = 0.5;
  validEdges.forEach(e => {{
    const s = nodeMap[e.source], t = nodeMap[e.target];
    if (!s || !t || !visibleCats.has(s.category) || !visibleCats.has(t.category)) return;
    ctx.strokeStyle = hoveredNode && (s === hoveredNode || t === hoveredNode) ? '#fbbf24' : '#334155';
    ctx.lineWidth = hoveredNode && (s === hoveredNode || t === hoveredNode) ? 1.5 : 0.5;
    ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(t.x, t.y); ctx.stroke();
  }});

  // Draw nodes
  NODES.forEach(n => {{
    if (!visibleCats.has(n.category)) return;
    ctx.fillStyle = COLORS[n.category] || COLORS.other;
    ctx.globalAlpha = n === hoveredNode ? 1 : 0.8;
    ctx.beginPath(); ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
    // Label
    if (n === hoveredNode || scale > 1.5) {{
      ctx.fillStyle = '#f8fafc';
      ctx.font = `${{Math.max(10, 11/scale)}}px system-ui`;
      ctx.textAlign = 'center';
      ctx.fillText(n.name, n.x, n.y - n.radius - 4);
    }}
  }});
  ctx.restore();
}}

function loop() {{ simulate(); draw(); requestAnimationFrame(loop); }}
loop();

// Mouse interaction
function screenToWorld(x, y) {{ return [(x - offsetX)/scale, (y - offsetY)/scale]; }}

canvas.addEventListener('mousedown', e => {{
  const [wx, wy] = screenToWorld(e.clientX, e.clientY);
  for (const n of NODES) {{
    if (!visibleCats.has(n.category)) continue;
    const dx = n.x - wx, dy = n.y - wy;
    if (dx*dx + dy*dy < (n.radius+4)*(n.radius+4)) {{
      dragging = n; dragOffX = dx; dragOffY = dy;
      document.getElementById('info').innerHTML = `<strong>${{n.name}}</strong> (${{n.category}}) &mdash; ${{n.id}}`;
      return;
    }}
  }}
}});

canvas.addEventListener('mousemove', e => {{
  const [wx, wy] = screenToWorld(e.clientX, e.clientY);
  if (dragging) {{ dragging.x = wx + dragOffX; dragging.y = wy + dragOffY; return; }}
  hoveredNode = null;
  for (const n of NODES) {{
    if (!visibleCats.has(n.category)) continue;
    const dx = n.x - wx, dy = n.y - wy;
    if (dx*dx + dy*dy < (n.radius+4)*(n.radius+4)) {{ hoveredNode = n; break; }}
  }}
  canvas.style.cursor = hoveredNode ? 'pointer' : 'default';
}});

canvas.addEventListener('mouseup', () => {{ dragging = null; }});

canvas.addEventListener('wheel', e => {{
  e.preventDefault();
  const factor = e.deltaY > 0 ? 0.9 : 1.1;
  const mx = e.clientX, my = e.clientY;
  offsetX = mx - (mx - offsetX) * factor;
  offsetY = my - (my - offsetY) * factor;
  scale *= factor;
}}, {{ passive: false }});
</script>
</body>
</html>"""


def main():
    # Determine base directory (project root)
    base_dir = os.getcwd()

    # Check if src/client exists
    client_dir = os.path.join(base_dir, 'src', 'client')
    if not os.path.isdir(client_dir):
        print(f"Error: {client_dir} not found. Run from project root.", file=sys.stderr)
        sys.exit(1)

    # Build graph
    graph = build_graph(base_dir)
    print(f"Found {len(graph['nodes'])} files and {len(graph['edges'])} dependencies")

    # Generate HTML
    html = generate_html(graph)

    # Write output
    output_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, 'component-graph.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Visualization written to: {output_path}")
    print("Open in a browser to explore the component dependency graph.")


if __name__ == '__main__':
    main()
