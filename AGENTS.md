---
title: Agent conventions
date: 2026-11-19
tags: [meta]
---

# Agent conventions

Rules for every agent working in this vault (Claudian, Claude in the Claude app, Claude Code, Hermes and others). Owner: Andrius.

## Layout
- `kb/`: **the AI governance second brain.** A career-long, reliable reference for client and project work, not exam notes. Every claim traceable to an original source. No exam material here (no BoK codes, no exam tips).
  - `concepts/` ideas and definitions (e.g. explainability, model drift), `frameworks/` (NIST AI RMF, ISO/IEC 42001, OECD principles), `laws/` (EU AI Act provisions, GDPR as applied to AI), `orgs/` (bodies that issue laws, standards, guidance), `practice/` (how to do a governance task, e.g. classify a system under the AI Act, run an impact assessment; built from the other notes), `sources/` one card per source.
- `study/`: everything exam-specific: progress, course notes, quizzes, practice exams. Study notes link *to* kb notes, never the other way round. [progress.md](study/progress.md) is the source of truth for exam progress.
- `_library/`: originals (`originals/`, never edit) and reading copies (`text/`). Local only, not in git (except the EU AI Act text).
- `_agents/inbox/`: web clippings saved by the Obsidian Web Clipper. Agents process them: create or update a source card in `kb/sources/` (with the clip's URL) and distil knowledge notes; leave the clip in place.
- `_agents/drafts/`: drafts and proposals from agents awaiting Andrius's review. `_agents/templates/`: note templates.

## Answering a question from the kb (retrieval protocol)
Used when Andrius (or another agent) asks something like "which rule applies to X?".
1. Start at [kb/INDEX.md](kb/INDEX.md); match the question against note titles, `aliases`, `tags` and `applies_to`. Search note text if nothing matches.
2. Read the matching notes, then follow their **Connected** links one hop. These exist to surface what the asker may not have thought to ask.
3. Check each key claim against the original it cites (`_library/` text or official URL). Prefer `binding-law` and `official-guidance` over other authority levels; flag anything whose `as_of` date is old or whose source may have been amended.
4. Answer with: the direct answer, citations to originals (article/section level), a short **"You may also need"** list from the Connected links, and any gaps where the kb has no note yet (offer to create one).

## Reading markers (in `_library/text/` and in PDFs)
- `==text==` is Andrius's highlight. Treat highlights as signals of what matters to him.
- `> [!question]` callouts are open questions. After answering, change the callout type to `> [!question]- answered` and log the Q and a one-line answer in [reading-log.md](study/reading-log.md).
- PDF highlights come from the PDF++ plugin as links to a selection (`file.pdf#page=N&selection=...`) inside notes.
- Do not change anything else in `_library/`.

## Writing knowledge notes (kb/)
- One idea per note, filename in kebab-case, unique across the vault. Use [the template](_agents/templates/kb-note.md).
- Frontmatter:
  - `title`, `date` (created), `updated`, `tags` (YAML list), `aliases` (other names people use, for retrieval)
  - `type`: concept · framework · law · org · practice
  - `authority`: binding-law · official-guidance · voluntary-standard · industry-practice · training-material (how much weight it carries with a client or regulator)
  - `jurisdiction`: EU · US · UK · international · n/a (add others as needed)
  - `applies_to`: roles it concerns, e.g. `[provider, deployer]` (optional)
  - `as_of`: date the content was last checked against its sources
  - `sources`: list of the originals used
- Body: **In one sentence** · **Key points** (each claim cited) · **In practice** (when it applies, what an organization actually has to do or decide) · **Connected** (related rules and notes, each with one line on *why* it matters together; this is what makes the kb catch what someone forgot to ask) · **Sources**.
- Write in our own words. Quote only short phrases where the exact wording matters (legal definitions). Never paste passages from licensed sources; IAPP material may not be reproduced.
- Cite originals at the most precise level: book section, AI Act article, official URL. A claim supported only by training material is marked as such and, where possible, traced to a primary source.
- Book citation: `[Book §1.2.2](../../_library/text/ai-governance-strategy-to-execution/ch01-why-ai-needs-to-be-governed.md#1.2.2%20Opacity)`. AI Act citation: `[AI Act Art. 6(3)](../../_library/text/eu-ai-act/art-006-classification-rules-for-high-risk-ai-systems.md)`; index at `_library/text/eu-ai-act/00-index.md`.
- Links are relative markdown links (`[Title](../concepts/x.md)`), not wikilinks, so they also work on GitHub. Add each new note to its folder's `INDEX.md`.
- When a law or standard changes, update the note, bump `updated` and `as_of`, and keep a one-line history ("Before the 2025 amendment: …") rather than deleting the old position.

## Writing course notes (study/)
- Exam angles, BoK codes and quiz material go in `study/course-notes/`, which links to the kb notes it draws on.

## Study state
- Quizzes: append results to [quiz-log.md](study/quiz-log.md) (date, topic, BoK codes, score, missed points), then update [weak-spots.md](study/weak-spots.md) and the status column in [progress.md](study/progress.md).
- Practice exams: Andrius records answers in `study/practice-exams/attempt-NN.md`. Grade against the answer key in the PDF; record only question numbers, letters, domains and scores. Never copy question text or rationales into the vault.
- Status scale in progress.md: `not started` → `reading` → `understood` → `exam-ready`. Only move to `exam-ready` after a quiz score of at least 80% on that competency.

## Online course
- When discussing a course section, always connect it to its BoK competency (e.g. I.A), the matching book chapter and section (e.g. §1.2) and, where relevant, the EU AI Act articles, using [course-progress.md](study/course-progress.md) and [progress.md](study/progress.md).
- Course notes: after reading a section in the browser, write `study/course-notes/mN-<section-slug>.md` (summary in our own words, key terms, exam angle, BoK / book / AI Act links, Andrius's questions), add it to that folder's INDEX, and create or update `kb/` notes for durable ideas. Do not copy course text, and do not clip course pages: the course is IAPP material.
- At the end of a course session, update **Where I stopped** in [course-progress.md](study/course-progress.md) (lesson, exact spot, URL, date) and the lesson's status.

## Changes
- Prefer small edits over rewrites. Do not delete Andrius's notes; propose deletions in `_agents/drafts/`.
- The vault is a git repo synced to a private GitHub repository. Pull before editing when working from another machine.
