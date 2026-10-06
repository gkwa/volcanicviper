# /// script
# requires-python = ">=3.12"
# ///
import argparse
import datetime
import pathlib
import re

DEFAULT_FRAME_DIR = pathlib.Path("/Users/mtm/dcim2/OpenCamera")
FRAME_NAME = re.compile(r"IMG_(\d{8})_(\d{6})(?:_\w+)?\.jpg$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the photos whose filename time falls in a window, oldest first"
    )
    parser.add_argument("--frame-dir", type=pathlib.Path, default=DEFAULT_FRAME_DIR)
    parser.add_argument("--start", type=datetime.datetime.fromisoformat, required=True)
    parser.add_argument("--end", type=datetime.datetime.fromisoformat)
    return parser.parse_args()


def frame_time(path: pathlib.Path) -> datetime.datetime | None:
    match = FRAME_NAME.match(path.name)
    if match is None:
        return None
    return datetime.datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S")


def in_window(
    when: datetime.datetime,
    start: datetime.datetime,
    end: datetime.datetime | None,
) -> bool:
    if when < start:
        return False
    if end is not None and when > end:
        return False
    return True


def main() -> None:
    args = parse_args()
    frames: list[tuple[datetime.datetime, pathlib.Path]] = []
    for path in args.frame_dir.glob("IMG_*.jpg"):
        when = frame_time(path)
        if when is None:
            continue
        if in_window(when, args.start, args.end):
            frames.append((when, path))
    for _, path in sorted(frames):
        print(path)


if __name__ == "__main__":
    main()
