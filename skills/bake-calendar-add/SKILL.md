---
name: bake-calendar-add
description: "Turn a short bake utterance such as 'bake two for Dana' into two all-day entries on the Google bake calendar, a start entry on the start day and a bake entry two days later. The start day defaults to today and can be overridden, as in 'bake two for Dana starting Sunday'. Also removes a bake, deleting both of its coupled entries, as in 'delete the bake for Dana'. Use when the user says to bake some number of loaves for a person, asks to put a bake on the bake calendar, dictates a bake order with a count and a name, or asks to delete, undo or cancel a bake."
---

## Adding a bake to the bake calendar

A bake takes three days.

On the evening of day one the starter is fed, which is the start entry.

On day two the dough is mixed, stretched and folded, shaped, and left to ferment overnight.

On day three the loaves are baked, which is the bake entry.

So the start entry falls two days before the bake entry.

### Step 1 — parse the utterance

Pull three parameters from the utterance: the loaf count, the person, and the start day.

The start day is optional and defaults to today.

Example: "bake two for Dana" is count 2, person dana, start day today.

Example: "bake two for Dana starting Sunday" is count 2, person dana, start day Sunday.

The count may be a digit or a spelled-out number.

The utterance is usually dictated, so it may carry transcription errors, such as "two" heard as "tulos" or "Lowe's loabes".

When a word plainly stands in for the count or for "loaves", read it as that.

Never correct a person's name on a guess; use it as given, and if it looks like a mishearing, say so in the report.

### Step 2 — resolve the dates

With no start day named, the start day is today.

A named weekday means the next occurrence of that weekday, counting today if today is that weekday.

"Tomorrow" and a calendar date are fine as start days too.

The bake day is the start day plus two days.

If the user names a bake day instead of a start day, for example "bake two for Dana on Tuesday", take it as the bake day and set the start day to two days before it.

When that start day would fall before today, create both entries anyway and say in the report that the start day has already passed.

### Step 3 — create the entries

Create two all-day events with the Google Calendar create_event tool on the bake calendar.

Bake calendar ID: `f5ba1ec696cefa533636d49aa5809be88a8c7e1c02ae2b31466d56e78ac0ad58@group.calendar.google.com`

If the call fails on that ID, run list_calendars, find the calendar named bake, and retry.

Pass `allDay` as true, with `startTime` at midnight of the day and `endTime` at midnight of the following day, no UTC offset.

Titles are all lowercase, including the first letter and the person's name:

```
start <count> loaves for <name>
bake <count> loaves for <name>
```

For a count of 1, write `loaf` in place of `loaves`.

Write the count as a digit or word the way the user said it; "two" stays "two".

Give both events the same `description`, a bake id that couples them so they can be removed together:

```
bake:<name>:<start day>
```

The name is lowercase with spaces turned into hyphens, and the start day is `YYYY-MM-DD`, for example `bake:dana:2026-10-25`.

Create both events in one parallel batch.

Do not query the calendar first; the entries are added, not deduplicated.

### Step 4 — report

State the two dates with their weekdays and the two titles, in one short line each.

Add a line only when it changes what the user would do next, such as a start day already in the past, or a name that looks like a mishearing.

Do not ask for confirmation before creating the entries.

## Removing a bake from the bake calendar

Use this when the user asks to delete, undo, remove or cancel a bake, for example "delete the bake for Dana" or "undo the Dana bake starting Sunday".

Both entries of a bake are removed together, because they share a bake id.

### Step 1 — find the bake

Pull the person from the utterance, and the start day or bake day if the user gave one.

Call list_events on the bake calendar, one call, from 7 days before today to 60 days after, with `fullText` set to `bake:<name>`.

Group the matches by the bake id in their description.

When nothing matches by id, fall back to events on the bake calendar in the same window whose title ends with `for <name>`.

The fallback covers entries created before bake ids existed.

Pair fallback entries as the start entry and the bake entry two days later.

### Step 2 — pick one bake

When exactly one bake matches, use it.

When the user gave a day, keep only the bake whose start day or bake day matches it.

When several bakes still match, list them as the start day, the count and the name, and ask which one.

When none match, say so and delete nothing.

### Step 3 — delete both entries

Call delete_event on the bake calendar for each of the two events, in one parallel batch.

Do not ask for confirmation once exactly one bake is matched; Google Calendar keeps deleted events in its trash for 30 days.

If only one of the two entries exists, delete it and say that its partner was missing.

### Step 4 — report

Name the two deleted titles with their dates, one short line each.
