---
name: shell-history
description: Search shell history using atuin. Use when the user mentions searching shell history, finding a past command, or recalling a URL or tool invocation from the terminal.
---

## Shell History Search

When the user wants to find something from their shell history, use atuin with timestamps and grep for filtering.

### Standard invocation

```
atuin search --limit <N> --format "{time} {command}"
```

Default `<N>` is 1000.

If the user specifies a count ("last 500 commands", "search 5000 entries"), use that number instead.

This returns the N most recent shell commands, each prefixed with a timestamp.

### Filtering by keyword

Then grep for the relevant term (URL, tool name, flag, etc.).

Run each command as a separate Bash call — never chain with pipes in a single call.

Step 1: capture history to a temp file in the job directory if one is available, otherwise write to a uniquely named file under /tmp.

Step 2: grep that file for the keyword.

### When to use this skill

- User says "check my shell history", "look in my history", "find that command I ran"
- User wants a URL they visited via curl/wget or a tool they ran recently
- User asks what flags or arguments they used for a past command
