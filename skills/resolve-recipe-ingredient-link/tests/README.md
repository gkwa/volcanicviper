# resolve-recipe-ingredient-link evals

Regression tests for the resolve-recipe-ingredient-link skill, run with promptfoo.

## What is tested

There are two eval configs.

promptfooconfig.yaml tests resolution: which note a link should point to.

Each case is a recipe ingredient line containing an unresolved wikilink, plus the note the skill should resolve it to.

The cases cover the skill's three-tier rule:

- tier 1: a near-exact name match resolves the link (leeks resolves to leek.md)
- tier 2: a left-side adjective on the line disambiguates (whole black peppercorns resolves to black peppercorn.md, not the literal plural match sichuan peppercorns.md)
- tier 3: a line with no distinguishing word is genuinely ambiguous and the skill answers ASK

linkform.promptfooconfig.yaml tests link writing: given a displayed word and the resolved note name, which wikilink form to write.

The cases cover the three link-form cases:

- case 1: displayed equals note, plain link (leek with note leek becomes [[leek]])
- case 2: note is a prefix of displayed, suffix outside the brackets (leeks with note leek becomes [[leek]]s)
- case 3: stem changes, alias form (leaves with note leaf becomes [[leaf|leaves]])

## How it stays hermetic

The skill normally runs islandiguana against the live vault to enumerate candidates.

The vault grows over time, so calling it from a test would make the test flaky.

products.txt is a frozen snapshot of the product-tagged note names, captured once.

build_prompt.py assembles each eval prompt from two sources at run time: the live SKILL.md and the frozen products.txt.

This keeps SKILL.md as the single source of truth while holding the candidate list fixed, so the eval measures the skill's ranking and disambiguation judgment rather than the current state of the vault.

## Running

The Anthropic API key is read from the macOS Keychain at call time, never from a file or a persisted environment variable.

The key lives under the generic-password service name ANTHROPIC_API_KEY.

```sh
ANTHROPIC_API_KEY="$(security find-generic-password -s ANTHROPIC_API_KEY -w)" pnpm dlx promptfoo eval --config promptfooconfig.yaml --no-cache
```

Run the link-form config the same way.

```sh
ANTHROPIC_API_KEY="$(security find-generic-password -s ANTHROPIC_API_KEY -w)" pnpm dlx promptfoo eval --config linkform.promptfooconfig.yaml --no-cache
```

View the last run in the browser.

```sh
pnpm dlx promptfoo view
```

## Sample run

Resolution config.

```
Running 4 test cases (up to 4 at a time)...

2 large [[leeks]], chopped into 2-inch pieces, cleaned     [PASS] leek.md
3 [[scallions]], thinly sliced                             [PASS] scallions.md
2 teaspoons whole black [[peppercorns]]                    [PASS] black peppercorn.md
[[peppercorns]] to taste                                   [PASS] ASK

Total Tokens: 54,133
  Eval: 54,133 (54,105 prompt, 28 completion)

Results:
  ✓ 4 passed (100%)
  0 failed (0%)
  0 errors (0%)
Duration: 3s (concurrency: 4)
```

Link-form config.

```
Running 4 test cases (up to 4 at a time)...

leek    leek    [PASS] [[leek]]
leeks   leek    [PASS] [[leek]]s
boxes   box     [PASS] [[box]]es
leaves  leaf    [PASS] [[leaf|leaves]]

Total Tokens: 5,329
  Eval: 5,329 (5,291 prompt, 38 completion)

Results:
  ✓ 4 passed (100%)
  0 failed (0%)
  0 errors (0%)
Duration: 3s (concurrency: 4)
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
