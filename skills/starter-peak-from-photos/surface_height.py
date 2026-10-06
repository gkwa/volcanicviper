# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow", "numpy"]
# ///
import argparse
import datetime
import pathlib
import re

import numpy
import PIL.Image

LEFT_STRIP = (230, 320)
RIGHT_STRIP = (370, 490)
GLASS_ROWS = (400, 440)
DOUGH_ROWS = (760, 790)
SCAN_ROWS = (380, 790)
FRAME_NAME = re.compile(r"IMG_\d{8}_\d{6}\.jpg")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the starter surface row for every frame in a manifest"
    )
    parser.add_argument("manifest", type=pathlib.Path)
    parser.add_argument("--frame-dir", type=pathlib.Path, required=True)
    return parser.parse_args()


def frame_names(manifest: pathlib.Path) -> list[str]:
    return FRAME_NAME.findall(manifest.read_text())


def luminance_profile(path: pathlib.Path) -> numpy.ndarray:
    with PIL.Image.open(path) as image:
        gray = numpy.asarray(image.convert("L"), dtype=numpy.float64)
    strips = [gray[:, left:right] for left, right in (LEFT_STRIP, RIGHT_STRIP)]
    profile = numpy.concatenate(strips, axis=1).mean(axis=1)
    return numpy.convolve(profile, numpy.ones(5) / 5, mode="same")


def surface_row(profile: numpy.ndarray) -> int:
    glass = profile[GLASS_ROWS[0] : GLASS_ROWS[1]].mean()
    dough = profile[DOUGH_ROWS[0] : DOUGH_ROWS[1]].mean()
    midpoint = (glass + dough) / 2
    bottom, top = SCAN_ROWS[1], SCAN_ROWS[0]
    for row in range(bottom, top, -1):
        if profile[row] < midpoint:
            return row
    return top


def stamp(name: str) -> datetime.datetime:
    return datetime.datetime.strptime(name[4:19], "%Y%m%d_%H%M%S")


def main() -> None:
    args = parse_args()
    for name in frame_names(args.manifest):
        row = surface_row(luminance_profile(args.frame_dir / name))
        print(f"{stamp(name).isoformat()} {row}")


if __name__ == "__main__":
    main()
