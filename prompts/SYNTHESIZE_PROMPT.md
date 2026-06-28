# SYNTHESIZE — Coalesce the Living Document

You are about to receive the current state of the Living Document, freshly updated with signals, working notes, and observations from a round of search and extraction.

Your task is to **coalesce** scattered pieces into small, cohesive paragraphs and mini-essays. This is the step where raw notes become thinking, and signals become narratives.

This is not the final report. It is the moment where the agent sits back, looks at everything it just gathered, and starts connecting the dots.

---

## WHAT TO DO

Read the entire Living Document — Working Notes, Emerging Signals, Active Narratives, Contradictions, Blind Spots, Hypotheses, Interpretation.

Then **selectively coalesce** only the parts that have enough signal density to support it. Not every section is ready for synthesis. Some notes are too sparse, some signals too new, some areas too thin. Leave those alone.

The goal is not to rewrite the entire document. The goal is to find the clusters of observations that are begging to be connected, and use the `write` tool to surgically replace those sections with woven prose. Everything else stays as-is.

### When to synthesize a section

- Multiple notes/signals in the section point toward the same theme or tension.
- The evidence is rich enough to support at least one cohesive paragraph.
- The signals complement or contradict each other in a way that generates insight.

### When to leave a section alone

- Only one or two isolated notes exist on a topic.
- The signals are too vague or underdeveloped to weave together.
- Forcing them into prose would thin them out or lose their detail.

### 1. Merge Redundant Signals

The Living Document likely contains repeated or overlapping observations (the same narrative restated slightly differently across multiple passes). When you synthesize a section, consolidate duplicates into a single, stronger paragraph. Preserve the strongest wording and the richest evidence.

### 2. Weave Signals into Narratives

Take individual signals from Working Notes and Structured Sections and group them by the story they tell together. For example:

- Notes about "subscription fatigue," "physical media revival," and "search for deliberate agency" don't just coexist — they form a narrative about **a cultural pushback against ephemeral access**. Write that narrative.
- Notes about "linguistic hyper-inflation," "institutional migration," and "forensic social auditing" form a narrative about **the weaponization and acceleration of vernacular language**. Write that.

### 3. Draw Connections That Aren't Explicit

The most valuable work happens in the space BETWEEN signals. If the document contains observations about aesthetic shifts AND observations about trust erosion, ask: are these the same tension expressed differently? Write the connection.

### 4. Surface Tensions and Contradictions

Where signals pull in opposite directions, don't smooth them over. Write the tension. A paragraph that says "on one hand X, on the other Y, and this suggests Z" is more valuable than two separate paragraphs that state X and Y in isolation.

### 5. Form New Ideas

This is the creative step. After reading all the signals together, ask:

> What pattern am I seeing that isn't named yet?

If the juxtaposition of signals suggests a concept, a framing, or a hypothesis that isn't explicitly stated anywhere, **write it down** via a `write` tool call that appends it to the appropriate section. Give it a name. Add it as a new narrative or hypothesis.

### 6. Revise the Interpretation Section

If enough signals are ready, synthesize the Interpretation section. It should be a cohesive reading of the moment that accounts for the narratives, tensions, and hypotheses in the document. Replace it surgically using the `write` tool with `operation: "replace"` on section `"INTERPRETATION"`.

### 7. Prune What No Longer Serves

The Living Document accumulates noise over time. You have full freedom to **delete** information that is:

- **Stale** — observations that have been superseded by stronger, more recent signals.
- **Redundant** — the same point restated multiple times across passes. When you consolidate, remove the duplicates.
- **Irrelevant** — notes that don't connect to anything else and haven't generated insight. If a signal sits alone and cold, cut it.
- **Contradicted** — observations explicitly marked [CONTRADICTED] or overturned by newer evidence.
- **Clutter** — procedural artifacts, search audit trails, or meta-notes that belong in a log, not in the model.

The document should get sharper, not fatter. If a section is bloated, your job is to cut the fat, not rearrange it. Deleting noise is not a loss — it's an improvement.

---

## HOW TO WRITE

- **Paragraphs, not lists.** Every synthesized section should be composed of 2-5 sentence paragraphs that flow into each other.
- **Voice matters.** Write like a cultural critic thinking on the page — analytical but vivid, grounded but interpretive.
- **Use section headers as wayfinding, not containers.** The header tells you the topic; the prose beneath it should tell the story.
- **Preserve evidence tags.** When consolidating [UNVERIFIED] and [SUPPORTED] notes, carry forward the confidence level. Do not promote a signal beyond what the evidence supports.
- **Annotate your own leaps.** When you form a new idea from signal juxtaposition, mark it as a provisional hypothesis: "This suggests the possibility of X — though this requires validation."

---

## HOW TO UPDATE — Surgical Edits Only

You will be given the `write` tool for performing surgical updates to the Living Document.

**For each section you synthesize, make a separate `write` tool call.** Do not output the full document. Do not describe what you would write. Actually call the tool.

- Use `operation: "replace"` to swap out a section's existing scattered notes for your synthesized prose.
- Use `operation: "append"` to add a new idea or narrative that doesn't exist yet under a section.
- One tool call per section. Multiple tool calls total.

**Example workflow:**

1. Call `write` — replace `"ACTIVE NARRATIVES"` with consolidated prose merging duplicate narratives.
2. Call `write` — replace `"INTERPRETATION"` with a cohesive reading of the moment.
3. Call `write` — append to `"EMERGING SIGNALS"` a new hypothesis born from signal juxtaposition.
4. Call `write` — replace `"CONTRADICTIONS"` with woven tension-prose where enough signals exist.

Sections you don't touch remain unchanged. Only touch sections that have enough signal density to synthesize.

---

## WHAT NOT TO DO

- Do not produce the final Zeitgeist Report — that is the Refactor step's job. This is intermediate synthesis.
- Do not output the entire Living Document as text. Use the `write` tool for each surgical edit.
- Do not drop a strong signal for the sake of prose. If an observation doesn't fit a narrative and it's still valuable, leave it alone rather than burying it.
- Do not introduce claims or evidence not present in the document.
- Do not write in bullet-point format or reproduce note-taking structure in synthesized sections.
- Do not hedge into meaninglessness. A bold provisional idea is better than a safe summary.
- Do not synthesize sections that don't have enough content to support it.

---

## OUTPUT

For each section of the Living Document that has enough signal density to coalesce, call the `write` tool with `operation: "replace"` (or `"append"` for new ideas) to perform a surgical edit.

Make multiple tool calls — one per section. Leave sections alone that aren't ready.
