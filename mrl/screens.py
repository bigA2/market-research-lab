"""Playwright screenshots of PUBLIC pages only (never fills or submits forms, never logs in).

Usage: python -m mrl.screens <domain> --data data --out screenshots
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.robotparser

SIGNUP_RE = re.compile(r"sign[-_]?up|register|get[-_]?started|start[-_]?free|try[-_]?free|/join\b", re.I)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36 market-research-lab/1.0"


def pick_targets(domain, summary, samples, home_links, n_families=5):
    base = f"https://{domain}"
    t = {"home": base + "/", "pricing": base + "/pricing"}
    same = [l for l in home_links if re.match(rf"https?://(www\.)?([a-z0-9-]+\.)*{re.escape(domain)}(/|$)", l)]
    sign = next((l for l in same if SIGNUP_RE.search(l)), None)
    t["signup"] = sign or base + "/signup"
    i = 0
    for fam in summary.get("families", []):
        s = next((x for x in samples if x.get("family") == fam["template"] and x.get("status") == 200), None)
        if s:
            i += 1
            t[f"family_{i}"] = s["url"]
        if i >= n_families:
            break
    return t


def capture(domain, data_dir, out_dir):
    from playwright.sync_api import sync_playwright
    d = pathlib.Path(data_dir) / domain
    summary = json.loads((d / "summary.json").read_text())
    samples = json.loads((d / "samples.json").read_text())
    rp = urllib.robotparser.RobotFileParser()
    rp.parse((d / "robots.txt").read_text().splitlines())
    out = pathlib.Path(out_dir) / domain
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA, locale="en-US")
        page = ctx.new_page()
        home_links = []
        try:
            page.goto(f"https://{domain}/", wait_until="domcontentloaded", timeout=45000)
            home_links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
        except Exception as exc:
            results.append({"name": "home-links", "error": str(exc)[:200]})
        targets = pick_targets(domain, summary, samples, home_links)
        for name, url in targets.items():
            rec = {"name": name, "url": url}
            if not rp.can_fetch("*", url):
                rec["skipped"] = "robots"
                results.append(rec)
                continue
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2500)
                rec.update(status=resp.status if resp else None, final_url=page.url, title=page.title())
                page.screenshot(path=str(out / f"{name}.png"), full_page=False)
                page.screenshot(path=str(out / f"{name}-full.png"), full_page=True, timeout=30000)
                rec["file"] = f"{name}.png"
            except Exception as exc:
                rec["error"] = str(exc)[:200]
            results.append(rec)
            time.sleep(2)
        br.close()
    (d / "screenshots.json").write_text(json.dumps(results, indent=1))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="screenshots")
    a = ap.parse_args(argv)
    r = capture(a.domain, a.data, a.out)
    ok = sum(1 for x in r if x.get("file"))
    print(json.dumps({"domain": a.domain, "screenshots": ok, "total": len(r)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
