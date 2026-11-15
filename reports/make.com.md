# make.com: acquisition channels (2026-11-15)

**How to read this.** **Measured** means our crawl in Actions run [43694969331](https://github.com/bigA2/market-research-lab/actions/runs/43694969331) (data in [`data/make.com/`](../data/make.com/)). Third-party facts are marked *unverified*. Traffic claims are *unverified*.

## TL;DR

Make runs the same playbook as Zapier at about 1/30 of the scale: **13,620 sitemap URLs**, almost all of them **7,830 template pages + 3,452 app pages + 1,102 app-pair pages**. On top of that it runs the strongest **creator/affiliate** channel of the three (35% commission, *unverified*), five partner programs, a free Academy, the Waves conference, and an AWS Marketplace listing. Gaps: app-pair coverage is tiny next to Zapier's 148k, template and integration pages carry **no structured data**, 218 category pages share **one title**, and sitemaps list parameterized non-canonical URLs. There are no comparison pages.

## 1. SEO page families (Measured)

robots.txt → 7 sitemaps, 0 failures ([`sitemaps.csv`](../data/make.com/sitemaps.csv)).

| # | Family | URLs | What it is | Sample quality |
|---|---|---|---|---|
| 1 | `/templates/{id}-{slug}` | **7,830** | workflow template pages, e.g. https://www.make.com/templates/4237-log-your-aircall-data-in-google-sheets | ~795 words, **no JSON-LD**, ~102 internal links; one sample has a generic slug (`/templates/10036-new-template`) behind a specific title ("Create Google Calendar events from Notion") |
| 2 | `/integrations/{app}` | **3,452** | app pages, e.g. https://www.make.com/integrations/2-solar-community | ~1,651 words, **no JSON-LD** |
| 3 | `/integrations/{app}/{app}` | **1,102** | app × app pair pages, e.g. https://www.make.com/integrations/activecampaign/google-ads-lead-forms | ~2,024 words, **no JSON-LD** |
| 4 | `/blog/{slug}` | 403 | blog (includes 2019 posts, e.g. https://www.make.com/blog/2019-the-year-of-the-employee-productivity) | `BlogPosting` |
| 5 | `/integrations/category/{cat}` | 218 | category hubs | **same title on 3/3 samples** ("3,500+ Integration Apps…"); sitemap URLs carry `?categoryType=subcategory` and canonicalize to the clean URL |
| 6 | `/how-to-guides/{slug}` | 212 | listicles and how-tos ("11 Best ClickUp Integrations for Digital Agencies") | `HowTo` schema |
| 7 | `/workflows/{slug}` | 121 | newer AI-workflow pages ("Verify GDPR data erasure across systems") | **empty meta description** on 3/3 |
| 8 | `/success-stories/{slug}` | 103 | case studies | `Article` |
| 9 | `/webinars/{slug}` | 64 | webinar pages | `Event` schema; empty meta on 2/3 |
| 10 | `/authors/{name}` | 27 | author pages | |
| 11 | `/solutions/{slug}` | 8 | solution pages | |

Sections: templates 7,952 · integrations 4,774 · blog 431 · academy/how-to 213 · customers 104 · events/webinars 66.

**What drives views (inference, *unverified*):** template pages ("log Aircall data in Google Sheets") and app pages target the same long tail as Zapier. Make lists **1,102 pair pages against Zapier's 148,333** and 3,452 apps against Zapier's 10,119, so it competes on depth (visual scenarios, price) rather than coverage.

## 2. Integrations and app directory

- https://www.make.com/integrations: "Explore over 3,500 apps" (Measured meta). This matches the 3,452 app URLs.
- Developer and partner programs: see section 7.

## 3. Templates

- https://www.make.com/templates: "Browse over 7000 ready-made automated workflow templates" (Measured meta; 7,830 URLs in the sitemap).

## 4. Blog / docs / academy

- Blog: 403 posts + 212 how-to guides (Measured).
- **Make Academy** is free, with badges and certification (third-party, *unverified*: https://academy.make.com/, https://credly.com/organizations/make/collections/make-intermediate/badge_templates). It lives on a subdomain, so our main-domain crawl doesn't see it.
- Help center: https://help.make.com (subdomain; not crawled).

## 5. Community / forums

- https://community.make.com (Discourse; *unverified*, found by search: https://community.make.com/t/make-academy-course-overview/29699). `/community` on the main site → 404 (Measured).

## 6. YouTube / social

- Footer (Measured, [`home.json`](../data/make.com/home.json)): YouTube https://www.youtube.com/@itsmake, LinkedIn, X `@make_hq`, Instagram, Facebook. The homepage also links **celonis.com** (Make's parent company). Subscriber counts: *unverified*.

## 7. Affiliate / partner / expert programs (strongest of the three)

- **Affiliate program**: https://make.com/affiliate, "Get paid to promote Make… Join our affiliate program" (Measured, 1,131 words). **35% commission for 12 months**, open to anyone with a Make account (third-party, *unverified*: https://help.make.com/affiliate-program). One referral-coded help page limits the 35% rate to Dec 1 2025 – Nov 1 2026, so the current rate may have changed (*unverified*).
- **Partners**: https://make.com/partners, "We offer five partnership programs" (Measured meta), including Solution Partners with required training and certification (*unverified*: https://www.make.com/solution-partners).
- Affiliate links show up on help-center URLs with `?pc=<code>` (e.g. `help.make.com/affiliate-program?pc=thanmen`; seen in search results). The affiliate channel visibly spreads through creators.

## 8. Marketplaces

- **AWS Marketplace** Enterprise listing since June 2022 (*unverified*: https://www.make.com/en/aws-make-partnership).

## 9. Product-led loops

- Free plan ("Get started free" in the integrations meta; Measured text). Sign-up: https://www.make.com/register (Measured, screenshot).
- Templates can be cloned straight into a scenario (inferred from the page; not measured).
- Waves conference: https://make.com/events, H1 "Waves '26 Recap" (Measured). Waves '26 took place in Prague, 19–20 Oct 2026 (*unverified*: https://www.make.com/blog/preview-waves-where-the-bold-make-it-happen).
- Webinars: 64 pages (Measured).

## 10. Paid ads signals

- No dedicated campaign landing-page family in sitemaps (landing = 60 single pages; Measured). Ad libraries were not reachable from this session. *Unverified.*

## 11. Launches / enterprise sales

- `/enterprise` → **403** to our crawler, and `/apps` → 403 (Measured; bot protection on some paths).
- Product Hunt: no Make launch found (*unverified*).

## 12. What Make is missing or does badly (Measured)

| Issue | Evidence | Why it matters |
|---|---|---|
| **No structured data on its money pages** | templates (7,830), integrations (3,452) and pairs (1,102): `schema_types: []` on all samples | Zapier ships `SoftwareApplication`/`HowTo`/`Action`, so Make misses rich results |
| **Tiny pair coverage** | 1,102 pair pages vs Zapier 148,333 | the long tail is ceded to Zapier |
| **218 category pages share one title** | "3,500+ Integration Apps \| Connect & Automate Software \| Make" on 3/3 | duplicate titles |
| **Parameterized URLs in sitemap** | `/integrations/category/*?categoryType=subcategory` canonicalize to the clean URL | non-canonical URLs submitted |
| **Empty meta descriptions** | `/workflows/*` 3/3, `/webinars/*` 2/3, `/authors/*` 1/3 | weak snippets |
| **Generic default meta on hub pages** | `/events`, `/webinars` use "Automate your work. Make allows you to visually create…" | weak snippets |
| **Generic template slugs** | `/templates/10036-new-template` titled "Create Google Calendar events from Notion" | lost keyword in the URL |
| **Stale content** | 2019 blog posts still in the sitemap | freshness |
| **No comparison pages** | `/compare`, `/vs`, `/alternatives` → 404 | "Zapier alternative" demand goes to third parties |
| **No localized URLs in sitemap** | `localized_urls: 0`, 0 hreflang on samples | international SEO (Make serves `/en/` paths, but other languages are *unverified*) |

Screenshots: artifact `raw-make.com`.
