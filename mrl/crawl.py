"""Per-domain research crawl: robots -> sitemaps -> families -> samples -> data/<domain>/.

Usage: python -m mrl.crawl <domain> [--out data] [--delay 1.0]
"""
import argparse
import csv
import gzip
import json
import pathlib
import sys
import time

from mrl.classify import families, is_localized, section_counts
from mrl.extract import extract_page
from mrl.probe import probe_channels
from mrl.sitemaps import parse_robots, walk_sitemaps

UA = "market-research-lab/1.0 (open-source sitemap research bot; polite, robots-respecting)"


class RequestsHTTP:
    def __init__(self, timeout=30, max_bytes=80_000_000):
        import requests
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
        self.timeout, self.max_bytes = timeout, max_bytes

    def get(self, url):
        for attempt in range(3):
            try:
                r = self.s.get(url, timeout=self.timeout, stream=True, allow_redirects=True)
                if r.status_code in (429, 503) and attempt < 2:
                    time.sleep(10 * (attempt + 1))
                    continue
                body = b""
                for chunk in r.iter_content(65536):
                    body += chunk
                    if len(body) > self.max_bytes:
                        break
                return r.status_code, body
            except Exception as exc:
                if attempt == 2:
                    return 0, str(exc).encode()
                time.sleep(3)
        return 0, b""


def _write_csv(path, rows, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run_domain(domain, out_root, http=None, delay=1.0, samples_per_family=3,
               min_family=5, max_sample_families=25, max_urls=1_500_000, probe=True):
    http = http or RequestsHTTP()
    out = pathlib.Path(out_root) / domain
    out.mkdir(parents=True, exist_ok=True)
    base = f"https://{domain}"
    errors, t0 = [], time.time()

    status, body = http.get(base + "/robots.txt")
    robots_txt = body.decode("utf-8", "replace") if status == 200 else ""
    if status != 200:
        errors.append(f"robots.txt status {status}")
    (out / "robots.txt").write_text(robots_txt)
    if status >= 500 or status == 0:
        robots = parse_robots("User-agent: *\nDisallow: /\n", base)  # unreachable => be conservative
    else:
        robots = parse_robots(robots_txt, base)
    eff_delay = min(max(delay, robots["crawl_delay"] or 0), 10) if delay else 0

    seeds = robots["sitemaps"] or [base + "/sitemap.xml", base + "/sitemap_index.xml"]

    def fetch(u):
        if not robots["can_fetch"](u):
            return None
        st, b = http.get(u)
        if eff_delay:
            time.sleep(eff_delay / 2)
        return b if st == 200 else None

    urls, smlog = walk_sitemaps(seeds, fetch, max_urls=max_urls)
    if not urls:
        errors.append("no URLs found in sitemaps")
    _write_csv(out / "sitemaps.csv", smlog, ["url", "ok", "kind", "count", "error"])
    with gzip.open(out / "urls.txt.gz", "wt") as f:  # artifact only (gitignored)
        f.write("\n".join(urls))

    fams = families(urls, min_size=min_family)
    secs = section_counts(urls)
    _write_csv(out / "families.csv",
               [dict(f, examples=" ".join(f["examples"])) for f in fams],
               ["template", "count", "section", "localized", "examples"])
    _write_csv(out / "sections.csv", [{"section": k, "count": v} for k, v in secs.items()],
               ["section", "count"])

    samples = []
    for fam in fams[:max_sample_families]:
        picks = fam["examples"][:samples_per_family]  # first / middle / last of the family
        for u in picks:
            if not robots["can_fetch"](u):
                samples.append({"url": u, "family": fam["template"], "skipped": "robots"})
                continue
            st, b = http.get(u)
            if eff_delay:
                time.sleep(eff_delay)
            rec = {"url": u, "family": fam["template"], "status": st}
            if st == 200 and b:
                try:
                    rec.update(extract_page(b.decode("utf-8", "replace"), u))
                except Exception as exc:
                    rec["error"] = str(exc)[:200]
            samples.append(rec)
    (out / "samples.json").write_text(json.dumps(samples, indent=1))

    home = {}
    st, b = http.get(base + "/")
    if st == 200 and b:
        home = extract_page(b.decode("utf-8", "replace"), base + "/")
    else:
        errors.append(f"home status {st}")
    (out / "home.json").write_text(json.dumps(home, indent=1))

    probes = probe_channels(domain, http, robots["can_fetch"], delay=eff_delay) if probe else []
    (out / "channels.json").write_text(json.dumps(probes, indent=1))

    summary = {
        "domain": domain,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "robots_status": status,
        "robots_sitemaps": robots["sitemaps"],
        "crawl_delay_used": eff_delay,
        "sitemaps_fetched": sum(1 for l in smlog if l["ok"]),
        "sitemaps_failed": sum(1 for l in smlog if not l["ok"]),
        "urls_total": len(urls),
        "urls_capped": len(urls) >= max_urls,
        "localized_urls": sum(1 for u in urls if is_localized(u)),
        "sections": secs,
        "family_count": len(fams),
        "families": [{k: f[k] for k in ("template", "count", "section", "localized")} for f in fams[:60]],
        "samples_fetched": sum(1 for s in samples if s.get("status") == 200),
        "channel_pages_found": [r["path"] for r in probes if r.get("status") == 200],
        "errors": errors,
        "elapsed_s": round(time.time() - t0, 1),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--out", default="data")
    ap.add_argument("--delay", type=float, default=1.0)
    a = ap.parse_args(argv)
    s = run_domain(a.domain.strip().lower(), a.out, delay=a.delay)
    print(json.dumps({k: s[k] for k in ("domain", "urls_total", "family_count", "sitemaps_fetched", "errors")}))
    return 0 if s["urls_total"] else 1


if __name__ == "__main__":
    sys.exit(main())
