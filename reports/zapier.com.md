# zapier.com: acquisition channels (2026-11-15)

**How to read this.** **Measured** means our own crawl in GitHub Actions run [43694969331](https://github.com/bigA2/market-research-lab/actions/runs/43694969331) (data in [`data/zapier.com/`](../data/zapier.com/)). **Third-party** means web search results; these are marked *unverified*. Any number without a source is *unverified*. Sitemap counts show what Zapier *submits* to search engines, not what Google indexes or what gets traffic. We have no traffic data, so every traffic claim is *unverified*.

## TL;DR

Zapier is a programmatic SEO machine. Of **424,127 URLs in its sitemaps, about 97% (411,409) are generated from two datasets: the app catalogue and the workflow/template catalogue.** The integration-pair pages (`/apps/A/integrations/B`, 148,333 URLs) and per-workflow pages (`/automations/…`, 130,627 URLs; zap templates, 101,026 URLs) are rich: around 2–3k words, real JSON-LD (`SoftwareApplication`, `HowTo`, `Action`/`Trigger`) and 300+ internal links each. Everything else (blog, Academy, partner directory, AWS Marketplace, Product Hunt launches, free plan) feeds that engine or monetizes it. Gaps: about 10k thin A–Z directory pages, sitemaps that list noindex and non-canonical URLs, stale 404s in sitemaps, and no localized URLs in sitemaps.

## 1. SEO page families: the core engine (Measured)

Source: [`data/zapier.com/families.csv`](../data/zapier.com/families.csv), [`summary.json`](../data/zapier.com/summary.json), [`samples.json`](../data/zapier.com/samples.json). Robots.txt lists 10 sitemaps, and 332 sitemap files were fetched with 0 failures.

| # | Family (template) | URLs | What it is | Sampled page quality (3 per family) |
|---|---|---|---|---|
| 1 | `/apps/{app}/integrations/{app}` | **148,333** | app × app pair page, e.g. https://zapier.com/apps/schedule/integrations/10000ft | median 2,917 words, 341 internal links, unique titles, self-canonical, JSON-LD `SoftwareApplication`+`HowTo`+`Action`+`BreadcrumbList`+`VideoObject`, custom `zapier:Trigger/Action` types |
| 2 | `/automations/{dept}/{area}/{topic}/{workflow}` | **130,627** | AI-era workflow-idea pages in a 4-level taxonomy, e.g. https://zapier.com/automations/finance/payment-operations/payment-processing-management/register-customer-and-payment-into-finance-system-reliably | ~2,284 words, `HowTo`+`CollectionPage`+`ItemList`, `index, follow` |
| 3 | `/apps/{app}/integrations/{app}/{id}/{slug}` | **101,026** | individual zap templates, e.g. https://zapier.com/apps/formsite/integrations/highrise/2546/formsite-form-submission-to-highrise-contact | ~1,758 words, **no JSON-LD, 2 H1s** on all 3 samples |
| 4 | `/apps/{app}/integrations` | 10,119 | app hub page (one per app), e.g. https://zapier.com/apps/0codekit/integrations | ~2,054 words, `OfferCatalog` |
| 5 | `/mcp/{app}` | 10,119 | **new family**: one "{App} MCP Server" page per app, e.g. https://zapier.com/mcp/manychat | ~1,567 words; same dataset reused for AI/MCP search terms |
| 6 | `/find-apps/{letter}/{app}` | 10,119 | A–Z app directory, e.g. https://zapier.com/find-apps/a/andopen-gifts/ | **thin**: 61–161 words, **no H1, no canonical** |
| 7 | `/automation/{industry}/{use-case}` | 6,080 | industry use-case pages, e.g. https://zapier.com/automation/education-automation/student-enrollment | ~1,243 words |
| 8 | `/blog/{slug}` | 3,871 | editorial blog | ~1,857 words, `Article` |
| 9 | `/blog/updates/{n}/{slug}` | 2,370 | old product-update posts | ~934 words |
| 10 | `/automations/{dept}/{area}/{topic}` (+2 upper levels) | 742 | taxonomy hub pages | ~2,000 words |
| 11 | `/learn/{course}/{chapter}` | 179 | legacy guides (e.g. "101 ways to use Zapier") | canonical points to `/blog/…` |
| 12 | `/agents/templates/{slug}` | 100 | agent templates | **`noindex`** yet listed in the sitemap |
| 13 | `/apps/categories/{cat}` | 98 | "Top {Category} Apps" lists | ~2,043 words |
| 14 | `/apps/ai-tools/{tool}` (`/apps/{x}/{x}`) | 31 | "Connect {AI tool} to 9,000+ apps" for Claude/Kiro/Zed/Amazon Quick… | `FAQPage` schema |
| 15 | `/l/{campaign}` | 24 | campaign/lead-gen landing pages (`/l/contact-sales`, `/l/demo`, `/l/linkedin-lead-gen-forms`) | paid/ABM landing pages |

Sections ([`sections.csv`](../data/zapier.com/sections.csv)): integrations 279,880 · templates 131,529 · blog 6,252 · use-cases 6,166 · academy/learn 211 · landing 44 · legal 34.

**What drives the views (inference; traffic is *unverified*):** every new app partner adds ~10–30 pages at once (hub, MCP, A–Z, one pair page per popular partner app, and zap templates). Pages 1 and 3 target the long tail "connect X to Y" / "X Y integration" with real per-row data (triggers, actions, step lists). That is Tier-1/2 product data in the vetted page-play methodology (see [`VETTING.md`](../VETTING.md)), which is why these pages are not thin. The new `/automations/*` (130k) and `/mcp/*` (10k) families show Zapier re-pointing the same catalogue at "AI workflow" and "MCP server" searches.

## 2. Integrations and app directory

- Developer platform invites app vendors to build their own integration, which is a supply loop for family 1: https://zapier.com/developer-platform ("Power your product or AI agent with 9,000 app integrations"). Measured, from [`channels.json`](../data/zapier.com/channels.json).
- 10,119 apps listed in sitemaps (count of `/apps/{x}/integrations` hubs). Measured. Zapier markets "9,000+ apps" in its meta descriptions (Measured, `samples.json`).

## 3. Templates

- `/templates` (H1 "Workflow Automation Templates"), `/templates/{product}` (10 URLs; `/templates/tables` has 6 hreflang alternates), and `/interfaces/forms/templates` (46 URLs that are filtered views of one page: same title "Form Templates | Zapier" on 3/3 samples, all canonicalizing to `/templates/forms`; the H1 reads "Form Templates templates"). Measured.
- Zap templates (family 3, 101k) and `/automations` (family 2, 131k) together are the real template engine.

## 4. Blog / docs / academy

- Blog: 6,252 URLs (Measured). Localized blog copies exist (e.g. https://zapier.com/de/blog/pay-per-click-tools, https://zapier.com/pt-br/blog/zapier-aws-marketplace, found by web search), but **0 localized URLs are in the sitemaps** (Measured: `localized_urls: 0`), and sampled English pages carry 0 hreflang tags.
- Academy: https://zapier.com/university → "Zapier Academy" (Measured). Free courses with certificate (third-party, *unverified*: https://verify.skilljar.com/c/srmoptbwzkmw).
- Guides: `/learn` (Measured, H1 "Zapier guides"); the legacy `/learn/*` pages canonicalize into `/blog/*`.

## 5. Community / forums

- https://community.zapier.com (Discourse-style; found by web search, not crawled; we crawl the main domain only). For example, the staff post on the affiliate question: https://community.zapier.com/show-tell-5/does-zapier-have-an-affiliate-program-13950. The `/community` path on zapier.com returns 404 (Measured).

## 6. YouTube / social

- Footer links (Measured, [`home.json`](../data/zapier.com/home.json)): YouTube https://www.youtube.com/user/ZapierApp, LinkedIn, X, Facebook, GitHub; all footer links carry `utm_source=zapier.com`. Subscriber counts were not found (*unverified*).

## 7. Affiliate / partner / expert programs

- **No public affiliate program**: `/affiliates`, `/affiliate`, `/referral` and `/refer` return 404 (Measured). A Zapier staff reply says there is "no affiliate program" (third-party, *unverified*: link in section 5).
- **Solution Partner directory** (formerly Experts): https://zapier.com/experts → "Solution Partner Directory" (Measured). The directory runs on PartnerPage and reportedly "matches more than 500 customers monthly" (*unverified*: https://www.partnerpage.io/customers/how-zapier-built-a-self-service-expert-marketplace-that-matches-more-than-500-customers-monthly).
- Programs for startups (https://zapier.com/startups) and education (https://zapier.com/education → the homepage is returned, so the program page appears to be gone; Measured title = home title).

## 8. Marketplaces

- **AWS Marketplace** listing since September 2025 (third-party, *unverified*: https://aws.amazon.com/marketplace/pp/prodview-tpfuhwmz6lzss, https://zapier.com/blog/zapier-aws-marketplace/). Enterprise buyers can spend their committed AWS budgets on it.
- Inbound "marketplace" of AI tools: the `/apps/ai-tools/*` pages and `/mcp/*` make Zapier the integration layer inside Claude, ChatGPT and Cursor (Measured page family; the client list comes from earlier capture in `fansachat-scripts/research/zapier/`).

## 9. Product-led loops

- Free forever plan (100 tasks, 2-step Zaps); 14-day Pro trial (verified earlier from founder capture, see `fansachat-scripts/research/zapier/COMPARISON_2026-11-15.md`).
- Sign-up page: https://zapier.com/sign-up (Measured, screenshot `raw-zapier.com` artifact).
- Template → "Try it" links on every pair page drive straight into the editor (inferred from the page structure; click-through not measured).
- Shared items: forms, chatbots and interfaces are public pages that end users of Zapier customers see (product inference, *unverified*).

## 10. Paid ads signals

- 24 `/l/*` campaign landing pages incl. `/l/linkedin-lead-gen-forms`, `/l/demo`, `/l/contact-sales` (Measured). This suggests paid/ABM campaigns.
- Google Ads Transparency and the Meta Ad Library were **not reachable** from this session (`adstransparency.google.com` is blocked by the network policy). No spend data. *Unverified.*

## 11. Launches / events / enterprise sales

- Product Hunt: "Zapier Agents" #2 Product of the Day, Feb 24 2025, 663 upvotes (*unverified*: https://hunted.space/product/zapier/launches/zapier-agents).
- Enterprise motion: https://zapier.com/enterprise ("Your automation partner for the agentic era"), `/l/contact-sales`, and SSO/admin features on the Team/Enterprise plans (Measured pages).
- `/events`, `/webinars` → 404 (Measured). No public events hub on the main domain.

## 12. What Zapier is missing or does badly (Measured unless marked)

| Issue | Evidence | Why it matters |
|---|---|---|
| **10,119 thin A–Z pages** | `/find-apps/{l}/{app}`: 61–161 words, no H1, no canonical (3/3 samples) | thin near-duplicates of the `/apps/{x}/integrations` hubs; this wastes crawl budget |
| **Sitemap lists noindex pages** | `/agents/templates/*` (100 URLs) are `noindex, follow` and canonicalize to `/templates/details/*` | sitemap/noindex conflict that Google Search Console flags |
| **Sitemap lists non-canonical URLs** | `/learn/*` → canonical `/blog/*`; `/roles/*` → `/solutions/*`; `/roles/software-engineers` → homepage | dilutes the sitemap signal |
| **Stale 404s in sitemap** | 2 of 75 sampled URLs return 404: `/learn/apis/chapter-1-introduction-to-apis/`, `/agents/templates/google-doc-to-asana-status-update-7deead` | about 3% stale in the sample; extrapolating would be *unverified* |
| **Zap template pages: no schema, 2 H1s** | family 3 (101k URLs): `schema_types: []`, 2 H1s on 3/3 samples | the biggest family after pairs has the weakest markup |
| **Localization hidden** | localized blog copies exist but 0 localized URLs in sitemaps; 0 hreflang on sampled English pages | weak international discovery (*partly unverified*) |
| **No affiliate program** | `/affiliate*` 404 | this leaves the creator/affiliate channel to Make (35% commission) |
| **Dead program page** | `/education` returns the homepage | broken program funnel |
| Blog index pages without H1 | `/blog/all-articles/` | minor |
| A `/compare` hub exists, but there is no comparison page family | https://zapier.com/compare returns 200, yet the sitemaps hold no `/compare/*` URLs; `/vs` and `/alternatives` return 404 | competitors can own the "Zapier alternative" searches |

Screenshots (home, pricing, sign-up, top 5 families; viewport + full page) are in the run artifact `raw-zapier.com`.
