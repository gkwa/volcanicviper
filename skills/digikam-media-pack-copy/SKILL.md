---
name: digikam-media-pack-copy
description: Query DigiKam for files matching given tags, shuffle them using the media pack spec, copy up to a size limit to a destination directory, and randomize file timestamps. Use when the user wants to fill a destination folder with a randomized selection of DigiKam-tagged media while preserving grouped sets.
---

## DigiKam Media Pack Copy Workflow

This skill is implemented by `savagestoat` — a Python CLI tool at `~/pdev/taylormonacelli/savagestoat` (GitHub: `gkwa/savagestoat`).

`savagestoat` handles everything: querying DigiKam, pack classification, shuffling, staging outside the Syncthing watch path, timestamp randomization to the 1950s, cleaning the destination, and moving files into place.

## Inputs

The user must supply all of the following. Do not proceed if any are missing — ask for them.

- Tag names (one or more)
- Size limit

Default values when not supplied:

- Destination directory: `~/Documents/jack`

## Step 1 — Run savagestoat

```
uv run --project ~/pdev/taylormonacelli/savagestoat savagestoat \
  --tag <tag1> --tag <tag2> \
  --size <size> \
  --dest <dest> \
  -v
```

Pass one `--tag` flag per tag name.
Pass `--no-clean` if the user wants to add to the destination rather than replace it.
Use `-v` for INFO logging or `-vv` for DEBUG.

savagestoat will:

1. Resolve tag names to DigiKam IDs
2. Query `~/Pictures/digikam4.db` for all matching files
3. Classify directories as media packs (1–20 media files) or standalones
4. Shuffle packs and standalones together, preserving internal pack order
5. Select files greedily up to the size limit — packs are always included whole, never split
6. rsync selected files to `/tmp/savagestoat-staging`
7. Randomize timestamps in staging (1950–1959 range, one shared timestamp per pack)
8. Clear destination files with `find <dest> -type f -delete` (never `rm -rf`)
9. rsync staging into destination — Syncthing sees each file once with its final timestamp
10. Remove staging

## Step 2 — Verify

```
find <dest> -type f | wc -l
```

```
du -sh <dest>
```

Confirm file count and disk usage match what savagestoat reported.

## Final report

After completing, report:

- Tags used
- Number of files selected and their total size
- Destination directory
- File count and disk usage confirmed by `find` and `du`

## Background: why staging

If files land in the Syncthing-watched destination before timestamps are set, Syncthing sees two events per file: arrival and timestamp rewrite.

Staging first ensures each file arrives in the watched directory exactly once, with its 1950s timestamp already in place.

## Background: media pack definition

A directory qualifies as a media pack when it contains between `--min-pack-size` and `--max-pack-size` media files directly inside it (defaults: 1 and 20).

Files whose stem ends in `_thumb` are excluded.

See `~/pdev/taylormonacelli/savagestoat` and [[media pack shuffle spec]] for full details.
