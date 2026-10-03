---
name: bulk-ferment-remaining
description: "Report the time remaining until the expected bulk fermentation finish for a Zephyr bake, as one terse line, by reading the bake log and running chargingcheetah and ferment.py. Use when asked how long is left on bulk, when the bulk will be done, how the bulk ferment is going, or to measure the ferment for a Zephyr key."
---

## Bulk ferment remaining

This skill answers one question: how long until the bulk ferment is expected to finish.

It reads the start time and the initial dough volume from the Zephyr bake log, rebuilds the temperature parquet with chargingcheetah, and runs ferment.py.

It prints one line on success and says nothing else.

Read the zephyr skill first for the key scheme, the bake log filenames, and the event_time tags.

## Inputs

`zephyr` is required and has no default.

It accepts only the Zephyr key form, such as `2` or `3-2`.

Anything else, including a bake log date, is an error, so say what was accepted and ask again.

`probe` defaults to `2`.

The user can override it with `1`, or with `1 2`.

The bulk start time and the initial dough volume are never typed by default.

Both are read from the bake log, as described below.

If a required input is missing, state exactly which one and ask for it, then continue once the user answers.

## Resolving the key to a bake log

Bake logs are named `bake log M-D-YYYY-N.md` and live in /Users/mtm/Documents/Obsidian Vault.

N is the bake number, taken from the key suffix, and is 1 when the key has none.

Consider every bake log whose start day equals the key day, across all months and years.

Pick the one whose start date has the smallest absolute difference in days from today, whether that date is ahead or behind.

A bake ahead of today is a valid match, because the user may refer to a bake not yet started.

If two logs are equally close, one ahead and one behind, stop, list both, and ask which.

If no log matches, stop and say which key and which filenames were looked for.

If the closest match is more than 3 days from today, ask whether to run anyway and state the date and distance, such as "Zephyr 28 resolves to September 28, 5 days back. Run anyway?"

## Bulk start time

Find the entry in the log that records the bulk ferment start, the one the zephyr skill lists as "Bulk ferment start (flour added)".

Use its `event_time` tag as the start.

If that entry has no `event_time`, use the time in the entry header.

If no entry records the bulk start, stop and ask the user for the time.

If several entries do, stop, list them with their times, and ask which.

## Initial dough volume

Find the entry in the log that records a measured initial dough volume.

Show the value to the user and ask them to confirm it, even when exactly one entry is found.

If no entry records one, stop and ask the user for the volume in mL.

If several do, stop, list them with their values, and ask which.

Do not use the flour weight prediction unless the user supplies it.

## Running the tools

Run each command as its own Bash call.

START is the bulk start as `YYYY-MM-DDTHH:MM:SS`.

```sh
uv run --no-active --directory /Users/mtm/pdev/taylormonacelli/chargingcheetah main.py parquet --start START --probe 2 --output /Users/mtm/pdev/taylormonacelli/chargingcheetah/merged_data.parquet
```

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/dreamydragonfly /Users/mtm/pdev/taylormonacelli/dreamydragonfly/ferment.py --parquet-path /Users/mtm/pdev/taylormonacelli/chargingcheetah/merged_data.parquet --meta --start START --json
```

For probes `1 2`, pass `--probe 1 2` to the first command.

The JSON carries `elapsed_minutes`, `estimated_rise_pct`, `target_rise_pct`, `avg_temp_f`, `last_temp_age_minutes`, and under `meta`, `reference_duration_minutes`, `reference_offset_minutes`, and `reference_offset_direction`.

## Stale readings

If `last_temp_age_minutes` is more than 5, ask whether to run anyway and state the age, such as "The last probe reading is 7m old. Run anyway?"

At 5 or under, continue without asking.

## Output

On success print exactly one plain line, with no code fence so it wraps, and fields separated by a semicolon and a space.

```
Zephyr 2; 5h04m elapsed; 6h09m remaining at 8:51 PM; 1,000mL → 1,711mL; 32% of 71.1% rise; 70.8°F avg
```

The fields, in order:

- the Zephyr key as given
- `elapsed_minutes` as a span, such as 5h04m, or 42m under an hour
- `reference_offset_minutes` as the remaining span, then the target clock time, which is the start plus `reference_duration_minutes`
- the confirmed initial volume, an arrow, and the target volume, which is `(1 + target_rise_pct / 100)` times the initial volume rounded to whole mL
- `estimated_rise_pct` of `target_rise_pct`, followed by the word rise
- `avg_temp_f` followed by avg

Clock times are 12-hour with AM or PM.

Put the day name before the target clock time only when the target falls on a different day than today.

Numbers at 1,000 and above carry a comma, and units are squashed against the number, as in 1,711mL and 70.8°F.

Print nothing else on success, no preamble and no summary.

## Errors

Any error or missing input stops the run.

Be verbose about errors, because a terse success line only works when failures are impossible to miss.

State what failed, what was tried, what is needed, and the exact command and its output when a tool failed.

If `reference_offset_direction` is `over`, the reference duration has already passed.

That case has no defined output yet, so stop and report the JSON values instead of inventing a format.
