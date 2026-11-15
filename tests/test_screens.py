from mrl.screens import pick_targets


def test_pick_targets_finds_signup_and_families():
    summary = {"families": [{"template": "/apps/{x}"}, {"template": "/blog/{x}"}]}
    samples = [{"family": "/apps/{x}", "url": "https://ex.com/apps/a", "status": 200},
               {"family": "/blog/{x}", "url": "https://ex.com/blog/b", "status": 200}]
    home_links = ["https://ex.com/about", "https://ex.com/sign-up?ref=nav", "https://other.com/signup"]
    t = pick_targets("ex.com", summary, samples, home_links, n_families=5)
    assert t["home"] == "https://ex.com/"
    assert t["pricing"] == "https://ex.com/pricing"
    assert t["signup"] == "https://ex.com/sign-up?ref=nav"
    assert t["family_1"] == "https://ex.com/apps/a" and t["family_2"] == "https://ex.com/blog/b"


def test_pick_targets_signup_fallback():
    t = pick_targets("ex.com", {"families": []}, [], [], n_families=5)
    assert t["signup"] == "https://ex.com/signup"
