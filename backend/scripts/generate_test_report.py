"""Generate a concise, committed test-report summary from local artifacts."""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "docs" / "reports" / "TEST_REPORT.md"


def command_output(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout.strip() or result.stderr.strip() or "No output"


def test_summary() -> tuple[int, int, int, float, list[str]]:
    root = ElementTree.parse(ROOT / "junit.xml").getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        raise RuntimeError("junit.xml contains no testsuite")
    failures: list[str] = []
    for case in suite.iter("testcase"):
        failure = case.find("failure")
        if failure is None:
            failure = case.find("error")
        if failure is not None:
            case_name = f"{case.get('classname')}.{case.get('name')}"
            failures.append(f"{case_name}: {failure.get('message', '')}")
    return (
        int(suite.get("tests", "0")),
        int(suite.get("failures", "0")) + int(suite.get("errors", "0")),
        int(suite.get("skipped", "0")),
        float(suite.get("time", "0")),
        failures,
    )


def coverage_summary() -> str:
    root = ElementTree.parse(ROOT / "coverage.xml").getroot()
    rate = float(root.get("line-rate", "0")) * 100
    return f"{rate:.2f}% line coverage"


def main() -> None:
    tests, failed, skipped, duration, failures = test_summary()
    sha = command_output(["git", "rev-parse", "HEAD"])
    ruff = command_output(["uv", "run", "ruff", "check", "."])
    mypy = command_output(["uv", "run", "mypy", "app"])
    report = [
        "# Test Report",
        "",
        f"- Git SHA: `{sha}`",
        f"- Generated: {datetime.now(UTC).isoformat()}",
        f"- Tests: {tests - failed - skipped} passed, {failed} failed, {skipped} skipped",
        f"- Duration: {duration:.2f}s",
        f"- Coverage: {coverage_summary()}",
        "",
        "## Quality checks",
        "",
        "```text",
        f"ruff: {ruff}",
        f"mypy: {mypy}",
        "```",
        "",
        "## Failures",
        "",
    ]
    report.extend([f"- {failure}" for failure in failures] or ["None."])
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
