---
name: how-to-cook-simplify
description: Reformat a "how to cook" note in the Obsidian vault into a dead simple list of ingredients and steps, moving every other fact into its own section rather than deleting it. Use when asked to simplify, clean up, or make dead simple a how to cook note, or to make one look like the brown lentils note.
---

## How To Cook Simplify

A how to cook note answers one question: how do I cook this thing.

The answer should be readable at a glance, however simple the food is.

The input is the path of one note whose filename starts with how to cook.

## Reference format

The model note is /Users/mtm/Documents/Obsidian Vault/how to cook brown lentils.md.

Read it before every run, because it is the source of truth for the format and may change.

## Rules

Top section:

- Section headings are all lowercase.
- The first section is the method, with a short heading naming the food and the method, such as `## boiling sweet potatoes`.
- It holds a bulleted ingredient list, then the steps.
- Give quantities only when the note states them, and never invent one.
- Link an ingredient to its product note when one exists in the vault.
- Each step is one short plain paragraph with a lowercase start and no trailing period.
- Write durations squashed against their unit, such as `8m` or `17m`.
- A step says what to do, not why, so move any reason into its own section.

Nothing is deleted:

- Simple does not mean shorter by removing facts.
- Every fact, link, and source in the original note survives somewhere in the result.
- Background, reasons, doneness checks, timing tables, and quoted sources each go in their own section below the method.
- Keep the original wording when moving text, apart from removing bold, italics, or emphasis.
- A line that only restates the note's title, such as `how to boil sweet potatoes`, may be dropped because the heading replaces it.
- When moved text applies more broadly than the note's food, such as general potato times in a sweet potato note, say so in one sentence under its heading.
- Bare wikilinks to related notes go last, under a heading such as `## related notes`.

Conflicts:

- When the note gives two different answers, such as a step saying 8m while a table says 10-15 minutes, use the note's own step for the method and keep the other value in its section.
- Do not resolve a conflict by guessing, and mention it in the final summary.

## Steps

1. Read the reference note and the target note.
2. Find the steps in the target note, wherever they sit, and put them in the top section.
3. Put every remaining fact into a short named section below the method.
4. Check no fact, link, or source from the original was lost.
5. Invoke the `outline-headings` skill on the note.
6. Follow the vault conventions in /Users/mtm/Documents/Obsidian Vault/CLAUDE.md.
7. Commit the note with `git commit -- <path>`, because background processes also commit to the vault.
8. Report the method in the summary, list any conflict found, and name anything dropped.
