import dataclasses
import pathlib
import re

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)


@dataclasses.dataclass
class Case:
    name: str
    expect: str
    prompt: str


def expected_direction(header: str) -> str:
    for line in header.splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "expect_direction":
            return value.strip()
    return ""


def parse(path: pathlib.Path) -> Case:
    match = FRONT_MATTER.match(path.read_text())
    if match is None:
        raise ValueError(f"{path} has no front matter")

    header, body = match.groups()
    expect = expected_direction(header)
    if not expect:
        raise ValueError(f"{path} has no expect_direction")

    return Case(name=path.stem, expect=expect, prompt=body.strip())


def load(directory: pathlib.Path) -> list[Case]:
    return [parse(path) for path in sorted(directory.glob("*.md"))]
