---
name: digikam-media-pack-copy
description: Query DigiKam for files matching given tags, shuffle them using the media pack spec, copy up to a size limit to a destination directory, and randomize file timestamps. Use when the user wants to fill a destination folder with a randomized selection of DigiKam-tagged media while preserving grouped sets.
---

## DigiKam Media Pack Copy Workflow

Given a list of DigiKam tag names, a destination directory, and a size limit, this skill:

1. Queries the DigiKam SQLite database for all files carrying any of the specified tags
2. Builds a shuffled collection using the media pack spec
3. Clears the destination's file contents without removing the directory itself
4. rsyncs the selected files preserving directory structure
5. Randomizes file timestamps, giving each media pack one shared random timestamp

Carry all values forward through steps — do not prompt the user between steps unless a step fails.

## Inputs

The user must supply all of the following. Do not proceed if any are missing — ask for them.

- Tag names (one or more)
- Destination directory
- Size limit

Default values when not supplied:

- Destination directory: `~/Documents/jack`
- Timestamp range: 1950-01-01 to 1959-12-31

## DigiKam Database

The database is always at `~/Pictures/digikam4.db`.

Resolve tag names to IDs:

```
sqlite3 ~/Pictures/digikam4.db "SELECT id, name, pid FROM Tags WHERE name IN ('tag1', 'tag2', ...);"
```

Resolve tagged file paths using this join pattern (status 4 = deleted/trashed, skip those):

```sql
SELECT DISTINCT ar.specificPath || a.relativePath || '/' || i.name,
       COALESCE(i.fileSize, 0)
FROM ImageTags it
JOIN Images i ON i.id = it.imageid
JOIN Albums a ON a.id = i.album
JOIN AlbumRoots ar ON ar.id = a.albumRoot
WHERE it.tagid IN (<ids>)
  AND i.status != 4
  AND i.album IS NOT NULL
ORDER BY 1
```

## Media Extension Allowlist

Only files whose extension (case-insensitive) appears in this list are counted as media:

- Image: jpg, jpeg, png, gif, webp, heic, tiff, bmp
- Video: mp4, mov, avi, mkv, m4v, wmv, flv, webm
- Audio: mp3, flac, wav, aac, ogg, m4a

Files whose stem ends in `_thumb` (e.g. `abc123_thumb.jpg`) are excluded even if the extension matches.
These are DigiKam-generated thumbnails, not source media.

## Media Pack Definition

After filtering to media files, group all selected files by their parent directory.

A directory qualifies as a media pack when it contains between 1 and 20 media files directly inside it (files in subdirectories do not count toward this limit).

A directory with more than 20 media files is not a media pack — its files are treated as standalone items.

Nesting depth does not matter: a directory fifty levels deep qualifies the same as one at the root.

## Randomization Rules

1. Treat each media pack as an indivisible block.
2. Treat each standalone media file as an individual item.
3. Shuffle all blocks and standalone items together.
4. Within each media pack, preserve lexicographic order by filename (case-insensitive).

## Size Selection

Iterate through the shuffled collection in order.
Add each item (pack or standalone) to the selection if it fits within the remaining budget.
Skip items that would exceed the limit and continue trying smaller items.
Stop when the full collection has been iterated.

## Step 1 — Query and build the Python script

Write the script to `$CLAUDE_JOB_DIR/tmp/media_pack_shuffle.py` (or `/tmp/` if that variable is not set).

The script must:

- Connect to `~/Pictures/digikam4.db`
- Query all files with any of the specified tag IDs
- Filter to media extensions, excluding `_thumb` files
- Group by parent directory and classify packs vs standalones
- Shuffle packs and standalones together
- Select files greedily up to the size limit
- Write paths (relative to `/`) to a temp file
- Run `rsync --archive --files-from=<list> / <dest>/`

Run with:

```
uv run --no-active /path/to/media_pack_shuffle.py
```

## Step 2 — Clear the destination

Never use `rm -rf <dest>` — that destroys the directory itself and any Finder metadata or app settings attached to it.

Instead, remove only the files inside:

```
find <dest> -type f -delete
```

Run this before rsync so stale files from a prior run do not remain.

## Step 3 — Run the copy

Run the script from Step 1. It will rsync the selected files to the destination, preserving directory structure so files with identical basenames in different source directories do not collide.

## Step 4 — Randomize timestamps

Write a second script to `$CLAUDE_JOB_DIR/tmp/randomize_timestamps.py`.

The script must:

- Walk the destination recursively
- Group media files by their parent directory
- Apply the same pack classification (1–20 files = pack, >20 = standalones)
- For each pack: call `random.randint` once and apply that timestamp to all files in the pack via `os.utime`
- For each standalone file: call `random.randint` independently per file
- Default timestamp range: 1950-01-01 00:00:00 UTC to 1959-12-31 23:59:59 UTC

Run with:

```
uv run --no-active /path/to/randomize_timestamps.py
```

## Step 5 — Verify

Run these checks and report the results:

```
find <dest> -type f | wc -l
```

```
du -sh <dest>
```

Confirm the file count and total size are consistent with what the copy script reported.

## Final report

After all steps complete, report:

- Tags queried
- Tag IDs resolved from the database
- Number of files found in the database
- Number of items in the shuffled collection (packs and standalones separately)
- Number of files selected and their total size
- Destination directory
- File count and disk usage confirmed by `find` and `du`
