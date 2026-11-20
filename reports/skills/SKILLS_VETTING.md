# Skills vetting — 2026-11-20 (run on branch research/skills-vetting-2026-11-21)

Plain English. Free sources only. Stars read from GitHub pages on 2026-11-20 (GitHub API was not available, so stars are rounded as shown). Last commit = from my shallow clones. Nothing from the cloned repos was executed; they were only read and scanned.

## 1. Vercel's free skills tooling

- **vercel-labs/skills** — the `npx skills` CLI (find, add, update, remove skills). 40.2k stars, MIT, last commit 2026-11-17. [repo](https://github.com/vercel-labs/skills)
- **find-skills** — a skill inside that repo (`skills/find-skills/SKILL.md`, read locally). It tells the agent to check the skills.sh leaderboard, then run `npx skills find <query>`. [source](https://github.com/vercel-labs/skills/tree/main/skills/find-skills)
- **skills.sh** — the leaderboard/directory. I could not open it: the host is blocked in this session's network. It is only referenced via the repo. Not verified.
- Telemetry: the CLI sends anonymous usage data and security-audit requests. Turn off with `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1`. [README](https://github.com/vercel-labs/skills)

Best free skills for our topics (all MIT/Apache, free, all cloned and checked here):

| Topic | Skill / repo | Stars | Last commit | Licence |
|---|---|---|---|---|
| SEO + GEO + SXO + schema + technical + competitor pages (broadest) | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (v2.6.2) | 31.1k | 2026-11-15 | MIT |
| Copywriting, content strategy, ai-seo, competitors, psychology (53 skills) | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 61.7k | 2026-11-19 | MIT |
| Huge catalogue incl. `aeo`, seo-audit, copywriting | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 30.2k | 2026-11-17 | MIT |
| GEO, entity SEO, competitor analysis, content refresh, SERP analysis (20) | [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | 253 | 2026-09-04 | Apache-2.0 |
| E-E-A-T audit, featured snippets, semantic gap, topic clusters (11) | [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | 415 | 2026-09-03 | Apache-2.0 |
| AI-search share of voice, backlink gap, competitor gap (SE Ranking; paid API for some) | [seranking/seo-skills](https://github.com/seranking/seo-skills) | 212 | 2026-11-19 | MIT |
| SEO + AEO patterns (Sanity-flavoured) | [sanity-io/agent-toolkit](https://github.com/sanity-io/agent-toolkit) | 201 | 2026-11-19 | MIT |
| Broad SEO/GEO marketing pack (56) | [whyashthakker/agent-skills-marketing](https://github.com/whyashthakker/agent-skills-marketing) | 20 | 2026-06-23 | MIT |
| Multi-skill pack incl. SEO/GEO | [resciencelab/opc-skills](https://github.com/resciencelab/opc-skills) | 1.9k | 2026-11-20 | Apache-2.0 |
| Self-hosted SEO app (not a pure skill) | [every-app/open-seo](https://github.com/every-app/open-seo) | 28.4k | 2026-11-19 | MIT |

Discovery source: a web search for SEO/GEO/AEO skill repos ([search results incl. aggregator lists](https://composio.dev/blog/best-marketing-skills)). Star-based ranking from aggregators is unreliable, so I treated stars only as a rough signal.

## 2. NVIDIA's scanner: it is called SkillSpector (name matches)

- Official repo: [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) — Apache-2.0, 27.0k stars, v2.12.0, last commit 2026-11-19. Docs: [NVIDIA scanning guide](https://docs.nvidia.com/skills/scanning-agent-skills). Coverage: [Help Net Security](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/).
- Lookalike repos exist (e.g. `ericmckinney/skillspector`, `badgids/skillspector`). I did not use them; only the NVIDIA repo was cloned and installed (from the local clone, in an isolated /tmp venv).

**Is it safe?**
- Static mode (`--no-llm`) reads files and does not execute the scanned skill. Its own docs say it is "defense in depth, not a sandbox" ([NVIDIA guide](https://docs.nvidia.com/skills/scanning-agent-skills)).
- Network: only one built-in call in static mode — a live CVE lookup to api.osv.dev, with automatic offline fallback (README line "SC4 queries OSV.dev"). In this session OSV was blocked and it fell back cleanly. LLM mode sends skill content to whichever provider you configure (default NVIDIA build.nvidia.com, needs a key) — I did not use it, no keys.
- Subprocess use is limited to optional agent-CLI LLM providers (`claude_cli`, etc.); the `codex_cli` provider is disabled by NVIDIA because its sandbox allows host-file reads (README).
- Telemetry: code search found no analytics/phone-home code; "inference usage telemetry" is a local report field about LLM calls (README/docs/INFERENCE_USAGE.md).
- Status: classifier says "Development Status :: 3 - Alpha" (pyproject.toml). Needs Python 3.12+ (this box had 3.11; used a uv-managed 3.12).

**Is it good?** Covers ~100 rule IDs: prompt injection (P*), supply chain (SC*), credential access (PE3), exfil taint-tracking (TT*), AST exec chains, hidden/concealed files, MCP tool poisoning, YARA rules (README rule tables). Observed in my runs:
- Good: it flagged real risk surface (install scripts, credential helpers, `curl|bash` text, unpinned `npx`).
- Noisy: many false positives on *security-defence* code and test fixtures — e.g. claude-seo's SSRF guard list (`169.254.169.254` blocklist) scored as "cloud metadata access" (115 hits, all in the blocklist, tests, or docs); HTML comment markers in a cluster doc flagged as "hidden instructions"; terminal-recording whitespace flagged as padding; "unpinned npx" on every doc mention.
- Weak spots: repo-level scoring is inflated (any installer or auth helper pushes it to 100/CRITICAL); recursive discovery found only 1 of 495 skills in claude-skills and "no sub-skills" in several repos, so I scanned whole repos as one unit; two big repos (marketingskills, open-seo) timed out at 9 minutes. Without an LLM key it cannot judge intent. Treat its score as a "go read these files" list, not a verdict.

## 3. Scan + manual review of the 10 candidates

Method: `skillspector scan --no-llm` (v2.12.0, telemetry off), then my own grep for `curl|sh`, base64 decode, "ignore previous instructions" phrases, zero-width characters, hooks, and network calls. Raw score = SkillSpector whole-repo score (0 best).

| Repo | Raw score | My verdict | Why |
|---|---|---|---|
| claude-seo | 100 CRITICAL (631 findings, 96.7% coverage) | **CAUTION** | Almost all findings are false positives (SSRF blocklist, tests, doc markers). Real surface: optional `extensions/*/install.sh`, scripts that call Google/DataForSEO/Moz APIs with *your* keys from env vars, and a PostToolUse hook that runs a local Python schema validator after every Write/Edit. [PRIVACY.md](https://github.com/AgriciDaniel/claude-seo/blob/main/PRIVACY.md) says no telemetry. Use core `skills/` only; skip installers and extensions. |
| marketingskills | scan timed out | **SAFE** (manual) | Instruction-only skills, no hooks, no scripts in skills. One doc (`tools/integrations/ploy.md`) shows a third-party `curl \| sh` line — docs only. The repo runs its own hidden-content CI check ([CONTRIBUTING](https://github.com/coreyhaines31/marketingskills/blob/main/CONTRIBUTING.md)). |
| claude-skills (alirezarezvani) | 7 LOW but saw only 1 of 495 skills | **CAUTION** | Too big to trust a blanket install: has session hooks (`productivity/handoff/hooks`) and `curl\|sh`-style text in 28 files; "ignore instructions" strings appear in triage/finance docs. Cherry-pick only `marketing-skill/skills/*` (read before adding). |
| seo-geo-claude-skills | 12 LOW / SAFE | **SAFE** | Only 22 "unpinned npx" mediums. No scripts, no hooks, no injection phrases. |
| superseo-skills | 80 HIGH | **SAFE** (after review) | The "HIGH" is one rubric sentence; the 27 "padding" hits are a terminal recording (`demo/*.cast`); one external URL is a star-history badge. No hooks/scripts. |
| seo-skills (SE Ranking) | 100 CRITICAL | **CAUTION** | Real: `install.sh` (clone + `curl\|bash` style), `scripts/google_auth.py` credential flow, firecrawl extension installer, `requests.post` helpers. Vendor repo pushing a paid API. Skill markdown itself looked normal. Use skills only, not installers. |
| agent-toolkit (Sanity) | 100 CRITICAL (83% coverage) | **CAUTION** | Score is driven by docs mentioning tokens/configs and 85 unpinned `npx sanity`. Official vendor repo, but only 1 skill (`seo-aeo-best-practices`) is relevant and it is Sanity-specific. |
| agent-skills-marketing | 31 MEDIUM | **CAUTION** | Low scan score, but 20 stars, last commit June 2026, one "external transmission" finding I did not trace. Low trust by popularity. |
| opc-skills | 0 (template only; discovery incomplete) | **CAUTION** | Scanner only saw the template; repo has hooks (`skills/archive/hooks/load-memory.py`, `.factory/hooks.json`) I did not review. Not needed for our topics. |
| open-seo | scan timed out | **CAUTION** | A web app (needs hosting), not a skill pack. No `curl\|sh`/injection hits in my grep. Out of scope for skills. |

Not run: SkillSpector LLM mode (no keys by rule), skills.sh audit data (host blocked).

## 4. Compare with what we use

Source checked: our 16 names map to these repos (verified by directory listing of the clones).

| Our skill | Where it lives | Status |
|---|---|---|
| seo, seo-page, seo-geo, seo-sxo, seo-schema, seo-technical, seo-content, seo-competitor-pages, seo-cluster, seo-programmatic, seo-audit | claude-seo (`skills/`) — all present | Current (v2.6.2, 2026-11-15). `seo-geo` carries 2026 data (AI Mode, ChatGPT/Perplexity numbers) and a myth list (llms.txt etc.). |
| seo-audit (alt), ai-seo, content-strategy, copywriting, marketing-psychology | marketingskills (`skills/`) — all present | Current (commit 2026-11-19). `ai-seo` is 5.4k words, `seo-audit` and `programmatic-seo` also exist. |
| aeo | claude-skills `marketing-skill/skills/aeo` — present, ~1.4k words | Current commit, but thinner than `ai-seo`/`seo-geo`. Overlaps them. |

Are ours current and enough? **Current: yes** — every source was committed within the last 6 days. **Enough: mostly.** Concrete gaps:
1. **E-E-A-T / experience audit** — we only have it as a section of `seo-content`; superseo has a dedicated `eeat-audit` (YMYL rubric).
2. **Featured snippet / answer-box targeting** — no dedicated skill; superseo `featured-snippet-optimizer`.
3. **Semantic / content-gap vs competitors** — we have competitor *pages*; no content-gap or SERP-analysis skill. aaron-he-zhu has `content-gap-analysis`, `serp-analysis`, `competitor-analysis`.
4. **Entity SEO and content refresh** — aaron-he-zhu `entity-optimizer`, `content-refresher`.
5. **AI-search share of voice (tracking citations over time)** — seranking `seo-ai-search-share-of-voice` (needs their API for live data).
6. **Overlap to prune:** `aeo` vs `ai-seo` vs `seo-geo` say similar things; keep `seo-geo` + `ai-seo`, treat `aeo` as optional.
7. Scanner gap: we had no routine skill-vetting step — SkillSpector fills it (with the false-positive caveat above).

**3–5 skills worth adding** (all MIT/Apache, read-only markdown skills):

| Add | From | Scan verdict |
|---|---|---|
| `eeat-audit` | inhouseseo/superseo-skills | SAFE |
| `featured-snippet-optimizer` + `semantic-gap-analysis` | inhouseseo/superseo-skills | SAFE |
| `content-gap-analysis` + `serp-analysis` + `competitor-analysis` | aaron-he-zhu/seo-geo-claude-skills | SAFE |
| `entity-optimizer` + `content-refresher` | aaron-he-zhu/seo-geo-claude-skills | SAFE |
| `seo-ai-search-share-of-voice` (optional, needs SE Ranking account for data) | seranking/seo-skills | CAUTION — copy the SKILL.md only, no installer |

Install rule going forward: copy only the `SKILL.md` and `references/` of the chosen skill (no `install.sh`, hooks, or `scripts/`), re-run SkillSpector on the copy, and read it once.

## Limits of this run
- skills.sh and the GitHub API were unreachable, so no install counts and rounded stars.
- Whole-repo scans, not per-skill, because SkillSpector's recursive discovery was unreliable; two scans timed out and were replaced by manual review.
- No LLM-mode scan; intent-level attacks (subtle prompt injection in prose) are only covered by my phrase/hidden-character greps.
