"""Execucao reproduzivel: python tests/sprint3_runner.py v1|v2|antes|DT-01|DT-02|DT-03."""
import json, os, pathlib, subprocess, sys, tempfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
os.chdir(ROOT)
phase = sys.argv[1]
version = "v1" if phase == "v1" else "v2"
folder = ROOT / "docs/testes/relatorios" / (version if phase in ("v1", "v2") else "refatoracao" + "-" + phase)
folder.mkdir(parents=True, exist_ok=True)
data_dir = pathlib.Path(os.environ.get("SPRINT_TEMP", tempfile.gettempdir()))
environment = os.environ.copy()
environment.update({"COVERAGE_FILE": str(data_dir / (".coverage-sprint-" + phase)), "PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"})
suite = "tests/v1-llm" if version == "v1" else "tests/v2"
command = [sys.executable, "-B", "-m", "coverage", "run", "--rcfile=docs/testes/coverage.ini", "-m", "pytest", "-q", "-p", "no:cacheprovider", suite, "--junitxml=" + str(folder / "junit.xml")]
result = subprocess.run(command, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
(folder / "execucao.log").write_text(result.stdout, encoding="utf-8")
for args in (["json", "-o", str(folder / "coverage.json")], ["html", "-d", str(folder)], ["report"]):
    completed = subprocess.run([sys.executable, "-m", "coverage", *args, "--rcfile=docs/testes/coverage.ini"], env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    if args[0] == "report":
        (folder / "coverage.txt").write_text(completed.stdout, encoding="utf-8")
if (folder / "junit.xml").exists():
    cases = ET.parse(folder / "junit.xml").findall(".//testcase")
    failed = sum(c.find("failure") is not None for c in cases)
    errors = sum(c.find("error") is not None for c in cases)
    skipped = sum(c.find("skipped") is not None for c in cases)
    totals = json.loads((folder / "coverage.json").read_text())["totals"] if (folder / "coverage.json").exists() else {}
    metrics = {"phase": phase, "generated": len(cases), "passed": len(cases)-failed-errors-skipped, "failed": failed, "errors": errors, "skipped": skipped,
               "lines_hit": totals.get("covered_lines",0), "lines_total": totals.get("num_statements",0),
               "branches_hit": totals.get("covered_branches",0), "branches_total": totals.get("num_branches",0), "exit_code": result.returncode}
    metrics["line_percent"] = round(100*metrics["lines_hit"]/metrics["lines_total"],2) if metrics["lines_total"] else 0
    metrics["branch_percent"] = round(100*metrics["branches_hit"]/metrics["branches_total"],2) if metrics["branches_total"] else 0
    (folder / "metricas.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print(json.dumps(metrics))
print(result.stdout[-3000:])
sys.exit(result.returncode)
