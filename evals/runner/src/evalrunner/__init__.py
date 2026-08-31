import argparse
import datetime
import importlib.metadata
import pathlib

import polars

import evalrunner.ask
import evalrunner.cases
import evalrunner.grade
import evalrunner.results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run and score skill eval cases")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {importlib.metadata.version('evalrunner')}",
    )
    parser.add_argument("--cases", type=pathlib.Path, required=True)
    parser.add_argument("--results", type=pathlib.Path, required=True)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=600)
    return parser.parse_args()


def trial(case: evalrunner.cases.Case, index: int, stamp: str, timeout: int) -> dict:
    got = evalrunner.grade.verdict(evalrunner.ask.claude(case.prompt, timeout))
    return {
        "run": stamp,
        "case": case.name,
        "trial": index,
        "expected": case.expect,
        "got": got,
        "passed": got == case.expect,
    }


def main() -> None:
    args = parse_args()
    stamp = datetime.datetime.now().isoformat(timespec="seconds")

    rows = [
        trial(case, index, stamp, args.timeout)
        for case in evalrunner.cases.load(args.cases)
        for index in range(args.repeat)
    ]

    frame = polars.DataFrame(rows)
    evalrunner.results.report(frame)
    evalrunner.results.store(frame, args.results)
