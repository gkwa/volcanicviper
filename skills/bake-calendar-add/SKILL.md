---
name: bake-calendar-add
description: "Turn a short bake utterance such as 'bake two for Dana on Tuesday' into two all-day entries on the Google bake calendar, a start entry two days before the bake day and a bake entry on the bake day. Use when the user says to bake some number of loaves for a person on a weekday, asks to put a bake on the bake calendar, or dictates a bake order with a count, a name and a day."
---

## Adding a bake to the bake calendar

A bake takes three days.

On the evening of day one the starter is fed, which is the start entry.

On day two the dough is mixed, stretched and folded, shaped, and left to ferment overnight.

On day three the loaves are baked, which is the bake entry.

So the start entry falls two days before the bake entry.

### Step 1 — parse the utterance

Pull three things from the utterance: the loaf count, the person, and the bake weekday.

Example: "bake two for Dana on Tuesday" is count 2, person dana, bake day Tuesday.

The count may be a digit or a spelled-out number.

The utterance is usually dictated, so it may carry transcription errors, such as "two" heard as "tulos" or "Lowe's loabes".

When a word plainly stands in for the count or for "loaves", read it as that.

Never correct a person's name on a guess; use it as given, and if it looks like a mishearing, say so in the report.

### Step 2 — resolve the dates

Take the bake day as the next occurrence of the named weekday after today.

If today is that weekday, use the same weekday one week later.

If the user said "start" with a weekday instead, for example "start two for Dana on Sunday", take that as the start day and put the bake day two days after it.

The start day is the bake day minus two days.

When the start day would fall before today, create both entries anyway and say in the report that the start day has already passed.

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

Create both events in one parallel batch.

Do not query the calendar first; the entries are added, not deduplicated.

### Step 4 — report

State the two dates with their weekdays and the two titles, in one short line each.

Add a line only when it changes what the user would do next, such as a start day already in the past, or a name that looks like a mishearing.

Do not ask for confirmation before creating the entries.
