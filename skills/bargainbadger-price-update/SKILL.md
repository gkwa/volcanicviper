---
name: bargainbadger-price-update
description: Turn one minimoths crawl session into a dated prices table appended to a product note in the Obsidian vault. Use when asked to update a product note with today's prices, add a prices section, or find the best price for a product after running a search.
---

## What this does

A crawl captures one product term across every store in one session.

This skill turns that session into a dated prices table in the product's vault note.

The product is a parameter, so the same steps run for whatever the session searched.

## Read the specification first

Everything factual — the database location, the schema, the field definitions, the sampling queries, the extraction rules, the arithmetic, and the edge cases — lives in the vault.

Read the hub note before touching anything:

```
/Users/mtm/Documents/Obsidian Vault/bargainbadger.md
```

Then read every note its Contents section links to, and follow second-order links where one of those notes defers to another for a definition.

Resolve a wikilink by joining the vault path and the link text with a `.md` suffix.

The Contents list is deliberately not reproduced here, because notes get added, split, and renamed there.

Read what the hub lists today, not what it listed when this skill was written.

This file is a workflow, not a reference.

It states no facts about the data, the database, or the schema, and it must not acquire any.

When something needed is missing from the vault, add it to the vault rather than to this file.

## Trigger

Run this only when asked to write prices into a product note.

Requests that trigger it:

- "I just now did a search for shallots, can you update our shallots markdown file to add a new section for prices based off today"
- "Add a prices section to the leeks note"
- "What is the best price for cultured butter right now"

Requests that do NOT trigger it:

- Sampling the database to develop the schema, which is specification work
- Adding a change log entry
- Anything that does not end in a table written to a product note

## The workflow

1. Read the specification, as above.
2. Identify the session, and confirm what it actually searched before trusting any label attached to it.
3. Resolve the product note in the vault, and never create one as a side effect.
4. Pull the session's rows and narrow them to the product, reporting how many were captured, kept, and dropped.
5. Extract the schema's fields from those rows, in batches, into a scratch file outside the vault.
6. Compute every derived price in code, never by hand.
7. Render the table and insert it above the newest existing prices section, leaving older sections untouched.
8. Commit the note, and delete the scratch file.

Each step's rules come from the specification.

Where the specification is silent, match what the note already does, and report the choice as a gap rather than adopting it quietly.

## Non-goals

- Deciding schema questions, which belong in the vault notes and their change log.
- Updating the store boolean fields in the note front matter.
- Deciding which product to buy.
- Running the crawl, which the user does before invoking this skill.
