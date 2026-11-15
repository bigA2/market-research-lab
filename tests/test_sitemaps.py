import gzip
from mrl.sitemaps import parse_robots, parse_sitemap, walk_sitemaps, maybe_gunzip

INDEX = b"""<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc>https://e.com/s1.xml</loc></sitemap><sitemap><loc>https://e.com/s2.xml.gz</loc></sitemap></sitemapindex>"""
S1 = b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://e.com/a</loc><lastmod>2026-01-01</lastmod></url><url><loc> https://e.com/b </loc></url></urlset>"""
S2 = b"""<urlset><url><loc>https://e.com/c</loc></url></urlset>"""


def test_parse_robots():
    txt = "User-agent: *\nDisallow: /private\nSitemap: https://e.com/sitemap.xml\nsitemap: https://e.com/other.xml\n"
    r = parse_robots(txt, "https://e.com")
    assert r["sitemaps"] == ["https://e.com/sitemap.xml", "https://e.com/other.xml"]
    assert r["can_fetch"]("https://e.com/public")
    assert not r["can_fetch"]("https://e.com/private/x")


def test_parse_sitemap_index_and_urlset():
    kind, locs = parse_sitemap(INDEX)
    assert kind == "index" and locs == ["https://e.com/s1.xml", "https://e.com/s2.xml.gz"]
    kind, locs = parse_sitemap(S1)
    assert kind == "urlset" and locs == ["https://e.com/a", "https://e.com/b"]


def test_gunzip_sniffs_magic():
    assert maybe_gunzip(gzip.compress(b"hello")) == b"hello"
    assert maybe_gunzip(b"plain") == b"plain"


def test_walk_recursive_with_gz():
    pages = {"https://e.com/sitemap.xml": INDEX, "https://e.com/s1.xml": S1,
             "https://e.com/s2.xml.gz": gzip.compress(S2)}
    fetch = lambda u: pages.get(u)
    urls, log = walk_sitemaps(["https://e.com/sitemap.xml"], fetch)
    assert sorted(urls) == ["https://e.com/a", "https://e.com/b", "https://e.com/c"]
    assert {l["url"] for l in log} == set(pages)
    assert all(l["ok"] for l in log)


def test_walk_survives_missing_and_loops():
    pages = {"https://e.com/sitemap.xml": INDEX.replace(b"s2.xml.gz", b"sitemap.xml")}
    urls, log = walk_sitemaps(["https://e.com/sitemap.xml"], pages.get)
    assert urls == []
    assert any(not l["ok"] for l in log)  # s1 missing
    assert len(log) == 2  # loop not re-fetched


def test_walk_caps_urls():
    big = b"<urlset>" + b"".join(b"<url><loc>https://e.com/p%d</loc></url>" % i for i in range(50)) + b"</urlset>"
    urls, _ = walk_sitemaps(["https://e.com/s.xml"], {"https://e.com/s.xml": big}.get, max_urls=10)
    assert len(urls) == 10
