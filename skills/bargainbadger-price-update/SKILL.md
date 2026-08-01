---
name: bargainbadger-price-update
description: Turn one minimoths crawl session into a dated prices table appended to a product note in the Obsidian vault. Use when asked to update a product note with today's prices, add a prices section, or find the best price for a product after running a search.
---

## Overview

A crawl captures one product term across every store in one session.

This skill turns that session into a dated prices table in the product's vault note.

The product is a parameter.

Nothing here is specific to half and half, celery, or any other term — the same steps run for whatever the session searched.

## What this skill owns, and what it does not

This skill owns mechanics: where the database is, how to run the tooling, how to find the session, how to find the note, and how to get the rows out without blowing up the context.

It does not own meaning.

The schema, the field definitions, the unit-price arithmetic, the extraction rules, the edge cases, and the open questions all live in the vault and are actively being revised.

Those are moving targets, so this skill does not copy them.

It points at them and requires that they be read fresh on every run.

Never answer a schema or arithmetic question from this file, from memory, or from a previous conversation.

## Step 1 — Load the specification

Read the hub note first, before touching the database:

```
/Users/mtm/Documents/Obsidian Vault/bargainbadger.md
```

The hub carries a Contents section listing the notes that hold the rest of the specification.

Read every note that section links to.

Resolve each wikilink by joining the vault path and the link text with a `.md` suffix, so `[[bargainbadger computation rules]]` becomes `/Users/mtm/Documents/Obsidian Vault/bargainbadger computation rules.md`.

Follow the second-order links too when a note the hub links to points at another note for a definition it does not itself carry.

The Contents list is deliberately not reproduced in this skill, because notes get added, split, and renamed there.

Read what the hub lists today rather than what it listed when this skill was written.

Together those notes govern the schema, the field distinctions, the computation, the escalation triggers, the edge cases, and the change log.

When the specification and this skill appear to disagree about anything other than a path or a command, the specification wins.

## Parameters

- vault — `/Users/mtm/Documents/Obsidian Vault`
- hub note — `/Users/mtm/Documents/Obsidian Vault/bargainbadger.md`
- database — `/Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db`
- minimoths project — `/Users/mtm/pdev/taylormonacelli/minimoths`
- product term — supplied by the user, or derived from the session in Step 2
- session — the most recent crawl unless the user names an older one
- scratch directory — any path outside the vault, never inside it

## Trigger

Run this skill only when asked to update a note with prices.

Requests that trigger it:

- "I just searched for shallots, update the shallots note with today's prices"
- "Add a prices section to the leeks note"
- "What is the best price for cultured butter right now"

Requests that do NOT trigger it:

- Sampling the database to develop the schema, which is specification work
- Adding a change log entry
- Any request that does not end in a table written to a product note

## Step 2 — Resolve the session

List the sessions, newest first:

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/minimoths --directory /Users/mtm/pdev/taylormonacelli/minimoths minimoths sessions
```

The `--directory` flag is not optional.

`MINIMOTHS_DB_PATH` defaults to the bare relative name `minimoths.db`, so the CLI resolves its database against the working directory and dies with `no such table: products` when run from anywhere else.

The columns are index, `run_id`, label, record count, and site count.

The label is derived by an Anthropic API call, so it fails with a 401 warning when no key is exported and falls back to the most common search term.

That warning is not fatal and the row is still usable.

The key lives in the macOS Keychain rather than the environment:

```
security find-generic-password -s ANTHROPIC_API_KEY -w
```

Never trust the label as the product identity.

Confirm what was actually searched by reading the search pages the cards came from:

```
sqlite3 /Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db "SELECT DISTINCT parentPageUrl FROM products WHERE run_id = '<run_id>' LIMIT 10"
```

The search term appears verbatim in the query string of those URLs, which is the authoritative record of what the crawl asked for.

Default to the newest session when the user says "I just now searched".

Older captures predate `run_id` and carry `batch_label` instead, so look there when no session matches the product:

```
sqlite3 /Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db "SELECT batch_label, COUNT(*) FROM products WHERE run_id IS NULL GROUP BY batch_label"
```

Stop and ask when the newest session's search term does not match the product the user named.

## Step 3 — Resolve the target note

The note is the vault file whose name is the product term, all lowercase, spaces between words.

Confirm it exists before extracting anything, because a missing note changes the whole job:

```
ls /Users/mtm/Documents/Obsidian\ Vault | grep -i '<term>'
```

Singular and plural notes often both exist, and only one carries the `product` tag and the prices tables.

Use the [[islandiguana]] skill to pick the one tagged `product` when more than one candidate matches.

Ask the user which note to write to when the tag does not settle it.

Never create a new product note as a side effect of a price update.

## Step 4 — Pull the rows

Query the database directly, selecting text and never html:

```
sqlite3 -json /Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db "SELECT id, site, productUrl, text FROM products WHERE run_id = '<run_id>'"
```

Do not use `minimoths search --run-id` for this step.

That command has no flag to suppress `html`, so it returns the product-card markup for every row.

Measured on the 656-row 2026-08-01 half and half session, its output is 5.48 MB against 310 KB for the same rows selected as `text`, a factor of 17.

The large form does not fit a context window, and paying it up front defeats the two-tier extraction rule the specification sets out.

## Step 5 — Filter to the product

A session is a search results page, not a product list, so much of what it captured is not the product.

Narrow in SQL first, then by reading:

```
sqlite3 -json /Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db "SELECT id, site, productUrl, text FROM products WHERE run_id = '<run_id>' AND lower(text) LIKE '%<keyword>%'"
```

Derive the keyword from the search term in `parentPageUrl`, not from the note name.

Check the keyword before trusting it, because a product name can be a common modifier.

Searching the 2026-08-01 half and half session for "half" returned half-gallon milk, half-pint mason jars, and a smoked half duck; matching "half and half" and "half & half" instead cut 339 rows to 288.

Report the counts every time: rows captured, rows kept, rows dropped.

Never silently drop rows without saying how many.

## Step 6 — Extract

Extraction is the only step done by judgment, and it stops at the key-value pairs the specification defines.

Work in batches of roughly 75 rows so a mistake in one batch does not cost the whole session.

Emit one record per row into a JSON file in the scratch directory, never into the vault.

Escalate to html for a single row only when its text cannot answer, using the escalation triggers from the specification:

```
sqlite3 /Users/mtm/pdev/taylormonacelli/minimoths/minimoths.db "SELECT html FROM products WHERE id = <id>"
```

The specification decides what to do with a listing that states no price, no size, several price tiers, a price range, or a sale price.

Do not invent a rule for those cases here.

## Step 7 — Compute

All arithmetic is deterministic and belongs in code, so write a short Python script and run it with uv.

Never compute a unit price by hand while writing the table.

The formulas, the unit categories, the conversions, and the printed-unit-price checksum all come from the specification.

## Step 8 — Render the table

Sort cheapest first.

Link the product name to its `productUrl`, take the store from `site`, and date the rows from the session's capture date.

The specification decides which columns the table can carry, because that follows from the unit category.

When the specification does not settle a formatting question, match the most recent prices table already in the note, and say which choice was inherited that way.

An inherited choice is a gap in the specification, so report it rather than quietly adopting it.

## Step 9 — Insert the section

The new section goes immediately above the first existing `## prices` heading, so the note reads newest first.

Append at the end only when the note has no prices section yet.

Never edit, merge, or delete an older prices section — each one is a dated observation and they stack.

Leave the note's front matter, store checklists, and images untouched.

## Step 10 — Commit

Commit the note with a message naming the product and the session date.

Delete the scratch JSON, since the vault tracks everything and stray files get auto-committed.

## Known failure modes

- The database is ephemeral and is periodically wiped, so a session listed yesterday may be gone today.
- The label degrades to the most common search term when no API key is exported.
- The same listing repeats across Instacart-backed stores under different retailer slugs, and within one session under duplicate `productUrl` values.
- A product term that is also a size word matches listings that have nothing to do with the product.

## Non-goals

- Deciding schema questions, which belong in the vault notes and their change log.
- Updating the store boolean fields in the note front matter.
- Deciding which product to buy.
- Running the crawl — the user runs the search before invoking this skill.
