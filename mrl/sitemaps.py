"""robots.txt + recursive sitemap walking (index, urlset, .gz)."""
import gzip
import html
import re
import urllib.robotparser
from collections import deque

LOC_RE = re.compile(rb"<loc>\s*(?:<!\[CDATA\[)?\s*(.*?)\s*(?:\]\]>)?\s*</loc>", re.S | re.I)


def parse_robots(text, base):
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    sitemaps = []
    for line in text.splitlines():
        if line.strip().lower().startswith("sitemap:"):
            sitemaps.append(line.split(":", 1)[1].strip())
    delay = rp.crawl_delay("*")
    return {"sitemaps": sitemaps, "crawl_delay": delay,
            "can_fetch": lambda url, ua="*": rp.can_fetch(ua, url)}


def maybe_gunzip(data):
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data


def parse_sitemap(data):
    data = maybe_gunzip(data)
    head = data[:2000].lower()
    kind = "index" if b"<sitemapindex" in head else "urlset"
    locs = [html.unescape(m.decode("utf-8", "replace")).strip() for m in LOC_RE.findall(data)]
    return kind, locs


def walk_sitemaps(seeds, fetch, max_urls=1_500_000, max_sitemaps=3000):
    """BFS over sitemap indexes. fetch(url) -> bytes|None. Returns (urls, log)."""
    seen, urls, log = set(), [], []
    url_seen = set()
    q = deque(seeds)
    while q and len(seen) < max_sitemaps and len(urls) < max_urls:
        sm = q.popleft()
        if sm in seen:
            continue
        seen.add(sm)
        entry = {"url": sm, "ok": False, "kind": None, "count": 0, "error": None}
        try:
            data = fetch(sm)
            if not data:
                entry["error"] = "empty or not fetched"
            else:
                kind, locs = parse_sitemap(data)
                entry.update(ok=True, kind=kind, count=len(locs))
                if kind == "index":
                    q.extend(l for l in locs if l not in seen)
                else:
                    for l in locs:
                        if l not in url_seen and len(urls) < max_urls:
                            url_seen.add(l)
                            urls.append(l)
        except Exception as exc:  # malformed gzip etc.
            entry["error"] = f"{type(exc).__name__}: {exc}"[:200]
        log.append(entry)
    return urls, log
