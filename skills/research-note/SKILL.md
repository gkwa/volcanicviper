---
name: research-note
description: Create a research note from a rough question. Cleans the question, splits into separate files if multiple questions, adds an answer and Google search links. Use when the user has a question they want documented as a note.
---

## Research Note Workflow

When the user gives you a rough question to document as a research note, follow these steps exactly.

### Step 1: Clean the question

Rewrite the question so it is clear, precise, and self-contained enough to copy-paste into any LLM.

Rules:

- Remove references to prior conversation or context another model would not have — inline any necessary background
- Remove ambiguity — choose the most likely reading or restructure
- Fix grammar, spelling, and punctuation
- Use plain, direct language — cut filler words
- Each sentence of the question is its own paragraph, separated by a blank line
- Do not answer the question during this step

### Step 2: Count distinct questions

If the input contains multiple independently answerable questions, split them — one file per question.

Two questions are distinct if they address different aspects of the topic and can be answered without reference to each other.

### Step 3: Name and create the file

Filename rules:

- All lowercase
- Words separated by spaces, not hyphens or underscores
- Descriptive of the specific question
- Extension `.md`

Example: `lamination fold what builds strength.md`

### Step 4: Write the file

Structure:

1. YAML frontmatter with `tags: [voice-memo-research]`
2. A context block (if the source file contains Obsidian wikilinks) — preserve any `[[wikilinks]]` verbatim before the question text
3. The cleaned question — no label, no header, just the question text
4. `## Answer` section
5. `## Search links` section
6. `## Original request` section

Formatting rules:

- Each sentence is its own paragraph, separated by a blank line
- No italics, bold, or emphasis anywhere in the file
- Bullet points for all lists
- File ends with a trailing newline

Frontmatter format:

```
---
tags:
  - voice-memo-research
---
```

### Step 5: Write the Answer section

Write a direct answer under `## Answer`.

Each sentence is its own paragraph.

The answer is your best understanding — the search links exist for the user to verify and extend it.

### Step 6: Write the Search links section

Add 4–6 Google search links under `## Search links` as a bulleted list.

Each link approaches the question from a different angle.

Every entry must be a clickable markdown link, never a bare URL.

Format each bullet as `- [descriptive link text](https://www.google.com/search?q=search+terms+separated+by+plus+signs)`.

The link text describes what kind of result to expect, and is never the URL itself.

Search terms in the URL are separated by plus signs.

This is a deliberate exception to the general vault convention that URLs sit bare on their own line for Obsidian to auto-link.

Example:

```
## Search links

- [clinical term for coughing triggered by swallowing](https://www.google.com/search?q=coughing+while+eating+medical+term+oropharyngeal+dysphagia)
- [how penetration and aspiration differ](https://www.google.com/search?q=laryngeal+penetration+vs+aspiration+difference)
```

Before finishing the file, reread the `## Search links` section and confirm every bullet uses the bracket-and-parenthesis form.

### Step 7: Write the Original request section

Append a `## Original request` section at the bottom of the note containing the verbatim original content of the source file.

Do not discard any text from the source file, even if it looks like stray wikilinks, copied text, or app-generated messages.

The user may have collected that content intentionally as context or raw material, even if it does not look like a clean question.

### Step 8: Delete the source file

After creating all research note files, delete the original source file the question came from.

Do not prompt the user before deleting.

Commit the deletion immediately after, before proceeding.

### Step 9: Commit

Commit each file to git immediately after creating or updating it.

Commit after each file individually so changes can be reverted one at a time.

Write a short, imperative commit message.

Do not prompt the user before committing.

### Step 10: Handle follow-up additions

If the user points out a missing question or sub-question, add it to the appropriate file and commit again without prompting.
