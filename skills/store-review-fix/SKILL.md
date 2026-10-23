---
name: store-review-fix
description: Fix the next vault note that carries the storereview tag by applying the outline-headings skill to it, then report the changes, commit the note, open it in a new Obsidian tab, and report how many storereview notes remain. Use when asked to fix another store review note, work through the storereview queue, or find the next note with the store review tag.
---

## Store Review Fix

A note tagged `storereview` has a "store review" section that records headings moved above its Stores section.

The queue is every note carrying that tag.

Each run clears one note from the queue, except for the final deletion of the section and tag, which the user does afterwards.

## Steps

1. Find the notes that carry the `storereview` tag, using the islandiguana skill or the vault MCP tag search, and pick one that has not been fixed yet.
2. Read the note.
3. Apply the outline-headings skill to it and follow that skill for every rule about headings, links and nesting.
4. Leave the "store review" section and the `storereview` tag in place, because the user deletes them after reviewing the fix.
5. Update any heading quoted inside the "store review" section so it matches the renamed heading.
6. Tell the user each change made, as a short list.
7. Commit the note with `git commit -- <path>` and a message in the standard style.
8. Open the note in a new Obsidian tab with obsidian-cli.
9. Search the tag again and tell the user how many notes still carry `storereview`.

## Gotchas

- Git tracks the filename with its original casing, which may differ from the file on disk, so run `git ls-files "[Xx]..."` with the first letter bracketed before committing.
- A background loop may commit the vault every few minutes with the message `stuff`, so a commit that reports no changes means the loop already captured the edit.
- Confirm that with `git log --oneline -3 -- <path>` and report it rather than retrying.
- Do not edit the loop.
- `status.showUntrackedFiles=no` is global, so a new file never shows in `git status`.

## Counting the queue

- Count notes that carry the tag in their front matter, not notes that merely mention the words.
- Report one number for the tag, since "review" and "store review" are the same `storereview` tag.

## Note conventions that still apply

Follow the vault conventions in /Users/mtm/Documents/Obsidian Vault/CLAUDE.md.

Never use italics, bold, or emphasis in a note.

Each sentence is its own paragraph.

Do not reformat anything else in the note.
