---
name: grouchygiraffe-ingest
description: Full grouchygiraffe ingestion workflow — given a grouchygiraffe media file path, identify the recipe, upload the source thumbnail to Imgur, and write a cleaned recipe note to the vault. Use when the user provides a grouchygiraffe .mp4 or .jpg file and wants the complete end-to-end recipe capture.
---

## Grouchygiraffe Ingest Workflow

Given a grouchygiraffe media file path (e.g. `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/DX9oSBkjsZR.mp4`), run the following three skills in order. Carry outputs forward between steps — do not prompt the user between steps unless a step fails.

### Step 1: grouchygiraffe-recipe-lookup

Invoke the `grouchygiraffe-recipe-lookup` skill on the provided media file path.

Collect from the output:
- The original Instagram post URL (from the `url` field in the YAML)
- The direct recipe URL (on the author's site, TikTok, or Substack)
- The author's name and Instagram handle
- The recipe name

### Step 2: social-to-imgur

Invoke the `social-to-imgur` skill using the original Instagram post URL collected in Step 1.

Collect from the output:
- The permanent Imgur URL for the thumbnail image

### Step 3: recipe-cleanup

Invoke the `recipe-cleanup` skill using the recipe URL from Step 1.

`recipe-cleanup` writes the ingredient wikilinks and then delegates to the `resolve-recipe-ingredient-link` skill to resolve any link that does not point to an existing product note — so the ingredient links in the note this workflow produces are already resolved by the time Step 3 returns. Do not resolve them separately.

After the recipe file is written, update the `pic` frontmatter field to use the Imgur URL from Step 2 instead of whatever URL was set during cleanup — the Imgur URL is permanent and not subject to CDN expiry.

### Final report

After all three steps complete, report:
- The recipe name
- The author's name and Instagram handle
- The recipe file path written to the vault
- The Imgur thumbnail URL
- The original Instagram post URL
