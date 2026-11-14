---
name: bake-log-photos
description: Insert recent Pixel photos of dough, flour, or starter into the matching Zephyr bake logs, both inline at the entry nearest the photo time and in the images section, which sits right after the contents block. Uploads each photo to Imgur and records its source filename. Use when asked to add bake photos to the bake logs, put the recent pictures in the bake log, match photos to bake entries by timestamp, or move the images section to the top of a bake log.
---

## Parameters

Resolve each by the precedence in the [[zephyr]] skill: explicit request, then machine-local configuration, then the default.

- photo directory: `/Users/mtm/dcim2/Camera`
- window: photos from the last 2 days, counted from now
- bake log directory: resolved by the [[zephyr]] skill

Only `PXL_*.jpg` files in the photo directory are candidates.

The `OpenCamera` folder is the starter time-lapse, covered by [[starter-timelapse-video]], so never use it here.

## Time

A `PXL_YYYYMMDD_HHMMSSmmm` filename carries UTC.

Convert it to Pacific local time before comparing it with anything in a bake log, which is all local.

Never use the file modification time, because syncing rewrites it.

## Select

1. List the `PXL_*.jpg` files whose converted time falls inside the window.
2. Drop every file whose bare filename already appears in a `%% source: <filename> %%` comment in any bake log, because that comment is the record that a photo is placed. Search the whole bake log directory with one `rg` call over all the filenames.
3. Look at each remaining photo with Read and keep only those showing dough, flour, starter, or the bake itself, such as loaves, pans, and bowls. Drop everything else, and never keep a photo you did not look at.
4. When a burst of near-identical frames exists, keep the sharpest one or two. A filename with `MACRO_FOCUS` is a variant of the burst, so it competes with the others rather than counting extra.

## Match to a bake log

A photo belongs to the bake log whose bake was in progress at the photo time.

Read the log's `## bake log` entries and use the event timestamps in the body rather than the header timestamps, as the [[zephyr]] skill requires.

Deduce the log from two timestamps together: the converted photo time, and the event times of the memo entries in each candidate log.

A photo fits a log when its time falls between that log's first and last event times, or within a short gap of an entry it plainly illustrates.

Gotcha: a photo can show a previous bake, such as a loaf or starter from the last Zephyr, and still be taken during a newer bake's window.

The timestamp alone then points at the wrong log.

Compare what the photo shows with what the candidate logs say was happening, such as its flour, its pans, its loaf count, and its stage.

Ask the user about a photo whenever more than one log could claim it, when its content does not fit the log its time points to, or when no log fits its time.

Name the photo, its converted time, and the candidate logs in the question, and never guess.

Ask these together in the one round of questions at the end, and leave the photo out of every log until it is answered.

## Insert inline

Find the entry whose event time is closest to the photo time, and place the image in that entry.

Entries run newest first, and an image goes after the entry's body text and before its `event_time` line.

An image line is:

```
![|300](<imgur url>) %% source: <bare filename> %%
```

Several photos for one entry share a single line, separated by a space, as the existing logs do.

## Insert in the images section

Every inline photo also goes in the log's `## images` section.

The section holds one line of all the log's images in capture order, each with its own source comment.

Look at an existing log with an images section before writing, and match it.

## Move the section to the top

In every log that gains a photo, move `## images` to sit right after the `## contents` block and before `## logbook`.

Move the `[[#images]]` contents entry to match, making it the first item in the list.

Keep the `[[#Contents|back to top]]` link under the heading, as the other sections have it.

A log with no images section yet gets one in that same place.

Logs that gain no photo are left alone.

## Upload

Upload with the Imgur steps in the [[social-to-imgur]] skill, using the local file instead of a downloaded thumbnail.

The Client ID is in the keychain under `imgur-api`, and it is never rotated.

Tag every upload with its local filename, so the Imgur side maps back to the file as well as the bake log doing so.

Add `-F name=<bare filename>` and `-F title=<bare filename>` to the upload `curl`, where the bare filename is the basename such as `PXL_20261111_173547356.jpg`.

The upload response echoes `name` and `title` in its `data` object.

Check that both match the filename before writing the URL into the log, and treat a mismatch as a failed upload.

Upload serially with a gap of about 5 seconds, because Imgur throttles bursts.

A 429 or 503 means the egress IP is blocked or throttled.

Stop on it, report which photos are not uploaded, and leave those photos out of the log rather than writing a placeholder.

## Commit

Commit after each bake log changes, with a one-line subject, so each change can be reverted on its own.

After the edits, run the [[outline-headings]] skill on every touched log, and do so without asking.

## Questions

Resolve every unambiguous case directly.

Collect the judgment calls, such as a photo with no matching log or a photo that may or may not show dough, and ask them together in one round at the end.

## Report

Report one line per bake log changed, with the count of photos added, and report any photos skipped or not uploaded.

Say nothing when no photo was added.
