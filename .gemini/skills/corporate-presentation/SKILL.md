---
name: corporate-presentation
description: Build, edit and export board-level, data-accurate presentations from a Qiplo dataset. Use for any request to create, restyle, extend or fix a deck, whether by prompt or by manual editing.
---

# Corporate Presentation Skill (Qiplo)

## Core principles
1. NUMBERS COME FROM CODE, NEVER FROM THE LLM. All metrics, percentages, deltas and chart
   data are computed by a deterministic analytics layer and passed to the deck as
   `dataRef` bindings. The LLM writes only titles, takeaways, and narrative, using
   placeholders like {{revenue.total}} that the renderer resolves.
2. ONE SOURCE OF TRUTH: a Deck JSON (schema below). Prompts, manual edits, preview
   and PPTX export all read/write this JSON. Nothing is edited in the PPTX file itself.
3. EVERY CHANGE IS A PATCH: prompt edits produce JSON patches (add/replace/remove/move),
   validated before applying, with undo/redo and version history.
4. ACTION TITLES: each slide title states the conclusion ("Churn rose 4.2 pts, driven by
   SMB"), not a topic ("Churn Analysis"). One message per slide.

## Deck JSON schema (minimum)
{
  "meta": {"title","audience","purpose","language","dataset_id","generated_at"},
  "theme": {"palette":[...], "fonts":{"heading","body"}, "logo","density":"standard|compact"},
  "slides": [{
    "id","layout","title","subtitle","notes",
    "blocks":[{"id","type":"text|bullets|kpi|chart|table|image|callout|shape",
               "dataRef":"metric|query id", "text":"with {{placeholders}}",
               "chart":{"kind":"bar|line|area|pie|donut|stacked|waterfall|scatter",
                        "x","y","series","format","highlight"},
               "pos":{"x","y","w","h"}, "style":{}}],
    "locked": false
  }]
}

## Standard corporate storyline (adapt to audience and purpose)
1 Title -> 2 Executive Summary (3-5 key findings + the ask) -> 3 KPI Scorecard ->
4-8 Insight slides (trend, segmentation, drivers, risk, opportunity, one idea each) ->
9 Recommendations (action, owner, impact, timeline) -> 10 Risks and Assumptions ->
11 Next Steps -> Appendix (methodology, data definitions, detailed tables).
Slide count follows the audience: board 8-12, working team 12-20, plus appendix.

## Layout library (fixed 16:9 grid, 12 columns, safe margins)
title, section-divider, exec-summary, kpi-row (3-5 cards), chart-full, chart+insight,
two-chart, chart+table, comparison, waterfall-bridge, timeline/roadmap, matrix 2x2,
recommendation-table, quote/callout, appendix-table.
Rules: max 6 bullets, max ~15 words/bullet, min body font 12pt, no overlap, no text
overflow (auto-shrink to a floor, then split into a new slide).

## Chart selection rules
- Trend over time -> line/area. Compare categories -> sorted horizontal bar.
- Part-to-whole (<=5 parts) -> donut; more -> stacked bar. Change between two points ->
  waterfall. Correlation -> scatter. Never 3D, never dual-axis unless asked.
- Always: axis titles with units, data labels on key points, highlight the insight series
  in the accent color and grey out the rest, source line "Source: <dataset>, <period>".
- Charts are NATIVE PPTX charts (editable in PowerPoint), not images.

## Visual design system
- Palette: 1 primary, 1 accent, neutrals; semantic green/amber/red for status only.
- Fonts: one heading + one body font; sizes: title 28-32, subtitle 16-18, body 14-16, footnote 10.
- White space >= 8% margins; consistent alignment; same layout = same positions everywhere.
- Footer: slide number, confidentiality label, source. Optional logo.
- Contrast ratio >= 4.5:1. Never red/green as the only signal.

## Accuracy guardrails (run before every preview and export)
- [ ] Every {{placeholder}} resolves; unresolved -> block export with a clear error
- [ ] Each number on a slide traces to a dataRef (show on hover in the editor: "from query X")
- [ ] Totals reconcile (parts sum to whole, rounding stated)
- [ ] Time periods and comparison basis are labeled (YoY, MoM, vs target)
- [ ] No claim of causation unless a driver analysis supports it; use "associated with"
- [ ] Small-sample or missing-data warnings shown in notes and the appendix
- [ ] If the data cannot support a requested slide, say so and offer the closest alternative

## Prompt-editing contract
User prompt + current Deck JSON + selected slide/block context -> LLM returns ONLY a
JSON patch list plus a one-line summary. Supported intents:
add/remove/reorder slides, rewrite tone (formal, concise, persuasive), change audience,
change chart type or metric, change theme/colors/fonts, translate, shorten to N slides,
expand a section, add appendix, "make this slide more visual".
Scope rule: if a slide or block is selected, edit ONLY that; otherwise the whole deck.
Locked slides/blocks are never modified. Show a before/after diff with Accept / Reject
and keep the previous version one click away.

## Manual editing features (must all work)
Slide panel: reorder (drag), duplicate, delete, add from layout library, lock.
Canvas: edit text inline, drag/resize blocks with snap guides, change chart type and
metric from a dropdown, edit table cells, replace images, per-block style (font size,
color, alignment, bold), alt text.
Deck: theme picker + custom brand colors/logo/fonts, undo/redo (>=50 steps), autosave,
version history with restore, speaker notes editor, comments.
Data: "refresh from dataset" re-resolves all bindings without losing manual layout edits.

## Export
- PPTX via a real library (pptxgenjs or python-pptx), native charts/tables, master
  slides, notes, 16:9. PDF export as a second format.
- Large files go to object storage with a signed URL; headers set correctly.
- Open-test: re-parse the generated PPTX and confirm slide count, no empty placeholders.

## Error handling
Return {ok:false, stage, message, fix}. Never silently drop a slide or block.
