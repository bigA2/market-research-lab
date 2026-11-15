from mrl.probe import probe_channels, CANDIDATES


class H:
    def get(self, url):
        if url.endswith("/affiliates"):
            return 200, b"<title>Affiliate program</title><h1>Earn 30%</h1>"
        return 404, b""


def test_probe_records_status_and_title():
    rows = probe_channels("ex.com", H(), can_fetch=lambda u: not u.endswith("/community"), delay=0)
    by = {r["path"]: r for r in rows}
    assert by["/affiliates"]["status"] == 200 and by["/affiliates"]["title"] == "Affiliate program"
    assert by["/community"]["status"] == "robots-disallowed"
    assert len(rows) == len(CANDIDATES)
