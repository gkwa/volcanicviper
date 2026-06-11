---
name: zephyr
description: Understand the Zephyr sourdough bake tagging scheme. Use when working with Zephyr bake logs, finding which bake log corresponds to a Zephyr key, reading Zephyr voice memo entries to extract bake events, or routing Zephyr entries from any document to their bake logs.
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

## Parameters

The skill accepts named parameters with defaults, like Python keyword arguments.

Resolution precedence, highest first:

1. An explicit value stated in the invocation or request
2. Machine-local configuration
3. The built-in default

Parameters:

- bake log directory — built-in default `/Users/mtm/Documents/Obsidian Vault/`; machine-local override via the `ZEPHYR_BAKE_LOG_DIR` environment variable; invocation override by naming a directory in the request
- mode — routing only; `move` or `copy`; default `move`; see ROUTING.md
- trigger — routing only; on-request by default; see ROUTING.md

Check `ZEPHYR_BAKE_LOG_DIR` with Bash at call time; fall back to the built-in default only when it is unset.

Never assume the current working directory is the bake log directory.

## Bake Log Naming Convention

This section is the single owner of bake log filename resolution.

All other components, including routing, resolve filenames through these rules rather than restating them.

Bake logs live in the bake log directory (see Parameters).

Naming pattern: `bake log M-D-YYYY-N.md`

N is the bake number for that day, starting at 1.

The suffix is not always `-1`: a second bake started the same day is `-2`, a third is `-3`, and so on.

N maps directly to the Zephyr key suffix — "Zephyr 3-2" resolves to bake number 2.

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

## Weight Notation

Voice memos are transcribed by speech-to-text, which spells out units as words or leaves a space between the number and the unit abbreviation.

When writing or editing Zephyr entries, normalize all weight values to compact form:

- No space between number and unit
- Use `g` not `grams`
- Use `mL` not `milliliters` or `ml`

Examples:

- "18 grams" → `18g`
- "562 grams" → `562g`
- "20 g" → `20g`
- "2190 milliliters" → `2190mL`

This applies to all weights and volumes anywhere in the entry body — ingredient amounts, dough weights, container tares, and measurements.

## Writing References to Zephyr Bakes

Never write a bare Zephyr number (e.g. "Zephyr 13") into any note or table.

A bare number is ambiguous across months — "Zephyr 13" could mean June 13 or July 13 depending on when the reader encounters it.

Always resolve the Zephyr key to a bake log wikilink before writing it into a note:

- Good: `[[bake log 5-13-2026-1]]`
- Bad: `Zephyr 13`

This applies to table cells, prose references, and any other written context.

## event_time Tags

Each Zephyr entry that records a specific bake action gets an inline event_time tag on its own line after the body text:

```
`event_time: YYYY-MM-DDTHH:MM:00`
```

Actions that get event_time:
- Feeding the starter
- Starter peaked
- Removing starter from bowl
- Mixing water with starter
- Adding tangzhong to dough
- Bulk ferment start (flour added)
- Adding salt / dimpling salt
- Stretch and fold sets
- Lamination folds
- Preshape
- Shape
- Cold retard start
- Bake start / bake done
- Inserting temperature probes

Entries that do NOT get event_time:
- General notes, reminders, or lessons learned
- Pure measurements or weight observations with no action
- Speculative or retrospective commentary

Time resolution:
- Use the time stated in the entry body when one is given
- Fall back to the header timestamp only when the body states no time
- Convert to ISO 8601: `YYYY-MM-DDTHH:MM:00`

Example entry with tag:

```
## Friday, June 5, 2026 at 9:57 AM

For Zephyr 4-2, the starter peaked at 9:57 AM on June 5th.

`event_time: 2026-06-05T09:57:00`
```

Example entry without tag (measurement only):

```
## Friday, June 5, 2026 at 10:59 AM

For Zephyr 4-2, the initial dough volume is 2100 ml.
```

## Workflow

To work with a Zephyr bake log:

1. Identify the Zephyr key (e.g. "Zephyr 28" or "Zephyr 3-2")
2. Resolve it to a bake log filename using the day number, optional bake-number suffix, and current date
3. Read the bake log and extract all "For Zephyr N" entries
4. Use event timestamps (body text), not header timestamps (H2 headings)
5. When writing any output that references the bake, use `[[bake log M-D-YYYY-N]]` — never the bare Zephyr number

To add event_time tags to a bake log:

1. Read the target bake log
2. For each Zephyr entry, decide if it records a specific action (see list above)
3. If yes, append the event_time tag after the last line of the body
4. Use the body time when stated; use the header time otherwise
5. Commit after all tags are added

## Routing

Routing delivers Zephyr entries found in any document to their proper bake logs, with deduplication, reverse chronological ordering, and move or copy semantics.

Routing is a separate component so it can be swapped out without changing the core scheme.

The full routing rules live in `ROUTING.md` in this skill directory.

Read `ROUTING.md` whenever asked to route Zephyr entries.
