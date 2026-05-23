import graphify
import inspect
from pathlib import Path

out = []
out.append(f"graphify dir: {dir(graphify)}")
out.append(f"graphify file: {graphify.__file__}")

# Check submodules
try:
    import graphify.detect as detect
    out.append(f"detect dir: {dir(detect)}")
except Exception as e:
    out.append(f"detect import failed: {e}")

try:
    import graphify.extract as extract
    out.append(f"extract dir: {dir(extract)}")
except Exception as e:
    out.append(f"extract import failed: {e}")

try:
    import graphify.build as build
    out.append(f"build dir: {dir(build)}")
except Exception as e:
    out.append(f"build import failed: {e}")

try:
    import graphify.cluster as cluster
    out.append(f"cluster dir: {dir(cluster)}")
except Exception as e:
    out.append(f"cluster import failed: {e}")

try:
    import graphify.report as report
    out.append(f"report dir: {dir(report)}")
except Exception as e:
    out.append(f"report import failed: {e}")

try:
    import graphify.cli as cli
    out.append(f"cli dir: {dir(cli)}")
except Exception as e:
    out.append(f"cli import failed: {e}")

Path("graphify-out/inspect_graphify.txt").write_text("\n".join(out))
