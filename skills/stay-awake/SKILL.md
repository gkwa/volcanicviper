---
name: stay-awake
description: "Keep this Mac awake for a stated period with miserlymouse, replacing whatever assertion is already running without letting the machine sleep during the handover. Use when asked to keep the machine running or awake for longer, to stop it sleeping for a while, or to check how much longer it will stay awake."
---

## Staying awake

miserlymouse holds a `caffeinate` assertion for a human-readable duration.

It lives at /Users/mtm/pdev/taylormonacelli/miserlymouse and runs from that checkout.

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse for 2h
```

The duration and clock-time grammars are documented in /Users/mtm/pdev/taylormonacelli/miserlymouse/README.md, so read that rather than guessing at a format.

## Requests are a replacement, never an addition

"Keep this machine running for two hours longer" means the machine should be awake until two hours from now.

It does not mean two hours on top of whatever is already scheduled.

So the new end time is always the moment of the request plus the span asked for, regardless of what was already running.

This shortens as readily as it extends, and asking for `20m` while an eight-hour assertion is up correctly brings the end time forward.

## What is running right now

The supervisor processes are the ones whose argv contains `bin/miserlymouse`:

```sh
pgrep -f bin/miserlymouse
```

Each supervisor owns exactly one assertion, found by parent:

```sh
pgrep -P 22088 caffeinate
```

That assertion carries the schedule in its own arguments:

```sh
ps -o lstart=,etime=,command= -p 22089
```

The end time is the `lstart` value plus the seconds given to `-t`, and the time remaining is those seconds minus `etime`.

## Only miserlymouse's own assertions are in scope

A `caffeinate` that is not a child of a miserlymouse supervisor belongs to some other tool.

Never kill one of those, and do not mention them.

The parent check above is what draws that line, so always reach the assertion through `pgrep -P`, never by searching for `caffeinate` across the whole process table.

## Answering how much longer

Read the running assertion as described above and report the end time and the time remaining.

Start nothing and kill nothing, because this is a question rather than a request.

If no supervisor is running, say the machine is free to sleep whenever it likes.

## Starting or replacing

The order of these steps is the whole point of the skill.

A new assertion has to be live before the old one dies, or the machine is briefly free to sleep in the gap.

Step one, record the assertion PIDs that exist now, which may be none.

Step two, start the new one detached, so it outlives this session:

```sh
nohup uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse for 2h > /dev/null 2>&1 &
```

Step three, find the new supervisor by listing supervisors again and taking the PID that was not there in step one.

Differencing the PID sets is what identifies it, because two runs of the same duration are indistinguishable by argv.

Step four, confirm the new supervisor has actually acquired its assertion:

```sh
pgrep -P <new supervisor PID> caffeinate
```

If that prints nothing, run it again in a fresh call, up to about ten seconds in total, because a cold `uv` start is not instant.

If it never appears, stop and report the failure, leaving the old assertion untouched.

The machine stays awake on the old schedule in that case, which is the safe outcome.

Step five, and only now, kill each assertion PID recorded in step one:

```sh
kill 22089
```

Step six, confirm that `pgrep -f bin/miserlymouse` reports the new supervisor and nothing else.

Report the new end time.

## Kill the assertion, never the supervisor

Killing the `uv` wrapper or the Python supervisor orphans `caffeinate`, which then holds the machine awake for the entire original span with nothing supervising it.

Killing the `caffeinate` child instead is a complete teardown, because the supervisor sees its child exit and shuts itself down, taking the `uv` wrapper with it.

One `kill` on the assertion PID removes the whole tree.

## Until a clock time

A request phrased against the clock keeps the same six steps and only changes the tail of the command:

```sh
nohup uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse until 5pm > /dev/null 2>&1 &
```

Pass the time through to miserlymouse rather than converting it to a duration, because it already resolves a time to its next occurrence.

## Reference

`nohup` and the trailing `&` are both required, and the process reparents to PID 1 and survives the session ending.

Sending `SIGINT` to a detached supervisor does nothing at all, because the backgrounding shell sets that signal to ignore and Python inherits it, so the tool's Ctrl-C teardown never runs.

The progress bar suppresses itself when detached, since stderr is not a terminal, so `--no-progress` is unnecessary.

`pgrep -f bin/miserlymouse` matches only the Python supervisor and not the `uv` wrapper, whose argv spells the project path without a `bin` component.

Adding `--json --dry-run` prints the exact end time as ISO 8601 and runs nothing, which is a way to state the resulting schedule before committing to it.
