from mrl.extract import extract_page

HTML = """<html><head><title> Connect Slack to Gmail | Zapier </title>
<meta name="description" content="Integrate Slack and Gmail in minutes.">
<link rel="canonical" href="https://zapier.com/apps/slack/integrations/gmail">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"x"}</script>
<script type="application/ld+json">[{"@type":"FAQPage"},{"@graph":[{"@type":"BreadcrumbList"}]}]</script>
<script>var junk = "lots of words here that should not count";</script>
</head><body><h1>Slack + Gmail</h1><p>One two three four five.</p>
<a href="/apps/slack">Slack</a><a href="https://zapier.com/pricing">p</a><a href="https://other.com/">o</a><a href="#top">t</a>
</body></html>"""


def test_extract_fields():
    d = extract_page(HTML, "https://zapier.com/apps/slack/integrations/gmail")
    assert d["title"] == "Connect Slack to Gmail | Zapier"
    assert d["h1"] == ["Slack + Gmail"]
    assert d["meta_description"].startswith("Integrate Slack")
    assert d["canonical"] == "https://zapier.com/apps/slack/integrations/gmail"
    assert set(d["schema_types"]) == {"SoftwareApplication", "FAQPage", "BreadcrumbList"}
    assert d["internal_links"] == 2
    assert d["external_links"] == 1
    assert 5 <= d["word_count"] <= 12  # h1 + p + anchor text, no script text


def test_extract_handles_bad_jsonld():
    d = extract_page("<html><script type='application/ld+json'>{bad</script></html>", "https://a.com/")
    assert d["schema_types"] == [] and d["title"] is None


def test_social_links_collected():
    h = "<a href='https://www.youtube.com/@zapier'>y</a><a href='https://apps.apple.com/app/x'>a</a><a href='https://foo.com'>f</a>"
    d = extract_page(h, "https://zapier.com/")
    assert d["social_and_store_links"] == ["https://www.youtube.com/@zapier", "https://apps.apple.com/app/x"]
