"""URL -> path template -> section / programmatic-SEO family."""
import re
from collections import defaultdict
from urllib.parse import urlsplit

LANGS = set("""af ar az be bg bn bs ca cs cy da de el en es et eu fa fi fil fr ga gl gu he hi hr hu hy id is it ja ka kk km kn ko lt lv mk ml mn mr ms my nb ne nl no pa pl pt ro ru si sk sl sq sr sv sw ta te th tl tr uk ur uz vi zh""".split())
LANG_RE = re.compile(r"^([a-z]{2,3})([-_][a-zA-Z0-9]{2,4})?$")

# Structural words: kept literal when they appear after the first segment.
STATIC = set("""integrations integration templates template compare vs versus alternatives alternative
tags tag category categories author authors page actions triggers action trigger use-cases
for by with how-to what-is glossary examples showcase directory en-us""".split())

SECTIONS = [
    ("integrations", {"integrations", "integration", "apps", "app", "connect", "connectors", "apps-directory", "directory", "mcp", "find-apps", "apps-and-integrations"}),
    ("templates", {"templates", "template", "zap-templates", "templates-gallery", "workflows", "workflow", "zaps", "showcase", "examples", "automations", "scenarios", "gallery"}),
    ("compare_alternatives", {"compare", "vs", "versus", "alternatives", "alternative", "comparison"}),
    ("blog", {"blog", "articles", "article", "news", "posts", "post", "stories"}),
    ("docs", {"docs", "doc", "documentation", "help", "support", "kb", "api", "reference", "sdk", "developer", "developers", "changelog", "releases"}),
    ("academy_learn", {"academy", "learn", "guides", "guide", "tutorials", "tutorial", "university", "courses", "course", "lessons", "how-to", "what-is", "glossary", "resources", "library"}),
    ("community", {"community", "forum", "discuss", "topics", "topic", "t", "c", "u", "bounties"}),
    ("events_webinars", {"events", "webinars", "webinar", "event"}),
    ("partners_experts_affiliates", {"partners", "partner", "experts", "expert", "affiliates", "affiliate", "hire", "agency", "agencies", "marketplace"}),
    ("customers", {"customers", "customer-stories", "case-studies", "case-study", "testimonials"}),
    ("use_cases_solutions", {"solutions", "use-cases", "for", "teams", "industries", "roles", "features", "ai", "agents", "agent", "products", "product", "automation", "use-case"}),
    ("pricing", {"pricing", "plans", "plan"}),
    ("legal", {"legal", "privacy", "terms", "policies", "policy", "security", "trust"}),
    ("careers", {"careers", "jobs", "job"}),
    ("landing", {"l", "lp", "page", "pages", "go", "campaign"}),
    ("signup_login", {"signup", "sign-up", "register", "login", "log-in", "signin", "sign-in"}),
]


WEAK_SECTIONS = {"use_cases_solutions"}


def _segments(url_or_path):
    path = urlsplit(url_or_path).path if "://" in url_or_path else url_or_path
    return [s for s in path.split("/") if s]


def _is_lang(seg):
    m = LANG_RE.match(seg)
    return bool(m) and m.group(1).lower() in LANGS


def is_localized(url):
    segs = _segments(url)
    return bool(segs) and _is_lang(segs[0])


def _looks_id(seg):
    return bool(re.fullmatch(r"[0-9]+|[0-9a-f]{8,}|[0-9a-f-]{20,}", seg.lower()))


def path_template(url):
    segs = _segments(url)
    out = []
    first = True
    for i, s in enumerate(segs):
        low = s.lower()
        if i == 0 and _is_lang(low):
            out.append("{lang}")
            continue
        if low.startswith("@"):
            out.append("{@user}")
        elif first and not _looks_id(low):
            out.append(low)
        elif low in STATIC and not _looks_id(low):
            out.append(low)
        else:
            out.append("{x}")
        first = False
    return "/" + "/".join(out)


def section_of(template):
    toks = [t for t in template.split("/") if t and t != "{lang}"]
    if not toks:
        return "home"
    if toks[0] == "{@user}":
        return "user_generated"
    weak = None  # left-most structural token wins; "weak" sections yield to a later strong one
    for t in toks:
        if t.startswith("{"):
            continue
        for name, words in SECTIONS:
            if t in words:
                if name in WEAK_SECTIONS:
                    weak = weak or name
                    break
                return name
    if weak:
        return weak
    return "landing" if len(toks) == 1 else "other"


def families(urls, min_size=5, n_examples=3):
    groups = defaultdict(list)
    loc = defaultdict(int)
    for u in urls:
        t = path_template(u)
        groups[t].append(u)
        if is_localized(u):
            loc[t] += 1
    fams = []
    for t, us in groups.items():
        if len(us) < min_size:
            continue
        idx = sorted({0, len(us) // 2, len(us) - 1})
        ex = [us[i] for i in idx][:n_examples]
        while len(ex) < min(n_examples, len(us)):
            ex.append(us[len(ex)])
        fams.append({"template": t, "count": len(us), "section": section_of(t),
                     "localized": loc[t], "examples": ex})
    fams.sort(key=lambda f: (-f["count"], f["template"]))
    return fams


def section_counts(urls):
    c = defaultdict(int)
    for u in urls:
        c[section_of(path_template(u))] += 1
    return dict(sorted(c.items(), key=lambda kv: -kv[1]))
