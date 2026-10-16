---
name: podcast-ad-removal
description: Download a podcast episode, transcribe it, find the sponsor and ad blocks by reading the transcript, cut them out, and post the ad-free MP3 to a temporary host for playback in the Voice app. Takes the podcast name, and the most recent episode unless the user names a particular one. Use when asked to remove ads from a podcast, clean today's episode of a show, pre-download a podcast without ads, or run the ad cleaning for a named show.
---

## Podcast Ad Removal

The input is a podcast name.

The episode is the most recent one unless the user names a particular episode by title, number, or date.

If the user names an episode and it cannot be found in the feed, stop and say so.

Never substitute the newest episode for a named one that cannot be found.

Carry outputs forward and do not prompt the user between steps unless a step fails.

## Where things live

The project is steamysquirrel at /Users/mtm/pdev/taylormonacelli/steamysquirrel

It holds `transcribe.py` and `remove_ads.py`, and a uv environment with faster-whisper installed.

Each run gets its own directory under the project, named by show slug and episode date, such as /Users/mtm/pdev/taylormonacelli/steamysquirrel/aidailybrief-2026-10-15

Create it with mkdir, and never write into a directory that already holds another run.

## Step 1: Find the feed

Look the show up with the iTunes search API.

```
curl --silent "https://itunes.apple.com/search?term=<url encoded name>&entity=podcast&limit=5"
```

Pick the result whose `collectionName` and `artistName` match the requested show.

Several unrelated shows often share a similar name, so check the artist and the genre before choosing.

Never use a feed URL that carries an `auth=` token, which is a private Patreon feed.

If no result matches, stop and report the candidates.

Download the feed with curl and the location flag into the run directory as feed.xml.

## Step 2: Pick the episode

Parse the feed and sort the items by `pubDate`, newest first.

Feed order alone is not reliable, because reruns and bonus items are interleaved.

For the default case take the newest item.

For a named episode match on title, episode number, or publication date against every item.

Show the user the chosen title, date, and duration in one line before continuing.

## Step 3: Download

Download the item enclosure with curl and the location flag, because the URL often goes through tracking redirects.

Compare the downloaded size with the enclosure `length` attribute when the feed provides one, and confirm with `file` that the result is audio and not an error page.

Stop on a mismatch.

## Step 4: Transcribe

Run the transcription in the background, because it takes a while on this machine.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/transcribe.py <run dir>/episode.mp3 <run dir>/transcript.json
```

The defaults are the small.en model with greedy decoding, which is about twice as fast as beam search for 98.8% text similarity.

Do not poll or sleep while waiting, and continue when the completion notice arrives.

Wall time stretches a lot when the machine is loaded, so expect roughly 24 CPU minutes for a 30 minute episode and report that if the user asks.

## Step 5: Find the ad blocks by reading

Detection is reading the timestamped transcript, because pattern matching alone was wrong on two of three shows tried.

Search the transcript for ad-like lines to find where to look.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python -I -c "import json,re; d=json.load(open('<run dir>/transcript.json')); p=re.compile(r'sponsor|brought to you|promo code|use code|\.com|\.ai|patreon|ad-free|free at|slash|offer', re.I); [print(round(s['start'],1), round(s['end'],1), s['text']) for s in d if p.search(s['text'])]"
```

Then print the segments around each cluster and read them to decide the start and end of each block.

What an ad block looks like:

- Ads are back to back with no speech gap between them, so a gap is not an edge.
- The edge is a topic change, such as a read that begins mid-sentence in content that was about something else.
- A block can start immediately after a host line like "Next up, the main episode".
- Content often resumes mid-sentence after dynamically inserted ads.
- The same read can appear more than once in one pod.
- A pod can also sit before the show starts and after the sign-off.
- A sponsor thanks, Patreon plug, or house promo in the intro counts as an ad block.

What is not an ad:

- A joke in the content that uses ad words, such as "Brought to you by Shopify" after a cash register sound.
- The host discussing a company in the story.

Keep the host's "Welcome back" line when it follows the ads.

Use the regex helper only as a hint.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/remove_ads.py <run dir>/transcript.json
```

Its ranges can swallow real content or run to the end of the file, so never cut with them unchecked.

## Step 6: Place the edges precisely

Transcript timestamps are per segment, and a long segment can hold both content and ad.

When an edge falls inside a segment, get word-level timing for only that window of about 15 seconds.

Decode the audio with PyAV, slice the window, and transcribe it with `word_timestamps=True`.

Place the cut start just after the last content word, and the cut end before the first content word that follows.

## Step 7: Cut

Pass each verified block as a `--range START:END` flag, where END can be `end` for a post-roll.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/remove_ads.py <run dir>/transcript.json --audio <run dir>/episode.mp3 --output <run dir>/episode.clean.mp3 --range 35.2:76.3 --range 752.2:923.4
```

Then probe both durations with ffprobe and confirm the difference equals the total of the ranges.

The ffmpeg on this machine is a Docker shim, so Docker Desktop must be running.

## Step 8: Post

Upload the cleaned file to Litterbox with a 72 hour expiry, and then check the headers.

```
curl --silent --show-error --max-time 600 --form reqtype=fileupload --form time=72h --form fileToUpload=@<run dir>/episode.clean.mp3 https://litterbox.catbox.moe/resources/internals/api.php
```

```
curl --silent --head --location https://litter.catbox.moe/<id>.mp3
```

Confirm `content-type: audio/mpeg`, a `content-length` equal to the local file size, and `accept-ranges: bytes`.

The file is someone else's copyrighted audio, so use only this expiring link and never a permanent public host.

Skip the upload only when the user says not to post.

## Final report

Lead with the link on its own line, bare so it is clickable.

Then report:

- The episode title and publication date
- Duration before and after, and the total removed
- Each cut range as clock times
- That the cut points were not listened to, and which joins are worth checking

To listen in Voice, tell the user to open the link in Chrome, download it, move it into the Audiobooks folder with the Files app, and open that folder in Voice.

The Download folder cannot be picked as a library folder.
