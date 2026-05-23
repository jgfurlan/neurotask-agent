import json
import sys
import os
import shutil
from pathlib import Path

# Step 1: Copy latest artifacts from brain directory to docs/
brain_dir = Path("/home/jgfurlan/.gemini/antigravity-cli/brain/0fbb4dd6-979d-4eb6-87a1-77343a18c30a")
docs_dir = Path("/home/jgfurlan/dev/projects/neurotask-agent/docs")

for name in ["implementation_plan.md", "task.md", "walkthrough.md"]:
    src = brain_dir / name
    dst = docs_dir / name
    if src.exists():
        shutil.copy2(src, dst)
        print(f"Copied {name} from brain to docs/")

# Step 2: Locate subagent message file
msg_dir = Path("/home/jgfurlan/.gemini/antigravity-cli/brain/0fbb4dd6-979d-4eb6-87a1-77343a18c30a/.system_generated/messages")
msg_files = sorted(msg_dir.glob("*.json"))

subagent_data = None
for f in reversed(msg_files):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("sender") == "0bd56e1f-1a7b-45c5-bed8-6f25347a6838":
            content_str = data.get("content")
            subagent_data = json.loads(content_str)
            print(f"Loaded subagent data from {f.name}")
            break
    except Exception as e:
        continue

if not subagent_data:
    print("Error: Could not find subagent data message.")
    sys.exit(1)

# Step 3: Populate semantic cache using graphify.cache
from graphify.cache import save_semantic_cache, check_semantic_cache
from graphify.detect import detect

nodes = subagent_data.get("nodes", [])
edges = subagent_data.get("edges", [])
hyperedges = subagent_data.get("hyperedges", [])

saved = save_semantic_cache(nodes, edges, hyperedges, root=Path("."))
print(f"Saved {saved} semantic cache entries.")

# Step 4: Query full semantic cache for all files in workspace
detection = detect(Path("."))
all_files = []
for files_list in detection.get('files', {}).values():
    all_files.extend(files_list)

cached_nodes, cached_edges, cached_hyperedges, uncached = check_semantic_cache(all_files, root=Path("."))
print(f"Loaded from cache: {len(cached_nodes)} nodes, {len(cached_edges)} edges, {len(cached_hyperedges)} hyperedges")

# Save merged semantic data
semantic_merged = {
    "nodes": cached_nodes,
    "edges": cached_edges,
    "hyperedges": cached_hyperedges,
}
Path("graphify-out/.graphify_semantic.json").write_text(json.dumps(semantic_merged, indent=2), encoding="utf-8")

# Step 5: Merge with AST data
ast_path = Path("graphify-out/.graphify_ast.json")
if ast_path.exists():
    ast_data = json.loads(ast_path.read_text(encoding="utf-8"))
else:
    ast_data = {"nodes": [], "edges": [], "hyperedges": []}

seen_ids = {n["id"] for n in ast_data.get("nodes", [])}
merged_nodes = list(ast_data.get("nodes", []))
for n in cached_nodes:
    if n["id"] not in seen_ids:
        merged_nodes.append(n)
        seen_ids.add(n["id"])

merged_edges = ast_data.get("edges", []) + cached_edges
merged_hyperedges = cached_hyperedges

merged = {
    "nodes": merged_nodes,
    "edges": merged_edges,
    "hyperedges": merged_hyperedges,
}
Path("graphify-out/.graphify_extract.json").write_text(json.dumps(merged, indent=2), encoding="utf-8")
print(f"Merged extract graph: {len(merged_nodes)} nodes, {len(merged_edges)} edges")

# Step 6: Build the networkx graph
from graphify.build import build
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json, to_html, _git_head

G = build([merged], dedup=True)
print(f"NetworkX graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Save to graph.json
to_json(G, cluster(G), "graphify-out/graph.json", force=True)

# Step 7: Run clustering and generate report/HTML
communities = cluster(G)
cohesion = score_all(G, communities)

try:
    gods = god_nodes(G)
except Exception:
    gods = []

try:
    surprises = surprising_connections(G, communities)
except Exception:
    surprises = []

labels_path = Path("graphify-out/.graphify_labels.json")
if labels_path.exists():
    try:
        labels = {int(k): v for k, v in json.loads(labels_path.read_text(encoding="utf-8")).items()}
    except Exception:
        labels = {cid: f"Community {cid}" for cid in communities}
else:
    labels = {cid: f"Community {cid}" for cid in communities}

questions = suggest_questions(G, communities, labels)
commit = _git_head()

report_content = generate(G, communities, cohesion, labels, gods, surprises,
                          detection, {"input": 0, "output": 0}, ".",
                          suggested_questions=questions, built_at_commit=commit)
Path("graphify-out/GRAPH_REPORT.md").write_text(report_content, encoding="utf-8")

to_html(G, communities, "graphify-out/graph.html", community_labels=labels)
print("Pipeline build complete! GRAPH_REPORT.md, graph.json, and graph.html updated.")
