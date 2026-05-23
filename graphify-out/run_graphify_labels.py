import sys, json
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_html
from pathlib import Path

extraction = json.loads(Path('graphify-out/.graphify_extract.json').read_text())
detection  = json.loads(Path('graphify-out/.graphify_detect.json').read_text())
analysis   = json.loads(Path('graphify-out/.graphify_analysis.json').read_text())

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}
cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

LABELS_DICT = {
    0: "Core Agent DTOs",
    1: "Bedrock LLM Supervisor",
    2: "Graph Routing Tests",
    3: "Supervisor Architecture",
    4: "DB Context Loading",
    5: "OceanCompass Chat UI",
    6: "ECR Setup Artifacts",
    7: "CI/CD Pipeline Artifacts",
    8: "Job Description Artifacts",
    9: "Agent Init",
    10: "Anticipatory Advisor",
    11: "Service Orders",
    12: "Workflow Standards",
    13: "Guest Service Worker",
    14: "LLM Routing Designs",
    15: "Database Schema",
    16: "Agent State",
    17: "Main App Entry",
    18: "Type Compliance Standard",
    19: "TDD Testing Standard",
    20: "Project Overview",
    21: "Spec Driven Development",
    22: "Workflow Sync",
    23: "JD Alignment Architecture"
}

labels = LABELS_DICT

questions = suggest_questions(G, communities, labels)

report = generate(G, communities, cohesion, labels, analysis['gods'], analysis['surprises'], detection, tokens, '.', suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report)
Path('graphify-out/.graphify_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}))
print('Report updated with community labels')

# Generate HTML
to_html(G, communities, 'graphify-out/graph.html', community_labels=labels)
print('HTML Graph generated: graphify-out/graph.html')
