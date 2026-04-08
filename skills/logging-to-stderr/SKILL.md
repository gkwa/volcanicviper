---
name: logging-to-stderr
description: Set up logging with verbosity levels via --verbose flags, sending log output to stderr. Use when adding logging to a CLI tool or script.
---

Set up logging so each additional `--verbose` flag increases the log level. `-v` is an alias for `--verbose`.

All log messages go to stderr, not stdout.

Exception: Chrome extensions must log to stdout. Chrome treats stderr output as an extension failure, so redirect logging to stdout when working in a Chrome extension context.
