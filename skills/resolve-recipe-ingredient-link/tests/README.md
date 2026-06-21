# resolve-recipe-ingredient-link evals

Regression tests for the resolve-recipe-ingredient-link skill, run with promptfoo.

## What is tested

Each case is a recipe ingredient line containing an unresolved wikilink, plus the note the skill should resolve it to.

The cases cover the skill's three-tier rule:

- tier 1: a near-exact name match resolves the link (leeks resolves to leek.md)
- tier 2: a left-side adjective on the line disambiguates (whole black peppercorns resolves to black peppercorn.md, not the literal plural match sichuan peppercorns.md)
- tier 3: a line with no distinguishing word is genuinely ambiguous and the skill answers ASK

## How it stays hermetic

The skill normally runs islandiguana against the live vault to enumerate candidates.

The vault grows over time, so calling it from a test would make the test flaky.

products.txt is a frozen snapshot of the product-tagged note names, captured once.

build_prompt.py assembles each eval prompt from two sources at run time: the live SKILL.md and the frozen products.txt.

This keeps SKILL.md as the single source of truth while holding the candidate list fixed, so the eval measures the skill's ranking and disambiguation judgment rather than the current state of the vault.

## Running

Set an Anthropic API key, then run promptfoo from this directory.

```sh
export ANTHROPIC_API_KEY=your-key
pnpm dlx promptfoo eval --config promptfooconfig.yaml
```

View the last run in the browser.

```sh
pnpm dlx promptfoo view
```

## Refreshing the fixture

Regenerate products.txt when the product pool has changed enough to warrant it.

```sh
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "product"' > /tmp/products.txt
sed 's#.*/##' /tmp/products.txt > products.txt
```

## Known coverage gap

The cases use links whose resolving note shares letters with the link text.

The skill's no-keyword-filter rule exists to catch non-lexical matches (a link resolving to a note that shares no letters with it), which these cases do not yet exercise.
