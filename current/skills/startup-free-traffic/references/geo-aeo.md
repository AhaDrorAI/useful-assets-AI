# Generative Engine Optimization (GEO / AEO)

Getting the startup cited in AI-generated answers — ChatGPT, Perplexity, Claude, Google AI Overviews, Gemini, Copilot. Read this whenever content, SEO, or AI-search visibility is a chosen channel.

## Why this matters now

- A growing share of product discovery happens by asking an AI assistant instead of Googling. The goal shifts from *ranking* on a results page to *being cited* in an answer.
- The overlap between top Google results and AI-cited sources has collapsed (industry research puts it below 20%, down from ~70%) — meaning a new site can win AI citations even without winning Google rankings, and vice versa.
- Citation behavior varies enormously by engine: Perplexity cites sources in nearly all responses, Google AI Overviews in roughly a third, ChatGPT in a small minority. Diversify rather than optimizing for one engine.
- This is a rare early-stage advantage: incumbents optimized for old SEO; the AI-citation game is still open in most niches.

## How AI search actually works: query fan-out

When someone asks an AI a complex question ("What's the best email tool for a small e-commerce shop under 10K subscribers?"), the AI does not search that sentence. It breaks it into several shorter sub-queries ("best email marketing platforms 2026", "email marketing e-commerce features", "email marketing pricing small business") and searches each separately, then synthesizes.

**Implication:** content must rank for the *fragments*, not just the long question. When planning content, list the likely fan-out sub-queries for each target question and make sure each is directly answered somewhere on the site.

## The GEO playbook

### 1. Make sure AI can read the site (most common failure)
- Check `robots.txt` — many sites block AI crawlers without knowing it. Cloudflare changed defaults to block AI bots; if the site uses Cloudflare, verify AI bot access explicitly.
- Check server logs for AI user agents (e.g., "ChatGPT-User") to confirm AI bots actually visit.
- Prefer server-rendered or static content; heavy client-side rendering can be invisible to crawlers.

### 2. Structure content for extraction
Research (Princeton, KDD 2024) found specific techniques lift AI citation rates by up to ~40%. The biggest gains:
- **Quotations** from named experts (+~41%)
- **Statistics** with specific numbers (+~32%)
- **Inline citations** to credible sources (+~30%)

Practical formatting:
- Clear headings, short paragraphs, direct answers in the first sentence of each section.
- FAQ-style question→answer blocks matching how people phrase questions to AI.
- Quotable, specific claims ("cuts grading time from 40 minutes to 6") rather than vague ones ("saves time").
- Schema markup / structured data so engines resolve the brand as a consistent entity.

### 3. Write bottom-of-funnel comparison content
The content type AI engines cite most readily for product questions: listicle-style comparison pages ("Top X tools for Y", "A vs B for [use case]"). They give LLMs a pre-packaged "marketplace of answers." For a startup:
- Publish honest comparison pages that include competitors — being the *source* of the comparison is how you get cited in the answer.
- Target 10-20 such pages around the exact buying questions of the ICP before writing top-of-funnel volume.

### 4. Build authority beyond the site
AI engines heavily favor a relatively small set of trusted sources. Mentions and citations in those sources matter more than backlink counts:
- Guest posts and PR in publications the engines trust (see channel-playbooks.md §8).
- Presence in directories, review sites, and "best of" lists that engines already cite in the niche — search the target question in Perplexity/ChatGPT, see which sources get cited, and get listed *there*.
- Consistent entity information everywhere (same product description, category language, founder names).

### 5. Keep content fresh
AI engines show strong recency bias. Update key pages at least every ~3 months (refresh statistics, dates, examples) — stale content quietly drops out of citations.

### 6. Measure it
- Free/manual: periodically ask the main engines the ICP's buying questions and record whether/how the brand appears.
- Budget tools exist for citation monitoring (entry tier around tens of dollars/month) — recommend only when manual checking becomes limiting.
- Track AI referral traffic in analytics (referrers like chatgpt.com, perplexity.ai).

## A grounding caveat

Google's official position is that optimizing for its AI features is still just good SEO — it recommends ignoring "GEO hacks" like special AI text files or chunked content, at least for Google surfaces. The honest synthesis: solid SEO fundamentals remain the base layer; the extraction-friendly structure, citation-worthy specifics, fan-out coverage, and off-site authority described above are the incremental GEO layer. Avoid vendors selling GEO magic tricks.
