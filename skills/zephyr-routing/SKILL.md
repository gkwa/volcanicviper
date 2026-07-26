---
name: zephyr-routing
description: Route Zephyr entries from any document to their proper bake logs, with deduplication, reverse chronological ordering, and move or copy semantics. Use when asked to route Zephyr entries, move entries out of a log to where they belong, or clean up a document holding mixed entries.
---

## Overview

Routing takes a document containing mixed content and delivers each Zephyr entry to its proper bake log.

This skill is deliberately self-contained so it can be replaced with a different routing implementation without touching the [[zephyr]] skill.

Filename resolution, weight notation, event_time tags, and parameter precedence are owned by the [[zephyr]] skill — routing consumes those rules, it does not restate them.

Read the [[zephyr]] skill before routing, for the bake log naming convention and the parameter defaults.

## Parameters

- mode — `move` or `copy`; default `move`
- bake log directory — resolved per the Parameters section of the [[zephyr]] skill

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

- "Update the event times in this log" — that is the [[zephyr]] skill
- "Add event_time tags to the Zephyr entries" — that is the [[zephyr]] skill
- "Apply Grafana annotations" — that is the [[grafana-bake-annotation]] skill
- "Update the Grafana links" — that is the [[zephyr-grafana-links]] skill
- Opening or reading a bake log for any other purpose

## Identify

An entry is an H2 timestamp heading plus the body below it, up to the next heading.

A Zephyr entry is one whose body contains a key of the form "For Zephyr N" or "For Zephyr N-M".

Entries without a Zephyr key are never touched, moved, or modified.

## Resolve

Resolve each key against the entry's header date, not today's date.

Choose the most recent date with that day number on or before the header date.

Example: "Zephyr 31" under a June 1 header resolves to May 31, not June 31.

Resolve the key to a filename through the Bake Log Naming Convention in the [[zephyr]] skill.

## Create Missing Targets

If the resolved bake log does not exist, create it.

Scaffold minimally: a `## bake log` section holding the routed entries, nothing more.

Do not generate a recipe layout — recipe scaffolding is its own deliberate step.

## Insert

Routed entries go under the `## bake log` section of the target.

Keep all Zephyr entries in that section in reverse chronological order — newest first.

Sort by the event time stated in the body; fall back to the header timestamp when the body states no time.

## Deduplication

Normalize the entry first (weight notation per the [[zephyr]] skill), then compare.

Skip an entry when the target already contains one with the same header timestamp, the same Zephyr key, and the same normalized body.

## Override Semantics

A later memo supersedes an earlier one only when it reads as a restatement or correction of the same fact.

When it does, keep the later entry and drop the earlier one.

Two entries at or near the same timestamp that record different facts both stay — same-minute timing alone never implies override.

When unsure whether one supersedes the other, keep both and report the pair to the user.

## Mode: Move or Copy

In move mode (the default), remove each routed entry from the source document after it lands in the target.

In copy mode, leave the source document untouched.

## Delete Empty Source

After move mode removes all routed entries, check whether the source document is now empty.

A document is considered empty for this purpose when it contains no headings and no body content — only whitespace or a trailing newline.

Delete the source file if and only if all of the following are true:

- Mode is move (not copy)
- At least one entry was actually routed out
- No non-Zephyr content remains (no headings, body text, frontmatter, or other entries that were present before routing)
- The file is now empty as a result of routing

Do not delete the file if any non-Zephyr content remains after routing, even if all Zephyr entries were removed.

Do not delete the file if it was already empty before routing began — nothing was routed, so the empty state is not a result of routing.

## Normalize on Write

Apply weight notation rules as entries land in the target.

Add event_time tags to entries that record discrete bake actions, per the [[zephyr]] skill.

## Commit

Commit each modified bake log, one commit per file.

For the source document:

- If it was modified but not deleted, commit it as a separate commit.
- If it was deleted (empty source, move mode), commit the deletion as a separate commit.
- If it was untouched (copy mode), skip it.
