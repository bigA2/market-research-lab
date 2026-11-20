# Competitor search demand: workflow automation (2026-11-20)

Branch: `research/competitor-search-2026-11-21`. Public repo: no private data.

## Read this first: what could NOT be done
This session's network only allowed WebSearch. Direct fetches failed (DNS/proxy block):
- **fansachat.com (home, /pricing, /compare/*, /integrations/*, /blog): not fetched.** A web search for it returned no page from that domain either. So every "current fansachat.com" statement below is **[unverified]** and the plan's fix-vs-create column is a default to confirm.
- Google autocomplete endpoint, competitor sitemaps, Reddit, G2/Capterra pages: not fetched directly. Query groups below are built from search-result titles (the pages that rank), not from real suggest/PAA data. No volume numbers exist here.
- Nothing about Pabbly, IFTTT, Activepieces, Lindy, Gumloop, Relay.app, Integrately was checked page-by-page, except what appears in the sources cited.

To finish properly: allow `fansachat.com`, `suggestqueries.google.com`, `zapier.com` in the session network settings and re-run.

## 1. Query groups (built from ranking-page titles; demand = [unverified])

| Group | Example queries | Evidence the query exists |
|---|---|---|
| Head | workflow automation tools, automation software, no-code automation, AI automation | [Make: automation-tools page](https://www.make.com/automation-tools), [Zoho SMB roundup](https://www.zoho.com/flow/best-integration-platforms-smb-2026.html) |
| Best / easy / cheap | best zapier alternative for small business; which workflow automation tool is easiest to use; zapier alternatives under $30 | [Softr](https://www.softr.io/blog/best-zapier-alternatives), [We Are Founders](https://www.wearefounders.uk/5-zapier-alternatives-that-cost-under-30-a-month/) |
| Alternatives | zapier alternative, make alternative, n8n alternative, cheaper than zapier, free zapier alternatives | [Lindy](https://www.lindy.ai/blog/zapier-alternatives), [Composio](https://composio.dev/content/zapier-alternatives), [Emergent: make alternatives](https://emergent.sh/learn/make-alternatives), [MonoVM: n8n alternatives](https://monovm.com/blog/n8n-alternatives) |
| Versus | zapier vs make, n8n vs make, make vs zapier vs n8n, pabbly vs zapier | [Zapier n8n-vs-make](https://zapier.com/blog/n8n-vs-make/), [n8n make-vs-zapier](https://blog.n8n.io/make-vs-zapier/), [G2 3-way compare](https://www.g2.com/compare/zapier-vs-n8n-vs-integromat-by-celonis-make), [Contabo](https://contabo.com/blog/n8n-vs-zapier-vs-make-an-in-depth-comparison/) |
| AI-answer questions | "which workflow automation tool is easiest to use", "best zapier alternative for small business", "is n8n cheaper than zapier", "what is the cheapest way to automate shopify orders" | answers synthesise the pages above (see section 3) |
| Use-case / niche | shopify orders to google sheets, gmail to google sheets, new lead to CRM, slack alerts | [Zapier Shopify→Sheets blog](https://zapier.com/blog/save-shopify-orders-google-sheet/), [Zapier template](https://zapier.com/apps/google-sheets/integrations/shopify/2758/add-new-paid-shopify-orders-to-google-sheets-rows), [Make template 3075](https://make.com/templates/3075-save-new-paid-shopify-orders-to-a-google-sheets-spreadsheet), [Make ecommerce guide](https://www.make.com/en/how-to-guides/google-sheets-automation-ecommerce) |
| Adjacent | AI agents, chatbot automation, AI workflow builder | [Lindy](https://www.lindy.ai/blog/zapier-alternatives) and [Composio](https://composio.dev/content/zapier-alternatives) both frame "AI automation tools" |

Not checked [unverified]: Gmail→Sheets and lead→CRM and Slack-alert result pages (the one search returned Shopify only).

## 2. Who wins each group, and why (from SERP evidence only)

- **Head terms:** vendor hub pages (Make `/automation-tools`) and SMB roundups (Zoho). Why: category pages from big vendors. Page internals not inspected [unverified].
- **Best/cheap/alternatives:** a mix of vendor posts (Lindy, Integrately's own blog, Softr, Composio) and affiliate/third-party roundups (Hostinger, Moosend, AppSumo, Larksuite, DEV.to, [Automation Atlas](https://automationatlas.io/answers/best-zapier-alternatives-small-business-2026/)). Pattern: titles carry the year ("2026"), list 8-16 tools, show starting prices. Summaries note most are affiliate or vendor-written; several are 2024-25 and stale, which is an opening.
- **Versus:** the *competitors themselves* win: Zapier ranks for "n8n vs make", n8n for "make vs zapier". Third-party: G2 compare, Contabo, DEV.to, digidop. Why: vendor authority plus long structured comparisons. Bias is acknowledged in the sources' own framing, so neutrality is a gap.
- **Use-case:** Zapier and Make win with templates and app-pair landing pages (many localized `/de/`, `/es/` variants) plus a long-form blog. Why: scale of programmatic pages, one page per trigger→action.
- **Third-party signals:** Reddit and YouTube matter for AI answers (see 3); not measured per query here.
- **Pricing signal:** the ranking roundups quote concrete starting prices (e.g. "$10.59/mo", "$29.99/mo", "$20/mo cloud") and a billing-model explanation (n8n counts executions, Zapier counts tasks). Pricing transparency is the common thread. [Sources: search summaries of [Softr](https://www.softr.io/blog/best-zapier-alternatives) and [Integrately blog](https://blog.integrately.com/?p=5009), unverified prices.]

## 3. What AI engines tend to cite (public studies; methods differ, treat as directional)

- ChatGPT: "best X" list pages were 43.8% of cited pages in [Ahrefs' study (750 prompts)](https://ahrefs.com/blog/best-lists-research/). Brands ranked on several lists get recommended more.
- Self-promo listicles: ~11% of citations overall, only ~4% on ChatGPT vs ~10-11% on Google AI Mode and Perplexity ([Peec](https://peec.ai/blog/self-promotional-listicles-analysis-from-232k-citations)). Ahrefs also found [a backfire risk](https://ahrefs.com/blog/self-promotional-content-ai-seo-experiment/): AI can cite your list and recommend someone else. A [Search Engine Land study](https://searchengineland.com/ai-search-loves-listicles-what-25000-urls-reveal-about-citations-477682) shows third-party lists dominating in one vertical.
- Listicle size: pages with 10-20 items are gaining, 5-8 item ones declining ([Seer](https://www.seerinteractive.com/insights/the-listicle-window-is-closing-in-ai-search-30-decline-mom)).
- Overlap with Google: only ~12% of AI-cited URLs rank in Google's top 10; Perplexity highest at ~28.6%; AI Overviews track classic rankings more ([Ahrefs](https://ahrefs.com/blog/ai-search-overlap/)).
- Source mix: YouTube leads AI Overviews on most query types ([Conductor](https://www.conductor.com/academy/how-ai-citations-differ/)); Reddit was 44% of social citations in AI Overviews in Jan 2026 ([Tinuiti via SEL](https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285)).
- On-page: HTML tables over images, visible pricing (not "contact sales"), and monthly refreshes are recommended; the "3.2x citations if updated in 30 days" figure is vendor-reported and weak. A test found major AI systems don't read JSON-LD on direct fetch, so schema helps mainly via indexing ([TripleDart](https://tripledart.com/ai-seo/schema-markup-ai-seo); [Similarweb](https://aisearch.similarweb.com/blog/aeo-for-saas-product-pages/)). Mostly self-reported evidence.
- No public answer-level data for this exact category was found. Run the 6 questions in section 1 manually in ChatGPT/Perplexity/Google weekly to build a baseline.

## 4. fansachat.com current state
Not fetchable from this session. All "exists?" values below are [unverified]. Do a quick manual check of home, /pricing, /compare/*, /integrations/*, /blog before building. (The existing [FANSACHAT_PLAYBOOK](../FANSACHAT_PLAYBOOK.md) in this repo also lists comparison and integration families as gaps and notes the same access limit.)

## 5. Prioritized page plan for fansachat.com

| # | Page type | Target query | Intent | Must contain to beat the current winner | Fix or create [unverified] |
|---|---|---|---|---|---|
| 1 | Alternatives page `/alternatives/zapier` | zapier alternative; cheaper than zapier | Commercial | 10-15 tools incl. honest "when NOT us"; HTML table (price, billing unit, free tier, ease, AI); real prices with check date; "Updated {month} 2026" and monthly refresh; sources on every competitor claim; FAQ answering the question in 2 sentences | Create (fix if /compare has one) |
| 2 | Best-for page `/best-zapier-alternative-for-small-business` | best zapier alternative for small business | Commercial, AI-answer target | Open with a one-line pick-by-situation answer (budget / non-technical / self-host); cost example for a fixed workload (e.g. 10-step flow at N runs) per tool; third-party-style neutral tone | Create |
| 3 | Versus `/compare/fansachat-vs-zapier`, `-vs-make`, `-vs-n8n` | zapier vs make-style "X vs fansachat" | Comparison | Side-by-side table, pricing math, migration steps, honest losses; winners (vendors) are biased, so neutral + dated wins | Fix existing /compare/*; create missing |
| 4 | Question hub `/guides/easiest-workflow-automation-tool` | which workflow automation tool is easiest to use | Informational, AI-answer | Ranked list with a stated test (time to first working flow) and screenshots/video; lists 10-20 tools (Seer pattern) | Create |
| 5 | Use-case pages `/templates/shopify-orders-to-google-sheets`, `gmail-to-sheets`, `lead-to-crm`, `slack-alerts` | the four niche queries | Task / how-to | Steps, template, per-run cost, troubleshooting, HowTo schema (indexing benefit only); beat Zapier/Make by being shorter and showing price | Fix /integrations/* if per-app pages exist; else create |
| 6 | Pricing `/pricing` | workflow automation pricing; zapier pricing alternative | Commercial | Visible prices, billing-unit explainer, calculator, `Offer` schema, last-updated date | Fix |
| 7 | AI/adjacent hub `/ai-agents-vs-workflows` | AI agents vs automation; chatbot automation | Informational | Definitions, decision table, examples; links down to templates | Create |
| 8 | Third-party presence (off-site) | all above | Trust | Honest answers on Reddit (r/nocode, r/automation, r/n8n, r/zapier) and a short YouTube demo; G2/Capterra listings | Create (no sign-up wall assumed: [unverified]) |

Order: 1 → 3 → 6 → 2 → 5 → 4 → 7 → 8. Rationale: buyer-intent alternatives/versus pages are where vendors currently win by default and where neutral, dated, priced content differentiates; pricing page feeds all of them.

## Next run checklist
1. Allow the three hosts; fetch fansachat.com pages and fill section 4.
2. Pull real autocomplete + PAA for ~40 seeds from section 1.
3. Record AI answers for the 6 questions (engine, date, cited URLs).
