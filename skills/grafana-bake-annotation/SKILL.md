---
name: grafana-bake-annotation
description: Annotate a sourdough bake log in Grafana. Use when asked to add Grafana annotations from a Zephyr bake log, build the annotation CLI, or update the bake log grafana section.
---

## Overview

This skill extracts annotatable bake events from a Zephyr bake log, runs the Grafana annotation CLI, and writes the command (without output) into the bake log's `## grafana` section.

See the [[zephyr]] skill for how to find the bake log and read Zephyr entries.

## What to Annotate

Only annotate discrete, time-bounded bake actions that have an explicit event timestamp.

Annotate:
- Feeding the starter → `feed_starter`
- Starter peaked → `starter_peaked`
- Mix (dough mixed with starter) → `mix`
- Each stretch and fold → `stretch_fold`
- Start of long uninterrupted bulk fermentation (after all stretch and folds are done) → `long_bulk_start`
- Shaping → `shape`
- Into cold retard/fridge → `cold_retard_start`
- Scoring → `score`
- Into oven → `bake_start`
- Lid off → `lid_off`
- Out of oven → `bake_done`

Skip observations, temperature readings, questions, reflections, and entries with no specific action time.

## Label Conventions

Use `snake_case` labels.

Use `_start` and `_done` suffixes for actions with clear start and end points.

Use `long_bulk_start` (not `bulk_start`) — bulk fermentation technically begins at mix; this label marks the start of the long uninterrupted fermentation phase after stretch and folds are complete.

## Scripts and Token

Annotation script:
```
/Users/mtm/pdev/taylormonacelli/diminutivedragon/scripts/annotate-grafana.py
```

Delete annotation script:
```
/Users/mtm/pdev/taylormonacelli/diminutivedragon/scripts/clear-annotations.py
```

Read the Grafana token at runtime:
```
GRAFANA_TOKEN=$(grep grafana_token /Users/mtm/pdev/taylormonacelli/diminutivedragon/terraform/grafana.tfvars | awk -F'"' '{print $2}')
```

Never write the token value into the bake log or any committed file.

## Running the Annotation Command

Pass all events in a single invocation using repeated `--time` and `--label` pairs.

Convert all timestamps to ISO 8601 before passing them.

```
GRAFANA_TOKEN=$(grep grafana_token ~/pdev/taylormonacelli/diminutivedragon/terraform/grafana.tfvars | awk -F'"' '{print $2}') \
  uv run --directory ~/pdev/taylormonacelli/diminutivedragon \
  scripts/annotate-grafana.py \
  --time 2026-05-28T20:39:00 --label feed_starter \
  --time 2026-05-29T06:31:00 --label starter_peaked
```

## Updating the Bake Log

After running the annotation command, write the command into the `## grafana` section of the bake log as a fenced code block.

Do NOT include the output lines (the "Added annotation id=..." lines) in the log — command only.

## Correcting Mistakes

To delete an annotation by id:
```
GRAFANA_TOKEN=$(grep grafana_token ~/pdev/taylormonacelli/diminutivedragon/terraform/grafana.tfvars | awk -F'"' '{print $2}') \
  uv run --directory ~/pdev/taylormonacelli/diminutivedragon \
  scripts/clear-annotations.py --id 42
```

After deleting, re-add the corrected annotation and update the CLI block in the bake log.

## Commit

Commit the bake log after every annotation run so individual changes can be reverted if needed.
