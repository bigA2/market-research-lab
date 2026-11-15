# FansaChat playbook: what to copy for free, now (2026-11-15)

Inputs: [`zapier.com.md`](zapier.com.md), [`replit.com.md`](replit.com.md), [`make.com.md`](make.com.md) (crawl run [43694969331](https://github.com/bigA2/market-research-lab/actions/runs/43694969331)), plus the earlier `fansachat-scripts/research/zapier/COMPARISON_2026-11-15.md`.

**FansaChat facts** come from the founder brief: 64 generated SEO pages from `scripts/seo` in the landing repo, 700+ integrations, 478 templates, pricing from $15/mo. Other facts come from the earlier comparison (runs-based billing, approve-before-run, chat editing, waitlist mode). **I could not open the landing repo from this session** (it is outside this session's repo access), so file names below are taken from that comparison and should be checked.

Method: the vetted page-play methodology ([`VETTING.md`](../VETTING.md), `page-play-builder/references/programmatic.md`, SAFE, read only). Every generated page needs a per-row **evidence block** from data only we have, an N-gram dedup check, selective indexation and batch launches. Comparison pages must be honest and every competitor claim must be sourced.

## The one-paragraph strategy

Zapier gets ~97% of its 424k sitemap URLs from **two datasets: apps and workflows** (Measured). Make does the same at 13.6k URLs. Replit skips SEO and grows from **product loops** (badge + referral + gallery). FansaChat already owns both datasets in miniature: 700+ apps and 478 templates. Going from 64 pages to **about 1,300–2,000 high-quality pages** (*estimate*) is the biggest free lever. Then add the one family **none of the three competitors has: comparison/alternative pages** (Measured: `/compare/*`, `/vs/*` and `/alternatives/*` are absent or 404 on all three). Then copy Replit's free loops.

## Ranked list (impact ÷ effort)

Effort: S = under a day, M = 1–3 days, L = a week or more. Impact is an estimate (*unverified*: we have no traffic data for anyone).

| Rank | Play | Copied from (evidence) | Impact | Effort | Cost |
|---|---|---|---|---|---|
| 1 | **Template pages** `/templates/{slug}` for all 478 templates | Make 7,830 template pages; Zapier zap templates 101,026 + `/automations` 130,627 | High | **S** (data exists) | free |
| 2 | **App pages** `/integrations/{app}` for 700+ apps | Zapier `/apps/{x}/integrations` 10,119; Make `/integrations/{x}` 3,452 | High | M | free |
| 3 | **Comparison + alternative pages** `/compare/fansachat-vs-{zapier,make,n8n,activepieces,pipedream}` + `/alternatives/{zapier,make}` | gap at all three (Measured) | High (buyer intent) | S (`scripts/seo/compare.mjs` exists per the comparison) | free |
| 4 | **App-pair pages** `/integrations/{a}/{b}`, **only for pairs used in ≥1 of the 478 templates** | Zapier 148,333 pair pages (the core engine); Make 1,102 | High | M | free |
| 5 | **Structured data on every generated page** (`SoftwareApplication`, `HowTo` with steps, `BreadcrumbList`, `FAQPage`) | Zapier has it; Make has none (Measured) | Med-High | S | free |
| 6 | **Use-case taxonomy hubs** `/automations/{department}/{use-case}` grouping the 478 templates by audience/role | Zapier `/automations/{dept}/{area}/{topic}` (742 hubs) + `/roles/*` | Med | S | free |
| 7 | **"Built with FansaChat" share loop**: public read-only `/w/{id}` page for a workflow a user chooses to share ("clone this workflow"), with the creator's referral link | Replit "Made with Replit" badge + referral link (*unverified* docs) | Med-High (compounding) | M | free |
| 8 | **Referral credits** (extra runs, not cash) | Replit `/refer` (Measured page), credits model (*unverified*) | Med | S–M | free (no cash out) |
| 9 | **Persona pages** `/for/{role}` from the Team role bundles | Zapier `/roles/*` (9), Make `/solutions/*` (8), Replit `/discover/*` (84) | Med | S | free |
| 10 | **Product Hunt launch** at the end of waitlist mode, with a "chat-built, you approve every step" angle | Zapier Agents #2 (663 upvotes), Replit Agent #2 (588) (*unverified*) | Med (one-off spike) | S | free |
| 11 | **Free short courses + certificate page** (`/learn/*`) reusing the faceless video scripts in this repo | Zapier Academy, Make Academy (free, badges) | Med | M | free |
| 12 | **App-marketplace listings** (Slack App Directory, Google Workspace Marketplace, HubSpot) | Zapier/Make developer platforms; Replit Azure/GCP | Med | M–L (reviews) | free |
| 13 | Affiliate program (cash %) | Make 35% × 12 months (*unverified*) | Med | M | revenue share, **not free** → later |
| 14 | AWS/Azure/GCP marketplace | Zapier AWS (2025), Make AWS (2022), Replit Azure+GCP (*unverified*) | Low now | L | needs an enterprise motion → later |
| 15 | Paid ads | Zapier `/l/*` campaign pages (24) | n/a | | **not free** → skip |

## Concrete page families to generate next (in this order)

Run them through `scripts/seo` as batches (the methodology says batches, never one big dump). Suggested cadence is about 100–200 URLs per week, watching Search Console indexation per batch.

### F1. `/templates/{slug}` (478 pages, batch 1–3)
- **Evidence block (unique per row):** the step list (trigger → actions) rendered from the template JSON, the apps used, how many runs one execution costs (always 1 run: our billing unit), the "you approve before it runs" preview, and editable fields.
- **Title:** `{Template name}: free workflow template | FansaChat`. Unique by construction.
- **Schema:** `HowTo` (steps) + `SoftwareApplication` + `BreadcrumbList`.
- **Links:** to each app's F2 page and to the F4 pair page; 3 related templates.
- **Lesson from Make:** put the keyword in the slug (Make has `/templates/10036-new-template`).

### F2. `/integrations/{app}` (700+ pages)
- **Evidence block:** that app's real triggers and actions (from the integration piece metadata), the templates using it (from F1), auth type, and whether it needs platform review (the comparison notes that some pieces do: say so honestly).
- **Noindex rule:** apps with 0 templates and ≤2 actions get `noindex` and stay **out of the sitemap** until they have content. This avoids Zapier's 10k-page thin `/find-apps` mistake.
- **Do not** build an A–Z directory family. Use one `/integrations` hub with client-side filtering, server-rendered.

### F3. Comparison family (≈7–10 pages)
- `/compare/fansachat-vs-zapier`, `-vs-make`, `-vs-n8n`, `-vs-activepieces`, `-vs-pipedream`; `/alternatives/zapier`, `/alternatives/make`.
- **Evidence block:** the worked per-run example from the comparison (1 trigger + 3 actions). Zapier tasks = 3 per run vs 1 FansaChat run. Every competitor number links to that competitor's pricing page with an "as of {date}" stamp. Re-check the numbers live (this session could not fetch zapier.com/pricing directly). The comparison already marks some Zapier tiers *unverified*: keep that.
- **Honesty rule:** state where they win (Zapier: 9,000+ apps and a free plan; Make: visual builder and a free plan).
- Ship this **only after** the open "do empty polls count as runs?" question in the comparison is settled, because it changes the price story.

### F4. `/integrations/{a}/{b}` pair pages (only data-backed pairs)
- Generate a pair **only if ≥1 of the 478 templates uses both apps**. The count is *unknown until computed*; my *estimate* is a few hundred to ~1,500.
- **Evidence block:** the templates connecting A→B and their steps, the A triggers × B actions available, and "describe it in chat" example prompts.
- **N-gram guardrail:** fail the build if a sentence appears on more than 30% of pair pages (methodology). Keep 8–15 intro variants.

### F5. `/automations/{department}/{use-case}` hubs (≈30–60 pages, *estimate*)
- Group the 478 templates by the audience/role labels that already filter onboarding. Each hub gets an intro, its template list, and a FAQ.

### F6. `/for/{role}` (≈8–12 pages)
- Built from the Team role bundles: role pain points, the bundle's templates, and price per run for that bundle.

## Free product loops to build (copy Replit)

1. **Share-a-workflow page `/w/{id}`.** Opt-in only, read-only, with secrets stripped. "Clone this workflow" CTA plus the creator's referral code. It is `noindex` by default, and the creator can choose "list in gallery" to make it indexable (Tier-3 UGC; moderate it).
2. **Referral credits:** both sides get extra runs on their first paid month. No cash, so no affiliate tooling cost.
3. **"Sent by a FansaChat workflow" footer** (opt-out) on emails or messages a workflow sends. This only fits where it doesn't hurt the user's brand. Free plan only, if a free plan is ever added (Replit removes its badge for paid users).

## Technical guardrails (lessons from the competitors' mistakes, all Measured)

Add these as a CI check in `scripts/seo` before every batch:

- [ ] The sitemap contains **only** 200, self-canonical, indexable URLs. Zapier lists noindex `/agents/templates/*` and non-canonical `/learn/*` and `/roles/*`; Replit lists noindex `/@user/*`; Make lists `?categoryType=` URLs.
- [ ] No sitemap file returns 404 (Replit: 3 do).
- [ ] Every page has exactly one H1 (Zapier zap templates have 2; Replit guides up to 9), a unique title (Make category pages share one) and a page-specific meta description (Replit gallery and Make workflows use generic or empty ones).
- [ ] Core content is **server-rendered** (Replit `/integrations`, `/community`, `/partners`: 0 words in HTML).
- [ ] Legacy URLs 301 to their replacement, never "render the homepage and canonicalize to /" (Replit `/languages/*`).
- [ ] Schema on every generated page (Make: none on any sampled page of its template, app and pair families, 12.4k URLs).
- [ ] hreflang **only if** real translations exist (none of the three lists localized URLs in sitemaps; don't fake it).

## What NOT to copy

- Thin A–Z directories (Zapier `/find-apps`, 10,119 pages of ~60–160 words).
- Invented social proof ("Used by 500+ teams") until we have real usage data (repeated from the comparison, G9).
- `/mcp/{app}` pages (Zapier 10,119) **until MCP works end to end**. The comparison says it isn't connected yet, so these pages would over-promise.

## Expected outcome

From 64 pages to ~1,300–2,000 indexable, data-backed pages in ~6–10 weekly batches (*estimate, unverified*), plus one buyer-intent family nobody else has and two free loops. Track per batch: pages submitted vs indexed (Search Console), impressions and clicks per family, and sign-ups from `/w/{id}` shares and referral codes.
