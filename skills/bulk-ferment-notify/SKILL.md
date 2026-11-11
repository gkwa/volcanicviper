---
name: bulk-ferment-notify
description: "Start funnyflamingo for a Zephyr bake in a detached tmux session, so it posts bulk ferment progress to ntfy on an interval until the expected bulk end and keeps running after the Claude session ends. Takes the Zephyr number, plus any funnyflamingo flags the user names such as an interval or lead. Use when asked to run funnyflamingo, start bulk ferment notifications or ntfy posts for a Zephyr bake, notify me about the bulk, or stop those notifications."
---

## What runs

funnyflamingo lives at /Users/mtm/pdev/taylormonacelli/funnyflamingo and runs from that checkout.

Its flags, its stop rule and its duration grammar are documented in /Users/mtm/pdev/taylormonacelli/funnyflamingo/README.md, so read that rather than guessing.

Pass only the flags the user asks for, and leave the defaults to the tool.

## One session per bake

Each bake gets a tmux session named `funnyflamingo-zephyr<N>`, with a log at /Users/mtm/Library/Logs/funnyflamingo-zephyr<N>.log.

tmux was chosen because its server outlives the Claude session, and the session name makes the run easy to find and stop.

Never log to /tmp, because macOS reaps old files there.

Check whether the session is already running first:

```sh
tmux has-session -t funnyflamingo-zephyr10
```

If it exists, the new request replaces it, so kill it before starting the new one:

```sh
tmux kill-session -t funnyflamingo-zephyr10
```

## Starting

Start the loop detached, with stdout and stderr appended to the log:

```sh
tmux new-session -d -s funnyflamingo-zephyr10 "uv run --no-active --project /Users/mtm/pdev/taylormonacelli/funnyflamingo funnyflamingo --zephyr 10 >> /Users/mtm/Library/Logs/funnyflamingo-zephyr10.log 2>&1"
```

Extra flags go after `--zephyr 10` inside the quoted command.

## Confirming

Wait about 15 seconds, then read the log:

```sh
cat /Users/mtm/Library/Logs/funnyflamingo-zephyr10.log
```

The first post prints a notice such as `5h52m left · 5:18 PM · 22/61%`.

funnyflamingo exits 1 at once if the first post fails, so also confirm the session is still there with `tmux has-session`.

If the session has gone, report the error lines from the log instead of claiming success.

## Stopping

A request to stop the notifications for a bake kills its session:

```sh
tmux kill-session -t funnyflamingo-zephyr10
```

## The reply

Report the time left and the expected end from the first notice, and give the stop command.

The loop does not survive the Mac sleeping or shutting down, which the stay-awake skill covers if the user wants it.
