# Competitor audit: workflow automation (crawl of 2026-11-20)

Data: `data/competitor_crawl_2026-11-21.json` (crawled 2026-11-20 19:20 UTC: robots.txt, llms.txt, sitemaps, 10-12 pages per site, Google autocomplete for 12 seeds, Wikipedia check).
Rubric: `reports/seo_aeo_geo/CONCEPTS.md` section 7 (branch `research/seo-aeo-geo-concepts-2026-11-21`). Query context: `reports/competitor_search/QUERIES.md`.
Public repo: competitor analysis only. Nothing about our own analytics, keys or plans.

## 0. How to read the scores (limits first)

- **Scores are estimates from what the crawl can see.** I scored only the rubric lines a crawl can observe (indexing tags, title/H1/meta, content depth, question headings, tables, schema, sitemap, robots, llms.txt, Wikipedia). I left out lines that need private or live data (rankings, Search Console, backlinks, AI-citation share, conversion rate). So each number is "on-site and crawl-visible strength", rounded to the nearest 5, plus or minus about 10. It is not a ranking prediction.
- AIO and GEO are the least certain: no AI Overview or ChatGPT answer was checked. They lean on indexability, answer structure, crawler policy and off-site presence.
- **robots.txt:** the crawl saved only the `User-agent:` lines for AI bots, not the Allow/Disallow lines. A bot being named means the site has a rule for it; it does not say whether that rule blocks or allows. Sites with no AI-bot lines fall under their `*` rule, which was not saved.
- **llms.txt:** every site returned `llms_txt = true`. The crawl stored only length. I did not verify each is a real llms.txt rather than a soft-404 page. Google says it does not use llms.txt, so this is a GEO signal only (CONCEPTS section 4).
- **Sitemap counts** are the totals the crawl read. Zapier's `apps: 50000` is exactly the 50,000-URL file limit, so its real app-page count is probably higher (the crawl shows only two families for it).
- `hreflang` was 0 on every page of every site. Make and Zapier are known to run localized pages (QUERIES.md), so this is likely a crawler limit. Treated as **unknown**.
- Gumloop's home page timed out, so its home was scored on its other pages.
- **fansachat.com:** the site is a React app, but it is pre-rendered (build runs `scripts/prerender.mjs`). The crawl got real HTML: home 530 words, FAQPage schema present. So the word counts are not a client-side artefact on the pages crawled. A few pages could still be lighter than they look if some blocks load only in the browser. This is not testable from the crawl.

## 1. Scorecard (0-100 per type)

Order of columns: SEO / AEO / AIO / GEO / SXO. Evidence is from the data file.

| Site | SEO | AEO | AIO | GEO | SXO |
|---|---|---|---|---|---|
| **Zapier** | 90 | 55 | 70 | 75 | 70 |
| **Make** | 80 | 55 | 60 | 65 | 65 |
| **n8n** | 85 | 40 | 55 | 65 | 60 |
| **Pabbly** | 60 | 30 | 35 | 30 | 45 |
| **IFTTT** | 80 | 50 | 55 | 65 | 60 |
| **Activepieces** | 80 | 75 | 65 | 70 | 65 |
| **Lindy** | 70 | 90 | 70 | 70 | 65 |
| **Gumloop** | 60 | 65 | 55 | 55 | 60 |
| **FansaChat** | 60 | 60 | 45 | 45 | 55 |

### One-line evidence per score

**Zapier**
- SEO 90: 53,885 sitemap URLs (apps 50,000+, blog 3,885); canonical on all 12 pages; Article, Organization schema and dates on every blog page; 2,500-6,100 words per guide.
- AEO 55: 0-3 question headings per page; one table on 5 of the 12 pages; no FAQPage schema on the sampled pages.
- AIO 70: deep, dated, indexable guides on exactly the comparison and alternatives queries (`/blog/n8n-vs-make/`, `/blog/pipedream-alternatives/`); no AIO check made.
- GEO 75: names 5 AI bots in robots (GPTBot, OAI-SearchBot, ClaudeBot, Google-Extended, PerplexityBot); llms.txt 14.8k chars; Wikipedia article exists.
- SXO 70: page types match intent (guide for guide queries); no demo, pricing or conversion data seen.

**Make**
- SEO 80: 13,696 URLs; but no canonical tag detected on home, blog and both compare pages; template and integration pages carry no JSON-LD at all.
- AEO 55: 4-5 question headings on integration and compare pages; 26-29 H2 on compare pages; 0 tables detected.
- AIO 60: long compare pages (4,400 and 5,450 words) are strong passages; thin templates (780-900 words) are not.
- GEO 65: llms.txt 14.3k; no AI-bot rules named; Wikipedia article exists.
- SXO 65: very large template and integration libraries match "how do I connect X to Y" intent; templates are short and repetitive.

**n8n**
- SEO 85: 316,443 URLs (integrations 301,333, workflows 14,379, vs 30); canonical on every page.
- AEO 40: 0-3 question headings; 1 table on 1 of 12 pages; vs pages have no JSON-LD.
- AIO 55: workflow and integration pages are thin (256-613 words); `/vs/*` pages are solid (2,470-2,900 words).
- GEO 65: llms.txt only 1.1k chars; no AI-bot rules; Wikipedia article exists.
- SXO 60: workflow pages carry Offer + AggregateRating + WebApplication schema; they are template pages with little prose.

**Pabbly**
- SEO 60: 20,373 URLs (connect 1,003); blog posts sit at the root path, with no `/blog/` family; some pages look off-topic (`/sell-lcd-tvs-online/`, `/free-wordpress-themes`, `/free-online-learning-sites`).
- AEO 30: 0 question headings on all 12 pages; 1 table on 2 pages. The 36-46 H2 per ~1,500-word page look like menu or sidebar headings, not answer sections.
- AIO 35: thin on the target topic; much of the content is loosely related blog filler.
- GEO 30: llms.txt 4k chars; no AI-bot rules; **no Wikipedia article**.
- SXO 45: home is 4,322 words; page types are mixed; unclear intent per page.

**IFTTT**
- SEO 80: 100,254 URLs (connect 60,556, applets 19,738, service pages 10,608, explore 199); canonical on all pages; HowTo schema on applets.
- AEO 50: 2-5 question headings on 6 of 7 `/explore/` articles; 1 table on `ifttt-alternatives`.
- AIO 55: explore articles 1,100-2,600 words with Blog/BlogPosting schema and dates; service pages can be very thin (174 words).
- GEO 65: llms.txt 9k; no AI-bot rules; Wikipedia article exists.
- SXO 60: home carries AggregateRating + Offer; applet pages show a clear task.

**Activepieces**
- SEO 80: 7,527 URLs (pieces 3,795, blog 1,846, resources 1,068, mcp 795); canonical on all pages; BlogPosting + Person + dates on every blog page.
- AEO 75: **FAQPage schema on home and pricing**; 1-6 question headings and 1-4 tables on most blog pages.
- AIO 65: 2,000-3,800 word posts; "X pricing 2026" posts about third-party tools (Krisp, Calendly, ProtonVPN) catch question traffic.
- GEO 70: llms.txt is **480,791 chars** (the largest by far, likely full docs); no AI-bot rules; Wikipedia not checked.
- SXO 65: pricing page has a table and FAQ; open-source positioning is clear.

**Lindy**
- SEO 70: only 1,736 URLs but dense; canonical on all pages.
- AEO 90: **41 question headings on one page** (`best-chatgpt-alternatives`), 6-10 on most others; FAQPage + Answer + AggregateRating schema on 5 of 11 pages; tables on every long post.
- AIO 70: 5,400-8,800 word list posts, regularly dated, with FAQ structure.
- GEO 70: llms.txt 2.6k; no AI-bot rules; Wikipedia not checked.
- SXO 65: `/integrations` is one page with 21,272 words and 2,735 H2: heavy and hard to scan.

**Gumloop**
- SEO 60: 930 URLs; home timed out in the crawl; **no canonical detected on 7 of 11 pages (incl. the timed-out home)**.
- AEO 65: FAQPage + Answer schema on `/pricing` and `/vs/*`; `/vs/*` pages have a table; blog posts have only 4-5 H2 and 1-2 question headings.
- AIO 55: long posts (3,800-6,100 words) with few headings: hard to lift passages from.
- GEO 55: llms.txt 44.6k; no AI-bot rules; Wikipedia not checked.
- SXO 60: pricing page is short (497 words) with Offer schema; `/vs/*` pages match intent.

**FansaChat (live crawl, before the notices pages are deployed)**
- SEO 60: 74 URLs; **every crawled page has canonical, `index, follow` and a clean unique title**; dates present; but small (230-1,780 words) and only 74 URLs.
- AEO 60: FAQPage + Answer schema on 8 of 10 pages (not /pricing or /blog); compare pages have 4 question headings; but home, blog, integrations and best-of page have 0 question headings; only 4 of 10 pages have a `<table>`.
- AIO 45: well indexable, but thin and no outside mentions; no Wikipedia; AIO presence unknown.
- GEO 45: names 5 AI bots in robots; llms.txt 13.8k; pre-rendered HTML; no third-party presence in the data; no Wikipedia checked.
- SXO 55: pricing page is detailed (1,780 words, 2 tables, Offer schema with unit prices); no demo or proof checked.

## 2. Programmatic page families (from sitemaps)

| Site | Total URLs | Largest families | What the family is |
|---|---|---|---|
| n8n | 316,443 | integrations 301,333; workflows 14,379; creators 542; vs 30 | app-detail and workflow-template pages (Offer + AggregateRating + WebApplication schema), 256-613 words each |
| IFTTT | 100,254 | connect 60,556; applets 19,738; p (service) 10,608; explore 199 | service connect pages, applets with HowTo schema, blog in `/explore/` |
| Zapier | 53,885+ | apps 50,000+ (cap); blog 3,885 | app and app-pair pages; blog of 2,500-6,100 word guides |
| Pabbly | 20,373 | connect 1,003; subscriptions 27; most others 1-2 | the rest is root-level blog posts |
| Make | 13,696 | templates 7,831; integrations 4,829; blog 404; how-to-guides 213; workflows 141; success-stories 104; compare 2 | template pages ~800 words with no schema; integration pages ~1,700 words |
| Activepieces | 7,527 | pieces 3,795; blog 1,846; resources 1,068; mcp 795 | app ("piece") pages; MCP server pages; a large blog |
| Lindy | 1,736 | integrations 1,409; blog 293 | integrations and AI-agent blog lists |
| Gumloop | 930 | connectors 350; blog 163; api-reference 112; help 65; use-cases 38; vs 8 | connectors plus docs |
| **FansaChat** | 74 | integrations 31; compare 13; alternatives 8; use-cases 6; blog 3 | pair pages, comparisons and alternatives |

- **Alternatives / vs pages:** Make 2 (`/compare`), n8n 30 (`/vs`), Gumloop 8 (`/vs`), Lindy has `lindy-vs-*` at root, IFTTT has `/explore/*-vs-*`, Zapier and Activepieces do them as blog posts, Pabbly as root-level posts. FansaChat has 13 compare + 8 alternatives pages, a high count for a 74-URL site.
- Template families (Make 7,831, n8n 14,379, IFTTT applets 19,738) are the biggest long-tail machine. FansaChat has 6 use-case pages and 31 integration pages.
- The crawl shows the **URL families**, not how many are indexed or earn clicks.

## 3. AI-crawler policy and llms.txt

| Site | AI-bot lines in robots.txt (names only) | llms.txt (chars) | Sitemap URLs |
|---|---|---|---|
| Zapier | GPTBot, OAI-SearchBot, ClaudeBot, Google-Extended, PerplexityBot | 14,763 | 53,885 |
| Make | none named | 14,344 | 13,696 |
| n8n | none named | 1,154 | 316,443 |
| Pabbly | none named | 4,043 | 20,373 |
| IFTTT | none named | 8,960 | 100,254 |
| Activepieces | none named | 480,791 | 7,527 |
| Lindy | none named | 2,576 | 1,736 |
| Gumloop | none named | 44,645 | 930 |
| FansaChat | GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended | 13,820 | 74 |

- Only Zapier and FansaChat say anything about AI bots. Whether those lines allow or block was not saved by the crawl (**unknown**). The other seven rely on their general rules.
- Every site has an llms.txt, so having one is no edge. Size runs from 1.2k (n8n) to 481k (Activepieces).
- Per CONCEPTS: llms.txt has no proven citation lift and Google ignores it. Count it as a small signal, not a differentiator.

## 4. Five tactics that win each competitor traffic

Inferred from the crawl and the SERP evidence in QUERIES.md. They are "what the data suggests", not traffic data.

**Zapier**
1. Huge app and app-pair programmatic base (50,000+ URLs).
2. Long, dated editorial guides (2,500-6,100 words) on comparison, alternatives and pricing topics, including competitors' own terms (`n8n-vs-make`, `pipedream-alternatives`, `uipath-pricing`).
3. Consistent schema: Article, Organization, Person, BreadcrumbList on every blog page; canonical everywhere.
4. Brand authority (Wikipedia article, 5 AI bots named, llms.txt).
5. Ranks for rivals' versus queries ("n8n vs make"), taking traffic that vendors cannot take for themselves.

**Make**
1. 7,831 template pages and 4,829 integration pages, one per trigger-to-action idea.
2. Two long compare pages (`make-vs-zapier` 4,394 words; `make-vs-n8n` 5,451 words) with 26-29 H2.
3. How-to guides (213) and workflow pages that target task queries.
4. Localized duplicates (known from QUERIES.md; crawl did not read hreflang).
5. Category hub pages ("automation tools") that win head terms.

**n8n**
1. 301,333 integration and 14,379 workflow pages: the largest long-tail base here.
2. 30 `/vs/` pages (Workato, Windmill, Azure Logic Apps), 2,500-2,900 words each, aimed at enterprise tool swaps.
3. Offer + AggregateRating + WebApplication schema on template pages (rich-result bait).
4. Open-source and self-hosted niche ("zapier alternative self hosted", "n8n alternative github" in autocomplete).
5. Community creators (542 creator pages) supply the templates.

**Pabbly**
1. Many "X alternatives" posts (`mailerlite-alternatives`, `subscriptions-alternatives`) plus a Make-vs-Pabbly page.
2. Review pages for subscription tools (baremetrics, recurly, profitwell, zoho).
3. Price-led positioning (lifetime deal; autocomplete shows "zapier alternative lifetime deal").
4. Programmatic `connect` pages (1,003).
5. Broad blog on unrelated topics for volume. Weak elsewhere: no question headings, no Wikipedia page.

**IFTTT**
1. 100k URL base: connect (60,556), applets (19,738), service pages (10,608).
2. `/explore/` articles: `ifttt-alternatives`, `ifttt-vs-make`, `zapier-vs-ifttt-ai-tools` on the same queries FansaChat targets.
3. HowTo schema on applets.
4. Consumer and smart-home families (SwitchBot, Aqara, Wyze, Spotify service pages).
5. Wikipedia presence, AggregateRating and Offer on the home page.

**Activepieces**
1. 3,795 "piece" pages plus 795 MCP-server pages (AI-agent angle).
2. Blog of 1,846 URLs: "best X alternatives in 2026" and "X pricing 2026" for third-party SaaS products (UiPath, Slack, Calendly, Krisp, ProtonVPN), 2,000-3,800 words with tables.
3. FAQPage schema on home and pricing.
4. Open-source positioning (autocomplete: "open source", "self hosted", "github" appear across alternative queries).
5. A huge llms.txt (481k chars) that exposes its docs to AI crawlers.

**Lindy**
1. Long "best X" and "X alternatives" posts (5,400-8,800 words) with 6-41 question headings each.
2. FAQPage + Answer + AggregateRating schema on its long blog posts.
3. 1,409 integration pages.
4. `lindy-vs-superhuman`, `lindy-vs-fyxer` comparison pages (1,500 words, table).
5. AI-agent framing: `best-ai-agents`, `best-ai-agent-builders`, `best-ai-apps-for-android`.

**Gumloop**
1. 350 connector pages and 112 API-reference pages.
2. Long "X alternatives" posts (Apify, Appsmith: 3,800-6,100 words).
3. `/vs/chatgpt-work` and `/vs/claude-cowork`: AI-assistant versus pages with FAQPage + table.
4. 38 use-case pages.
5. "Best AI agent builder" and "best agent harness" listicles for the newest query group.

## 5. Query map (Google autocomplete, 12 seeds)

Source: `google_suggest` in the data file. No volumes exist.

| Group | Suggestions seen | Which competitor page type serves it |
|---|---|---|
| **Head** | workflow automation tools (+ list, free, examples, open source, integrate, ai, like n8n, microsoft); no code automation (+ tools, platforms, course, jobs, meaning); ai automation tools (+ list, free, examples, for hr, for digital marketing) | Category hubs and "best X" listicles on vendor blogs (Make's `/automation-tools` per QUERIES.md; Lindy/Gumloop "best" lists). Some suggestions are job and course queries, not buyer intent. |
| **Best / easy / cheap** | best workflow automation (software, platform, tools for creating ai agents, for small business, free, reddit); best automation software for small business; which automation tool is best / in demand / free; easiest automation tool (mostly test-automation sense) | Listicles: Lindy `best-ai-agents`, Gumloop `best-ai-agent-builder`, FansaChat `/best-ai-workflow-automation-tools`. "Reddit" suffix appears, so Reddit threads rank here too. |
| **Alternative** | zapier alternatives (free, open source, lifetime deal, for wordpress, reddit, self hosted, **dsgvo**, **alternativen** (German)); n8n alternative (open source, self hosted, github, 2026, reddit); make alternative (mostly noise: the English word "make") | Pabbly/Activepieces/Lindy/Gumloop/IFTTT `/x-alternatives` pages; Zapier's own alternatives guides for rival names; FansaChat `/alternatives/*` (8). |
| **Vs** | zapier vs n8n / make / make vs n8n / power automate / composio / claude / ifttt / workato / "which is better" | Make `/compare/*`, n8n `/vs/*`, Zapier blog, IFTTT `/explore/*-vs-*`, Gumloop `/vs/*`, Lindy `/lindy-vs-*`, FansaChat `/compare/fansachat-vs-*`. |
| **Questions / price** | what is cheaper than zapier; is make cheaper than zapier; is n8n cheaper than zapier; zapier vs n8n which is better | Pricing pages and comparison pages. **No dedicated "is X cheaper than Y" page was seen on any crawled site**: an open gap (it feeds AI answers). Activepieces' "X pricing 2026" posts show the pattern. |
| **Niche** | zapier alternative for wordpress, self hosted, dsgvo, lifetime deal; workflow automation tools open source, microsoft; ai automation tools for hr / digital marketing | n8n and Activepieces own self-hosted and open source; Pabbly owns lifetime deal. **GDPR/dsgvo, WordPress, HR and marketing: no crawled page targets these.** |

Not covered by autocomplete: the app-pair queries (Shopify to Sheets etc.) were not among the 12 seeds, so their demand is unmeasured here.

## 6. Off-page signals

- **Known:** Wikipedia article exists for Zapier, Make (software), n8n and IFTTT; **none for Pabbly**. Activepieces, Lindy, Gumloop and FansaChat were not in the Wikipedia check.
- **Indirect:** autocomplete includes "reddit" for three of the groups (best workflow automation reddit, zapier alternatives reddit, n8n alternatives reddit). CONCEPTS cites Reddit, Wikipedia and YouTube as the most-cited AI sources (study-dependent).
- **Unknown (not in the data):** backlinks and referring domains; G2/Capterra/Product Hunt listings and review counts; Reddit and YouTube presence; Wikidata; organic traffic and keyword rankings; AI-citation share in ChatGPT, Perplexity, Gemini, Claude; field Core Web Vitals; whether the AI-bot lines in robots.txt allow or block; which sitemap URLs are indexed.
- To fill those gaps: allow `google.com`, `g2.com`, `reddit.com` and a rank-data source, run the prompt set from CONCEPTS section 5, and re-run with robots.txt Allow/Disallow lines saved.

## 7. What this means (short)

- The big vendors (n8n, Zapier, IFTTT, Make) win on volume of programmatic pages; no small site can match 50,000+ URLs, so copy the page types that need little volume: alternatives, vs, pricing questions.
- Lindy and Activepieces show that answer structure (question headings, tables, FAQ schema) is the cheapest edge, and neither is a giant.
- Nobody serves "is X cheaper than Y", GDPR/dsgvo, WordPress or HR niches in the crawled pages.
- Pabbly is the weakest on-site (0 question headings, no Wikipedia, off-topic pages).
