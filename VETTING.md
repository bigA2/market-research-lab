# VETTING: third-party marketing skills

Date: 2026-11-15. Reviewer: automated (NVIDIA SkillSpector) + manual review. **Verdict for use: methodology only. Read SAFE `.md` files, never install the plugin, never run its scripts or hooks.**

## 1. Which repo is "Aaron marketing skills"

GitHub search (`aaron marketing skills`, `marketing-skills`, `marketing skills claude`, sorted by stars) on 2026-11-15:

| repo | stars | note |
|---|---|---|
| **[aaron-he-zhu/aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills)** | 3,145 | **picked**: the only one by an author named Aaron (Aaron He Zhu) with real content; 120 SKILL.md skills, Apache-2.0, v20.2.0 |
| [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | 248 | signpost repo, now points to the one above |
| aaron-he-zhu/{email-marketing,paid-ads,product-launch,social-media,brand-narrative,influencer-marketing}-agent-skills | 0–8 | signpost repos that point to the one above |
| JatinyKatyal/aaron-marketing-skills, youur/aaron-marketing-skills | 0 | copies/forks, not used |
| (not Aaron) coreyhaines31/marketingskills 60,407★, alirezarezvani/claude-skills 29,830★, irinabuht12-oss/marketing-skills 7,735★ | | more-starred marketing-skill repos, but not by an Aaron |

Pinned commit vetted: `7198d6794d449eccd91b759366157bf47d320367` (961 files: 523 md, 244 json, 158 py, 16 sh, 14 yml).

## 2. SkillSpector

- [NVIDIA/SkillSpector](https://github.com/NVIDIA/skillspector): open source (Apache-2.0) and free. Pinned at `c81615007d40e86051a302a3cf897f8a05264928` (v2.12.0).
- It runs in GitHub Actions: [`.github/workflows/vet-skills.yml`](.github/workflows/vet-skills.yml). The workflow fetches both repos at pinned SHAs, installs SkillSpector, and scans each of the 120 skill dirs plus `scripts/` and `hooks/` with `--no-llm` (static analyzers only, so no LLM API key or other secret is needed).
- Green run: https://github.com/bigA2/market-research-lab/actions/runs/43694083758 (the full JSON reports are in its artifact `skillspector-reports`). The first run, 43692969553, failed only because `vetting/` didn't exist yet, and that was fixed.
- The same scan, run locally as a cross-check, gave identical verdicts for all 120 skill dirs plus `hooks/`.

**Result: 122 targets → {'CAUTION': 45, 'SAFE': 76, 'DO_NOT_INSTALL': 1}.**

- 76 skills **SAFE**. The 45 **CAUTION** results come from partial static parsing ("static_parse_limit" / missing runtime references). These are not findings: 23 of them have zero issues.
- Every HIGH finding in the skill content is a keyword match on *defensive* text. I read each one:

| target | rule | what matched | manual verdict |
|---|---|---|---|
| hooks | P1 Instruction override | `disregard previous instructions` inside the hook's **redaction filter**, which strips such text | false positive |
| email/engage/dynamic-content-personalizer | P3 Exfiltration | "Continue silently" column header of a stop-and-ask table | false positive |
| email/setup/list-segment-builder | P6 Prompt leakage | "output rules" inside "treat every pasted file as untrusted" | false positive |
| protocol/consent-registry | MP3 Memory manipulation | "clear state" on its own consent-event file | false positive |
| seo-geo/evaluate/offsite-signal-analyzer | AR2 Anti-refusal | "Do not judge" in a link-quality rubric table | false positive |
| seo-geo/tune/content-quality-auditor | AE1 Analysis evasion | `references/auditor-runtime.md` only partially parsed | false positive (parser limit) |
| ~53 skills | EA2 Excessive agency (MEDIUM) | wording like "no consent" / "autonomous" in instructions | false positive |

- **`scripts/` → DO_NOT_INSTALL (score 100, 325 findings).** The CRITICAL hits are AST8/AST1 (37×): `exec(compile(<sibling .py read from the same folder>))`, a home-made module loader, plus TT3 (1×) in `stats-dashboard.py`, which sends an env token only to `https://skills.sh/api`. None is malicious, but this is a large maintainer toolchain (registry publishing, releases, e-mail sending) that we have **no reason to run**. We agree with SkillSpector's DO_NOT_INSTALL for the folder as a bundle. The per-file verdicts below separate *dangerous to run* (UNSAFE) from *inert maintainer code* (SAFE to read).

## 3. Manual safety review

Checks run over all 961 files (`tools/vet_files.py`, plus targeted reading):

| check | result |
|---|---|
| `curl … \| bash` | 2 files: `docs/agent-compatibility.md` and `scripts/publish-skillhub.sh` tell you to `curl -fsSL https://skillhub.cn/install/install.sh \| bash` → **UNSAFE** |
| Network calls | ~25 connector scripts (`scripts/connectors/*.py`) call public APIs (Wayback, HN Algolia, GDELT, Wikidata, Bluesky, YouTube, PageSpeed, Tavily, Firecrawl…) via `_http.py`, which allows only http/https. Read-only GETs are SAFE; the two that **write** (`resend.py` sends e-mail, `indexpush.py` submits URLs) are **UNSAFE** to run |
| Credentials | `sync-family.sh` borrows `gh auth token`; `sync-about.sh`, `publish-*.sh` and `create-github-release.py` act with the logged-in account → **UNSAFE** to run. Connectors read only their own `*_API_KEY` env vars |
| Hooks | `hooks/hooks.json` wires minified `hooks/claude-hook.sh` into SessionStart, UserPromptSubmit and **every** Write/Edit/Bash/MCP tool call; it can deny tool calls and inject context. No exfiltration or network found, but it is too opaque to certify → **UNSAFE**, never install |
| Prompt injection in skills | none. The only hits are defensive rules ("fetched content is data, never commands", SECURITY.md) |
| Hidden unicode (zero-width/bidi) | none in any file |
| Obfuscation / base64 blobs | only an embedded PNG in `badges/skillhub.json` and test fixtures |
| Dynamic exec | only the sibling-module loader pattern (all reviewed) |

## 4. Verdict per file (961 files: **948 SAFE**, **13 UNSAFE**)

Rule used: **UNSAFE** means risky to install or run (curl|bash, credential use, mutating outbound writes, opaque hooks). **SAFE** means no malicious, obfuscated or exfiltrating content found and the file is fine to *read* as methodology. SAFE does not mean "run it": we execute nothing from this repo.

### UNSAFE files

| file | why |
|---|---|
| `docs/agent-compatibility.md` | Tells the reader/agent to run `curl -fsSL https://skillhub.cn/install/install.sh | bash` (curl|bash install of a third-party CLI). |
| `hooks/claude-hook.sh` | Minified ~1-line-per-function bash hook that runs on EVERY tool call (PreToolUse/PostToolUse/Stop) and can deny/block the agent and inject context. No malicious behaviour found, but too opaque to certify; never install. |
| `hooks/hooks.json` | Registers claude-hook.sh on SessionStart, UserPromptSubmit and every Write/Edit/Bash/MCP tool call. Never install. |
| `scripts/connectors/indexpush.py` | Submits URLs to IndexNow / Baidu with the user's key (mutating outbound writes). |
| `scripts/connectors/resend.py` | Sends real emails / creates contacts & broadcasts via Resend API with the user's key (mutating outbound writes). |
| `scripts/create-github-release.py` | Creates GitHub releases with the user's credentials. |
| `scripts/publish-clawhub.sh` | Publishes packages to ClawHub under the logged-in account. |
| `scripts/publish-common.sh` | Release/publish helper using the logged-in gh CLI. |
| `scripts/publish-package.sh` | Publishes packages to ClawHub under the logged-in account. |
| `scripts/publish-registries.sh` | Orchestrates live registry publishing (--live). |
| `scripts/publish-skillhub.sh` | Publishes packages to SkillHub with the user's key. |
| `scripts/sync-about.sh` | PATCHes the GitHub repo description/topics through the logged-in `gh` CLI (mutating, uses the user's credential). |
| `scripts/sync-family.sh` | Borrows the user's GitHub credential via `gh auth token` when GITHUB_TOKEN is unset (sent only to api.github.com, but credential-borrowing). |

### Skills actually used (read as methodology, nothing executed)

- `seo-geo/survey/competitor-analysis/SKILL.md`: SAFE
- `seo-geo/implement/page-play-builder/SKILL.md`: SAFE
- `seo-geo/implement/page-play-builder/references/programmatic.md`: SAFE
- `seo-geo/implement/page-play-builder/references/comparison.md`: SAFE
- `seo-geo/survey/content-gap-analysis/SKILL.md`: SAFE

What we took from them: label every number Measured / User-provided / Estimated (we use *verified / unverified*). For programmatic pages, require a per-row evidence block, an N-gram dedup check, selective indexation and batch launches. For comparison pages, apply an honesty rule and source every competitor claim.

### All files

| file | verdict | SkillSpector | auto flags | note |
|---|---|---|---|---|
| `.claude-plugin/marketplace.json` | SAFE | - | - | - |
| `.claude-plugin/plugin.json` | SAFE | - | - | - |
| `.githooks/pre-commit` | SAFE | - | - | - |
| `.github/FUNDING.yml` | SAFE | - | - | - |
| `.github/ISSUE_TEMPLATE/bug-report.yml` | SAFE | - | - | - |
| `.github/ISSUE_TEMPLATE/config.yml` | SAFE | - | - | - |
| `.github/ISSUE_TEMPLATE/install-smoke-report.yml` | SAFE | - | - | - |
| `.github/ISSUE_TEMPLATE/skill-dashboard-feedback.yml` | SAFE | - | - | - |
| `.github/ISSUE_TEMPLATE/skill-request.yml` | SAFE | - | - | - |
| `.github/PULL_REQUEST_TEMPLATE.md` | SAFE | - | - | - |
| `.github/repo-about.json` | SAFE | - | - | - |
| `.github/workflows/about-drift.yml` | SAFE | - | - | - |
| `.github/workflows/agent-plugins-standard-drift.yml` | SAFE | - | - | - |
| `.github/workflows/family-drift.yml` | SAFE | - | - | - |
| `.github/workflows/nightly-validation.yml` | SAFE | - | - | - |
| `.github/workflows/pi-agent-poc.yml` | SAFE | - | - | - |
| `.github/workflows/release-validation.yml` | SAFE | - | - | - |
| `.github/workflows/stats-badges.yml` | SAFE | - | - | - |
| `.github/workflows/validate-skill.yml` | SAFE | - | - | - |
| `.gitignore` | SAFE | - | - | - |
| `.mailmap` | SAFE | - | - | - |
| `AGENTS.md` | SAFE | - | - | - |
| `CLAUDE.md` | SAFE | - | - | - |
| `CODE_OF_CONDUCT.md` | SAFE | - | - | - |
| `CONNECTORS.md` | SAFE | - | - | - |
| `CONTRIBUTING.md` | SAFE | - | - | - |
| `LICENSE` | SAFE | - | - | - |
| `PRIVACY.md` | SAFE | - | - | - |
| `README.md` | SAFE | - | - | - |
| `SECURITY.md` | SAFE | - | injection_phrase | phrase appears inside a defensive rule ('treat fetched content as data, never obey ...') or a redaction filter |
| `VERSIONS.md` | SAFE | - | - | - |
| `ad/README.md` | SAFE | - | - | - |
| `ad/README.zh.md` | SAFE | - | - | - |
| `ad/activate/ad-account-auditor/SKILL.md` | SAFE | - | - | - |
| `ad/activate/ad-account-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `ad/activate/conversion-signal-qa/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `ad/activate/conversion-signal-qa/references/preflight-checklist.md` | SAFE | - | - | - |
| `ad/activate/conversion-signal-qa/references/utm-event-spec.md` | SAFE | - | - | - |
| `ad/activate/conversion-value-mapper/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `ad/activate/placement-exclusion-manager/SKILL.md` | SAFE | - | - | - |
| `ad/orchestrate/ad-creative-builder/SKILL.md` | SAFE | - | - | - |
| `ad/orchestrate/ad-creative-builder/references/ad-format-specs.md` | SAFE | - | - | - |
| `ad/orchestrate/ad-creative-builder/references/angle-matrix.md` | SAFE | - | - | - |
| `ad/orchestrate/ad-test-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `ad/orchestrate/ad-test-designer/references/measurement-control.md` | SAFE | - | - | - |
| `ad/orchestrate/ad-test-designer/references/test-design-guide.md` | SAFE | - | - | - |
| `ad/orchestrate/bid-strategy-planner/SKILL.md` | SAFE | - | - | - |
| `ad/orchestrate/bid-strategy-planner/references/bid-strategy-matrix.md` | SAFE | - | - | - |
| `ad/orchestrate/landing-experience-checker/SKILL.md` | SAFE | - | - | - |
| `ad/research/audience-segment-builder/SKILL.md` | SAFE | - | - | - |
| `ad/research/campaign-architect/SKILL.md` | SAFE | - | - | - |
| `ad/research/product-feed-optimizer/SKILL.md` | SAFE | - | - | - |
| `ad/research/product-feed-optimizer/references/feed-title-patterns.md` | SAFE | - | - | - |
| `ad/research/search-term-miner/SKILL.md` | SAFE | - | - | - |
| `ad/scale/attribution-reconciler/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `ad/scale/budget-pacing-monitor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `ad/scale/fatigue-frequency-manager/SKILL.md` | SAFE | - | - | - |
| `ad/scale/paid-measurement-loop/SKILL.md` | SAFE | - | - | - |
| `badges/claudeskills.json` | SAFE | - | - | - |
| `badges/clawhub.json` | SAFE | - | - | - |
| `badges/skillhub.json` | SAFE | - | base64_blob | embedded PNG badge / test fixture data |
| `badges/skillssh.json` | SAFE | - | - | - |
| `commands/ad.md` | SAFE | - | - | - |
| `commands/auto.md` | SAFE | - | - | - |
| `commands/email.md` | SAFE | - | - | - |
| `commands/influencer.md` | SAFE | - | - | - |
| `commands/launch.md` | SAFE | - | - | - |
| `commands/narrative.md` | SAFE | - | - | - |
| `commands/seo-geo.md` | SAFE | - | - | - |
| `commands/social.md` | SAFE | - | - | - |
| `docs/README.de.md` | SAFE | - | - | - |
| `docs/README.es.md` | SAFE | - | - | - |
| `docs/README.fr.md` | SAFE | - | - | - |
| `docs/README.it.md` | SAFE | - | - | - |
| `docs/README.ja.md` | SAFE | - | - | - |
| `docs/README.ko.md` | SAFE | - | - | - |
| `docs/README.md` | SAFE | - | - | - |
| `docs/README.pt.md` | SAFE | - | - | - |
| `docs/README.zh-Hant.md` | SAFE | - | - | - |
| `docs/README.zh.md` | SAFE | - | - | - |
| `docs/agent-compatibility.md` | UNSAFE | - | curl_pipe_shell | Tells the reader/agent to run `curl -fsSL https://skillhub.cn/install/install.sh / bash` (curl/bash install of a third-party CLI). |
| `docs/agent-plugins-v1.md` | SAFE | - | - | - |
| `docs/ai-staff-install.md` | SAFE | - | - | - |
| `docs/connector-playbook.md` | SAFE | - | - | - |
| `docs/context-engineering.md` | SAFE | - | - | - |
| `docs/distribution.md` | SAFE | - | - | - |
| `docs/mcp-catalog.json` | SAFE | - | - | - |
| `docs/optimization-v3-bench-definitions.md` | SAFE | - | - | - |
| `docs/optimization-v3-validation.md` | SAFE | - | - | - |
| `docs/optimization-v3.zh.md` | SAFE | - | - | - |
| `docs/registry-submissions.md` | SAFE | - | - | - |
| `docs/repo-family.md` | SAFE | - | - | - |
| `docs/skill-dashboard.md` | SAFE | - | - | - |
| `docs/system-architecture.md` | SAFE | - | - | - |
| `docs/workflow-graph.md` | SAFE | - | - | - |
| `email/README.md` | SAFE | - | - | - |
| `email/README.zh.md` | SAFE | - | - | - |
| `email/deliver/cold-outbound-sequencer/SKILL.md` | SAFE | - | - | - |
| `email/deliver/email-quality-auditor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/deliver/email-quality-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `email/deliver/inbox-placement-monitor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/deliver/inbox-placement-monitor/references/placement-telemetry-checklist.md` | SAFE | - | - | - |
| `email/deliver/send-experiment-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/engage/dynamic-content-personalizer/SKILL.md` | SAFE | P3:HIGH | - | SkillSpector hits reviewed -> P3: 'continue silently' column header in a stop-and-ask table, no transmission |
| `email/engage/email-creative-builder/SKILL.md` | SAFE | - | - | - |
| `email/engage/email-creative-builder/references/email-creative-modes.md` | SAFE | - | - | - |
| `email/engage/email-creative-builder/references/subject-line-specs.md` | SAFE | - | - | - |
| `email/engage/email-render-builder/SKILL.md` | SAFE | - | - | - |
| `email/engage/email-render-builder/references/client-render-matrix.md` | SAFE | - | - | - |
| `email/engage/email-render-builder/references/email-render-specs.md` | SAFE | - | - | - |
| `email/engage/subject-line-lab/SKILL.md` | SAFE | - | - | - |
| `email/engage/subject-line-lab/references/spam-trigger-checklist.md` | SAFE | - | - | - |
| `email/nurture/email-sequence-designer/SKILL.md` | SAFE | - | - | - |
| `email/nurture/email-sequence-designer/references/send-control.md` | SAFE | - | - | - |
| `email/nurture/newsletter-monetization-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/nurture/preference-frequency-manager/SKILL.md` | SAFE | - | - | - |
| `email/nurture/reactivation-specialist/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/setup/deliverability-qa/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/setup/deliverability-qa/references/deliverability-checklist.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/setup/list-growth-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/setup/list-hygiene-monitor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `email/setup/list-hygiene-monitor/references/hygiene-checklist.md` | SAFE | - | - | - |
| `email/setup/list-segment-builder/SKILL.md` | SAFE | EA2:MEDIUM,P6:HIGH | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / P6: 'output rules' wording inside an untrusted-i |
| `evals/README.md` | SAFE | - | - | - |
| `evals/ad-account-auditor/cases.md` | SAFE | - | - | - |
| `evals/ad-creative-builder/cases.md` | SAFE | - | - | - |
| `evals/ad-test-designer/cases.md` | SAFE | - | - | - |
| `evals/advocacy-program-designer/cases.md` | SAFE | - | - | - |
| `evals/attribution-reconciler/cases.md` | SAFE | - | - | - |
| `evals/audience-belief-mapper/cases.md` | SAFE | - | - | - |
| `evals/audience-mapper/cases.md` | SAFE | - | - | - |
| `evals/audience-segment-builder/cases.md` | SAFE | - | - | - |
| `evals/auto-routing-scenarios.source.md` | SAFE | - | - | - |
| `evals/behavior-adapter-v2.schema.json` | SAFE | - | - | - |
| `evals/behavior-adapter-v3.schema.json` | SAFE | - | - | - |
| `evals/behavior-adapter.schema.json` | SAFE | - | - | - |
| `evals/behavior-profiles.json` | SAFE | - | - | - |
| `evals/bid-strategy-planner/cases.md` | SAFE | - | - | - |
| `evals/brand-language-codifier/cases.md` | SAFE | - | - | - |
| `evals/brief-generator/cases.md` | SAFE | - | - | - |
| `evals/budget-optimizer/cases.md` | SAFE | - | - | - |
| `evals/budget-pacing-monitor/cases.md` | SAFE | - | - | - |
| `evals/campaign-architect/cases.md` | SAFE | - | - | - |
| `evals/campaign-planner/cases.md` | SAFE | - | - | - |
| `evals/category-narrative-mapper/cases.md` | SAFE | - | - | - |
| `evals/change-impact.json` | SAFE | - | - | - |
| `evals/channel-portfolio-planner/cases.md` | SAFE | - | - | - |
| `evals/channel-registry/cases.md` | SAFE | - | - | - |
| `evals/codex-behavior-candidate-output.schema.json` | SAFE | - | - | - |
| `evals/codex-behavior-model-output.schema.json` | SAFE | - | - | - |
| `evals/codex-behavior-routing-output.schema.json` | SAFE | - | - | - |
| `evals/cold-outbound-sequencer/cases.md` | SAFE | - | - | - |
| `evals/community-launch-runner/cases.md` | SAFE | - | - | - |
| `evals/competitor-analysis/cases.md` | SAFE | - | - | - |
| `evals/competitor-tracker/cases.md` | SAFE | - | - | - |
| `evals/consent-registry/cases.md` | SAFE | - | - | - |
| `evals/content-amplifier/cases.md` | SAFE | - | - | - |
| `evals/content-gap-analysis/cases.md` | SAFE | - | - | - |
| `evals/content-quality-auditor/cases.md` | SAFE | - | - | - |
| `evals/content-writer/cases.md` | SAFE | - | - | - |
| `evals/context-efficiency-policy.json` | SAFE | - | - | - |
| `evals/context-usage-v1.schema.json` | SAFE | - | - | - |
| `evals/contract-helper/cases.md` | SAFE | - | - | - |
| `evals/conversion-signal-qa/cases.md` | SAFE | - | - | - |
| `evals/conversion-value-mapper/cases.md` | SAFE | - | - | - |
| `evals/creator-content-auditor/cases.md` | SAFE | - | - | - |
| `evals/creator-registry/cases.md` | SAFE | - | - | - |
| `evals/crisis-response-planner/cases.md` | SAFE | - | - | - |
| `evals/dark-social-attributor/cases.md` | SAFE | - | - | - |
| `evals/deliverability-qa/cases.md` | SAFE | - | - | - |
| `evals/deterministic-suites.json` | SAFE | - | - | - |
| `evals/domain-authority-auditor/cases.md` | SAFE | - | - | - |
| `evals/dynamic-content-personalizer/cases.md` | SAFE | - | - | - |
| `evals/early-access-designer/cases.md` | SAFE | - | - | - |
| `evals/email-creative-builder/cases.md` | SAFE | - | - | - |
| `evals/email-quality-auditor/cases.md` | SAFE | - | - | - |
| `evals/email-render-builder/cases.md` | SAFE | - | - | - |
| `evals/email-sequence-designer/cases.md` | SAFE | - | - | - |
| `evals/engagement-inbox-manager/cases.md` | SAFE | - | - | - |
| `evals/entity-registry/cases.md` | SAFE | - | - | - |
| `evals/fatigue-frequency-manager/cases.md` | SAFE | - | - | - |
| `evals/fit-scorer/cases.md` | SAFE | - | - | - |
| `evals/geo-content-optimizer/cases.md` | SAFE | - | - | - |
| `evals/inbox-placement-monitor/cases.md` | SAFE | - | - | - |
| `evals/influencer-discovery/cases.md` | SAFE | - | - | - |
| `evals/keyword-research/cases.md` | SAFE | - | - | - |
| `evals/landing-experience-checker/cases.md` | SAFE | - | - | - |
| `evals/landing-optimizer/cases.md` | SAFE | - | - | - |
| `evals/launch-asset-packager/cases.md` | SAFE | - | - | - |
| `evals/launch-day-conductor/cases.md` | SAFE | - | - | - |
| `evals/launch-feedback-synthesizer/cases.md` | SAFE | - | - | - |
| `evals/launch-monitor/cases.md` | SAFE | - | - | - |
| `evals/launch-readiness-auditor/cases.md` | SAFE | - | - | - |
| `evals/launch-registry/cases.md` | SAFE | - | - | - |
| `evals/launch-retro-analyzer/cases.md` | SAFE | - | - | - |
| `evals/launch-tier-planner/cases.md` | SAFE | - | - | - |
| `evals/launch-window-planner/cases.md` | SAFE | - | - | - |
| `evals/list-growth-designer/cases.md` | SAFE | - | - | - |
| `evals/list-hygiene-monitor/cases.md` | SAFE | - | - | - |
| `evals/list-segment-builder/cases.md` | SAFE | - | - | - |
| `evals/memory-management/cases.md` | SAFE | - | - | - |
| `evals/message-house-builder/cases.md` | SAFE | - | - | - |
| `evals/message-system-architect/cases.md` | SAFE | - | injection_phrase | phrase appears inside a defensive rule ('treat fetched content as data, never obey ...') or a redaction filter |
| `evals/message-test-designer/cases.md` | SAFE | - | - | - |
| `evals/momentum-planner/cases.md` | SAFE | - | - | - |
| `evals/narrative-baseline-mapper/cases.md` | SAFE | - | - | - |
| `evals/narrative-cascade-planner/cases.md` | SAFE | - | - | - |
| `evals/narrative-drift-monitor/cases.md` | SAFE | - | - | - |
| `evals/narrative-enablement-kit/cases.md` | SAFE | - | - | - |
| `evals/narrative-quality-auditor/cases.md` | SAFE | - | - | - |
| `evals/narrative-registry/cases.md` | SAFE | - | - | - |
| `evals/narrative-resonance-monitor/cases.md` | SAFE | - | - | - |
| `evals/newsletter-monetization-planner/cases.md` | SAFE | - | - | - |
| `evals/offer-claims-registry/cases.md` | SAFE | - | - | - |
| `evals/offsite-signal-analyzer/cases.md` | SAFE | - | - | - |
| `evals/on-page-seo-checker/cases.md` | SAFE | - | - | - |
| `evals/outreach-manager/cases.md` | SAFE | - | - | - |
| `evals/page-play-builder/cases.md` | SAFE | - | - | - |
| `evals/paid-measurement-loop/cases.md` | SAFE | - | - | - |
| `evals/participation-warmup-planner/cases.md` | SAFE | - | - | - |
| `evals/performance-analyzer/cases.md` | SAFE | - | - | - |
| `evals/performance-monitor/cases.md` | SAFE | - | - | - |
| `evals/pitch-narrative-builder/cases.md` | SAFE | - | - | - |
| `evals/placement-exclusion-manager/cases.md` | SAFE | - | - | - |
| `evals/platform-norm-profiler/cases.md` | SAFE | - | - | - |
| `evals/positioning-mapper/cases.md` | SAFE | - | - | - |
| `evals/positioning-truth-tracer/cases.md` | SAFE | - | - | - |
| `evals/preference-frequency-manager/cases.md` | SAFE | - | - | - |
| `evals/press-media-relations/cases.md` | SAFE | - | - | - |
| `evals/pricing-packaging-planner/cases.md` | SAFE | - | - | - |
| `evals/product-feed-optimizer/cases.md` | SAFE | - | - | - |
| `evals/proof-point-packager/cases.md` | SAFE | - | - | - |
| `evals/rank-tracker/cases.md` | SAFE | - | - | - |
| `evals/reactivation-specialist/cases.md` | SAFE | - | - | - |
| `evals/report-generator/cases.md` | SAFE | - | - | - |
| `evals/roi-calculator/cases.md` | SAFE | - | - | - |
| `evals/routing-retrieval/README.md` | SAFE | - | - | - |
| `evals/routing-retrieval/cases.json` | SAFE | - | - | - |
| `evals/sales-enablement-kit/cases.md` | SAFE | - | - | - |
| `evals/search-term-miner/cases.md` | SAFE | - | - | - |
| `evals/semantic-evidence-policy.json` | SAFE | - | - | - |
| `evals/send-experiment-designer/cases.md` | SAFE | - | - | - |
| `evals/serp-analysis/cases.md` | SAFE | - | - | - |
| `evals/serp-markup-builder/cases.md` | SAFE | - | - | - |
| `evals/share-of-voice-tracker/cases.md` | SAFE | - | - | - |
| `evals/short-video-scripter/cases.md` | SAFE | - | - | - |
| `evals/site-structure-optimizer/cases.md` | SAFE | - | - | - |
| `evals/social-calendar-builder/cases.md` | SAFE | - | - | - |
| `evals/social-creative-builder/cases.md` | SAFE | - | - | - |
| `evals/social-measurement-loop/cases.md` | SAFE | - | - | - |
| `evals/social-pulse-monitor/cases.md` | SAFE | - | - | - |
| `evals/social-quality-auditor/cases.md` | SAFE | - | - | - |
| `evals/social-selling-planner/cases.md` | SAFE | - | - | - |
| `evals/story-bank-builder/cases.md` | SAFE | - | - | - |
| `evals/strategic-narrative-designer/cases.md` | SAFE | - | - | - |
| `evals/structure-manifest.json` | SAFE | - | - | - |
| `evals/subject-line-lab/cases.md` | SAFE | - | - | - |
| `evals/technical-seo-checker/cases.md` | SAFE | - | - | - |
| `evals/trend-spotter/cases.md` | SAFE | - | - | - |
| `evals/voice-dossier-builder/cases.md` | SAFE | - | - | - |
| `hooks/claude-hook.sh` | UNSAFE | P1:HIGH | injection_phrase | Minified ~1-line-per-function bash hook that runs on EVERY tool call (PreToolUse/PostToolUse/Stop) and can deny/block the agent and inject context. No malicious |
| `hooks/hooks.json` | UNSAFE | - | - | Registers claude-hook.sh on SessionStart, UserPromptSubmit and every Write/Edit/Bash/MCP tool call. Never install. |
| `influencer/README.md` | SAFE | - | - | - |
| `influencer/README.zh.md` | SAFE | - | - | - |
| `influencer/activate/content-amplifier/SKILL.md` | SAFE | - | - | - |
| `influencer/activate/content-amplifier/references/atom-extraction.md` | SAFE | - | - | - |
| `influencer/activate/content-amplifier/references/templates.md` | SAFE | EA3:LOW | - | SkillSpector hits reviewed -> EA3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `influencer/activate/contract-helper/SKILL.md` | SAFE | - | - | - |
| `influencer/activate/contract-helper/references/templates.md` | SAFE | EA2:MEDIUM,EA3:LOW | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / EA3: keyword/AST pattern hit; manual grep found  |
| `influencer/activate/creator-content-auditor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `influencer/activate/creator-content-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `influencer/activate/creator-content-auditor/references/quality-review-aids.md` | SAFE | - | - | - |
| `influencer/activate/creator-content-auditor/references/review-templates.md` | SAFE | - | - | - |
| `influencer/activate/outreach-manager/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `influencer/activate/outreach-manager/references/cold-copy-rules.md` | SAFE | - | - | - |
| `influencer/activate/outreach-manager/references/templates.md` | SAFE | - | - | - |
| `influencer/report/landing-optimizer/SKILL.md` | SAFE | - | - | - |
| `influencer/report/landing-optimizer/references/templates.md` | SAFE | - | - | - |
| `influencer/report/performance-analyzer/SKILL.md` | SAFE | - | - | - |
| `influencer/report/performance-analyzer/references/analysis-templates.md` | SAFE | - | - | - |
| `influencer/report/report-generator/SKILL.md` | SAFE | - | - | - |
| `influencer/report/report-generator/references/report-templates.md` | SAFE | - | - | - |
| `influencer/report/roi-calculator/SKILL.md` | SAFE | - | - | - |
| `influencer/report/roi-calculator/references/roi-templates.md` | SAFE | - | - | - |
| `influencer/scout/audience-mapper/SKILL.md` | SAFE | - | - | - |
| `influencer/scout/audience-mapper/references/templates.md` | SAFE | - | - | - |
| `influencer/scout/fit-scorer/SKILL.md` | SAFE | - | - | - |
| `influencer/scout/fit-scorer/references/scoring-templates.md` | SAFE | - | - | - |
| `influencer/scout/influencer-discovery/SKILL.md` | SAFE | - | - | - |
| `influencer/scout/influencer-discovery/references/creator-dossier.md` | SAFE | - | - | - |
| `influencer/scout/influencer-discovery/references/platform-vetting.md` | SAFE | - | - | - |
| `influencer/scout/influencer-discovery/references/templates.md` | SAFE | - | - | - |
| `influencer/scout/trend-spotter/SKILL.md` | SAFE | - | - | - |
| `influencer/scout/trend-spotter/references/templates.md` | SAFE | - | - | - |
| `influencer/scout/trend-spotter/references/trend-scout-recipe.md` | SAFE | - | - | - |
| `influencer/target/brief-generator/SKILL.md` | SAFE | - | - | - |
| `influencer/target/brief-generator/references/brief-templates.md` | SAFE | - | - | - |
| `influencer/target/brief-generator/references/creator-voice-intake.md` | SAFE | - | - | - |
| `influencer/target/budget-optimizer/SKILL.md` | SAFE | - | - | - |
| `influencer/target/budget-optimizer/references/templates.md` | SAFE | - | - | - |
| `influencer/target/campaign-planner/SKILL.md` | SAFE | - | - | - |
| `influencer/target/campaign-planner/references/influencer-tiers.md` | SAFE | - | - | - |
| `influencer/target/campaign-planner/references/templates.md` | SAFE | - | - | - |
| `influencer/target/competitor-tracker/SKILL.md` | SAFE | - | - | - |
| `influencer/target/competitor-tracker/references/templates.md` | SAFE | - | - | - |
| `launch/README.md` | SAFE | - | - | - |
| `launch/README.zh.md` | SAFE | - | - | - |
| `launch/assemble/launch-asset-packager/SKILL.md` | SAFE | - | - | - |
| `launch/assemble/launch-asset-packager/references/action-control.md` | SAFE | - | - | - |
| `launch/assemble/launch-asset-packager/references/asset-specs.md` | SAFE | - | - | - |
| `launch/assemble/message-house-builder/SKILL.md` | SAFE | - | - | - |
| `launch/assemble/pricing-packaging-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/assemble/sales-enablement-kit/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/mobilize/community-launch-runner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/mobilize/community-launch-runner/references/channel-matrix.md` | SAFE | - | - | - |
| `launch/mobilize/launch-day-conductor/SKILL.md` | SAFE | - | - | - |
| `launch/mobilize/launch-readiness-auditor/SKILL.md` | SAFE | - | - | - |
| `launch/mobilize/launch-readiness-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `launch/mobilize/press-media-relations/SKILL.md` | SAFE | - | - | - |
| `launch/prove/launch-feedback-synthesizer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/prove/launch-monitor/SKILL.md` | SAFE | - | - | - |
| `launch/prove/launch-retro-analyzer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/prove/momentum-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/research/early-access-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/research/launch-tier-planner/SKILL.md` | SAFE | - | - | - |
| `launch/research/launch-window-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `launch/research/positioning-mapper/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `marketplace.json` | SAFE | - | - | - |
| `memory/README.md` | SAFE | - | - | - |
| `memory/templates/decisions.md` | SAFE | - | - | - |
| `memory/templates/glossary.md` | SAFE | - | - | - |
| `memory/templates/hot-cache.md` | SAFE | - | - | - |
| `memory/templates/open-loops.md` | SAFE | - | - | - |
| `memory/templates/session-checkpoint.md` | SAFE | - | - | - |
| `narrative/README.md` | SAFE | - | - | - |
| `narrative/README.zh.md` | SAFE | - | - | - |
| `narrative/architect/brand-language-codifier/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/architect/message-system-architect/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/architect/story-bank-builder/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/architect/strategic-narrative-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/evaluate/message-test-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/evaluate/message-test-designer/references/stimulus-binding.md` | SAFE | - | - | - |
| `narrative/evaluate/narrative-drift-monitor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/evaluate/narrative-quality-auditor/SKILL.md` | SAFE | - | - | - |
| `narrative/evaluate/narrative-quality-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `narrative/evaluate/narrative-resonance-monitor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/land/narrative-cascade-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/land/narrative-enablement-kit/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/land/pitch-narrative-builder/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/land/proof-point-packager/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/trace/audience-belief-mapper/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/trace/category-narrative-mapper/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/trace/narrative-baseline-mapper/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `narrative/trace/positioning-truth-tracer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `openclaw.plugin.json` | SAFE | - | - | - |
| `protocol/channel-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/consent-registry/SKILL.md` | SAFE | MP3:HIGH | - | SkillSpector hits reviewed -> MP3: 'clear state' refers to the skill's own consent/loop event files |
| `protocol/creator-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/creator-registry/references/creator-record-template.md` | SAFE | - | - | - |
| `protocol/entity-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/entity-registry/references/entity-signal-checklist.md` | SAFE | - | - | - |
| `protocol/entity-registry/references/entity-type-reference.md` | SAFE | - | - | - |
| `protocol/entity-registry/references/example-audit-report.md` | SAFE | - | - | - |
| `protocol/entity-registry/references/knowledge-graph-guide.md` | SAFE | - | - | - |
| `protocol/entity-registry/references/knowledge-panel-wikidata-guide.md` | SAFE | - | - | - |
| `protocol/launch-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/memory-management/SKILL.md` | SAFE | - | - | - |
| `protocol/memory-management/references/consolidation-pass.md` | SAFE | - | - | - |
| `protocol/memory-management/references/examples.md` | SAFE | - | - | - |
| `protocol/memory-management/references/gdpr-purge-log-template.md` | SAFE | - | - | - |
| `protocol/memory-management/references/glossary-template.md` | SAFE | - | - | - |
| `protocol/memory-management/references/hot-cache-template.md` | SAFE | - | - | - |
| `protocol/memory-management/references/promotion-demotion-rules.md` | SAFE | - | - | - |
| `protocol/memory-management/references/update-triggers-integration.md` | SAFE | - | - | - |
| `protocol/narrative-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/offer-claims-registry/SKILL.md` | SAFE | - | - | - |
| `protocol/offer-claims-registry/references/claims-ledger-schema.md` | SAFE | - | - | - |
| `references/aaron-product-api-contract.md` | SAFE | - | - | - |
| `references/agent-plugin-portable-profile.json` | SAFE | - | - | - |
| `references/agent-plugin-portable-profile.schema.json` | SAFE | - | - | - |
| `references/audit-artifact.schema.json` | SAFE | - | - | - |
| `references/audit-loop-protocol.md` | SAFE | - | - | - |
| `references/audit-loop-state.schema.json` | SAFE | - | - | - |
| `references/audit-run.schema.json` | SAFE | - | - | - |
| `references/auditor-prompt-contract-index.schema.json` | SAFE | - | - | - |
| `references/auditor-prompt-contract.schema.json` | SAFE | - | - | - |
| `references/auditor-runbook.md` | SAFE | - | - | - |
| `references/auto-routing/ad.md` | SAFE | - | - | - |
| `references/auto-routing/cross-discipline.md` | SAFE | - | - | - |
| `references/auto-routing/email.md` | SAFE | - | - | - |
| `references/auto-routing/influencer.md` | SAFE | - | - | - |
| `references/auto-routing/launch.md` | SAFE | - | - | - |
| `references/auto-routing/narrative.md` | SAFE | - | - | - |
| `references/auto-routing/seo-geo.md` | SAFE | - | - | - |
| `references/auto-routing/social.md` | SAFE | - | - | - |
| `references/auto-routing-scenarios.md` | SAFE | - | - | - |
| `references/benchmark-boundary-examples.md` | SAFE | - | - | - |
| `references/bot-roster-profiles.json` | SAFE | - | - | - |
| `references/bot-roster-profiles.schema.json` | SAFE | - | - | - |
| `references/capability-profiles.json` | SAFE | - | - | - |
| `references/capability-profiles.md` | SAFE | - | - | - |
| `references/capability-profiles.schema.json` | SAFE | - | - | - |
| `references/cite-domain-rating.md` | SAFE | - | - | - |
| `references/context-assembly.schema.json` | SAFE | - | - | - |
| `references/context-manifest.schema.json` | SAFE | - | - | - |
| `references/context-modules.json` | SAFE | - | - | - |
| `references/context-modules.schema.json` | SAFE | - | - | - |
| `references/context-planning.md` | SAFE | - | - | - |
| `references/context-request.schema.json` | SAFE | - | - | - |
| `references/context-resolution.md` | SAFE | - | - | - |
| `references/control-artifact.schema.json` | SAFE | - | - | - |
| `references/control-bindings.json` | SAFE | - | - | - |
| `references/control-bindings.schema.json` | SAFE | - | - | - |
| `references/core-eeat-benchmark.md` | SAFE | - | - | - |
| `references/distribution-files.json` | SAFE | - | - | - |
| `references/echo-benchmark.md` | SAFE | - | - | - |
| `references/engineering-maturity-report.schema.json` | SAFE | - | - | - |
| `references/engineering-maturity-rubric.json` | SAFE | - | - | - |
| `references/engineering-maturity-rubric.schema.json` | SAFE | - | - | - |
| `references/engineering-maturity.md` | SAFE | - | - | - |
| `references/engineering-release-receipt.schema.json` | SAFE | - | - | - |
| `references/entity-geo-handoff-schema.md` | SAFE | - | - | - |
| `references/expert-panel.md` | SAFE | - | - | - |
| `references/framework-catalog.json` | SAFE | - | - | - |
| `references/framework-catalog.schema.json` | SAFE | - | - | - |
| `references/host-capability-profiles.json` | SAFE | - | - | - |
| `references/host-capability-profiles.schema.json` | SAFE | - | - | - |
| `references/humanizer-slop.md` | SAFE | - | - | - |
| `references/llms-txt-okf.md` | SAFE | - | - | - |
| `references/measurement-protocol.md` | SAFE | - | - | - |
| `references/platforms/bluesky-fediverse.md` | SAFE | - | - | - |
| `references/platforms/discourse.md` | SAFE | - | - | - |
| `references/platforms/grokipedia.md` | SAFE | - | - | - |
| `references/platforms/linkedin.md` | SAFE | - | - | - |
| `references/platforms/reddit.md` | SAFE | - | - | - |
| `references/platforms/threads.md` | SAFE | - | - | - |
| `references/platforms/tiktok.md` | SAFE | - | - | - |
| `references/platforms/wechat.md` | SAFE | - | - | - |
| `references/platforms/x.md` | SAFE | - | - | - |
| `references/platforms/xiaohongshu.md` | SAFE | - | - | - |
| `references/platforms/youtube.md` | SAFE | - | - | - |
| `references/policy-kernel.md` | SAFE | - | - | - |
| `references/profile-config.schema.json` | SAFE | - | - | - |
| `references/profile-outcome-evidence.schema.json` | SAFE | - | - | - |
| `references/profile-outcome-receipt.schema.json` | SAFE | - | - | - |
| `references/profile-resolution.schema.json` | SAFE | - | - | - |
| `references/prompt-contracts/ad-account-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/content-quality-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/creator-content-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/domain-authority-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/email-quality-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/index.json` | SAFE | - | - | - |
| `references/prompt-contracts/launch-readiness-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/narrative-quality-auditor.json` | SAFE | - | - | - |
| `references/prompt-contracts/social-quality-auditor.json` | SAFE | - | - | - |
| `references/prompt-profiles.json` | SAFE | - | - | - |
| `references/prompt-profiles.schema.json` | SAFE | - | - | - |
| `references/publication-metadata.json` | SAFE | - | - | - |
| `references/ramp-benchmark.md` | SAFE | - | - | - |
| `references/registry-event-protocol.md` | SAFE | - | secret_paths | manual: mentions macOS keychain only as advice for storing the maintainer's own registry key; no instruction to read user secrets |
| `references/registry-event.schema.json` | SAFE | - | - | - |
| `references/release-assets.schema.json` | SAFE | - | - | - |
| `references/roas-benchmark.md` | SAFE | - | - | - |
| `references/router-facade-sidecar.schema.json` | SAFE | - | - | - |
| `references/run-envelope.schema.json` | SAFE | - | - | - |
| `references/run-event.schema.json` | SAFE | - | - | - |
| `references/runtime-controller-request.schema.json` | SAFE | - | - | - |
| `references/runtime-controller.md` | SAFE | - | - | - |
| `references/runtime-invocation.md` | SAFE | - | - | - |
| `references/runtime-protocol.md` | SAFE | - | - | - |
| `references/save-point.schema.json` | SAFE | - | - | - |
| `references/scheduling.md` | SAFE | - | - | - |
| `references/scoring-rubrics/conversion-quality.md` | SAFE | - | - | - |
| `references/scoring-rubrics/visual-quality.md` | SAFE | - | - | - |
| `references/scoring-semantics.md` | SAFE | - | - | - |
| `references/send-benchmark.md` | SAFE | - | - | - |
| `references/skill-contract.md` | SAFE | - | - | - |
| `references/skill-contracts/ad-account-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/ad-creative-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/ad-test-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/advocacy-program-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/attribution-reconciler.json` | SAFE | - | - | - |
| `references/skill-contracts/audience-belief-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/audience-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/audience-segment-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/bid-strategy-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/brand-language-codifier.json` | SAFE | - | - | - |
| `references/skill-contracts/brief-generator.json` | SAFE | - | - | - |
| `references/skill-contracts/budget-optimizer.json` | SAFE | - | - | - |
| `references/skill-contracts/budget-pacing-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/campaign-architect.json` | SAFE | - | - | - |
| `references/skill-contracts/campaign-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/category-narrative-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/channel-portfolio-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/channel-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/cold-outbound-sequencer.json` | SAFE | - | - | - |
| `references/skill-contracts/community-launch-runner.json` | SAFE | - | - | - |
| `references/skill-contracts/competitor-analysis.json` | SAFE | - | - | - |
| `references/skill-contracts/competitor-tracker.json` | SAFE | - | - | - |
| `references/skill-contracts/consent-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/content-amplifier.json` | SAFE | - | - | - |
| `references/skill-contracts/content-gap-analysis.json` | SAFE | - | - | - |
| `references/skill-contracts/content-quality-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/content-writer.json` | SAFE | - | - | - |
| `references/skill-contracts/contract-helper.json` | SAFE | - | - | - |
| `references/skill-contracts/conversion-signal-qa.json` | SAFE | - | - | - |
| `references/skill-contracts/conversion-value-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/creator-content-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/creator-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/crisis-response-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/dark-social-attributor.json` | SAFE | - | - | - |
| `references/skill-contracts/deliverability-qa.json` | SAFE | - | - | - |
| `references/skill-contracts/domain-authority-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/dynamic-content-personalizer.json` | SAFE | - | - | - |
| `references/skill-contracts/early-access-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/email-creative-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/email-quality-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/email-render-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/email-sequence-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/engagement-inbox-manager.json` | SAFE | - | - | - |
| `references/skill-contracts/entity-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/fatigue-frequency-manager.json` | SAFE | - | - | - |
| `references/skill-contracts/fit-scorer.json` | SAFE | - | - | - |
| `references/skill-contracts/geo-content-optimizer.json` | SAFE | - | - | - |
| `references/skill-contracts/inbox-placement-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/index.json` | SAFE | - | - | - |
| `references/skill-contracts/influencer-discovery.json` | SAFE | - | - | - |
| `references/skill-contracts/keyword-research.json` | SAFE | - | - | - |
| `references/skill-contracts/landing-experience-checker.json` | SAFE | - | - | - |
| `references/skill-contracts/landing-optimizer.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-asset-packager.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-day-conductor.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-feedback-synthesizer.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-readiness-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-retro-analyzer.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-tier-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/launch-window-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/list-growth-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/list-hygiene-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/list-segment-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/memory-management.json` | SAFE | - | - | - |
| `references/skill-contracts/message-house-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/message-system-architect.json` | SAFE | - | - | - |
| `references/skill-contracts/message-test-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/momentum-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-baseline-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-cascade-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-drift-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-enablement-kit.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-quality-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/narrative-resonance-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/newsletter-monetization-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/offer-claims-registry.json` | SAFE | - | - | - |
| `references/skill-contracts/offsite-signal-analyzer.json` | SAFE | - | - | - |
| `references/skill-contracts/on-page-seo-checker.json` | SAFE | - | - | - |
| `references/skill-contracts/outreach-manager.json` | SAFE | - | - | - |
| `references/skill-contracts/page-play-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/paid-measurement-loop.json` | SAFE | - | - | - |
| `references/skill-contracts/participation-warmup-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/performance-analyzer.json` | SAFE | - | - | - |
| `references/skill-contracts/performance-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/pitch-narrative-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/placement-exclusion-manager.json` | SAFE | - | - | - |
| `references/skill-contracts/platform-norm-profiler.json` | SAFE | - | - | - |
| `references/skill-contracts/positioning-mapper.json` | SAFE | - | - | - |
| `references/skill-contracts/positioning-truth-tracer.json` | SAFE | - | - | - |
| `references/skill-contracts/preference-frequency-manager.json` | SAFE | - | - | - |
| `references/skill-contracts/press-media-relations.json` | SAFE | - | - | - |
| `references/skill-contracts/pricing-packaging-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/product-feed-optimizer.json` | SAFE | - | - | - |
| `references/skill-contracts/proof-point-packager.json` | SAFE | - | - | - |
| `references/skill-contracts/rank-tracker.json` | SAFE | - | - | - |
| `references/skill-contracts/reactivation-specialist.json` | SAFE | - | - | - |
| `references/skill-contracts/report-generator.json` | SAFE | - | - | - |
| `references/skill-contracts/roi-calculator.json` | SAFE | - | - | - |
| `references/skill-contracts/sales-enablement-kit.json` | SAFE | - | - | - |
| `references/skill-contracts/search-term-miner.json` | SAFE | - | - | - |
| `references/skill-contracts/send-experiment-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/serp-analysis.json` | SAFE | - | - | - |
| `references/skill-contracts/serp-markup-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/share-of-voice-tracker.json` | SAFE | - | - | - |
| `references/skill-contracts/short-video-scripter.json` | SAFE | - | - | - |
| `references/skill-contracts/site-structure-optimizer.json` | SAFE | - | - | - |
| `references/skill-contracts/social-calendar-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/social-creative-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/social-measurement-loop.json` | SAFE | - | - | - |
| `references/skill-contracts/social-pulse-monitor.json` | SAFE | - | - | - |
| `references/skill-contracts/social-quality-auditor.json` | SAFE | - | - | - |
| `references/skill-contracts/social-selling-planner.json` | SAFE | - | - | - |
| `references/skill-contracts/story-bank-builder.json` | SAFE | - | - | - |
| `references/skill-contracts/strategic-narrative-designer.json` | SAFE | - | - | - |
| `references/skill-contracts/subject-line-lab.json` | SAFE | - | - | - |
| `references/skill-contracts/technical-seo-checker.json` | SAFE | - | - | - |
| `references/skill-contracts/trend-spotter.json` | SAFE | - | - | - |
| `references/skill-contracts/voice-dossier-builder.json` | SAFE | - | - | - |
| `references/skill-dashboard.schema.json` | SAFE | - | - | - |
| `references/skill-machine-contract-index.schema.json` | SAFE | - | - | - |
| `references/skill-machine-contract.schema.json` | SAFE | - | - | - |
| `references/social/owned-community-loop.md` | SAFE | - | - | - |
| `references/social-platform-access.md` | SAFE | - | - | - |
| `references/standards/agent-plugins/1.0.0/PROVENANCE.json` | SAFE | - | - | - |
| `references/standards/agent-plugins/1.0.0/plugin.schema.json` | SAFE | - | - | - |
| `references/star-benchmark.md` | SAFE | - | - | - |
| `references/state-model.md` | SAFE | - | - | - |
| `references/system-catalog.json` | SAFE | - | - | - |
| `references/system-catalog.schema.json` | SAFE | - | - | - |
| `references/tale-benchmark.md` | SAFE | - | - | - |
| `references/turn-snapshot.schema.json` | SAFE | - | - | - |
| `references/wiki/SCHEMA.md` | SAFE | - | - | - |
| `references/wiki/entities/example-brand.md` | SAFE | - | - | - |
| `references/wiki/evolution-pipeline.md` | SAFE | - | - | - |
| `references/wiki/examples/wiki-annotation-dry-run.md` | SAFE | - | - | - |
| `references/wiki/frameworks/cite-annotation.md` | SAFE | - | - | - |
| `references/wiki/frameworks/core-eeat-annotation.md` | SAFE | - | - | - |
| `references/wiki/frameworks/tale-annotation.md` | SAFE | - | - | - |
| `references/wiki/index.md` | SAFE | - | - | - |
| `references/wiki/log.md` | SAFE | - | - | - |
| `references/wiki/okf-terminology.md` | SAFE | - | - | - |
| `references/wiki/ops-cadence.md` | SAFE | - | - | - |
| `references/wiki/patterns/evidence-taxonomy.md` | SAFE | - | - | - |
| `references/wiki/patterns/focused-retrieval.md` | SAFE | - | - | - |
| `references/wiki/patterns/handoff-budget.md` | SAFE | - | - | - |
| `references/wiki/patterns/sole-writer-registries.md` | SAFE | - | - | - |
| `references/wiki/patterns/status-is-not-verdict.md` | SAFE | - | - | - |
| `references/wiki/skill-evolution-proposal.md` | SAFE | - | - | - |
| `references/workflow-execution-approval-trust.schema.json` | SAFE | - | - | - |
| `references/workflow-execution-approval.schema.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-00.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-01.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-02.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-03.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-04.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-05.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-06.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-07.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-08.json` | SAFE | - | - | - |
| `references/workflow-graph/edges-09.json` | SAFE | - | - | - |
| `references/workflow-graph-edge-shard.schema.json` | SAFE | - | - | - |
| `references/workflow-graph-protocol.md` | SAFE | - | - | - |
| `references/workflow-graph-source.schema.json` | SAFE | - | - | - |
| `references/workflow-graph.json` | SAFE | - | - | - |
| `references/workflow-graph.schema.json` | SAFE | - | - | - |
| `references/workflow-graph.source.json` | SAFE | - | - | - |
| `references/workflow-loop-event.schema.json` | SAFE | - | - | - |
| `references/workflow-loop-plan.schema.json` | SAFE | - | - | - |
| `references/workflow-loop-protocol.md` | SAFE | - | - | - |
| `references/workflow-loop-request.schema.json` | SAFE | - | - | - |
| `references/workflow-loop-state.schema.json` | SAFE | - | - | - |
| `scripts/adapters/codex-behavior-adapter.py` | SAFE | AST4:MEDIUM,AST7:LOW | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST7: keyword/AST pattern hit; manual grep foun |
| `scripts/agent_plugin_builder.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/audit-loop.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,MP3:HIGH | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/audit-trends.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST7:LOW,AST8:CRITICAL,TT2:MEDIUM | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/build-distribution.py` | SAFE | AST3:MEDIUM,AST4:MEDIUM,AST7:LOW | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST4: keyword/AST pattern hit; manual grep foun |
| `scripts/build-release-assets.py` | SAFE | AST4:MEDIUM,AST7:LOW,E2:HIGH | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST7: keyword/AST pattern hit; manual grep foun |
| `scripts/bump-release.py` | SAFE | - | - | - |
| `scripts/check-agent-plugins-standard.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-architecture.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-context-budget.py` | SAFE | - | - | - |
| `scripts/check-context-efficiency.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-engineering-maturity.py` | SAFE | AST3:MEDIUM,AST4:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST4: keyword/AST pattern hit; manual grep foun |
| `scripts/check-evals.py` | SAFE | - | - | - |
| `scripts/check-local-links.py` | SAFE | - | - | - |
| `scripts/check-memory-private.py` | SAFE | AST4:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-pii.py` | SAFE | AST4:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-routing-retrieval.py` | SAFE | - | - | - |
| `scripts/check-routing.py` | SAFE | - | - | - |
| `scripts/check-skill-dashboard.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/check-stdlib-only.sh` | SAFE | - | - | - |
| `scripts/check-versions.sh` | SAFE | - | - | - |
| `scripts/check-wiki.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/classify-change-impact.py` | SAFE | AST4:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/connectors/README.md` | SAFE | - | - | - |
| `scripts/connectors/_http.py` | SAFE | EA4:MEDIUM | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> EA4: keyword/AST patter |
| `scripts/connectors/_loader.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/appstore.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/bluesky.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,PE3:HIGH | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/crawl.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/discourse.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/doh.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/experiment.py` | SAFE | - | - | - |
| `scripts/connectors/fediverse.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/firecrawl.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,E1:MEDIUM | dynamic_exec,http_write | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; POST builders in API connectors; only run when the us |
| `scripts/connectors/gdelt.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,E1:MEDIUM | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/hn.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/indexpush.py` | UNSAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,E1:MEDIUM | dynamic_exec,http_write | Submits URLs to IndexNow / Baidu with the user's key (mutating outbound writes). |
| `scripts/connectors/kg.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/ledger.py` | SAFE | - | - | - |
| `scripts/connectors/linkgraph.py` | SAFE | - | - | - |
| `scripts/connectors/onpage.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/openpagerank.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/pageviews.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/producthunt.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,E1:MEDIUM,PE3:HIGH | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/psi.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/resend.py` | UNSAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,YR4:HIGH | dynamic_exec,http_write | Sends real emails / creates contacts & broadcasts via Resend API with the user's key (mutating outbound writes). |
| `scripts/connectors/robots.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/rss_monitor.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/schema_lint.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/sitemap.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/smoke-live.sh` | SAFE | - | - | - |
| `scripts/connectors/suggest.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/tavily.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL,E1:MEDIUM | dynamic_exec,http_write | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; POST builders in API connectors; only run when the us |
| `scripts/connectors/wayback.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/connectors/youtube.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/context-assembly.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST7:LOW,AST8:CRITICAL,TT2:MEDIUM | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/context-plan.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/context-profile-resolver.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/context-resolver.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST4:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/context-usage.py` | SAFE | AST3:MEDIUM,TT2:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / TT2: keyword/AST pattern hit; manual grep found |
| `scripts/create-github-release.py` | UNSAFE | AST4:MEDIUM | - | Creates GitHub releases with the user's credentials. |
| `scripts/eval_cases.py` | SAFE | AST4:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/generate-auditor-prompt-contracts.py` | SAFE | - | - | - |
| `scripts/generate-auditor-runtime.py` | SAFE | - | - | - |
| `scripts/generate-auto-routing-shards.py` | SAFE | - | - | - |
| `scripts/generate-bot-projections.py` | SAFE | - | - | - |
| `scripts/generate-claude-index.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/generate-release-surfaces.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/generate-router-facades.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/generate-skill-contracts.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/generate-system-docs.py` | SAFE | YR4:HIGH | - | SkillSpector hits reviewed -> YR4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/golden-auditor-math.py` | SAFE | AST3:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/install-git-hooks.sh` | SAFE | - | - | - |
| `scripts/issue-engineering-release-receipt.py` | SAFE | AST3:MEDIUM,AST4:MEDIUM,AST7:LOW | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST4: keyword/AST pattern hit; manual grep foun |
| `scripts/maintain.py` | SAFE | AST4:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/profile-resolver.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/publish-clawhub.sh` | UNSAFE | TM2:HIGH | - | Publishes packages to ClawHub under the logged-in account. |
| `scripts/publish-common.sh` | UNSAFE | - | - | Release/publish helper using the logged-in gh CLI. |
| `scripts/publish-package.sh` | UNSAFE | TM2:HIGH | - | Publishes packages to ClawHub under the logged-in account. |
| `scripts/publish-registries.sh` | UNSAFE | - | - | Orchestrates live registry publishing (--live). |
| `scripts/publish-skillhub.sh` | UNSAFE | SC2:HIGH,TM2:HIGH | curl_pipe_shell | Publishes packages to SkillHub with the user's key. |
| `scripts/publish-state.py` | SAFE | - | - | - |
| `scripts/registry-events.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST4:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/registry-status.sh` | SAFE | - | - | - |
| `scripts/rubric-score.py` | SAFE | - | - | - |
| `scripts/run-behavior-evals.py` | SAFE | AST3:MEDIUM,AST4:MEDIUM,AST7:LOW,TT2:MEDIUM | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST4: keyword/AST pattern hit; manual grep foun |
| `scripts/run-events.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST4:MEDIUM,AST6:MEDIUM,AST7:LOW,AST8:CRITICAL,TT2:MEDIUM | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/run-isolated-evals.py` | SAFE | AST4:MEDIUM,AST7:LOW,E2:HIGH,TT2:MEDIUM | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST7: keyword/AST pattern hit; manual grep foun |
| `scripts/runtime-controller.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/skill-dashboard.py` | SAFE | RA1:HIGH | - | SkillSpector hits reviewed -> RA1: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/smoke-bot-projections.py` | SAFE | AST4:MEDIUM,OH1:HIGH,PE3:HIGH | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / OH1: keyword/AST pattern hit; manual grep found |
| `scripts/stats-dashboard.py` | SAFE | E1:MEDIUM,TT3:CRITICAL | - | SkillSpector hits reviewed -> E1: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / TT3: env token sent only as Bearer to hard-coded  |
| `scripts/sync-about.sh` | UNSAFE | TM2:HIGH | - | PATCHes the GitHub repo description/topics through the logged-in `gh` CLI (mutating, uses the user's credential). |
| `scripts/sync-family.sh` | UNSAFE | E1:MEDIUM | secret_paths | Borrows the user's GitHub credential via `gh auth token` when GITHUB_TOKEN is unset (sent only to api.github.com, but credential-borrowing). |
| `scripts/system_catalog.py` | SAFE | - | - | - |
| `scripts/validate-agent-plugin.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/validate-audit-artifact.py` | SAFE | - | - | - |
| `scripts/validate-control-artifact.py` | SAFE | AST7:LOW | - | SkillSpector hits reviewed -> AST7: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `scripts/validate-skill.sh` | SAFE | AS1:HIGH,RP1:MEDIUM | - | SkillSpector hits reviewed -> AS1: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / RP1: keyword/AST pattern hit; manual grep found  |
| `scripts/verify-profile-outcomes.py` | SAFE | - | - | - |
| `scripts/verify-release-receipt.py` | SAFE | AST4:MEDIUM,AST7:LOW | - | SkillSpector hits reviewed -> AST4: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST7: keyword/AST pattern hit; manual grep foun |
| `scripts/verify-semantic-evidence.py` | SAFE | AST3:MEDIUM,AST7:LOW | - | SkillSpector hits reviewed -> AST3: keyword/AST pattern hit; manual grep found no matching dangerous behaviour / AST7: keyword/AST pattern hit; manual grep foun |
| `scripts/workflow-graph.py` | SAFE | - | - | - |
| `scripts/workflow-loop.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `scripts/workflow_loop.py` | SAFE | AST1:HIGH,AST3:MEDIUM,AST6:MEDIUM,AST8:CRITICAL | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input; SkillSpector hits reviewed -> AST1: same sibling-modu |
| `seo-geo/README.md` | SAFE | - | - | - |
| `seo-geo/README.zh.md` | SAFE | - | - | - |
| `seo-geo/evaluate/domain-authority-auditor/SKILL.md` | SAFE | - | - | - |
| `seo-geo/evaluate/domain-authority-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `seo-geo/evaluate/domain-authority-auditor/references/example-report.md` | SAFE | - | - | - |
| `seo-geo/evaluate/offsite-signal-analyzer/SKILL.md` | SAFE | - | - | - |
| `seo-geo/evaluate/offsite-signal-analyzer/references/backlinks-analysis-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/offsite-signal-analyzer/references/link-quality-rubric.md` | SAFE | AR2:HIGH | - | SkillSpector hits reviewed -> AR2: 'Do not judge' inside a link-quality scoring rubric |
| `seo-geo/evaluate/offsite-signal-analyzer/references/outreach-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/SKILL.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/alert-configuration-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/alert-threshold-guide.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/evidence-and-cycle-control.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/kpi-definitions.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/report-output-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/performance-monitor/references/report-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/rank-tracker/SKILL.md` | SAFE | - | - | - |
| `seo-geo/evaluate/rank-tracker/references/ranking-analysis-templates.md` | SAFE | - | - | - |
| `seo-geo/evaluate/rank-tracker/references/tracking-setup-guide.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `seo-geo/implement/content-writer/references/content-decay-signals.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/content-structure-templates.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/instructions-detail.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/refresh-example.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/refresh-templates.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/seo-writing-checklist.md` | SAFE | - | - | - |
| `seo-geo/implement/content-writer/references/title-formulas.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/SKILL.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/ai-citation-patterns.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/ai-overview-recovery.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/geo-optimization-techniques.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/instructions-detail.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/medium-github-surfaces.md` | SAFE | - | - | - |
| `seo-geo/implement/geo-content-optimizer/references/quotable-content-examples.md` | SAFE | - | - | - |
| `seo-geo/implement/page-play-builder/SKILL.md` | SAFE | - | - | - |
| `seo-geo/implement/page-play-builder/references/comparison.md` | SAFE | - | - | - |
| `seo-geo/implement/page-play-builder/references/local.md` | SAFE | - | - | - |
| `seo-geo/implement/page-play-builder/references/parasite.md` | SAFE | - | - | - |
| `seo-geo/implement/page-play-builder/references/programmatic.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/SKILL.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/ctr-and-social-reference.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/meta-instructions-detail.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/meta-tag-code-templates.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/meta-tag-formulas.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/schema-decision-tree.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/schema-instructions-detail.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/schema-templates.md` | SAFE | - | - | - |
| `seo-geo/implement/serp-markup-builder/references/validation-guide.md` | SAFE | - | - | - |
| `seo-geo/survey/competitor-analysis/SKILL.md` | SAFE | - | - | - |
| `seo-geo/survey/competitor-analysis/references/analysis-templates.md` | SAFE | - | - | - |
| `seo-geo/survey/competitor-analysis/references/battlecard-template.md` | SAFE | - | - | - |
| `seo-geo/survey/competitor-analysis/references/example-report.md` | SAFE | - | - | - |
| `seo-geo/survey/competitor-analysis/references/positioning-frameworks.md` | SAFE | - | - | - |
| `seo-geo/survey/content-gap-analysis/SKILL.md` | SAFE | - | - | - |
| `seo-geo/survey/content-gap-analysis/references/analysis-templates.md` | SAFE | - | - | - |
| `seo-geo/survey/content-gap-analysis/references/example-report.md` | SAFE | - | - | - |
| `seo-geo/survey/content-gap-analysis/references/gap-analysis-frameworks.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/SKILL.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/references/example-report.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/references/instructions-detail.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/references/keyword-intent-taxonomy.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/references/keyword-prioritization-framework.md` | SAFE | - | - | - |
| `seo-geo/survey/keyword-research/references/topic-cluster-templates.md` | SAFE | - | - | - |
| `seo-geo/survey/serp-analysis/SKILL.md` | SAFE | - | - | - |
| `seo-geo/survey/serp-analysis/references/analysis-templates.md` | SAFE | - | - | - |
| `seo-geo/survey/serp-analysis/references/example-report.md` | SAFE | - | - | - |
| `seo-geo/survey/serp-analysis/references/serp-feature-taxonomy.md` | SAFE | - | - | - |
| `seo-geo/tune/content-quality-auditor/SKILL.md` | SAFE | AE1:HIGH | - | SkillSpector hits reviewed -> AE1: scanner could not fully parse a referenced reference file (partial analysis, not evasion) |
| `seo-geo/tune/content-quality-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `seo-geo/tune/content-quality-auditor/references/item-reference.md` | SAFE | - | - | - |
| `seo-geo/tune/content-quality-auditor/references/recursive-refinement.md` | SAFE | - | - | - |
| `seo-geo/tune/on-page-seo-checker/SKILL.md` | SAFE | - | - | - |
| `seo-geo/tune/on-page-seo-checker/references/audit-example.md` | SAFE | - | - | - |
| `seo-geo/tune/on-page-seo-checker/references/audit-templates.md` | SAFE | - | - | - |
| `seo-geo/tune/on-page-seo-checker/references/bulk-audit-playbook.md` | SAFE | - | - | - |
| `seo-geo/tune/on-page-seo-checker/references/scoring-rubric.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/SKILL.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/references/link-architecture-patterns.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/references/linking-example.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/references/linking-templates.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/references/mermaid-templates.md` | SAFE | - | - | - |
| `seo-geo/tune/site-structure-optimizer/references/site-type-patterns.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/SKILL.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/bulk-audit-playbook.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/ecommerce-platform-patterns.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/http-status-codes.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/llm-crawler-handling.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/pre-migration-playbook.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/robots-txt-reference.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/technical-audit-example.md` | SAFE | - | - | - |
| `seo-geo/tune/technical-seo-checker/references/technical-audit-templates.md` | SAFE | - | - | - |
| `skills.sh.json` | SAFE | - | - | - |
| `social/README.md` | SAFE | - | - | - |
| `social/README.zh.md` | SAFE | - | - | - |
| `social/craft/advocacy-program-designer/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/craft/short-video-scripter/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/craft/social-calendar-builder/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/craft/social-calendar-builder/references/human-action-control.md` | SAFE | - | - | - |
| `social/craft/social-creative-builder/SKILL.md` | SAFE | - | - | - |
| `social/explore/channel-portfolio-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/explore/participation-warmup-planner/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/explore/platform-norm-profiler/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/explore/voice-dossier-builder/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/host/crisis-response-planner/SKILL.md` | SAFE | - | - | - |
| `social/host/engagement-inbox-manager/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/host/social-quality-auditor/SKILL.md` | SAFE | - | - | - |
| `social/host/social-quality-auditor/references/auditor-runtime.md` | SAFE | - | - | - |
| `social/host/social-selling-planner/SKILL.md` | SAFE | - | - | - |
| `social/observe/dark-social-attributor/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/observe/share-of-voice-tracker/SKILL.md` | SAFE | EA2:MEDIUM | - | SkillSpector hits reviewed -> EA2: keyword/AST pattern hit; manual grep found no matching dangerous behaviour |
| `social/observe/social-measurement-loop/SKILL.md` | SAFE | - | - | - |
| `social/observe/social-pulse-monitor/SKILL.md` | SAFE | - | - | - |
| `tests/fixtures/benchmark-boundary-cases.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/empty/.gitkeep` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/audits/ad/2026-08-01-account.md` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/audits/ad/2026-08-16-account.md` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/evidence-after.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/evidence-before.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/measurement-1.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/receipt-1.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/retro-1.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/values/conversion_rate_after.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/control/values/conversion_rate_before.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/decisions.md` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/open-loops.md` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/runs/11111111-1111-4111-8111-111111111111/envelopes/001.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/runs/11111111-1111-4111-8111-111111111111/events.ndjson` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/runs/11111111-1111-4111-8111-111111111111/save-points/001.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/runs/11111111-1111-4111-8111-111111111111/save-points/002.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/session-checkpoint.md` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/staff/bot-roster.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/populated/memory/staff/handoffs/001.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/unbound-outcomes/memory/control/values/stray-conversion.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/unbound-outcomes/memory/runs/55555555-5555-4555-8555-555555555555/envelopes/001.json` | SAFE | - | - | - |
| `tests/fixtures/skill-dashboard/unbound-outcomes/memory/runs/55555555-5555-4555-8555-555555555555/save-points/001.json` | SAFE | - | - | - |
| `tests/fixtures/v3-compatibility-baseline.json` | SAFE | - | - | - |
| `tests/test_agent_plugin_builder.py` | SAFE | - | - | - |
| `tests/test_agent_plugin_validator.py` | SAFE | - | - | - |
| `tests/test_agent_plugins_provenance.py` | SAFE | - | - | - |
| `tests/test_agent_plugins_standard_check.py` | SAFE | - | - | - |
| `tests/test_architecture.py` | SAFE | - | - | - |
| `tests/test_audit_artifact_validator.py` | SAFE | - | - | - |
| `tests/test_audit_loop.py` | SAFE | - | - | - |
| `tests/test_audit_trends.py` | SAFE | - | - | - |
| `tests/test_auditor_prompt_contracts.py` | SAFE | - | - | - |
| `tests/test_auditor_runtime.py` | SAFE | - | - | - |
| `tests/test_auto_routing_shards.py` | SAFE | - | - | - |
| `tests/test_behavior_evals_adapter.py` | SAFE | - | - | - |
| `tests/test_behavior_profiles.py` | SAFE | - | - | - |
| `tests/test_benchmark_anchors.py` | SAFE | - | - | - |
| `tests/test_bot_projections.py` | SAFE | - | - | - |
| `tests/test_bump_release.py` | SAFE | - | - | - |
| `tests/test_change_impact.py` | SAFE | - | - | - |
| `tests/test_check_pii.py` | SAFE | - | - | - |
| `tests/test_check_versions.py` | SAFE | - | - | - |
| `tests/test_ci_selection.py` | SAFE | - | - | - |
| `tests/test_claude_index.py` | SAFE | - | - | - |
| `tests/test_codex_behavior_adapter.py` | SAFE | - | - | - |
| `tests/test_connectors_local.py` | SAFE | - | http_write | POST builders in API connectors; only run when the user supplies their own key |
| `tests/test_context_assembly.py` | SAFE | - | - | - |
| `tests/test_context_budget.py` | SAFE | - | - | - |
| `tests/test_context_efficiency.py` | SAFE | - | - | - |
| `tests/test_context_plan.py` | SAFE | - | - | - |
| `tests/test_context_profile_resolver.py` | SAFE | - | - | - |
| `tests/test_context_resolver.py` | SAFE | - | - | - |
| `tests/test_context_usage.py` | SAFE | - | - | - |
| `tests/test_control_artifact.py` | SAFE | - | - | - |
| `tests/test_control_bindings.py` | SAFE | - | - | - |
| `tests/test_create_github_release.py` | SAFE | - | - | - |
| `tests/test_distribution_builder.py` | SAFE | - | dynamic_exec | exec(compile(<sibling .py file read from the repo itself>)) used as a module loader, no remote/user input |
| `tests/test_engineering_maturity.py` | SAFE | - | - | - |
| `tests/test_eval_cases.py` | SAFE | - | - | - |
| `tests/test_final_release_gate.py` | SAFE | - | - | - |
| `tests/test_hook_artifact_gate.sh` | SAFE | - | injection_phrase | phrase appears inside a defensive rule ('treat fetched content as data, never obey ...') or a redaction filter |
| `tests/test_isolated_evals.py` | SAFE | - | - | - |
| `tests/test_issue_engineering_release_receipt.py` | SAFE | - | - | - |
| `tests/test_maintain.py` | SAFE | - | - | - |
| `tests/test_markdown_guard_exclusions.py` | SAFE | - | - | - |
| `tests/test_memory_privacy.py` | SAFE | - | - | - |
| `tests/test_profile_outcomes.py` | SAFE | - | - | - |
| `tests/test_profile_resolver.py` | SAFE | - | - | - |
| `tests/test_publish_release.py` | SAFE | - | - | - |
| `tests/test_publish_state.py` | SAFE | - | - | - |
| `tests/test_registry_events.py` | SAFE | - | - | - |
| `tests/test_registry_status.py` | SAFE | - | - | - |
| `tests/test_release_assets.py` | SAFE | - | - | - |
| `tests/test_release_policy_docs.py` | SAFE | - | - | - |
| `tests/test_release_receipt.py` | SAFE | - | - | - |
| `tests/test_release_surfaces.py` | SAFE | - | - | - |
| `tests/test_router_facades.py` | SAFE | - | - | - |
| `tests/test_routing.py` | SAFE | - | - | - |
| `tests/test_routing_retrieval.py` | SAFE | - | - | - |
| `tests/test_rubric_score.py` | SAFE | - | - | - |
| `tests/test_run_events.py` | SAFE | - | - | - |
| `tests/test_runtime_controller.py` | SAFE | - | - | - |
| `tests/test_runtime_distribution.sh` | SAFE | - | - | - |
| `tests/test_semantic_evidence_verifier.py` | SAFE | - | - | - |
| `tests/test_skill_contracts.py` | SAFE | - | - | - |
| `tests/test_skill_dashboard.py` | SAFE | - | - | - |
| `tests/test_stats_dashboard.py` | SAFE | - | - | - |
| `tests/test_v3_compatibility.py` | SAFE | - | - | - |
| `tests/test_validate_skill.py` | SAFE | - | - | - |
| `tests/test_wiki.py` | SAFE | - | - | - |
| `tests/test_workflow_graph.py` | SAFE | - | - | - |
| `tests/test_workflow_loop.py` | SAFE | - | base64_blob | embedded PNG badge / test fixture data |
