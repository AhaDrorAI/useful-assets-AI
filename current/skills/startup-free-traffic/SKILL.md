---
name: startup-free-traffic
description: A diagnose-then-execute framework for generating free, organic traffic for early-stage startups (B2B and B2C). Use this skill whenever a user asks about getting their first users, organic growth, zero-budget or low-budget marketing, lead generation, launching a product, growing an audience, distribution strategy, GEO/AEO (visibility in AI search like ChatGPT and Perplexity), Product Hunt, build-in-public, or how to market without paid ads — even if they don't use the word "traffic". Also trigger when a user describes having built a product but having no users.
license: Complete terms in LICENSE.txt
---

# Startup Free Traffic Framework

A structured methodology for generating free, organic traffic for early-stage startups, based on the "Growth First" philosophy. The skill works in two phases: **diagnose** the startup's situation first, then **execute** on 1-2 recommended channels with concrete deliverables.

Respond in the user's language (e.g., Hebrew if they write in Hebrew), even though this skill is written in English.

## Core Philosophy: Growth First

Building an MVP is easier than ever; acquiring users is the hard part. The common mistake is burning cash on paid ads prematurely. The "Growth First" approach:

1. Secure cheap or free traffic during the early stages.
2. Build the product through daily friction with real users, not in a theoretical vacuum.
3. Establish initial traction — essential for fundraising and validation.
4. Focus beats breadth: master 1-2 channels that fit the stage and audience before adding more. Spreading across many channels at once is the most common failure mode.

## Phase 1: Diagnose

**Check for a founder profile first.** Before asking anything, look for a profile file the user may have provided — `founder-profile.md`, `about_me.md`, or equivalent — in uploaded files, project knowledge, or the working directory (also check conversation memory/context for the same facts). If one exists, read it, treat it as the diagnosis baseline, and ask only what's missing or likely stale. See `references/founder-profile-template.md` for the expected structure.

**Exception — direct tactical questions.** If the user asks a specific tactical question ("how do I get cited by ChatGPT?", "write me a Product Hunt launch plan"), answer it directly; weave in only the 1-2 diagnostic questions that would actually change the answer. Full diagnosis is for open-ended situations ("I have no users, what do I do?").

Otherwise, never recommend channels before understanding the situation. Ask the user (conversationally, not as an interrogation — skip anything already clear from context):

1. **Stage**: Pre-launch, just launched (MVP), or post-launch with some users?
2. **Audience**: B2B or B2C? Who exactly is the ideal customer, and where do they already spend time online?
3. **Founder resources**: How many hours per week can they invest in marketing? What are they naturally good at (writing, video, talking to people, coding)?
4. **Existing assets**: Any audience already (LinkedIn followers, email list, community memberships)? Any content or data that could become a lead magnet?
5. **Product dynamics**: Is there a natural sharing/collaboration mechanic (potential viral loop)? Is the problem something people actively search for?

Then recommend **1-2 primary channels** (not more) using the selection logic below, explain *why* they fit, and set honest expectations about time-to-results.

**Persist the diagnosis.** After the first full diagnosis, offer to save the answers as a `founder-profile.md` (structure in `references/founder-profile-template.md`) so future sessions start from context instead of questions. If a profile already existed but the conversation revealed changes (new stage, new learnings, a channel that worked/failed), offer to update it.

### Channel selection logic

| Situation | Lean toward |
|---|---|
| Pre-launch, any type | Pre-launch playbook (waitlist, community seeding, build-in-public) — read `references/pre-launch.md` |
| B2B, founder can write | Founder-led LinkedIn content + signal-based outreach |
| B2B, clear searchable pain point | GEO/AEO + bottom-of-funnel content — read `references/geo-aeo.md` |
| B2C, visual/demonstrable product | Short-form video |
| B2C, product with sharing mechanics | Viral loops & referrals |
| Any, founder has unique data/expertise | Lead magnet + guest posting |
| Any, audience concentrated in communities | Community engagement ("dark social") |
| Launch moment approaching | Product Hunt + directory launches |

## Phase 2: Execute

After the user agrees on channels, produce concrete deliverables — not just advice. Read the relevant reference file(s) before executing:

- **`references/channel-playbooks.md`** — Detailed playbooks for all traffic methods (lead magnets, influencers, communities, launches, LinkedIn engine, founder-led content & build-in-public, signal-based outreach, guest posting, viral loops, SEO, short-form video). Read the sections for the chosen channels.
- **`references/geo-aeo.md`** — Deep dive on Generative Engine Optimization: getting cited by ChatGPT, Perplexity, Google AI Overviews. Read whenever SEO/content/AI-visibility is chosen.
- **`references/pre-launch.md`** — The pre-launch phase: waitlist building, community seeding, directory listings, launch-week sequencing.
- **`references/deliverable-templates.md`** — Output templates: 30-day traction plan, LinkedIn content calendar, lead magnet spec, launch checklist. Use these structures when producing deliverables.
- **`references/founder-profile-template.md`** — Structure for the persistent founder profile (`founder-profile.md` / `about_me.md`). Read when creating or updating a profile.

Typical deliverables to offer: a 30-day traction plan, a content calendar with actual draft posts, a lead magnet outline, a launch checklist, cold outreach message drafts, or a GEO content brief. Ask which the user wants, or propose the most fitting one.

## Implementation Guidelines

1. **Assess the stage** and focus on 1-2 channels initially. Resist the urge to hand over all ten methods as a list.
2. **Tailor B2B vs. B2C** — the playbooks mark which methods fit which audience.
3. **Emphasize measurement**: traffic is useless without tracking. Push for conversion metrics (signups, demos, activation), not vanity metrics (impressions, likes). A useful diagnostic: "If this channel stopped tomorrow, would demand continue?" — that distinguishes building pull from renting attention.
4. **Prioritize the email list**: most free traffic methods should funnel users toward an owned audience rather than immediate purchase.
5. **Set honest expectations**: content/SEO/GEO channels take months to compound; launches produce spikes measured in days. Say so explicitly so the user doesn't quit a working channel too early.
