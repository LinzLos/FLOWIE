#!/usr/bin/env python3
# Checks FLOWIE reports against REPORT-CONTRACT.md v1.0: envelope, finding fields, worst-first order, counts, body sections.
#
# Usage:  python3 scripts/check_report.py operator/reports/<report>.md [more reports...]
#
# Works on a single-target report or a sweep report (one JSON object per target),
# fenced or bare. Problems are breaks of the contract's Conformance section and
# make the exit code 1. Warnings are things the contract says elsewhere (field
# order, heuristic findings marked deterministic) and do not change the exit code.
# Exit 2 means no FLOWIE report object was found in a file.
import json
import re
import sys

ENVELOPE = ["tool", "script_version", "contract_version", "target", "target_type",
            "lens", "timestamp", "invariant_failures", "counts"]
BODY = ["findings", "contract", "verified_clean", "coverage"]
FINDING = ["id", "invariant", "kind", "severity", "location", "defect",
           "consequence", "source", "verified"]
RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1}
TARGET_TYPES = {"folder", "files", "url", "screenshot", "prose", "mcp"}
LENSES = {"all", "navigator", "friction", "a11y"}
SOURCES = {"flowie", "react", "data", "lint", "browser"}
ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")


def find_reports(text):
    """Every JSON object in the text whose "tool" is FLOWIE, fenced or not."""
    decoder = json.JSONDecoder()
    found, pos = [], 0
    while True:
        start = text.find("{", pos)
        if start == -1:
            return found
        try:
            obj, end = decoder.raw_decode(text, start)
        except ValueError:
            pos = start + 1
            continue
        if isinstance(obj, dict) and obj.get("tool") == "FLOWIE":
            found.append(obj)
        pos = end


def in_order(keys, wanted):
    return [k for k in keys if k in wanted] == [k for k in wanted if k in keys]


def check(report):
    problems, warnings = [], []
    for key in ENVELOPE + BODY:
        if key not in report:
            problems.append(f"missing '{key}'")
    if not in_order(list(report), ENVELOPE + BODY):
        warnings.append("top-level fields are not in the contract's order")
    extra = [k for k in report if k not in ENVELOPE + BODY]
    if extra:
        warnings.append(f"fields the contract does not define: {extra}")
    if report.get("target_type") not in TARGET_TYPES:
        problems.append(f"target_type {report.get('target_type')!r} is not in the contract's list")
    if report.get("lens") not in LENSES:
        problems.append(f"lens {report.get('lens')!r} is not in the contract's list")
    if not ISO_8601.match(str(report.get("timestamp", ""))):
        problems.append(f"timestamp {report.get('timestamp')!r} is not ISO 8601")

    findings = report.get("findings")
    if not isinstance(findings, list):
        problems.append("'findings' is not a list")
        findings = []
    tally = {name: 0 for name in RANK}
    previous = max(RANK.values())
    seen = set()
    for finding in findings:
        fid = finding.get("id", "?")
        for key in FINDING:
            if key not in finding:
                problems.append(f"{fid}: missing '{key}'")
        if fid in seen:
            problems.append(f"{fid}: id used twice")
        seen.add(fid)
        if not in_order(list(finding), FINDING + ["fix"]):
            warnings.append(f"{fid}: fields are not in the contract's order")
        kind = finding.get("kind")
        if kind not in ("deterministic", "judgment"):
            problems.append(f"{fid}: kind {kind!r} is neither deterministic nor judgment")
        if not isinstance(finding.get("verified"), bool):
            problems.append(f"{fid}: 'verified' is not true or false")
        if "source" in finding and finding["source"] not in SOURCES:
            warnings.append(f"{fid}: source {finding['source']!r} is not in the contract's list")
        heuristic = str(finding.get("invariant", "")).startswith("heuristic:")
        if heuristic and kind == "deterministic":
            warnings.append(f"{fid}: {finding.get('invariant')} is marked deterministic (heuristics are judgment)")
        if not heuristic and kind == "judgment":
            warnings.append(f"{fid}: invariant {finding.get('invariant')!r} is marked judgment (invariants are deterministic)")
        severity = finding.get("severity")
        if severity not in RANK:
            problems.append(f"{fid}: severity {severity!r} is not on the scale")
            continue
        tally[severity] += 1
        if RANK[severity] > previous:
            problems.append(f"{fid}: {severity} listed after a lower severity (not worst-first)")
        previous = RANK[severity]

    if report.get("invariant_failures") != len(findings):
        problems.append(f"invariant_failures is {report.get('invariant_failures')} but there are {len(findings)} findings")
    if report.get("counts") != tally:
        problems.append(f"counts {report.get('counts')} do not match the findings {tally}")
    for key in ("contract", "verified_clean"):
        if key in report and (not isinstance(report[key], list) or not report[key]):
            problems.append(f"'{key}' is empty")
    if "coverage" in report and not str(report["coverage"]).strip():
        problems.append("coverage note is empty")
    return problems, warnings, tally


def main(paths):
    if not paths:
        print("usage: python3 scripts/check_report.py operator/reports/<report>.md [more reports...]")
        return 2
    worst = 0
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            reports = find_reports(handle.read())
        if not reports:
            print(f"{path}: no FLOWIE report object found")
            worst = max(worst, 2)
            continue
        for report in reports:
            problems, warnings, tally = check(report)
            kinds = [f.get("kind") for f in report.get("findings", []) if isinstance(f, dict)]
            verdict = "FAIL" if problems else "ok"
            print(f"{path}: {verdict}  target={report.get('target')}  lens={report.get('lens')}  "
                  f"findings={len(kinds)} ({tally['critical']}/{tally['high']}/{tally['medium']}/{tally['low']})  "
                  f"deterministic={kinds.count('deterministic')} judgment={kinds.count('judgment')}")
            for line in problems:
                print(f"  problem: {line}")
            for line in warnings:
                print(f"  warning: {line}")
            if problems:
                worst = max(worst, 1)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
