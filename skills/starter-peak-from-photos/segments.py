# /// script
# requires-python = ">=3.12"
# ///
import argparse
import datetime
import pathlib
import re
import sys

DEFAULT_FRAME_DIR = pathlib.Path("/Users/mtm/dcim2/OpenCamera")
FRAME_NAME = re.compile(r"IMG_(\d{8})_(\d{6})(?:_\w+)?\.jpg$")
FRAME_DURATION = "0.066667"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bookkeeping for appending time-lapse segments, so only uv and docker are needed"
    )
    parser.add_argument("--workdir", type=pathlib.Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare", help="write pending.txt for the frames newer than the last segment")
    prepare.add_argument("--start", type=datetime.datetime.fromisoformat)
    prepare.add_argument("--end", type=datetime.datetime.fromisoformat)
    prepare.add_argument("--frame-dir", type=pathlib.Path, default=DEFAULT_FRAME_DIR)
    sub.add_parser("commit", help="register pending.mp4 as the next segment")
    return parser.parse_args()


def frame_time(name: str) -> datetime.datetime | None:
    match = FRAME_NAME.match(name)
    if match is None:
        return None
    return datetime.datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S")


def resume_point(frames_all: pathlib.Path) -> datetime.datetime | None:
    if not frames_all.exists():
        return None
    names = frames_all.read_text().split()
    if not names:
        return None
    last = frame_time(names[-1])
    if last is None:
        return None
    return last + datetime.timedelta(seconds=1)


def prepare(args: argparse.Namespace) -> int:
    workdir: pathlib.Path = args.workdir
    start = resume_point(workdir / "frames-all.txt") or args.start
    if start is None:
        print("no earlier segment, so --start is required", file=sys.stderr)
        return 2
    found: list[tuple[datetime.datetime, str]] = []
    for path in args.frame_dir.glob("IMG_*.jpg"):
        when = frame_time(path.name)
        if when is None or when < start:
            continue
        if args.end is not None and when > args.end:
            continue
        found.append((when, path.name))
    if not found:
        print(f"no frames since {start.isoformat()}", file=sys.stderr)
        return 1
    names = [name for _, name in sorted(found)]
    (workdir / "pending-frames.txt").write_text("".join(f"{n}\n" for n in names))
    (workdir / "pending.txt").write_text(
        "".join(f"file /config/{n}\nduration {FRAME_DURATION}\n" for n in names)
    )
    return 0


def commit(args: argparse.Namespace) -> int:
    workdir: pathlib.Path = args.workdir
    pending = workdir / "pending.mp4"
    if not pending.exists():
        print("pending.mp4 is missing, so encode first", file=sys.stderr)
        return 1
    segments = workdir / "segments.txt"
    existing = segments.read_text().splitlines() if segments.exists() else []
    name = f"seg-{len(existing)}.mp4"
    pending.rename(workdir / name)
    with segments.open("a") as handle:
        handle.write(f"file /workspace/{name}\n")
    with (workdir / "frames-all.txt").open("a") as handle:
        handle.write((workdir / "pending-frames.txt").read_text())
    (workdir / "pending-frames.txt").unlink()
    (workdir / "pending.txt").unlink()
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "prepare":
        return prepare(args)
    return commit(args)


if __name__ == "__main__":
    sys.exit(main())
