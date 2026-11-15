"""On-page SEO extraction with selectolax."""
import json
import re
from urllib.parse import urljoin, urlsplit

from selectolax.lexbor import LexborHTMLParser as HTMLParser


SOCIAL = ("youtube.com", "youtu.be", "twitter.com", "x.com", "linkedin.com", "facebook.com",
          "instagram.com", "tiktok.com", "reddit.com", "discord.gg", "discord.com", "github.com",
          "apps.apple.com", "play.google.com", "chromewebstore.google.com", "chrome.google.com",
          "aws.amazon.com", "console.cloud.google.com", "cloud.google.com", "azuremarketplace.microsoft.com",
          "appsource.microsoft.com", "producthunt.com", "threads.net", "bsky.app", "medium.com", "podcasts.apple.com",
          "open.spotify.com", "g2.com", "capterra.com")


def _host(u):
    h = urlsplit(u).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def _types(obj, out):
    if isinstance(obj, list):
        for o in obj:
            _types(o, out)
    elif isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, str):
            out.add(t)
        elif isinstance(t, list):
            out.update(x for x in t if isinstance(x, str))
        for v in obj.values():
            if isinstance(v, (dict, list)):
                _types(v, out)


def extract_page(html_text, url):
    tree = HTMLParser(html_text)
    title = tree.css_first("title")
    title = re.sub(r"\s+", " ", title.text()).strip() if title else None
    md = tree.css_first('meta[name="description"]')
    canon = tree.css_first('link[rel="canonical"]')
    robots = tree.css_first('meta[name="robots"]')
    types = set()
    for s in tree.css('script[type="application/ld+json"]'):
        try:
            _types(json.loads(s.text()), types)
        except Exception:
            pass
    hreflangs = [l.attributes.get("hreflang") for l in tree.css('link[rel="alternate"][hreflang]')]
    base = _host(url)
    internal = external = 0
    ext_domains = {}
    social = []
    for a in tree.css("a[href]"):
        href = (a.attributes.get("href") or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absu = urljoin(url, href)
        h = _host(absu)
        if h == base or h.endswith("." + base):
            internal += 1
        else:
            external += 1
            ext_domains[h] = ext_domains.get(h, 0) + 1
            if any(h == d or h.endswith("." + d) for d in SOCIAL) and absu not in social:
                social.append(absu)
    h1 = [re.sub(r"\s+", " ", n.text()).strip() for n in tree.css("h1")]
    h2 = len(tree.css("h2"))
    for tag in ("script", "style", "noscript", "template", "svg"):
        for n in tree.css(tag):
            n.decompose()
    body = tree.body
    text = body.text(separator=" ") if body else ""
    return {
        "url": url,
        "title": title,
        "h1": h1,
        "h2_count": h2,
        "meta_description": md.attributes.get("content") if md else None,
        "canonical": canon.attributes.get("href") if canon else None,
        "meta_robots": robots.attributes.get("content") if robots else None,
        "schema_types": sorted(types),
        "hreflang_count": len(hreflangs),
        "internal_links": internal,
        "external_links": external,
        "external_domains": dict(sorted(ext_domains.items(), key=lambda kv: -kv[1])[:30]),
        "social_and_store_links": social[:40],
        "word_count": len(re.findall(r"\w+", text)),
    }
