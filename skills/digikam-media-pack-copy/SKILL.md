---
name: digikam-media-pack-copy
description: Query DigiKam for files matching given tags, shuffle them using the media pack spec, copy up to a size limit to a destination directory, and randomize file timestamps. Use when the user wants to fill a destination folder with a randomized selection of DigiKam-tagged media while preserving grouped sets.
---

## DigiKam Media Pack Copy Workflow

Given a list of DigiKam tag names, a destination directory, and a size limit, this skill:

1. Queries the DigiKam SQLite database for all files carrying any of the specified tags
2. Builds a shuffled collection using the media pack spec
3. rsyncs the selected files into a staging directory outside the Syncthing watch path
4. Randomizes timestamps in staging so each file has its final timestamp before it ever enters the watched directory
5. Clears the destination's file contents without removing the directory itself
6. Moves files from staging into the destination — Syncthing sees each file exactly once, with its 1950s timestamp already set
7. Removes the staging directory

Carry all values forward through steps — do not prompt the user between steps unless a step fails.

## Why staging

If files are rsynced directly into the Syncthing-watched destination and then timestamped, Syncthing sees two events per file: the file arriving and then the timestamp being rewritten.

By staging first, all timestamp work happens outside the watched path. The final move into the destination is a single event per file, with the correct timestamp already in place.

## Inputs

The user must supply all of the following. Do not proceed if any are missing — ask for them.

- Tag names (one or more)
- Destination directory
- Size limit

Default values when not supplied:

- Destination directory: `~/Documents/jack`
- Timestamp range: 1950-01-01 to 1959-12-31

## Staging directory

Use `$CLAUDE_JOB_DIR/tmp/jack_staging` as the staging directory (or `/tmp/jack_staging` if that variable is not set).

The staging directory is always cleaned up after the move completes.

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

## Step 1 — Query and build the copy script

Write the script to `$CLAUDE_JOB_DIR/tmp/media_pack_shuffle.py` (or `/tmp/` if that variable is not set).

The script must:

- Connect to `~/Pictures/digikam4.db`
- Query all files with any of the specified tag IDs
- Filter to media extensions, excluding `_thumb` files
- Group by parent directory and classify packs vs standalones
- Shuffle packs and standalones together
- Select files greedily up to the size limit
- Write paths (relative to `/`) to a temp file
- Run `rsync --archive --files-from=<list> / <staging>/`

Run with:

```
uv run --no-active /path/to/media_pack_shuffle.py
```

## Step 2 — Randomize timestamps in staging

Write the timestamp script to `$CLAUDE_JOB_DIR/tmp/randomize_timestamps.py`.

The script must:

- Walk the staging directory recursively
- Group media files by their parent directory
- Apply the same pack classification (1–20 files = pack, >20 = standalones)
- For each pack: call `random.randint` once and apply that timestamp to all files in the pack via `os.utime`
- For each standalone file: call `random.randint` independently per file
- Default timestamp range: 1950-01-01 00:00:00 UTC to 1959-12-31 23:59:59 UTC

Run with:

```
uv run --no-active /path/to/randomize_timestamps.py
```

## Step 3 — Clear the destination

Never use `rm -rf <dest>` — that destroys the directory itself and any Finder metadata or app settings attached to it.

Instead, remove only the files inside:

```
find <dest> -type f -delete
```

## Step 4 — Move staging into destination

```
rsync --archive <staging>/ <dest>/
```

Syncthing sees each file arrive once with its 1950s timestamp already set — no second event.

## Step 5 — Remove staging

```
rm -rf <staging>
```

## Step 6 — Verify

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
