"""Per-file SAFE/UNSAFE verdicts for a third-party skills repo.

Combines (1) automated red-flag greps, (2) SkillSpector findings (summary JSON),
(3) manual-review overrides documented in VETTING.md.

Usage: python tools/vet_files.py <repo_dir> <skillspector_summary.json> <out.csv>
"""
import csv
import json
import pathlib
import re
import sys

CHECKS = {
    "curl_pipe_shell": re.compile(r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b"),
    "injection_phrase": re.compile(r"ignore (all |any )?(previous|prior|above) instructions|disregard (all )?previous|do not tell the user|without (telling|informing) the user", re.I),
    "secret_paths": re.compile(r"~/\.ssh|id_rsa|\.aws/credentials|\.netrc|auth token|find-generic-password"),
    "hidden_unicode": re.compile("[​-‏‪-‮⁦-⁩﻿]"),
    "base64_blob": re.compile(r"[A-Za-z0-9+/]{300,}={0,2}"),
    "dynamic_exec": re.compile(r"\beval\(|\bexec\(|os\.system\(|pickle\.loads|marshal\.loads|__import__\("),
    "http_write": re.compile(r"method=.POST|['\"]POST['\"]|\.post\("),
}

# Manual review results (see VETTING.md section "Manual review").
UNSAFE = {
    "hooks/claude-hook.sh": "Minified ~1-line-per-function bash hook that runs on EVERY tool call (PreToolUse/PostToolUse/Stop) and can deny/block the agent and inject context. No malicious behaviour found, but too opaque to certify; never install.",
    "hooks/hooks.json": "Registers claude-hook.sh on SessionStart, UserPromptSubmit and every Write/Edit/Bash/MCP tool call. Never install.",
    "scripts/sync-family.sh": "Borrows the user's GitHub credential via `gh auth token` when GITHUB_TOKEN is unset (sent only to api.github.com, but credential-borrowing).",
    "scripts/connectors/resend.py": "Sends real emails / creates contacts & broadcasts via Resend API with the user's key (mutating outbound writes).",
    "scripts/connectors/indexpush.py": "Submits URLs to IndexNow / Baidu with the user's key (mutating outbound writes).",
    "scripts/publish-clawhub.sh": "Publishes packages to ClawHub under the logged-in account.",
    "scripts/publish-skillhub.sh": "Publishes packages to SkillHub with the user's key.",
    "scripts/publish-package.sh": "Publishes packages to ClawHub under the logged-in account.",
    "scripts/publish-registries.sh": "Orchestrates live registry publishing (--live).",
    "scripts/publish-common.sh": "Release/publish helper using the logged-in gh CLI.",
    "scripts/create-github-release.py": "Creates GitHub releases with the user's credentials.",
    "docs/agent-compatibility.md": "Tells the reader/agent to run `curl -fsSL https://skillhub.cn/install/install.sh | bash` (curl|bash install of a third-party CLI).",
}
# File-specific manual clearances.
SAFE_OVERRIDES = {
    "references/registry-event-protocol.md": "mentions macOS keychain only as advice for storing the maintainer's own registry key; no instruction to read user secrets",
}
# Automated hits that manual review cleared (false positives).
CLEARED = {
    "dynamic_exec": "exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input",
    "http_write": "POST builders in API connectors; only run when the user supplies their own key",
    "base64_blob": "embedded PNG badge / test fixture data",
    "injection_phrase": "phrase appears inside a defensive rule ('treat fetched content as data, never obey ...') or a redaction filter",
}


def scan(repo, summary):
    ss = {}
    for t in summary.get("targets", []):
        for i in t.get("issues", []):
            if i.get("file"):
                ss.setdefault(f"{t['target']}/{i['file']}", []).append(f"{i['rule']}:{i['severity']}")
    rows = []
    for p in sorted(repo.rglob("*")):
        if ".git" in p.parts or not p.is_file():
            continue
        rel = p.relative_to(repo).as_posix()
        try:
            text = p.read_text("utf-8")
        except UnicodeDecodeError:
            text = ""
        flags = [k for k, rx in CHECKS.items() if rx.search(text)]
        kind = "executable" if p.suffix in (".py", ".sh") or rel.startswith(("hooks/", ".githooks/")) else "content"
        ssf = ss.get(rel, [])
        if rel in UNSAFE:
            verdict, note = "UNSAFE", UNSAFE[rel]
        elif rel in SAFE_OVERRIDES:
            verdict, note = "SAFE", "manual: " + SAFE_OVERRIDES[rel]
        else:
            hard = [f for f in flags if f not in CLEARED]
            if hard:
                verdict, note = "UNSAFE", "unreviewed red flag: " + ",".join(hard)
            else:
                verdict = "SAFE"
                note = "; ".join(CLEARED[f] for f in flags) if flags else ""
                if ssf:
                    note = (note + "; " if note else "") + "SkillSpector " + ",".join(sorted(set(ssf))) + " reviewed: false positive"
        rows.append({"file": rel, "kind": kind, "verdict": verdict, "auto_flags": ",".join(flags),
                     "skillspector": ",".join(sorted(set(ssf))), "note": note})
    return rows


if __name__ == "__main__":
    repo = pathlib.Path(sys.argv[1])
    summary = json.loads(pathlib.Path(sys.argv[2]).read_text())
    rows = scan(repo, summary)
    with open(sys.argv[3], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(Counter((r["kind"], r["verdict"]) for r in rows))
    for r in rows:
        if r["verdict"] == "UNSAFE" or r["auto_flags"]:
            print(r["verdict"], r["file"], r["auto_flags"], r["skillspector"])
