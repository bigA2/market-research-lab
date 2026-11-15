from mrl.classify import path_template, section_of, families


def test_template_replaces_variable_segments():
    assert path_template("https://zapier.com/apps/slack/integrations/gmail") == "/apps/{x}/integrations/{x}"
    assert path_template("https://zapier.com/apps/slack/integrations") == "/apps/{x}/integrations"
    assert path_template("https://make.com/en/integrations/google-sheets") == "/{lang}/integrations/{x}"
    assert path_template("https://zapier.com/blog/best-crm-apps/") == "/blog/{x}"
    assert path_template("https://replit.com/") == "/"


def test_template_numeric_and_ids():
    assert path_template("https://x.com/templates/12345") == "/templates/{x}"
    assert path_template("https://x.com/t/abc-123-def") == "/t/{x}"


def test_sections():
    assert section_of("/apps/{x}/integrations/{x}") == "integrations"
    assert section_of("/blog/{x}") == "blog"
    assert section_of("/templates/{x}") == "templates"
    assert section_of("/{lang}/integrations/{x}") == "integrations"
    assert section_of("/compare/{x}") == "compare_alternatives"
    assert section_of("/alternatives/{x}") == "compare_alternatives"
    assert section_of("/docs/{x}") == "docs"
    assert section_of("/pricing") == "pricing"
    assert section_of("/") == "home"
    assert section_of("/foo") == "landing"


def test_localized_flag():
    from mrl.classify import is_localized
    assert is_localized("https://make.com/de/integrations/x")
    assert is_localized("https://x.com/pt-br/blog/y")
    assert not is_localized("https://x.com/blog/de")


def test_families_counts_and_threshold():
    urls = [f"https://z.com/apps/a{i}/integrations/b{i}" for i in range(7)] + [
        "https://z.com/pricing", "https://z.com/about"]
    fams = families(urls, min_size=5)
    assert fams[0]["template"] == "/apps/{x}/integrations/{x}"
    assert fams[0]["count"] == 7
    assert fams[0]["section"] == "integrations"
    assert len(fams[0]["examples"]) == 3
    assert all(f["count"] >= 5 for f in fams)


def test_app_slugs_that_look_structural_stay_variable():
    # real zapier URLs: 'ai' / 'agents' are app slugs here, not structure
    assert path_template("https://zapier.com/apps/airtable/integrations/ai") == "/apps/{x}/integrations/{x}"
    assert path_template("https://zapier.com/apps/ai/integrations/linear/255644524/x") == "/apps/{x}/integrations/{x}/{x}/{x}"
    assert path_template("https://zapier.com/find-apps/c/clockie/") == "/find-apps/{x}/{x}"


def test_first_segment_decides_section():
    assert section_of("/automations/legal/{x}/{x}/{x}") == "templates"
    assert section_of("/mcp/{x}") == "integrations"
    assert section_of("/find-apps/{x}/{x}") == "integrations"
    assert section_of("/l/{x}") == "landing"
    assert section_of("/agents/templates/{x}") == "templates"


def test_more_real_families():
    assert section_of("/build/{x}") == "use_cases_solutions"          # replit "build an X" pages
    assert section_of("/discover/{x}") == "use_cases_solutions"
    assert section_of("/languages/{x}") == "use_cases_solutions"
    assert section_of("/how-to-guides/{x}") == "academy_learn"        # make
    assert section_of("/success-stories/{x}") == "customers"
    assert section_of("/authors/{x}") == "blog"
