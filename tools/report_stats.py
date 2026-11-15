"""Print per-domain evidence tables (markdown) from data/<domain>/ for the reports."""
import collections
import json
import pathlib
import statistics
import sys


def main(domain):
    d = pathlib.Path("data") / domain
    s = json.loads((d / "summary.json").read_text())
    samples = json.loads((d / "samples.json").read_text())
    ch = json.loads((d / "channels.json").read_text())
    home = json.loads((d / "home.json").read_text())
    print(f"## {domain}: {s['urls_total']:,} sitemap URLs, {s['sitemaps_fetched']} sitemaps ok / {s['sitemaps_failed']} failed, generated {s['generated_at']}")
    print("\n### families\n| template | URLs | section | sampled | median words | titles unique | meta desc present | canonical self | schema types (top) | median internal links |\n|---|---|---|---|---|---|---|---|---|---|")
    by = collections.defaultdict(list)
    for x in samples:
        by[x["family"]].append(x)
    for f in s["families"]:
        xs = [x for x in by.get(f["template"], []) if x.get("status") == 200]
        if not xs:
            print(f"| `{f['template']}` | {f['count']:,} | {f['section']} | 0 | | | | | | |")
            continue
        wc = statistics.median(x["word_count"] for x in xs)
        il = statistics.median(x["internal_links"] for x in xs)
        titles = len({x["title"] for x in xs})
        md = sum(1 for x in xs if x.get("meta_description"))
        canon = sum(1 for x in xs if (x.get("canonical") or "").rstrip("/") == x["url"].rstrip("/"))
        st = collections.Counter(t for x in xs for t in x["schema_types"])
        top = ",".join(t for t, _ in st.most_common(4)) or "none"
        print(f"| `{f['template']}` | {f['count']:,} | {f['section']} | {len(xs)} | {wc:.0f} | {titles}/{len(xs)} | {md}/{len(xs)} | {canon}/{len(xs)} | {top} | {il:.0f} |")
    bad = [x for x in samples if x.get("status") != 200]
    print("\n### non-200 samples")
    for x in bad:
        print(f"- {x.get('status')} {x['url']}")
    print("\n### sample titles / H1 / meta (1 per family)")
    for f in s["families"][:25]:
        xs = [x for x in by.get(f["template"], []) if x.get("status") == 200]
        if xs:
            x = xs[0]
            print(f"- `{f['template']}`: {x['url']}\n  - title: {x['title']!r}; h1: {(x['h1'] or [None])[0]!r}; h1 count {len(x['h1'])}; meta: {(x.get('meta_description') or '')[:140]!r}; robots: {x.get('meta_robots')}; hreflang: {x.get('hreflang_count')}")
    print("\n### channel probes (200)")
    for r in ch:
        if r["status"] == 200:
            print(f"- {r['url']}: {r.get('title')!r} / h1 {r.get('h1')!r}")
    print("non-200:", ", ".join(f"{r['path']}={r['status']}" for r in ch if r["status"] != 200))
    print("\n### home")
    print(f"title {home.get('title')!r}; h1 {home.get('h1')}; words {home.get('word_count')}; schema {home.get('schema_types')}; hreflang {home.get('hreflang_count')}")
    print("social/store links:", home.get("social_and_store_links"))
    print("top external domains:", home.get("external_domains"))


if __name__ == "__main__":
    for dom in sys.argv[1:]:
        main(dom)
        print("\n")
