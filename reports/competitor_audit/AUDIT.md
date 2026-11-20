# Competitor audit — BLOCKED (no scores given)

Run date: 2026-11-20. Branch: research/competitor-audit-2026-11-21.

## Result
The audit could not be done. This session's network proxy refuses every target site, so no robots.txt, sitemap, page, schema or llms.txt could be read.
I did not invent scores. A scorecard without data would be fiction.

## What was tried
| Check | Result |
|---|---|
| curl robots.txt on zapier.com, make.com, n8n.io, pabbly.com, ifttt.com, activepieces.com, lindy.ai, gumloop.com, fansachat.com | All refused (proxy 403 / no connection) |
| Wikipedia, google.com | Refused |
| WebFetch zapier.com/robots.txt | Host does not resolve in this session |
| PageSpeed Insights API (www.googleapis.com, no key) | Reachable, but HTTP 429: shared daily quota exhausted |
| WebSearch (standard) | Works. Gives SERP-level evidence only (below) |

## What search results do show (SERP level only)
- "zapier alternative": top results are vendor blogs and affiliates: Jotform, Hostinger, ClickUp, Softr, Lark, Moosend, and n8n's own post. https://www.jotform.com/blog/best-zapier-alternatives/ , https://www.hostinger.com/tutorials/zapier-alternatives , https://clickup.com/en-US/blog/114187/zapier-alternatives , https://blog.n8n.io/free-zapier-alternatives/
- Tools named most often in those lists: n8n, Make, Pabbly Connect, ActivePieces. Same sources, plus snippet summary.
- "best workflow automation tool 2026": Zapier's own blog ranks at the top. https://zapier.com/blog/best-workflow-automation-tools/ . Also Relay.app, Storydoc, Airtable, Fiverr guides. https://www.relay.app/blog/best-workflow-automation-tools
- "easiest automation tool for beginners": Zapier (https://zapier.com/blog/best-automation-software/) and IFTTT (https://ifttt.com/explore/no-code-automation) have pages in the results. Third-party pages name Zapier, Make and Albato. https://albato.com/blog/publications/most-user-friendly-automation-software
- "fansachat.com": the site itself did not appear. Results were unrelated FanChat/Fachat apps. https://theresanaiforthat.com/ai/fanchat . This hints at weak entity clarity, but it is one search only and not proof.

## Pattern worth acting on (from SERPs, low confidence)
Competitors win these queries two ways: their own "best X / X alternatives" blog pages, and third-party roundups that list them. A site that has neither is not in the answer set.

## To unblock
Allow these hosts in the environment network settings, then re-run: zapier.com, www.make.com, n8n.io, blog.n8n.io, pabbly.com, ifttt.com, activepieces.com, lindy.ai, gumloop.com, fansachat.com, en.wikipedia.org, www.reddit.com, www.g2.com, www.capterra.com. PageSpeed needs a different day or key (a key is not allowed under the free-only rule).
