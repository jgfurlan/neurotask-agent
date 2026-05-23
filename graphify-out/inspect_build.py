import graphify.build as build
import graphify.cluster as cluster
import graphify.report as report
import inspect
from pathlib import Path

out = []
out.append("build.build signature:")
try:
    out.append(str(inspect.signature(build.build)))
except Exception as e:
    out.append(str(e))

out.append("build.build_from_json signature:")
try:
    out.append(str(inspect.signature(build.build_from_json)))
except Exception as e:
    out.append(str(e))

out.append("cluster.cluster signature:")
try:
    out.append(str(inspect.signature(cluster.cluster)))
except Exception as e:
    out.append(str(e))

out.append("report.generate signature:")
try:
    out.append(str(inspect.signature(report.generate)))
except Exception as e:
    out.append(str(e))

Path("graphify-out/inspect_build.txt").write_text("\n".join(out))
