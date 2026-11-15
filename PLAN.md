# PLAN — market-research-lab

## Brainstorm (what we need and why)

Goal: a free, secret-less, repeatable way to reverse-engineer how big SaaS
competitors (Zapier, Make, Replit) acquire users, so FansaChat can copy the
free channels first.

Constraints (non-negotiable):
- No secrets anywhere. The only credential is the workflow's built-in `GITHUB_TOKEN`.
- Public data only, never log in, respect robots.txt, polite rate limits.
- Everything runs in GitHub Actions (the build sandbox can't reach most competitor sites).
- Third-party skills are read as methodology only, never executed, and only after vetting.

Options considered:
1. **Crawl4AI**: capable but heavy (it pulls a browser plus LLM extras) and we don't need its LLM features.
2. **advertools** sitemap/robots helpers: useful, but it brings pandas/scrapy and hides recursion details we want to control and test.
3. **requests + selectolax + Playwright** (chosen): small, fast, easy to unit-test offline with fixtures; Playwright only for screenshots.

Design decisions:
- The sitemap walker is recursive over `<sitemapindex>` and handles `.xml.gz` (magic-byte sniffing, not just the extension). It caps total sitemaps and URLs so a single run stays bounded.
- URL classification is **two-layer**: (a) rule-based sections (blog, docs, templates, compare, integrations, localized, pricing, legal, careers, …); (b) automatic *family* detection: the path is turned into a template with variable segments replaced by `{x}` (e.g. `/apps/{x}/integrations/{x}`). A family is reported when ≥5 URLs share the template, which is exactly what programmatic SEO looks like.
- Sampling: 3 pages per top family (cap 25 families/domain) are fetched with robots-check + delay. We extract title, H1, meta description, canonical, JSON-LD @types, internal/external link counts and word count.
- Screenshots: Playwright, public URLs only (home, pricing, signup page *rendered*, never submitted, plus 1 page from each of the top 5 families). Uploaded as artifacts, not committed (to keep the repo small).
- Compact outputs committed to `data/<domain>/`: `summary.json`, `families.csv`, `sections.csv`, `samples.json`, `robots.txt`, `sitemaps.csv`, `run.json` (errors and timings). Full URL lists are uploaded as gzipped artifacts only.
- The workflow commits back with `GITHUB_TOKEN` (`contents: write`), with a rebase-and-retry loop for concurrent pushes.

## Plan

### Part 0: skills vetting
1. Identify the "Aaron marketing skills" repo (GitHub search) and NVIDIA SkillSpector.
2. Workflow `.github/workflows/vet-skills.yml`: clone both at pinned SHAs, install SkillSpector, and scan every skill dir plus `scripts/` and `hooks/` with `--no-llm` (no LLM keys = no secrets). Upload the JSON and commit `vetting/skillspector-summary.json`.
3. Manual review: curl|bash, network hosts, exec/eval, env/secret reads, hooks, prompt-injection phrases, obfuscation (base64 blobs, zero-width/bidi unicode).
4. `VETTING.md` with a SAFE/UNSAFE verdict per file (generated table + manual notes).

### Part 1: tool (test-first)
1. `tests/` with offline fixtures: robots parsing, sitemap index recursion, gz decoding, URL templating/family detection, section rules, HTML extraction.
2. Implement `mrl/` modules until the tests pass.
3. `research.yml`: on push to `targets/*.txt` plus workflow_dispatch; matrix over domains; unit tests run first; crawl; screenshots; upload artifacts; final job commits `data/`.
4. README usage.

### Part 2: run plus reports
1. Push `targets/first.txt` (zapier.com, replit.com, make.com).
2. Poll the run via the GitHub API, then pull the data.
3. `reports/<domain>.md`, and `reports/FANSACHAT_PLAYBOOK.md`. Unverified numbers are marked, with URLs cited.
4. Copy the reports to `fansachat-scripts@research/zapier-compare:research/market/`.

### Part 3: verify
- The run is green, and `data/<domain>/summary.json` is non-empty for all 3 domains.
- `reports/STATUS.md` lists all failures honestly.
