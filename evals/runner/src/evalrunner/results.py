import pathlib

import polars


def report(frame: polars.DataFrame) -> None:
    for row in frame.iter_rows(named=True):
        mark = "pass" if row["passed"] else "FAIL"
        print(
            f"{mark}  {row['case']:<26}"
            f"expected={row['expected']:<6}got={row['got']}"
        )

    passed = int(frame["passed"].sum())
    print(f"score {passed}/{frame.height}")


def store(frame: polars.DataFrame, path: pathlib.Path) -> None:
    if path.exists():
        frame = polars.concat([polars.read_csv(path), frame])
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.write_csv(path)
