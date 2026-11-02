# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow", "polars"]
# ///
"""Stamp each time-lapse photo with time since the feed, the running average
temperature since the feed, and a full-frame border whose colour changes every
elapsed hour, writing numbered frames for ffmpeg."""

import argparse
import datetime
import math
import pathlib
import re

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import polars

FONT = "/System/Library/Fonts/Helvetica.ttc"
STROKE = 16
BANNER_HEIGHT = 205
PALETTE = [
    (255, 235, 59),
    (0, 229, 255),
    (118, 255, 3),
    (255, 64, 255),
    (255, 255, 255),
    (255, 145, 0),
    (64, 156, 255),
    (255, 128, 171),
    (0, 200, 83),
    (179, 136, 255),
    (255, 215, 64),
    (29, 233, 182),
    (234, 128, 252),
    (204, 255, 144),
    (255, 110, 64),
    (128, 216, 255),
]
NAME = re.compile(r"IMG_(\d{8}_\d{6})(?:_\w+)?\.jpg$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frame_list", type=pathlib.Path, help="photo paths, one per line, as list_frames.py prints them")
    parser.add_argument("--feed", required=True, type=datetime.datetime.fromisoformat)
    parser.add_argument("--temps", required=True, type=pathlib.Path, help="chargingcheetah parquet")
    parser.add_argument("--out-dir", required=True, type=pathlib.Path)
    parser.add_argument("--hours", type=float, help="keep only photos within this many hours of the newest one")
    parser.add_argument("--zone", default="America/Los_Angeles")
    return parser.parse_args()


def frame_time(path: pathlib.Path) -> datetime.datetime:
    match = NAME.search(path.name)
    if match is None:
        raise ValueError(f"no timestamp in {path.name}")
    return datetime.datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")


def clock(moment: datetime.datetime) -> str:
    return moment.strftime("%-I:%M %p")


def elapsed_text(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    if hours == 0:
        return f"{mins}m since feed"
    return f"{hours}h {mins:02d}m since feed"


def select_frames(listing: pathlib.Path, hours: float | None) -> list[pathlib.Path]:
    paths = sorted((pathlib.Path(line) for line in listing.read_text().splitlines() if line.strip()), key=frame_time)
    if hours is None or not paths:
        return paths
    cutoff = frame_time(paths[-1]) - datetime.timedelta(hours=hours)
    return [path for path in paths if frame_time(path) >= cutoff]


def running_average(temps: pathlib.Path, feed: datetime.datetime, zone: str) -> polars.DataFrame:
    readings = (
        polars.read_parquet(temps)
        .with_columns(polars.col("datetime").dt.convert_time_zone(zone).dt.replace_time_zone(None))
        .filter(polars.col("datetime") >= feed)
        .sort("datetime")
    )
    return readings.with_columns(polars.col("temperature_f").cum_sum().truediv(polars.int_range(1, polars.len() + 1)).alias("avg_f"))


def average_at(averages: polars.DataFrame, taken: datetime.datetime) -> float | None:
    before = averages.filter(polars.col("datetime") <= taken)
    if before.is_empty():
        return None
    return before["avg_f"][-1]


def annotate(
    src: pathlib.Path,
    dst: pathlib.Path,
    feed: datetime.datetime,
    averages: polars.DataFrame,
    fonts: tuple[PIL.ImageFont.FreeTypeFont, PIL.ImageFont.FreeTypeFont],
) -> None:
    taken = frame_time(src)
    minutes = int((taken - feed).total_seconds() // 60)
    hour = minutes // 60
    color = PALETTE[hour % len(PALETTE)]
    big, small = fonts
    average = average_at(averages, taken)

    image = PIL.Image.open(src).convert("RGB")
    draw = PIL.ImageDraw.Draw(image)
    draw.rectangle((0, 0, image.width, BANNER_HEIGHT), fill=(0, 0, 0))
    draw.text((36, 26), elapsed_text(minutes), font=big, fill=color)
    draw.text((36, 106), f"hour {hour + 1}   now {clock(taken)}   fed {clock(feed)}", font=small, fill=(230, 230, 230))
    if average is not None:
        draw.text((36, 150), f"avg {math.floor(average + 0.5)}°F since feed", font=small, fill=(230, 230, 230))
    draw.rectangle((0, 0, image.width - 1, image.height - 1), outline=color, width=STROKE)
    image.save(dst, quality=92)


def main() -> None:
    args = parse_args()
    fonts = (PIL.ImageFont.truetype(FONT, 72, index=1), PIL.ImageFont.truetype(FONT, 34))
    averages = running_average(args.temps, args.feed, args.zone)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for index, path in enumerate(select_frames(args.frame_list, args.hours)):
        annotate(path, args.out_dir / f"frame_{index:05d}.jpg", args.feed, averages, fonts)


if __name__ == "__main__":
    main()
