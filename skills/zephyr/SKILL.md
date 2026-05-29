---
name: zephyr
description: Understand the Zephyr sourdough bake tagging scheme. Use when working with Zephyr bake logs, finding which bake log corresponds to a Zephyr key, or reading Zephyr voice memo entries to extract bake events.
---

## The Zephyr Scheme

"Zephyr" is a sentinel word used to tag sourdough bake voice memos.

Each voice memo related to a bake begins with "Zephyr N", where N is the day of the month the bake started.

Example: a bake started on May 28th uses the key "Zephyr 28" for all memos across the full bake cycle.

The sentinel word "Zephyr" was chosen because it is rare in baking speech, two syllables, and phonetically distinctive — speech-to-text will not confuse it with a date, number, or common word.

## Bake Log Naming Convention

Bake logs live in the Obsidian vault at `/Users/mtm/Documents/Obsidian Vault/`.

Naming pattern: `bake log M-D-YYYY-N.md`

Examples:
- `bake log 5-28-2026-1.md` — first bake started May 28, 2026
- `bake log 5-21-2026-1.md` — first bake started May 21, 2026

## Mapping a Zephyr Key to a Bake Log

"Zephyr 28" with current date in May 2026 → `bake log 5-28-2026-1.md`.

The Zephyr day number is the day of the month the bake started. Combine with the current month and year to resolve the full date.

## Reading Zephyr Entries

Each Zephyr entry in the bake log follows this pattern:

```
For Zephyr N, [event description] at [time] on [date].
```

The header timestamp (the H2 heading above the entry) is when the memo was recorded.

The event timestamp is the time mentioned inside the body text — this is the actual time the bake action occurred.

Always use the event timestamp, not the header timestamp, when extracting bake events.

## Workflow

To work with a Zephyr bake log:

1. Identify the Zephyr key (e.g. "Zephyr 28")
2. Resolve it to a bake log filename using the day number and current date
3. Read the bake log and extract all "For Zephyr N" entries
4. Use event timestamps (body text), not header timestamps (H2 headings)
