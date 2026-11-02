---
name: starter-timelapse-video
description: Build an annotated, seamlessly looping time-lapse video of a sourdough starter from the photos in /Users/mtm/dcim2/OpenCamera, measured from the feed in the Zephyr bake log, then send it to the Pixel through Syncthing and play it in VLC. Each frame shows the time since the feed, the clock time, the running average probe temperature since the feed, and a full-frame border whose colour changes every elapsed hour. Covers the whole time since the feed unless a number of hours is given. Use when asked to make, refresh or loop a starter time-lapse video, a starter movie, the last N hours of the starter, a reversed starter video, or to put the starter video on the phone.
---

## Starter time-lapse video

This skill turns the starter photos since a feed into one looping video on the Pixel, playing in VLC without the screen shifting between passes.

Read the zephyr skill first for the key scheme, the bake log filenames, and the event_time tags.

Read the starter-peak-from-photos skill for where the photos live and how they are named, because this skill reuses its list_frames.py.

## Inputs

`zephyr` is required and has no default.

It accepts only the Zephyr key form, such as `1` or `3-2`.

`hours` defaults to the whole time since the feed.

When given, such as "the last 3 hours", keep only the photos within that many hours of the newest photo.

`direction` defaults to forward.

`reverse` plays newest first, as in "play it backwards".

`probe` defaults to `2`.

The feed time is never typed by default.

It is the `event_time` of the feed starter entry in the bake log, resolved through the zephyr skill.

If no feed entry has a time, stop and ask for it.

## Before starting

Docker must be running, because ffmpeg runs in a container and is never installed on the host.

```sh
docker info --format {{.ServerVersion}}
```

If that fails, run `open -a Docker`, then check again.

Use the session scratchpad for every temporary file, or `mktemp -d` when there is none.

SCRATCH below means that directory.

## Collect the photos and temperatures

Always fetch fresh, because new photos and probe readings keep arriving while the starter is still going.

FEED is the feed time as `YYYY-MM-DDTHH:MM:SS`.

```sh
uv run --no-active --script /Users/mtm/pdev/taylormonacelli/volcanicviper/skills/starter-peak-from-photos/list_frames.py --start FEED > SCRATCH/frames-list.txt
```

Write the probe readings into the scratch directory, never over chargingcheetah's own merged_data.parquet.

```sh
uv run --no-active --directory /Users/mtm/pdev/taylormonacelli/chargingcheetah main.py parquet --start FEED --probe 2 --output SCRATCH/temps.parquet
```

The probes are the diminutivedragon hardware, and the parquet holds one reading about every 30 seconds in UTC.

## Annotate the frames

Clear the frame directory first with `find SCRATCH/frames -mindepth 1 -delete` when it already exists.

```sh
uv run --no-active --script /Users/mtm/pdev/taylormonacelli/volcanicviper/skills/starter-timelapse-video/annotate_frames.py SCRATCH/frames-list.txt --feed FEED --temps SCRATCH/temps.parquet --out-dir SCRATCH/frames
```

Add `--hours N` when hours was given.

The script converts the readings to America/Los_Angeles and writes `frame_00000.jpg` onwards, oldest first.

Every frame carries these properties, which the user settled on and should not drift:

- A black banner across the top.
- A large line such as `9h 34m since feed`, or `26m since feed` under an hour, in the colour of the current hour.
- A smaller line such as `hour 10   now 4:21 AM   fed 6:47 PM`.
- A third line such as `avg 69°F since feed`, the mean of every probe reading from the feed up to that photo's time, rounded to the nearest whole degree with no decimals.
- A 16px border around the whole frame, not around the jar, whose colour steps through a 16-colour palette once per elapsed hour since the feed, so it changes at the feed minute past each hour rather than on the clock hour.
- The camera's own date stamp stays in the bottom right corner.

## Encode one pass

The pass is 15 frames per second, so each photo, taken about 2 minutes apart, lasts one frame.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffmpeg --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -y -framerate 15 -i /work/frames/frame_%05d.jpg -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p /work/pass.mp4
```

For reverse, add `-vf reverse` before `-c:v`.

Do not add a held last frame, because the user found the pause confusing.

Do not add chapters unless asked.

## Repeat the pass inside one file

VLC's own repeat reloads the file at every end, and each reload drops out of full screen so the status and navigation bars flash and the picture shifts.

Repeating the pass inside the file makes each restart just the next frame, so VLC only reloads once per file.

Choose the repeat count so the file runs about 10 minutes: count = ⌈600 / pass seconds⌉, where pass seconds is the frame count divided by 15.

Read the frame count from the pass rather than counting files by hand.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffprobe --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 /work/pass.mp4
```

For example, 484 frames is a 32s pass and ⌈600 / 32.27⌉ = 19 repeats, and 91 frames is a 6s pass and ⌈600 / 6.07⌉ = 99 repeats.

`-stream_loop` takes the number of extra plays, which is the count minus one.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffmpeg --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -y -stream_loop LOOPS -i /work/pass.mp4 -c copy /work/loop.mp4
```

The copy is not re-encoded, so the file grows in step with the count, at roughly 2MB per pass for a full night and 0.6MB per pass for 3 hours.

## Check before sending

Cut the first frame, the last frame of the first pass, and the first frame of the second pass, cropped to the banner, and read the image.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffmpeg --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -y -i /work/loop.mp4 -vf "select='eq(n,0)+eq(n,LAST)+eq(n,FIRST2)',crop=720:210:0:0,tile=1x3" -frames:v 1 /work/check.png
```

LAST is the frame count minus one and FIRST2 is the frame count.

The banners should run from the first window time to the newest photo time and straight back, with the average line present.

## Send it to the Pixel

The file name is `zephyr<KEY>-starter-loop.mp4`, with `-<N>h` before `-loop` when hours was given and `-reversed` before `-loop` for reverse, such as `zephyr1-starter-3h-loop.mp4`.

Copy it into the Syncthing drop folder.

```sh
cp SCRATCH/loop.mp4 /Users/mtm/pixel-sync/NAME
```

Read its size with `ls -l`, then wait in the background until the phone's copy has the same size.

```sh
until /Users/mtm/Library/Android/sdk/platform-tools/adb -s SERIAL shell ls -l /storage/emulated/0/Sync/NAME 2>/dev/null | grep -q SIZE; do sleep 5; done
```

Get the adb serial from `adb devices` first, because the IP and port change, and see the pixel9a-wireless-adb memory when the phone is offline.

VLC has permission to read videos only, not all files, so it cannot open the Sync folder.

Copy the file into Movies and register it with the media library.

```sh
/Users/mtm/Library/Android/sdk/platform-tools/adb -s SERIAL shell cp /storage/emulated/0/Sync/NAME /storage/emulated/0/Movies/NAME
```

```sh
/Users/mtm/Library/Android/sdk/platform-tools/adb -s SERIAL shell content call --uri content://media/external/file --method scan_file --arg /storage/emulated/0/Movies/NAME
```

## Play it in VLC

Start VLC fresh at the beginning, because VLC otherwise resumes where the last video stopped or hands the file to whatever VLC screen is open.

```sh
/Users/mtm/Library/Android/sdk/platform-tools/adb -s SERIAL shell "am start -S -a android.intent.action.VIEW -d file:///storage/emulated/0/Movies/NAME -t video/mp4 -p org.videolan.vlc --el position 0 >/dev/null; sleep 3; dumpsys window | grep mCurrentFocus; screencap -p /sdcard/Download/claude-check.png"
```

Pull the screenshot, read it, and confirm the video fills the screen in portrait with the banner readable, then delete the screenshot from the phone.

Never launch apps with `monkey`, because it turns the phone's auto-rotate back on.

## VLC settings this relies on

Google Photos and Files by Google both loop videos with no way to stop it, which is why VLC is the player.

VLC's "Video screen orientation" must be Portrait, under More, Settings, Video, because the default "Automatic (sensor)" ignores the phone's rotation lock.

The player's repeat mode should be repeat one, set in the player's "…" menu under "Repeat mode" until its icon shows a 1, so the file also restarts after its own 10 minutes.

VLC needs only `android.permission.READ_MEDIA_VIDEO`, granted with `pm grant org.videolan.vlc android.permission.READ_MEDIA_VIDEO`, and never all-files access.

If the picture is squashed or stretched and choosing "Best fit" by long-pressing the aspect ratio button does not fix it, `pm clear org.videolan.vlc` resets VLC, after which the video permission and Portrait orientation must be set again.

Check a setting only when something looks wrong, not on every run.

## Driving the phone

Check the focused window inside the same adb shell command as each tap, and stop when it is not VLC, because the user often switches back to the Claude app and a blind tap lands there.

Never run a tap in parallel with the focus check that is meant to guard it.

`uiautomator dump` fails on VLC's main screen, which never goes idle while it looks for network shares, so read that screen from a screenshot instead.

VLC does not redraw while paused, so read a paused position from `dumpsys media_session` rather than from the picture.

When done, post the Ping notification described in the return-to-claude-app memory.

## Output

Report in a few lines what was made and verified: the window as clock times, the photo count, the pass length, the repeat count and total length, the file size, the file name, and that it is playing in VLC.

Say plainly when a step was not verified, such as a screenshot that was not taken.

## Errors

If Docker will not start, the photo folder has no frames since the feed, the parquet is empty, or the phone is not reachable over adb, stop and say which, with the command and its output.

Do not install ffmpeg, adb, or anything else on the host to work around a failure.
