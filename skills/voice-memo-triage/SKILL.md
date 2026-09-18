---
name: voice-memo-triage
description: Triage entries in an aggregate voice memo file, turn the ones that are questions into research notes, and remove those entries from the aggregate. Takes the path to the aggregate file, and either a count of newest entries or the entries one transcription run just added. Use when asked to look at the most recent N voice memos, research the ones that are questions, drain an aggregate voice memo file, or triage the memos that were just transcribed.
---

## Overview

The aggregate voice memo file collects dictated memos newest first, each under a `## <weekday>, <Month> <D>, <YYYY> at <H>:<MM> <AM|PM>` header.

Some of those memos are questions or things that need to be discovered, and those belong in their own research notes.

The rest are reminders, shopping notes, transcripts of conversations and ambient chatter, and those stay in the aggregate.

This skill takes a window of entries, splits them into those two piles, researches the first pile with a workflow, and removes exactly those entries from the aggregate.

Nothing is ever discarded — every removed entry survives verbatim inside its research note's `## Original request` section, and the removal is verified by byte accounting before the commit.

## Parameters

- aggregate — absolute path to the aggregate file to drain; default `/Users/mtm/Documents/Obsidian Vault/claude aggregate voice memos.md`
- scope — which entries to consider, either a count of the newest entries or one transcription run; default a count
- count — how many of the newest entries to consider under a count scope; default 10
- scratch directory — `$CLAUDE_JOB_DIR/tmp` when that variable is set, otherwise `mktemp -d`

Bind the parameters once, at the top of the run, and refer to them by variable everywhere after:

```sh
AGGREGATE="/Users/mtm/Documents/Obsidian Vault/claude aggregate voice memos.md"
```

```sh
VAULT="$(dirname "$AGGREGATE")"
```

```sh
SCRATCH="${CLAUDE_JOB_DIR:-$(mktemp -d)}/tmp"
```

The vault is derived rather than given, because the aggregate file sits at the vault root, and the research notes belong beside it.

Deriving it is what lets a different aggregate file be triaged into its own vault without the path being restated in eight places, so never hardcode a vault path once `AGGREGATE` is bound.

The two files whose rules the workflow agents must read are then `/Users/mtm/pdev/taylormonacelli/volcanicviper/skills/research-note/SKILL.md`, which is fixed, and `$VAULT/CLAUDE.md`, which is not.

Never write scratch files under `$VAULT`, because git tracks everything there.

## Which entries are in scope

Two things can define the window, and the wording of the request says which.

A count means the newest N entries in the aggregate, and that is the default at 10.

A run scope means the entries one transcription run just added, which is what "triage them" means when it follows a transcription in the same breath.

Never resolve a run scope into a count, because a run that added four entries and a run that added forty both read as "them", and the newest ten is wrong in each case.

### Resolving a run scope

The transcription run records where every memo went, so the set is read rather than guessed.

Take the newest run directory:

```sh
ls -dt /Users/mtm/.local/share/valorousverdin/runs/*/ | head -1
```

Then take the memos that reached the aggregate:

```sh
grep '"outcome": "leftover"' /Users/mtm/.local/share/valorousverdin/runs/2026-09-18T11-36-49/audit.jsonl
```

Each matching line carries a `heading`, and those headings are the entries in scope.

A memo whose outcome is `routed` is not in scope, because a router already filed it in the vault and it never reached the aggregate at all.

Match those headings against the aggregate's own `## ` lines rather than taking the top N, because the leftovers are prepended and any other writer that prepends in between shifts the window without saying so.

A heading the audit names that no longer appears in the aggregate was triaged already, so drop it from the set and say so rather than failing.

A run whose audit has no `leftover` lines routed everything, so there is nothing to triage and the reply is one line.

## Step 1: Back up and index

Copy `$AGGREGATE` to the scratch directory as `aggregate.orig.md`.

```sh
cp "$AGGREGATE" "$SCRATCH/aggregate.orig.md"
```

That copy is the reference for the byte accounting in Step 6, so take it before anything is edited.

Index every entry:

```sh
grep -n '^## ' "$AGGREGATE"
```

Entry K spans from its own header line through the line before the next header line, so the entry after the last one in scope is what gives that one an end boundary.

Under a count scope the window is the first N of those headings.

Under a run scope it is the headings the audit named, wherever in the list they turn up.

## Step 2: Read the window

Read every entry in scope in full before deciding anything about any of them.

A memo can open as chatter and close on a question, so a header-only skim misclassifies.

## Step 3: Classify

An entry becomes a research note when it asks something, wonders whether a thing is possible, proposes an approach and asks whether it would work, or names something that has to be found or identified before it can be acted on.

An entry stays in the aggregate when it is a reminder to do a thing, a transcript of a conversation, a list of what is in the refrigerator, or an observation with nothing to look up.

Judgment calls that fall between the two are batched and asked in a single round at the end, never one at a time mid-run.

State the classification of every entry in scope to the user in one block before running the workflow, so a misread is caught before notes get written.

## Step 4: Extract the research entries verbatim

Write each research entry to its own file in the scratch directory using the line ranges from Step 1:

```sh
sed -n '4,33p' "$AGGREGATE" > "$SCRATCH/entries/01-notebooklm.md"
```

Confirm each extracted file starts with its `## ` header line, so an off-by-one in the ranges is caught here rather than after the aggregate has been edited.

These files are what the workflow agents read, and they are also what the byte accounting in Step 6 sums.

## Step 5: Research with a workflow

Run one Workflow with a two-stage pipeline over the research entries, one item per entry.

The first stage researches and writes the note.

The second stage audits the written note against the format rules and repairs it in place.

Give every agent in the first stage the shared preamble telling it to read `/Users/mtm/pdev/taylormonacelli/volcanicviper/skills/research-note/SKILL.md` and `$VAULT/CLAUDE.md`, then follow them, with these deviations:

- The source is a section of an aggregate file, not a standalone file, so Step 3 of that skill does not apply — create a new file directly under `$VAULT` rather than renaming a source
- The agent runs no `git add` and no `git commit`, because the orchestrator commits centrally and background writers share the vault repo
- The agent never touches `$AGGREGATE`
- The `## Original request` section carries the memo byte for byte, emphasis included, which overrides the vault's no-emphasis rule for that one section
- The only edit permitted inside that verbatim block is demoting the memo's own `## ` lines to `### `, so they do not read as siblings of the note's own sections

Interpolate the resolved absolute paths into those prompts rather than writing the variable names into them, because a subagent gets a fresh shell that never saw `AGGREGATE`, `VAULT` or `SCRATCH`, and an unexpanded `$VAULT` reaches it as literal text it cannot resolve.

In a workflow script that means binding them as script constants at the top and building each prompt with template interpolation.

Give each agent a paragraph of research direction specific to its memo, naming the concrete things to look into, rather than handing it the raw memo and hoping.

Have the first stage return the note path, the cleaned question, and the section headers, as a schema-validated object.

Have the second stage check and fix: frontmatter, no emphasis outside the verbatim block, the verbatim block matching the extracted entry file, one sentence per paragraph, markdown search links at the bottom of each section rather than one collected block, bare non-search URLs on their own lines, squashed number and unit notation, absolute paths, a single trailing newline, and every non-search URL returning a live status code.

## Step 6: Remove the researched entries and verify nothing was lost

Delete the researched line ranges in one pass, addressing original line numbers:

```sh
sed -e '4,33d' -e '282,333d' "$SCRATCH/aggregate.orig.md" > "$SCRATCH/aggregate.new.md"
```

Use `-e '<start>,<end>d'` per removed entry, and note that ranges are read against the original numbering, so they do not need adjusting for earlier deletions.

Then verify the byte accounting:

```sh
wc -c "$SCRATCH/aggregate.orig.md" "$SCRATCH/aggregate.new.md" "$SCRATCH/entries/"*.md
```

The new file plus the extracted entry files must sum to exactly the original.

A mismatch means a range was wrong, and the aggregate must not be replaced until the sum balances.

Then confirm each entry's text reached its note, checking the extracted file against the note's `## Original request` section rather than trusting the agent's report.

Only after both checks pass, install the new file:

```sh
cp "$SCRATCH/aggregate.new.md" "$AGGREGATE"
```

## Step 7: Commit

Commit each new research note individually, then the aggregate edit, each with its own pathspec, from `$VAULT`:

```sh
git commit -- "note name.md"
```

The pathspec is required because background processes commit to this repo concurrently, so a bare `git commit -a` sweeps up work that is not yours.

Do not prompt before committing.

## Step 8: Report

Say which entries became notes, naming each note file, and which entries stayed in the aggregate and why.

Give the byte accounting result as the evidence that nothing was lost.

Name the scope that was used, because "the newest 10" and "the 4 this run added" leave different memos unexamined, and only the person who asked can tell whether the remainder matters.
