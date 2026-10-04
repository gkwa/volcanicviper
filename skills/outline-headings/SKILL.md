---
name: outline-headings
description: Reformat a vault note so every line sits under a short heading that Obsidian Outline (the outline sidebar, outline mode) can jump to. Removes any table-of-contents block, adds headings for text outside any section, shortens long headings that nothing links to, nests dated entries, and moves the abstract or motivating question to the first section so it is easy to jump to. Use when given a note and asked to fix its outline, make it outline-friendly or easier to navigate in the sidebar, get it ready for outline mode, remove its TOC, shorten headings that wrap, put everything under a section, or apply the outline policy or outline pass to it.
---

## Outline Headings

Obsidian Outline is the navigation tool for the vault, not a table-of-contents block.

The Outline sidebar is often narrow, so a long heading wraps and is hard to scan.

Short headings stay on one line.

A longer explanation goes in a plain sentence directly under the heading, stating why the section exists.

There is no hard length limit for a heading.

If a heading needs more words than fit on one line, shorten it and put the rest in that sentence.

The input is the path of one note.

## Rules

Table of contents:

- If the note contains a table-of-contents block, remove it.
- A table-of-contents block is a fenced code block whose info string is `table-of-contents`, including its settings lines.
- Remove the blank lines it leaves behind so the note has no run of more than one blank line.

Text outside any section:

- Every line of body text sits under a heading.
- Text between the front matter and the first heading has no Outline entry, so it gets a heading.
- Give it a short heading that is contextually correct for what the text is.
- Use the content to choose the heading: an image plus links to a video and a recipe page become `## Video and recipe`, not `## Source`.
- If the short heading is too terse to explain the section, add a sentence directly under it.
- Never add a heading above the front matter.

First section:

- The first section holds the reason to open the note, such as the motivating question or the abstract.
- If the note carries an abstract, pitch, or summary of the subject lower down, move it up to become the first section, directly after any section created for text outside any section.
- Move whole paragraphs only, and keep their wording.
- Give the moved text a short heading, such as `## Author's pitch`.
- If a note has no motivating text, do not invent any.

Dated and repeated entries:

- Dated or repeated entries nest under one parent heading, one level down.
- A log heading followed by sibling dated headings becomes a parent with the dated headings demoted by one level, along with their subsections.
- Shorten a long date heading to a compact form, for example `Friday, August 21, 2026 at 9:46 PM` becomes `Aug 21 2026 9:46 PM`.

Shortening existing headings:

- Shorten a heading that would wrap in a narrow sidebar, but only after checking for links to it, as described below.
- A question used as a heading becomes a short heading, with the original question as the sentence beneath.
- A qualifier like `(152g starter instance)` moves under the heading only when the shortened heading is still unique among its siblings.
- If the shortened heading would match a sibling, keep the qualifier in the heading, abbreviated, for example `Ingredients 152g`.
- Put the moved qualifier in a plain sentence directly under the heading.

## Checking for links before renaming a heading

Renaming a heading breaks any link that points at it.

Before renaming any existing heading, search the whole vault at /Users/mtm/Documents/Obsidian Vault for references to it.

If any reference exists, leave the heading exactly as it is.

If none exists, shorten it.

Every kind of reference blocks a rename:

- wikilinks from other notes, such as `[[note#Heading]]`
- links within the same note, such as `[[#Heading]]`
- embeds, such as `![[note#Heading]]`
- markdown-style links, such as `[text](note.md#Heading%20with%20spaces)`

Search once for all of them with a single `rg` invocation per heading, case-insensitive and fixed-string.

Search for `#` followed by the heading text, and again for the same text with spaces written as `%20`.

Obsidian matches heading links case-insensitively, so the search must be case-insensitive too.

A nested reference such as `[[note#Parent#Child]]` still contains `#Child`, so it is caught.

Headings are matched on their text, not their level, so demoting a heading to nest it does not break links.

Adding a new heading breaks nothing.

## Steps

1. Read the note.
2. Remove any table-of-contents block.
3. List every heading and note any text that sits outside a section.
4. Add short headings for text outside any section.
5. Move the abstract to the first section.
6. Nest dated and repeated entries under one parent heading.
7. For each long existing heading, run the link search, then shorten it only if no reference exists.
8. Re-read the note and confirm that no body text sits above the first heading and that no heading change broke a link.
9. Commit only that note with `git commit -- <path>`, because background processes also commit to the vault.

## Note conventions that still apply

Follow the vault conventions in /Users/mtm/Documents/Obsidian Vault/CLAUDE.md.

Never use italics, bold, or emphasis in a note.

Each sentence is its own paragraph.

Do not reformat anything else in the note.

If a heading blocks a rename because of a link, report that heading in the final summary so the user can decide.
