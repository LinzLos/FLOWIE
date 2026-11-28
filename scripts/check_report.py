#!/usr/bin/env python3
# Checks FLOWIE reports against REPORT-CONTRACT.md (v1.0 and v1.1): envelope, finding fields, worst-first order, counts, body sections, and that each finding's kind matches its name.
#
# Usage:  python3 scripts/check_report.py operator/reports/<report>.md [more reports...]
#
# Works on a single-target report or a sweep report (one JSON object per target),
# fenced or bare. Problems are breaks of the contract's Conformance section and
# make the exit code 1. Warnings are things the contract says elsewhere (field
# order) and do not change the exit code.
# Exit 2 means no FLOWIE report object was found in a file.
#
# Names and kinds: contract 1.1 says a finding's kind follows from its name. A
# name from the script's <invariants> library is deterministic; heuristic:<name>
# and candidate:<name> are judgment; no other names are allowed. For a report
# that declares contract 1.1 or later a mismatch is a problem. For a 1.0 report
# it stays a warning, as it was when those reports were written.
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def library(script_version):
    """The invariant names defined by a script version, or None if it cannot be read."""
    paths = []
    if re.fullmatch(r"[0-9]+(\.[0-9]+)*", str(script_version or "")):
        paths.append(os.path.join(REPO, "scripts", "versions", f"v{script_version}", f"flowie_v{script_version}.xml"))
    try:
        with open(os.path.join(REPO, "manifest.json"), encoding="utf-8") as handle:
            paths.append(os.path.join(REPO, json.load(handle)["script"]["xml"]))
    except (OSError, ValueError, KeyError, TypeError):
        pass
    for path in paths:
        try:
            with open(path, encoding="utf-8") as handle:
                names = set(re.findall(r'<invariant\s+name="([^"]+)"', handle.read()))
        except OSError:
            continue
        if names:
            return names
    return None


def at_least(version, wanted):
    """True when a dotted version string such as '1.1' is at least the wanted tuple."""
    try:
        return tuple(int(part) for part in str(version).split(".")) >= wanted
    except ValueError:
        return False


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
    strict = at_least(report.get("contract_version"), (1, 1))
    names = library(report.get("script_version"))
    if names is None:
        warnings.append("could not read the script's invariant library, so finding names were not checked")
    mismatches = problems if strict else warnings
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
        name = str(finding.get("invariant", ""))
        heuristic = name.startswith("heuristic:")
        candidate = name.startswith("candidate:")
        if heuristic and kind == "deterministic":
            mismatches.append(f"{fid}: {name} is marked deterministic (heuristics are judgment)")
        elif candidate and kind == "deterministic":
            mismatches.append(f"{fid}: {name} is marked deterministic (candidates are judgment)")
        elif not heuristic and not candidate and names is not None and name not in names:
            if strict:
                problems.append(f"{fid}: {name!r} is not a named invariant (use candidate:{name} or heuristic:<name>)")
            elif kind == "deterministic":
                warnings.append(f"{fid}: {name!r} is marked deterministic but is not a named invariant")
            else:
                warnings.append(f"{fid}: invariant {name!r} is marked judgment (invariants are deterministic)")
        elif not heuristic and not candidate and kind == "judgment":
            mismatches.append(f"{fid}: invariant {name!r} is marked judgment (invariants are deterministic)")
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
