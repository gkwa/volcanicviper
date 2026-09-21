# /// script
# requires-python = ">=3.12"
# ///
"""List Instagram shortcodes in starlitseal's urls.db that have no vault note yet.

Prints one tab-separated line per shortcode: received_at, shortcode, archived, url.
`archived` says whether grouchygiraffe already holds <shortcode>.yaml.
"""

import argparse
import datetime
import logging
import pathlib
import re
import sqlite3
import subprocess
import sys

DB = pathlib.Path("/Users/mtm/pdev/taylormonacelli/starlitseal/server/urls.db")
VAULT = pathlib.Path("/Users/mtm/Documents/Obsidian Vault")
DATA = pathlib.Path("/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data")
SHORTCODE = re.compile(r"instagram\.com/(?:[^/]+/)?(?:p|reels?|tv)/([A-Za-z0-9_-]+)")

log = logging.getLogger("new_shortcodes")


def local_midnight_utc() -> str:
    midnight = datetime.datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight.astimezone(datetime.timezone.utc).isoformat()


def fetch_rows(since: str) -> list[tuple[str, str]]:
    with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as conn:
        cur = conn.execute("select received_at, url from urls where url like '%instagram.com%' and received_at >= ? order by received_at", (since,))
        return cur.fetchall()


def unique_shortcodes(rows: list[tuple[str, str]]) -> dict[str, tuple[str, str]]:
    seen: dict[str, tuple[str, str]] = {}
    for received_at, url in rows:
        match = SHORTCODE.search(url)
        if not match:
            log.warning("no shortcode in %s", url)
            continue
        seen.setdefault(match.group(1), (received_at, url))
    return seen


def in_vault(shortcode: str) -> bool:
    cmd = ["rg", "--fixed-strings", "--files-with-matches", "--max-count", "1", "--glob", "*.md", "--glob", "!.claude/**", shortcode, str(VAULT)]
    return bool(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default=local_midnight_utc(), help="ISO-8601 UTC lower bound on received_at (default: local midnight today)")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING - 10 * min(args.verbose, 2))

    candidates = unique_shortcodes(fetch_rows(args.since))
    todo = {code: row for code, row in candidates.items() if not in_vault(code)}
    log.info("since=%s unique=%d in_vault=%d todo=%d", args.since, len(candidates), len(candidates) - len(todo), len(todo))
    for code, (received_at, url) in todo.items():
        archived = (DATA / f"{code}.yaml").exists()
        print(f"{received_at}\t{code}\t{archived}\t{url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
