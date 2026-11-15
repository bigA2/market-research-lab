# market-research-lab

Free, secret-less competitor research: robots.txt, sitemaps, programmatic-SEO page families, on-page samples, public growth-channel probes and screenshots. Everything runs on GitHub Actions.

**Rules this repo follows:** public data only; it never logs in or submits forms; it respects robots.txt (and `Crawl-delay`) and waits at least 1 s between page requests; it uses no API keys or repository secrets. The only credential it uses is the workflow's built-in `GITHUB_TOKEN`, which commits results.

## Usage

1. Add a file `targets/<anything>.txt` with one domain per line (`#` comments allowed):
   ```
   zapier.com
   make.com
   ```
2. Push it. `.github/workflows/research.yml` runs only for the target files changed in that push. Alternatively, run **Actions → research → Run workflow** and pass `domains` (space or comma separated), or leave it empty to run all `targets/*.txt`.
3. Results:
   - The run commits compact files to `data/<domain>/` (see below) plus `data/INDEX.json`.
   - Artifacts: `raw-<domain>` (screenshots: home, pricing, signup page as rendered, and the top 5 page families, viewport + full page; plus the full `urls.txt.gz`) and `data-<domain>`.

### `data/<domain>/` files

| file | content |
|---|---|
| `summary.json` | totals, sections, top 60 families, the channel pages found, errors |
| `families.csv` | every URL family (≥5 URLs sharing a path template, e.g. `/apps/{x}/integrations/{x}`) with count, section, localized count and 3 example URLs |
| `sections.csv` | URL counts per section (integrations, templates, blog, docs, compare_alternatives, academy_learn, community, partners…, landing, user_generated, other) |
| `samples.json` | 3 sampled pages per top-25 family: title, H1, H2 count, meta description, canonical, meta robots, JSON-LD types, hreflang count, internal/external links, word count |
| `home.json` | the same extraction for the homepage, plus social/app-store links |
| `channels.json` | status, title and H1 of ~40 well-known public paths (`/affiliates`, `/partners`, `/experts`, `/community`, `/templates`, `/enterprise`, …) |
| `sitemaps.csv` | every sitemap fetched (index/urlset, URL count, errors) |
| `robots.txt` | the raw robots.txt |
| `screenshots.json` | screenshot targets, HTTP status, final URL, title |

## How classification works

The tool turns each URL path into a template. The first segment stays literal unless it is an id; a leading language code becomes `{lang}`; `@handles` become `{@user}`; after that, only known structural words (`integrations`, `templates`, `vs`, `blog`, …) stay literal and everything else becomes `{x}`. Templates with at least 5 URLs are *families*. That is how programmatic SEO shows up: one template, thousands of pages. The section is taken from the first structural word in the template (`mrl/classify.py`).

## Local development

```bash
pip install -r requirements.txt
python -m pytest -q            # offline tests with fixtures
python -m mrl.crawl example.com --out data --delay 1
python -m playwright install chromium && python -m mrl.screens example.com
```

The stack is `requests` + `selectolax` (lexbor) for fetching and parsing, and Playwright for screenshots. Crawl4AI and advertools were considered but not needed (see `PLAN.md`).

## Other contents

- `VETTING.md`: security vetting of the third-party marketing-skills repo used as methodology (NVIDIA SkillSpector run in `.github/workflows/vet-skills.yml` plus a manual review).
- `reports/`: channel reports per competitor and the FansaChat playbook.

## Limits

- Sitemap walking stops at 3,000 sitemaps / 1.5M URLs per domain (`urls_capped` in `summary.json`).
- A sitemap only shows what a site *chooses* to list. Pages missing from sitemaps are not counted.
- Counts are a snapshot taken on the run date.
