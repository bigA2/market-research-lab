# STATUS: verification (2026-11-15)

## Verdict

**PASS.** The final research run is green, and the data files are non-empty for all 3 domains. Earlier failures and the remaining gaps are listed below.

## Workflow runs

| Run | Workflow | Result | Notes |
|---|---|---|---|
| [43692969553](https://github.com/bigA2/market-research-lab/actions/runs/43692969553) | vet-skills #1 | ❌ failure | the scan itself finished; the summary step crashed because `vetting/` didn't exist. Fixed in `ba1b04c` |
| [43694083758](https://github.com/bigA2/market-research-lab/actions/runs/43694083758) | vet-skills #2 | ✅ success | committed `vetting/skillspector-summary.json` + `file-verdicts.csv` |
| [43694693524](https://github.com/bigA2/market-research-lab/actions/runs/43694693524) | vet-skills #3 | ✅ success | re-run after the vet tool changed |
| [43693308485](https://github.com/bigA2/market-research-lab/actions/runs/43693308485) | research #1 (push of `targets/first.txt`) | ❌ failure | all 3 crawls succeeded, but the merge step copied every artifact flat into `data/`, so the domains overwrote each other; the "no URLs" check then failed. Fixed in `8e08557` |
| [43694063199](https://github.com/bigA2/market-research-lab/actions/runs/43694063199) | research #2 (dispatch) | ✅ success | per-domain data; Replit returned 429 on 3 screenshots |
| [43694969331](https://github.com/bigA2/market-research-lab/actions/runs/43694969331) | **research #3 (dispatch, all targets) = final** | ✅ **success** | the data used in the reports (commit `bd1b30a`) |

Unit tests: 24 passed (offline, run in CI inside the `plan` job and locally).

## Data check (final run, `data/<domain>/`)

| Domain | sitemap URLs | sitemaps ok/failed | families | samples (200) | screenshots ok | files non-empty |
|---|---|---|---|---|---|---|
| zapier.com | 424,127 | 332 / 0 | 27 | 73 of 75 | 8/8 | ✅ 9/9 |
| replit.com | 1,606 | 16 / 3 | 14 | 41 of 42 | 7/8 | ✅ 9/9 |
| make.com | 13,620 | 7 / 0 | 11 | 33 of 33 | 8/8 | ✅ 9/9 |

Artifacts (kept 30 days, until 2026-12-15): `raw-zapier.com` (10.8 MB), `raw-replit.com` (8.2 MB), `raw-make.com` (3.9 MB) contain the screenshots and full `urls.txt.gz`; `data-*` contain the compact JSON/CSV.

## Known failures and limits

1. **Replit sign-up screenshot:** https://replit.com/signup returns **403** to headless Chromium (bot protection). We did not try to get around it.
2. **Replit sitemaps:** 3 sitemaps listed in Replit's own index return **404** (careers, enterprise, partners). This is a site-side issue, recorded as a finding.
3. **Make `/enterprise` and `/apps`** return **403** to the probe (bot protection).
4. **Sample 404s:** 2 Zapier sample URLs and 1 Replit sample URL from the sitemaps return 404. This is a site-side issue, recorded as a finding.
5. **Ad libraries not checked:** `adstransparency.google.com` is blocked by this session's network policy, and we did not add an Actions job for it (the page is JS-heavy, and the Meta Ad Library needs a browser session). Paid-ads sections are therefore *unverified*.
6. **No traffic data:** without a paid SEO tool (Similarweb/Ahrefs connectors failed to connect, and we use no API keys by rule), every "drives views" statement is an *inference*.
7. **Subdomains not crawled:** community.zapier.com, community.make.com, academy.make.com, help.make.com, docs.replit.com, replit.discourse.group. Facts about them come from web search and are marked *unverified*.
8. **YouTube subscriber counts** were not found and are not reported.
9. **Sampling:** quality stats are based on 3 pages per family (top 25 families), so they are indicative, not exhaustive.
10. **Localized URLs:** 0 found in all three sitemaps. Localized pages may still exist outside sitemaps (Zapier has `/de/blog/...`, found via search).
11. **FansaChat landing repo** (`scripts/seo`, 64 pages) is outside this session's repo access. Playbook facts about it come from the founder brief and the earlier comparison, and need a check against the code.
12. **SkillSpector ran with `--no-llm`** (static analysis only), because LLM mode needs an API key and the rules forbid secrets. In static mode, 45 targets came back CAUTION with partial analysis.
13. **Node 20 deprecation warnings** from `actions/checkout@v4`, `setup-python@v5` and `upload-artifact@v4`. They are harmless today; bump the action versions later.

## Rules compliance

- Secrets: none. The workflows use only the built-in `GITHUB_TOKEN` (`permissions: contents: write`), and the repo has no repository secrets.
- No logins and no form submissions. Screenshots are taken of public pages only; the sign-up pages are rendered, never filled in.
- robots.txt is respected (sitemaps, samples, probes and screenshots are all checked with `can_fetch`), with a delay of at least 1 s between requests.
- Commits carry no `Co-Authored-By` lines.
- Third-party skills were not executed. Only SAFE `.md` files were read as methodology (see `VETTING.md`).
