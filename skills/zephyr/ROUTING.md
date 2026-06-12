# Routing Zephyr Entries

Routing takes a document containing mixed content and delivers each Zephyr entry to its proper bake log.

This file is the routing component of the zephyr skill.

It is deliberately self-contained so it can be replaced with a different routing implementation without touching `SKILL.md`.

Filename resolution, weight notation, event_time tags, and parameter precedence are owned by `SKILL.md` — routing consumes those rules, it does not restate them.

## Parameters

- mode — `move` or `copy`; default `move`
- bake log directory — resolved per the Parameters section of `SKILL.md`

## Trigger

Route only when explicitly asked.

Never route automatically just because a bake log or other document is open.

A request may grant a session-level standing instruction, for example "keep routing entries as we go" — honor it for that session only.

Requests that trigger routing:

- "Route the Zephyr entries in this log"
- "Route Zephyr entries from bake log 6-10 to their proper logs"
- "Move the Zephyr 9 entries out of this file"
- "Clean up the mixed entries in this log"

Requests that do NOT trigger routing (even if they involve Zephyr entries):

- "Update the event times in this log"
- "Apply Grafana annotations"
- "Add event_time tags to the Zephyr entries"
- Opening or reading a bake log for any other purpose

## Identify

An entry is an H2 timestamp heading plus the body below it, up to the next heading.

A Zephyr entry is one whose body contains a key of the form "For Zephyr N" or "For Zephyr N-M".

Entries without a Zephyr key are never touched, moved, or modified.

## Resolve

Resolve each key against the entry's header date, not today's date.

Choose the most recent date with that day number on or before the header date.

Example: "Zephyr 31" under a June 1 header resolves to May 31, not June 31.

Resolve the key to a filename through the Bake Log Naming Convention in `SKILL.md`.

## Create Missing Targets

If the resolved bake log does not exist, create it.

Scaffold minimally: a `## bake log` section holding the routed entries, nothing more.

Do not generate a recipe layout — recipe scaffolding is its own deliberate step.

## Insert

Routed entries go under the `## bake log` section of the target.

Keep all Zephyr entries in that section in reverse chronological order — newest first.

Sort by the event time stated in the body; fall back to the header timestamp when the body states no time.

## Deduplication

Normalize the entry first (weight notation per `SKILL.md`), then compare.

Skip an entry when the target already contains one with the same header timestamp, the same Zephyr key, and the same normalized body.

## Override Semantics

A later memo supersedes an earlier one only when it reads as a restatement or correction of the same fact.

When it does, keep the later entry and drop the earlier one.

Two entries at or near the same timestamp that record different facts both stay — same-minute timing alone never implies override.

When unsure whether one supersedes the other, keep both and report the pair to the user.

## Mode: Move or Copy

In move mode (the default), remove each routed entry from the source document after it lands in the target.

In copy mode, leave the source document untouched.

## Normalize on Write

Apply weight notation rules as entries land in the target.

Add event_time tags to entries that record discrete bake actions, per `SKILL.md`.

## Commit

Commit the source document and each modified bake log, one commit per file.
