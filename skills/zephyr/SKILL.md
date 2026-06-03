---
name: zephyr
description: Understand the Zephyr sourdough bake tagging scheme. Use when working with Zephyr bake logs, finding which bake log corresponds to a Zephyr key, or reading Zephyr voice memo entries to extract bake events.
---

## The Zephyr Scheme

"Zephyr" is a sentinel word used to tag sourdough bake voice memos.

Each voice memo related to a bake begins with "Zephyr N", where N is the day of the month the bake started.

Example: a bake started on May 28th uses the key "Zephyr 28" for all memos across the full bake cycle.

The sentinel word "Zephyr" was chosen because it is rare in baking speech, two syllables, and phonetically distinctive — speech-to-text will not confuse it with a date, number, or common word.

## Multiple Bakes on the Same Day

When multiple bakes start on the same day, a numeric suffix after a hyphen distinguishes them.

"Zephyr 3" means the first bake on the 3rd of the current month — the -1 suffix is implied and may be omitted.

"Zephyr 3-2" means the second bake on the 3rd of the current month.

"Zephyr 5-5" said in May means the fifth bake started on May 5th.

The suffix maps directly to the trailing bake number in the bake log filename.

## Bake Log Naming Convention

Bake logs live in the Obsidian vault at `/Users/mtm/Documents/Obsidian Vault/`.

Naming pattern: `bake log M-D-YYYY-N.md`

Examples:
- `bake log 5-28-2026-1.md` — first bake started May 28, 2026
- `bake log 5-21-2026-1.md` — first bake started May 21, 2026
- `bake log 6-3-2026-2.md` — second bake started June 3, 2026

## Mapping a Zephyr Key to a Bake Log

"Zephyr 28" with current date in May 2026 → `bake log 5-28-2026-1.md`.

"Zephyr 3-2" with current date in June 2026 → `bake log 6-3-2026-2.md`.

The Zephyr day number is the day of the month the bake started. Combine with the current month and year to resolve the full date. The optional suffix is the bake number; when absent, assume 1.

## Reading Zephyr Entries

Each Zephyr entry in the bake log follows this pattern:

```
For Zephyr N, [event description] at [time] on [date].
```

The header timestamp (the H2 heading above the entry) is when the memo was recorded.

The event timestamp is the time mentioned inside the body text — this is the actual time the bake action occurred.

Always use the event timestamp, not the header timestamp, when extracting bake events.

## Writing References to Zephyr Bakes

Never write a bare Zephyr number (e.g. "Zephyr 13") into any note or table.

A bare number is ambiguous across months — "Zephyr 13" could mean June 13 or July 13 depending on when the reader encounters it.

Always resolve the Zephyr key to a bake log wikilink before writing it into a note:

- Good: `[[bake log 5-13-2026-1]]`
- Bad: `Zephyr 13`

This applies to table cells, prose references, and any other written context.

## Workflow

To work with a Zephyr bake log:

1. Identify the Zephyr key (e.g. "Zephyr 28" or "Zephyr 3-2")
2. Resolve it to a bake log filename using the day number, optional bake-number suffix, and current date
3. Read the bake log and extract all "For Zephyr N" entries
4. Use event timestamps (body text), not header timestamps (H2 headings)
5. When writing any output that references the bake, use `[[bake log M-D-YYYY-N]]` — never the bare Zephyr number
