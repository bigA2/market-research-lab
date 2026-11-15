"""Summarize per-target SkillSpector JSON reports into one compact file.

Usage: python tools/summarize_skillspector.py <reports_dir> <out.json>
"""
import json
import pathlib
import sys


def summarize(reports_dir: pathlib.Path) -> dict:
    targets = []
    for p in sorted(reports_dir.glob("*.json")):
        name = p.stem
        exit_file = reports_dir / f"{name}.exit"
        exit_code = exit_file.read_text().strip() if exit_file.exists() else "?"
        try:
            d = json.loads(p.read_text())
        except Exception as exc:  # report missing/corrupt
            targets.append({"target": name, "error": str(exc), "exit": exit_code})
            continue
        ra = d.get("risk_assessment", {})
        issues = [
            {
                "rule": i.get("rule_id") or i.get("id"),
                "severity": i.get("severity"),
                "file": (i.get("location") or {}).get("file") if isinstance(i.get("location"), dict) else i.get("file"),
                "message": (i.get("message") or i.get("title") or "")[:200],
            }
            for i in d.get("issues", [])
        ]
        targets.append({
            "target": name.replace("__", "/"),
            "exit": exit_code,
            "score": ra.get("score"),
            "severity": ra.get("severity"),
            "recommendation": ra.get("recommendation"),
            "files": [c.get("path") for c in d.get("components", [])],
            "issue_count": len(issues),
            "issues": issues,
        })
    recs = {}
    for t in targets:
        recs[t.get("recommendation")] = recs.get(t.get("recommendation"), 0) + 1
    return {"targets_scanned": len(targets), "recommendations": recs, "targets": targets}


if __name__ == "__main__":
    out = summarize(pathlib.Path(sys.argv[1]))
    pathlib.Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("targets_scanned", "recommendations")}))
