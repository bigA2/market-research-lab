"""Probe well-known public growth-channel paths (no login, robots-respecting)."""
import time

from mrl.extract import extract_page

CANDIDATES = ["/pricing", "/enterprise", "/affiliates", "/affiliate", "/partners", "/partner-program",
              "/experts", "/community", "/developers", "/developer-platform", "/marketplace", "/templates",
              "/integrations", "/apps", "/blog", "/learn", "/academy", "/university", "/events", "/webinars",
              "/customers", "/referral", "/refer", "/bounties", "/careers", "/compare", "/alternatives",
              "/vs", "/solutions", "/use-cases", "/ai", "/agents", "/mobile", "/download", "/startups",
              "/education", "/students", "/nonprofits", "/gallery", "/showcase", "/changelog", "/status"]


def probe_channels(domain, http, can_fetch, delay=1.0):
    rows = []
    for p in CANDIDATES:
        url = f"https://{domain}{p}"
        if not can_fetch(url):
            rows.append({"path": p, "url": url, "status": "robots-disallowed", "title": None, "h1": None})
            continue
        st, b = http.get(url)
        row = {"path": p, "url": url, "status": st, "title": None, "h1": None}
        if st == 200 and b:
            try:
                e = extract_page(b.decode("utf-8", "replace"), url)
                row.update(title=e["title"], h1=(e["h1"] or [None])[0], word_count=e["word_count"],
                           meta_description=e["meta_description"])
            except Exception as exc:
                row["error"] = str(exc)[:200]
        rows.append(row)
        if delay:
            time.sleep(delay)
    return rows
