---
name: resolve-wikilink
description: "Find the correct note to resolve an unresolved Obsidian wikilink. Use when a wikilink like [[leeks]] does not resolve to an existing note and you need to find the best matching note to point it at. Uses islandiguana to enumerate product-tagged candidate notes, then semantically ranks the full list against the link text and its surrounding source line."
---

## Resolving an unresolved Obsidian wikilink

Given an unresolved wikilink (e.g. `[[leeks]]`), find the existing note that best matches it.

Binary: `/Users/mtm/go/bin/islandiguana`

Vault path: `/Users/mtm/Documents/Obsidian Vault`

### Method

The link text is the bare name inside the brackets (e.g. `leeks` from `[[leeks]]`).

For a piped wikilink (`[[leek|leeks]]`), the link text is the part before the `|`.

Step 1 — enumerate candidates.

Resolution candidates live among notes tagged `product`.

```sh
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "product"'
```

Step 2 — read the full candidate list and rank it semantically.

Read every filename islandiguana returned and rank the whole list against the link text.

Do not pre-filter the list with a keyword search.

The match is semantic, not lexical — a keyword filter would discard good candidates the keywords failed to anticipate (a note named `wild ramps.md` resolves `[[leeks]]` even though it shares no letters with "leek").

The product pool is currently around 1,300 notes, which is small enough to read in full in a single pass.

Step 3 — resolve using a three-tier rule.

Tier 1 — near-exact name match.

If a candidate matches the link text exactly, or differs only by singular/plural, resolve to it.

Example: `leek.md` resolves `[[leeks]]`.

Tier 2 — disambiguate with the source line.

If no near-exact match exists, read the full line containing the wikilink in the source note, not just the bracketed text.

The descriptive words to the left of the linked noun are the disambiguators.

Example: the line `2 teaspoons whole black [[peppercorns]]` carries "black" and "whole", so the target is "whole black peppercorns", which resolves to `black peppercorn.md` rather than the literal-string match `sichuan peppercorns.md`.

Tier 3 — ask the user.

If the source line still does not settle the choice (e.g. `[[peppercorns]] to taste` names no type), report the candidates and ask the user to choose.

If no candidate is a plausible resolution at all, say so rather than forcing a wrong match.

Step 4 — report.

Report the number of candidates considered and the resolution, or the ranked shortlist when asking the user.

Do not edit the wikilink unless explicitly asked — surface the resolution first.

### Notes

Always quote the vault path — it contains spaces.
