# The architecture review report

Scaffold and conventions for the HTML file written in Step 3. Read this before writing the report.

## Contents

- Constraints (read first)
- Page structure
- Scaffold
- Card structure
- Diagram patterns for before/after
- Verification

## Constraints

**No external resources.** No `<script src>`, no `<link href>` to a CDN, no webfonts, no images by URL. Everything inline. You never see this page rendered, so an external resource that fails — blocked proxy, offline laptop, an SRI hook that computes a hash against different bytes than the browser receives — leaves the user with a blank page while you report success.

**One file.** The user should be able to move it, mail it, or open it on a plane.

**System fonts only.** `ui-sans-serif, -apple-system, Segoe UI, Roboto, sans-serif` for prose and `ui-monospace, SFMono-Regular, Menlo, monospace` for paths and identifiers. Both are available everywhere and need no network.

## Page structure

1. **Header** — repo name, timestamp, scan scope, and whether exploration was parallel or sequential. The reader needs to know what was and was not looked at before they trust a ranking.
2. **Top recommendation** — first, not last. The reader who reads one thing reads this one.
3. **Candidate cards** — ordered `Strong`, then `Worth exploring`, then `Speculative`.
4. **Coverage note** — areas scanned, areas deliberately skipped, and why.

## Scaffold

Derive the palette from the strength badges outward, so colour carries meaning rather than decoration. Keep the whole page on one restrained ramp plus one accent; a review that looks like a dashboard reads as noise.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Architecture review — REPO_NAME</title>
<style>
  :root {
    --ink: #16181d; --muted: #5b6270; --line: #dfe2e8; --bg: #fbfbfc;
    --strong: #1f6f4a; --exploring: #8a6d1f; --speculative: #6b7280;
  }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 2.5rem 1.25rem; background: var(--bg); color: var(--ink);
         font: 16px/1.6 ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif; }
  main { max-width: 62rem; margin: 0 auto; }
  code, .path { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.875em; }
  .card { border: 1px solid var(--line); border-radius: 10px; background: #fff;
          padding: 1.5rem; margin: 1.25rem 0; }
  .badge { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px;
           font-size: 0.75rem; font-weight: 600; letter-spacing: 0.02em; color: #fff; }
  .badge.strong { background: var(--strong); }
  .badge.exploring { background: var(--exploring); }
  .badge.speculative { background: var(--speculative); }
  .field { margin-top: 1rem; }
  .field > h4 { margin: 0 0 0.25rem; font-size: 0.8rem; text-transform: uppercase;
                letter-spacing: 0.06em; color: var(--muted); font-weight: 600; }
  .ba { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  @media (max-width: 40rem) { .ba { grid-template-columns: 1fr; } }
  .warn { border-left: 3px solid var(--exploring); padding-left: 0.9rem; }
</style>
</head>
<body><main>
  <!-- header, top recommendation, cards, coverage note -->
</main></body>
</html>
```

## Card structure

All six fields, every card, in this order. A card missing a field is a candidate you have not finished thinking about.

```html
<article class="card">
  <h3>Deepen the Order intake module <span class="badge strong">Strong</span></h3>
  <div class="field"><h4>Files</h4> <p class="path">src/orders/intake.ts, src/orders/validate.ts</p></div>
  <div class="field"><h4>Problem</h4> <p>…friction the current shape causes…</p></div>
  <div class="field"><h4>Solution</h4> <p>…plain English, no code…</p></div>
  <div class="field"><h4>Benefits</h4> <p>…locality, leverage, which tests get simpler…</p></div>
  <div class="field"><h4>Before / After</h4>
    <div class="ba"><figure>…svg…</figure><figure>…svg…</figure></div>
  </div>
</article>
```

For a candidate that contradicts an ADR, add `<p class="warn">Contradicts ADR-0007 — worth reopening because…</p>`.

## Diagram patterns

Hand-build these. Three patterns cover nearly every candidate:

**Call fan-out** — before: one caller box with arrows to five small module boxes. After: one caller, one module, the five now inside it. Shows locality directly.

**Interface width** — draw the interface as the top edge of a box, its width proportional to how much a caller must know. Before: a wide lid on a shallow box. After: a narrow lid on a tall one. This is the clearest picture of depth there is.

**Seam** — a dashed vertical line with adapters attached. Before: no line, callers wired straight to the concrete thing. After: the line, with the concrete thing and a fake both hanging off it.

Keep them small — roughly 320×200 — with labels in the domain's own nouns. Two boxes and an arrow that a reader understands in a second beat an accurate diagram they have to decode.

## Verification

Run the check in Step 4 of SKILL.md. It should return 0. If it does not, something external crept in — usually a font link or an icon URL. Inline it or remove it, then re-check.
