---
name: grouchygiraffe-ingest
description: Full grouchygiraffe ingestion workflow — given either a grouchygiraffe media file path or a recipe URL (YouTube, Instagram, or any recipe page), identify the recipe, upload the thumbnail to Imgur where applicable, and write a cleaned recipe note to the vault.
---

## Grouchygiraffe Ingest Workflow

The argument is either a local grouchygiraffe media file path or a URL.

Detect the input mode from the argument:
- If it starts with `http://` or `https://`: **URL mode** — skip to the URL path below
- Otherwise: **file mode** — follow the file path below

Do not prompt the user between steps unless a step fails.

---

## URL mode

When the argument is a URL, skip Steps 1 and 2 of the file flow and go directly to recipe-cleanup, with one variation depending on the URL type:

**YouTube URLs** (`youtube.com/watch?v=...` or `youtu.be/...`):

Invoke the `recipe-cleanup` skill with the YouTube URL directly.

`recipe-cleanup` extracts the video thumbnail from YouTube and sets the `pic` field — no separate Imgur upload is needed.

**Instagram or other social media URLs**:

First invoke the `social-to-imgur` skill with the URL to get a permanent Imgur thumbnail URL.

Then invoke the `recipe-cleanup` skill with the URL.

After `recipe-cleanup` writes the file, update the `pic` frontmatter field to use the Imgur URL — social CDN URLs expire.

**Final report (URL mode)**:

After all steps complete, report:
- The recipe name
- The author's name
- The recipe file path written to the vault
- The source URL

---

## File mode

Given a grouchygiraffe media file path (e.g. `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/DX9oSBkjsZR.mp4`), run the following three skills in order.

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

### Final report (file mode)

After all three steps complete, report:
- The recipe name
- The author's name and Instagram handle
- The recipe file path written to the vault
- The Imgur thumbnail URL
- The original Instagram post URL
