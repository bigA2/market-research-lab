import csv
import gzip
import json

from mrl.crawl import run_domain


class FakeHTTP:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def get(self, url):
        self.calls.append(url)
        v = self.pages.get(url)
        return (200, v) if v is not None else (404, b"")


def _site():
    urls = "".join(f"<url><loc>https://ex.com/apps/a{i}/integrations/b{i}</loc></url>" for i in range(6))
    urls += "<url><loc>https://ex.com/private/x</loc></url><url><loc>https://ex.com/pricing</loc></url>"
    page = b"<html><head><title>T</title></head><body><h1>H</h1><a href='/x'>x</a></body></html>"
    pages = {
        "https://ex.com/robots.txt": b"User-agent: *\nDisallow: /private\nSitemap: https://ex.com/sm.xml.gz\n",
        "https://ex.com/sm.xml.gz": gzip.compress(f"<urlset>{urls}</urlset>".encode()),
        "https://ex.com/": page,
    }
    for i in range(6):
        pages[f"https://ex.com/apps/a{i}/integrations/b{i}"] = page
    return pages


def test_run_domain_end_to_end(tmp_path):
    http = FakeHTTP(_site())
    summary = run_domain("ex.com", tmp_path, http=http, delay=0, samples_per_family=3, min_family=5)
    d = tmp_path / "ex.com"
    assert summary["urls_total"] == 8
    assert summary["sitemaps_fetched"] == 1
    assert summary["families"][0]["template"] == "/apps/{x}/integrations/{x}"
    assert (d / "robots.txt").read_text().startswith("User-agent")
    rows = list(csv.DictReader(open(d / "families.csv")))
    assert rows[0]["count"] == "6"
    samples = json.loads((d / "samples.json").read_text())
    assert len(samples) == 3 and samples[0]["title"] == "T"
    assert "https://ex.com/private/x" not in http.calls  # robots respected
    assert json.loads((d / "summary.json").read_text())["domain"] == "ex.com"
    assert (d / "sections.csv").exists() and (d / "sitemaps.csv").exists()


def test_run_domain_records_errors(tmp_path):
    summary = run_domain("down.com", tmp_path, http=FakeHTTP({}), delay=0)
    assert summary["urls_total"] == 0
    assert summary["errors"]


def test_sitemap_http_status_recorded(tmp_path):
    pages = _site()
    pages["https://ex.com/robots.txt"] += b"Sitemap: https://ex.com/missing.xml\n"
    run_domain("ex.com", tmp_path, http=FakeHTTP(pages), delay=0)
    rows = list(csv.DictReader(open(tmp_path / "ex.com" / "sitemaps.csv")))
    miss = [r for r in rows if r["url"].endswith("missing.xml")][0]
    assert miss["ok"] == "False" and miss["http_status"] == "404"
