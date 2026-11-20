# SEO, AEO, AIO, GEO, SXO: what they are and how to audit them

Run date: 2026-11-20. Public repo: no private data here. Free sources only.
Mark legend: **[unverified]** = could not confirm against the original or primary page this run.

## 0. Research limits (read first)
- This run's network blocked direct fetch of developers.google.com, arxiv.org and ahrefs.com. All facts below come from web-search result summaries that quote those pages, not from reading the pages in full. Where a number came from a secondary write-up, it is flagged.
- Many AI-citation studies are from vendors that sell AI-visibility tools. Treat percentages as study-specific, not universal.
- Not covered this run (searched, not read in full): Moz academy, Backlinko page text, Semrush page text, Bing's guideline text itself, Lily Ray's own posts.

## 1. The five terms in plain English

| Term | Goal | Where you "win" | Honest summary |
|---|---|---|---|
| **SEO** | Rank and get clicks in classic search results | Google/Bing blue links, snippets | The base layer. Everything else sits on it. |
| **AEO** (answer engine optimization) | Be the direct answer | Featured snippets, voice, AI answers | Older meaning: featured snippets/voice. Newer meaning: being cited by AI answer engines. Sources define it differently ([HubSpot](https://www.hubspot.com/glossary/aeo-answer-engine-optimization), [Ahrefs](https://ahrefs.com/aeo/what-is-aeo), [Conductor](https://www.conductor.com/academy/glossary/answer-engine-optimization/)). |
| **AIO** (AI Overviews optimization) | Be a cited source inside Google's AI Overviews / AI Mode | Google AI features | "AIO" is also used for generic "AI optimization", so say which you mean. Google says no special optimization is needed beyond SEO basics ([Google: AI features](https://developers.google.com/search/docs/appearance/ai-features)). |
| **GEO** (generative engine optimization) | Be cited or recommended by LLM answer engines | ChatGPT, Perplexity, Gemini, Claude, Copilot | Coined in the academic paper ([arXiv 2311.09735](https://arxiv.org/abs/2311.09735)): a black-box framework to raise visibility in generative engine responses, tested on GEO-bench, "up to 40%" visibility gain, effect varies by domain. Industry often just calls it "AI search optimization" ([Aleyda Solis](https://www.aleydasolis.com/en/ai-search/ai-search-optimization-checklist)). |
| **SXO** (search experience optimization) | Win the click, then satisfy the visit and convert | The whole journey: SERP, page, conversion | SEO + UX + CRO ([Ahrefs](https://ahrefs.com/blog/?p=179350), [Coveo](https://www.coveo.com/blog/search-experience-optimization/), [Yoast](https://yoast.com/what-is-search-experience-optimization-sxo/)). A vendor/agency framing, not an industry standard; the idea itself (match intent, then deliver) is sound. |

### How they differ and overlap
- **Overlap is large.** Google calls its AI features "rooted in our core Search ranking and quality systems" and says SEO best practices stay relevant ([SEJ on Google's May 2026 guide](https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/), [Google's guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)). A 2026 Aleyda Solis talk slide asks whether "good SEO is good GEO" is enough ([deck](https://speakerdeck.com/aleyda/winning-organic-in-2026-a-framework-for-surviving-googles-ai-era)).
- **Real differences:**
  1. *Unit of retrieval.* Classic SEO scores pages; AI systems score passages and expand one query into many sub-queries ("query fan-out") ([iPullRank AI Search Manual](https://ipullrank.com/ai-search-manual/relevance-engineering), [fan-out](https://ipullrank.com/blog/query-fan-out)).
  2. *Success metric.* SEO = clicks/rankings. GEO/AEO = citations, mentions, share of answer. AI Overviews correlate with fewer clicks: Ahrefs reports -58% CTR for position 1 where an AI Overview shows (300k keywords, Dec 2023 vs Dec 2025; correlation; Google disputes the framing) ([Ahrefs](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update)).
  3. *Off-site weight.* Brand mentions beat backlinks as a correlate of AI Overview brand visibility (0.664 vs 0.218, 75k brands, correlation not causation) ([Ahrefs](https://ahrefs.com/blog/ai-overview-brand-correlation/)).
  4. *Which crawler/index.* ChatGPT search uses OAI-SearchBot; Google uses Googlebot; Bing powers Copilot citations ([OpenAI docs](https://developers.openai.com/docs/gptbot), [Bing AI Performance](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)).
- **Mental model:** SEO = be findable. SXO = be satisfying once found. AEO/AIO/GEO = be quotable and be trusted by name. One content program, three surfaces.

### What AI answers actually cite (studies, dated)
- Reddit, Wikipedia, YouTube dominate, but shares differ by engine and study. Semrush (June 2025, 150k+ citations): Reddit 40.1%, Wikipedia 26.3%, YouTube 23.5% (frequency, totals >100%) ([Semrush via search summary](https://www.semrush.com/blog/most-cited-domains-ai/)). Profound: ChatGPT top source Wikipedia 47.9%; Reddit leads AI Overviews (21%) and Perplexity (46.7%) ([Profound](https://tryprofound.com/blog/the-data-on-reddit-and-ai-search), figures via search summary). Ahrefs: Wikipedia led all three engines ([Ahrefs](https://ahrefs.com/blog/top-10-most-cited-domains-ai-assistants)). Shares moved fast (ChatGPT cut Reddit/Wikipedia citations around Sept 2025, per Semrush) so re-check quarterly.
- Citations cluster near the top of a page: ~44% from the first third in a Growth Memo analysis; sample sizes differ across write-ups; full memo paywalled ([Growth Memo](https://www.growth-memo.com/p/the-science-of-how-ai-picks-its-sources), [Search Engine Land](https://searchengineland.com/chatgpt-citations-content-study-469483)).
- Reviews: G2's own study of 30k citations: +10% reviews ~ +2% citations; authors admit causality is unclear; G2 is a seller of the thing studied ([G2](https://learn.g2.com/do-more-g2-reviews-mean-more-ai-visibility)).
- YouTube: a figure of 0.737 correlation with AI brand visibility circulates on LinkedIn **[unverified]**; Ahrefs' own pages in this run only supported the 75k-brand mentions study.

---
## 2. SEO

**On-page:** one clear search intent per page; title/H1/meta match intent; helpful original content with first-hand expertise; internal links with descriptive anchors; images with alt text; clean URL; fresh and accurate content. ([Google SEO starter guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)).
**Off-page:** quality backlinks from relevant sites; brand searches; digital PR; reviews and local/business profiles; mentions on real communities.
**Technical:** crawlable (robots.txt, no accidental noindex), indexable, XML sitemap, canonical tags, HTTPS, mobile-friendly, fast Core Web Vitals, sane site architecture, structured data only where it matches visible content.
**Measured by:** Google Search Console (impressions, clicks, position, indexing), Bing Webmaster Tools, rank trackers, GA4 organic sessions and conversions, backlink counts (Ahrefs/Semrush free tiers).

**15-item checklist for a small SaaS**
1. Verify the site in Search Console and Bing Webmaster Tools.
2. Submit an XML sitemap; fix every "Excluded/Error" coverage reason.
3. Confirm robots.txt does not block key pages or CSS/JS.
4. One canonical URL per page; redirect www/non-www and http/https.
5. Map each target keyword to one page by intent (not one page for ten intents).
6. Write unique title (~60 chars) and meta description per page, with the main benefit.
7. One H1; H2s that mirror real questions from search suggestions and support tickets.
8. Add product proof: screenshots, real numbers, named customers if allowed.
9. Build comparison and alternative pages ("X vs Y", "X alternatives") honestly.
10. Internal link from every blog post to the relevant product/use-case page.
11. Pass Core Web Vitals on mobile (check PageSpeed Insights).
12. Add Organization/Product/FAQ schema only where the page truly shows that content.
13. Publish and refresh 1 helpful, original page per week or two; date-stamp updates.
14. Earn 5-10 relevant links: integrations directories, partner pages, podcasts, product launches.
15. Track organic clicks and conversions monthly in a simple sheet; prune thin pages.

**Myths:** "more keywords per page ranks better" (stuffing hurts); "meta keywords matter" (ignored); "AI content is auto-penalized" (Google targets unhelpful/scaled spam, not the tool) **[unverified this run]**; "SEO is dead" (Google says its AI features rest on core ranking systems, [SEJ](https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/)).

---
## 3. AEO (answer engine optimization)

**Scope used here:** getting your content chosen as *the direct answer* (featured snippet, People Also Ask, voice, and answer boxes in AI engines).
**On-page:** question-style headings; a 40-60 word direct answer right under the heading; definitions, steps, tables, lists; "what is / how to / vs / cost" pages; FAQ sections that mirror real questions ([Conductor](https://www.conductor.com/academy/glossary/answer-engine-optimization/), [HubSpot](https://www.hubspot.com/glossary/aeo-answer-engine-optimization)). Put the answer early (citations skew to the top of pages, [Growth Memo](https://www.growth-memo.com/p/the-science-of-how-ai-picks-its-sources)).
**Off-page:** third-party corroboration of your claims (reviews, directories, communities); Wikipedia/Wikidata presence only if you meet notability **[unverified for small SaaS]**.
**Technical:** indexable, snippet-eligible pages (no `nosnippet`; Google requires snippet eligibility for AI supporting links, [Google](https://developers.google.com/search/docs/appearance/ai-features)); clear heading hierarchy; FAQ/HowTo schema is optional, not required.
**Measured by:** featured-snippet ownership (Semrush/Ahrefs free tiers), Search Console queries phrased as questions, manual checks in ChatGPT/Perplexity/Gemini, referral traffic from AI domains in GA4.

**15-item checklist for a small SaaS**
1. List 30 real customer questions (support, sales calls, Reddit threads).
2. One page or section per question; question as the heading.
3. Answer in the first 1-2 sentences, plainly, then expand.
4. Use a definition sentence: "X is a Y that does Z for W."
5. Add a short table or list for comparisons, steps, pricing ranges.
6. Include one specific number, date, or example per answer.
7. Keep a visible "last updated" date and update facts quarterly.
8. Add author name and role with a real bio page.
9. FAQ block on money pages (3-6 real questions, visible text).
10. Add matching FAQ schema only if the text is on the page.
11. Check Search Console for question queries and improve those pages first.
12. Run your 30 questions monthly in 3 answer engines and log who is cited.
13. Fix wrong answers about you: update your own pages first, then correct profiles.
14. Give each answer a stable URL with a descriptive anchor/fragment.
15. Never hide the answer behind a form, tab-only UI, or script-only rendering.

**Myths:** "schema guarantees snippets" (Ahrefs found no reliable citation lift from schema: ChatGPT +2.2%, AI Overviews -4.6%, AI Mode +2.4%, per [SEJ summary](https://www.searchenginejournal.com/ai-search-myths-debunked-ahrefs-spa/)); "voice search is the main channel" **[unverified]**; "AEO replaces SEO" (sources treat it as complementary, [HubSpot](https://www.hubspot.com/glossary/aeo-answer-engine-optimization)).

---
## 4. AIO (Google AI Overviews / AI Mode)

**What Google says:** no additional requirements or special optimization for AI Overviews/AI Mode; page must be indexed and snippet-eligible; appearances are counted in Search Console's overall data; Google's May 2026 guide says llms.txt, special schema/Markdown and "tiny chunks" are not needed for Google ([AI features](https://developers.google.com/search/docs/appearance/ai-features), [guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [SEJ](https://www.searchenginejournal.com/google-says-llms-txt-is-purely-speculative-for-now/575026/)). Google later added a clarifying note on llms.txt use; re-read the current wording ([SEJ](https://www.searchenginejournal.com/googles-says-its-fine-to-use-llms-txt-for-ai-seo/579608/)). A June 2026 Google post describes a Search Console toggle to opt out of generative AI features, in testing in the UK ([Google blog](https://blog.google/products-and-platforms/products/search/new-opportunities-control-and-insights-for-website-owners/)).
**On-page:** unique, useful, people-first content; direct, well-structured passages; multimodal support (images, video) where it helps ([Google's May 2025 post](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search)).
**Off-page:** ranking helps but does not guarantee citation: 0.347 correlation between top-10 ranking and being cited in the top three AI Overview results ([Ahrefs](https://ahrefs.com/blog/does-ranking-higher-on-google-mean-youll-get-cited-in-ai-overviews)). Brand web mentions correlate strongest ([Ahrefs](https://ahrefs.com/blog/ai-overview-brand-correlation/)). Reddit and YouTube are frequent AIO citations ([Profound](https://tryprofound.com/blog/the-data-on-reddit-and-ai-search)).
**Technical:** Googlebot allowed (including by CDN/WAF); no `nosnippet`/`max-snippet` that blocks use; content in HTML, not hidden behind JS-only rendering or logins; structured data that matches visible text.
**Measured by:** Search Console (AI features are blended into normal Performance data, no separate report as of the cited page), manual query checks, third-party AIO trackers (Semrush/Ahrefs trial tiers), CTR trends on queries that show AIOs.

**15-item checklist for a small SaaS**
1. Confirm the target pages are indexed (URL Inspection).
2. Confirm no `nosnippet` or restrictive `max-snippet` on key pages.
3. Check that Googlebot is not blocked by WAF/CDN rules (review server logs/Crawl Stats).
4. Pick 20 informational queries; note which show an AI Overview.
5. For each, see who is cited; list their format (guide, Reddit, YouTube, docs).
6. Make your page the most complete, original answer; add unique data or a worked example.
7. Lead each section with a self-contained answer paragraph.
8. Use descriptive headings and short lists/tables where the query wants them.
9. Add a real video for how-to queries (YouTube is heavily cited).
10. Post genuine, non-promotional answers on Reddit/Quora where your team has authority; disclose affiliation.
11. Get listed on category pages and review sites that AIOs cite for your space.
12. Keep brand name, product name and category wording consistent everywhere.
13. Refresh stale pages; AIOs favor current facts **[unverified for Google specifically]**.
14. Track impressions/clicks on those 20 queries in Search Console monthly.
15. Do NOT add llms.txt, "AI-only" pages, or chunk-splitting for Google's sake.

**Myths:** "You need llms.txt for AI Overviews" (Google says no, see above); "blocking Google-Extended removes you from AI Overviews" (secondary sources say it does not control Search; **[unverified: Google page not read]**); "position 1 always gets cited" (0.347 correlation only); "schema is a switch" (Google: not required).

---
## 5. GEO (being cited by ChatGPT, Perplexity, Gemini, Claude)

**Paper findings:** on GEO-bench, methods that add sources, quotations and statistics improved visibility in generative answers, up to ~40%, with variation by domain ([arXiv 2311.09735](https://arxiv.org/abs/2311.09735)). The specific per-method gains were not retrieved this run **[unverified; read the PDF]**. These tests used the authors' generative engine setup, so treat results as directional for real products.
**On-page:** passage-level clarity (each section answers one thing); specific stats with sources; quotations from named experts; definitive, entity-rich, direct language ([Search Engine Land](https://searchengineland.com/chatgpt-citations-content-study-469483) reports ChatGPT favors direct definitions, balanced tone, dense entities; the definitive-language effect was not quantified in what I found); answer-first structure; cover the sub-questions of a topic because engines fan queries out ([iPullRank](https://ipullrank.com/blog/query-fan-out), [AirOps](https://www.airops.com/research/the-fan-out-effect-what-happens-between-a-query-and-a-citation)).
**Off-page:** brand mentions across the web; Reddit threads and YouTube videos; Wikipedia where eligible; G2/Capterra reviews for software; "best X" listicles on third-party sites; consistent entity data. G2 reports review-site share of citations is large within review sites but review sites are only ~30% of the citations in one analysis ([G2](https://learn.g2.com/do-more-g2-reviews-mean-more-ai-visibility), [summary of third-party data](https://learn.g2.com/tech-signals-does-g2-get-ranked-in-ai-llm-search)); vendor sources, verify independently.
**Technical:** allow search crawlers: OpenAI documents OAI-SearchBot (search) separately from GPTBot (training); changes take ~24h ([OpenAI](https://developers.openai.com/docs/gptbot)). Perplexity/Claude/Gemini crawler names: confirm on each vendor's docs **[unverified, only secondary guides found]**. Server-render core content; no login/paywall on pages you want cited; fast, stable URLs. Bing indexing matters for Copilot: use Bing Webmaster Tools and IndexNow ([Bing blog](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)).
**Measured by:** a fixed prompt set run monthly in each engine (share of answers that cite or name you, position, sentiment, accuracy); Bing Webmaster Tools AI Performance (citations, cited pages, grounding queries, citation share; no clicks) ([Bing](https://blogs.bing.com/search/June-2026/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare)); GA4 referrals from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com; "how did you hear about us" answers; paid trackers (not used here).

**15-item checklist for a small SaaS**
1. Build a prompt set: 25 prompts across "what is", "best X for Y", "X vs Y", "alternatives to X".
2. Run it in ChatGPT, Perplexity, Gemini, Claude; log cited domains and whether you appear.
3. Allow OAI-SearchBot and other search crawlers in robots.txt; decide separately on training bots.
4. Verify site in Bing Webmaster Tools; turn on IndexNow.
5. Publish an "About / What is [Product]" page with one-sentence definition, category, audience, pricing model.
6. Add 3+ cited statistics and 1 expert quote to each pillar page, with source links.
7. Make "X vs Y" and "alternatives" pages that include honest limits of your product.
8. Put the answer in the first third of each page and each section.
9. Create a public changelog and docs; clear docs get cited for how-to prompts.
10. Get listed on G2, Capterra, Product Hunt, and relevant niche directories; ask real users for honest reviews.
11. Join relevant subreddits as a transparent participant; answer questions without link-dropping.
12. Publish 3-5 short YouTube walkthroughs with transcripts and descriptive titles.
13. Pitch 3 "best X tools" list authors with a fair, factual brief (no paid fake reviews).
14. Keep facts identical across site, profiles, directories (name, category, pricing, features).
15. Re-run the prompt set monthly; fix any wrong claims at the source.

**Myths:** "llms.txt boosts citations" (an analysis of ~18k citations found 0.03% came from llms.txt, via [DesignRush summary](https://news.designrush.com/llmstxt-ai-search-visibility), second-hand **[unverified]**); "schema markup gets you cited" (no reliable lift, [SEJ/Ahrefs](https://www.searchenginejournal.com/ai-search-myths-debunked-ahrefs-spa/)); "GEO is totally different from SEO" (Aleyda Solis, Lily Ray decks lean "good SEO first": [Lily Ray deck](https://www.slideshare.net/slideshow/how-seo-geo-work-together-do-great-geo-without-destroying-your-seo/288304832)); "one citation share number is universal" (shares differ by engine and shift quickly); "keyword stuffing for LLMs works" **[unverified]**.

---
## 6. SXO (search experience optimization)

**On-page:** page type matches what the SERP rewards (guide vs product vs comparison); above-the-fold answer plus a clear next step; scannable layout; honest, specific copy; trust signals (reviews, security, pricing clarity); no intrusive pop-ups; one primary CTA.
**Off-page:** review ratings, brand reputation, social proof that shows in snippets and AI answers.
**Technical:** Core Web Vitals, mobile layout, accessibility, no layout shift, fast forms, working internal search, clean analytics events.
**Measured by:** conversion rate by landing page and query group, engaged sessions and scroll depth (GA4), session recordings/heatmaps (free tiers), form and trial-start completion, Search Console CTR, SERP-intent match audits.
Definitions: [Ahrefs](https://ahrefs.com/blog/?p=179350), [Coveo](https://www.coveo.com/blog/search-experience-optimization/), [Yoast](https://yoast.com/what-is-search-experience-optimization-sxo/), [Kinsta](https://kinsta.com/blog/search-experience-optimization/).

**15-item checklist for a small SaaS**
1. For each target query, open the top 5 results; note the dominant page type and intent.
2. Match that page type; if the SERP is all comparisons, do not ship a feature page.
3. Put the answer or core promise above the fold, in plain words.
4. One primary CTA per page (start trial / book demo), repeated after proof.
5. Show pricing or a clear pricing path; hiding it loses trust.
6. Add real screenshots or a short demo clip near the top.
7. Use social proof with specifics (logos you have rights to, rated reviews).
8. Remove pop-ups that cover content on mobile.
9. Cut page weight; pass mobile Core Web Vitals.
10. Make headings scannable; keep paragraphs short.
11. Test the signup flow on a phone; remove every non-essential field.
12. Set GA4 conversion events for signup, trial, demo request.
13. Review a heatmap/recording sample for each key page monthly.
14. Align title/meta promise with the page content (no bait).
15. Run a quarterly A/B or before/after test on one headline or CTA, log the result.

**Myths:** "SXO is a new ranking factor" (it is a framing; Google's guidance on page experience stays within core quality systems **[unverified this run]**); "bounce rate is a direct ranking signal" **[unverified]**; "UX tweaks replace content quality".

---
## 7. Combined audit rubric (run on any page; 0-100 per type)

How to run (about 20 minutes per page): open the page, view source, test in Search Console/URL Inspection, run its target query in Google, ChatGPT, Perplexity. Score each line 0 (absent), 1 (partial), 2 (solid). Each type has 10 lines x 2 = 20 raw points, x5 = 100.

Score bands: 0-39 weak, 40-69 workable, 70-84 good, 85-100 strong. Always record the URL, date and evidence per line.

### SEO (0-100)
| # | Check | 0 / 1 / 2 |
|---|---|---|
| 1 | Indexed, canonical correct, no noindex | |
| 2 | One clear intent matching target query | |
| 3 | Title, H1, meta match intent and are unique | |
| 4 | Content is original, specific, current | |
| 5 | Internal links in and out with descriptive anchors | |
| 6 | Mobile-friendly, Core Web Vitals pass | |
| 7 | In XML sitemap; no crawl blocks | |
| 8 | Relevant backlinks to the page or its section | |
| 9 | Valid schema matching visible content (if used) | |
| 10 | Ranks top 10 for target query (Search Console) | |
Score = sum x 5.

### AEO (0-100)
| # | Check | 0 / 1 / 2 |
|---|---|---|
| 1 | Question-style heading for the target question | |
| 2 | Direct answer in the first 1-2 sentences under it | |
| 3 | Answer is self-contained (makes sense if lifted alone) | |
| 4 | Uses list/table/steps where query type wants it | |
| 5 | Includes a definition sentence for key terms | |
| 6 | Has FAQ or related questions covered | |
| 7 | Snippet-eligible (no nosnippet) | |
| 8 | Owns or competes for a featured snippet/PAA | |
| 9 | Date, author and source links visible | |
| 10 | Answers are correct and match third-party sources | |
Score = sum x 5.

### AIO (Google AI Overviews / AI Mode) (0-100)
| # | Check | 0 / 1 / 2 |
|---|---|---|
| 1 | Indexed and snippet-eligible; Googlebot not blocked by CDN | |
| 2 | Target query shows an AI Overview (record yes/no) | |
| 3 | Page is cited in the AI Overview/AI Mode (record yes/no) | |
| 4 | Content more complete or original than cited pages | |
| 5 | Passages answer sub-questions of the query | |
| 6 | Page ranks in top 10 for the query or a fan-out variant | |
| 7 | Brand has third-party mentions for the topic | |
| 8 | Video or image support present where relevant | |
| 9 | No reliance on llms.txt/special markup | |
| 10 | Search Console shows stable or rising impressions for the query group | |
Score = sum x 5. (Lines 2-3 are observations, so a page with no AIO can still score by treating "no AIO" as 1.)

### GEO (0-100)
| # | Check | 0 / 1 / 2 |
|---|---|---|
| 1 | Search crawlers allowed (OAI-SearchBot etc.); Bing indexed | |
| 2 | Key content is server-rendered, no login wall | |
| 3 | Answer in first third; passages are self-contained | |
| 4 | Cited stats and a named quote/source on the page | |
| 5 | Entity clarity: brand, category, audience stated plainly | |
| 6 | Appears in answers for the prompt set (score by share: 0 / <25% / >=25% of 25 prompts) | |
| 7 | Cited by at least 2 of 4 engines | |
| 8 | Third-party presence: reviews (G2/Capterra), lists, directories | |
| 9 | Reddit/YouTube/community presence on the topic | |
| 10 | Facts consistent across web; AI answers about you are accurate | |
Score = sum x 5.

### SXO (0-100)
| # | Check | 0 / 1 / 2 |
|---|---|---|
| 1 | Page type matches SERP intent | |
| 2 | Value clear above the fold in under 5 seconds | |
| 3 | One clear primary CTA | |
| 4 | Proof: screenshots, numbers, reviews | |
| 5 | Load speed and layout stable on mobile | |
| 6 | Scannable structure, readable text | |
| 7 | No intrusive pop-ups or dark patterns | |
| 8 | Conversion tracking set up | |
| 9 | Conversion or engaged-session rate known and above site average | |
| 10 | Next step for non-ready visitors (docs, demo, email) | |
Score = sum x 5.

### Combined summary sheet
| Page URL | Date | SEO | AEO | AIO | GEO | SXO | Top 3 fixes |
|---|---|---|---|---|---|---|---|
| | | /100 | /100 | /100 | /100 | /100 | |

Reading it: low SEO caps everything else (AIO and GEO both lean on ranking and indexing). High SEO + low GEO = go work off-site (mentions, reviews, Reddit/YouTube). High traffic + low SXO = fix the page, not the keywords.

## 8. Open items to verify next run
- Read the GEO paper PDF for per-method gains (arXiv blocked here).
- Read Google's AI features page and optimization guide in full (blocked here).
- Pull Bing's actual Webmaster Guidelines text.
- Get primary docs for Perplexity, Anthropic and Google crawler tokens.
- Confirm the YouTube 0.737 correlation against Ahrefs' own study.
- Read Moz, Backlinko and Semrush course pages directly.
