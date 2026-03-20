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

1. The cleaned question — no label, no header, just the question text at the very top of the file
2. `## Answer` section
3. `## Search links` section

Formatting rules:

- Each sentence is its own paragraph, separated by a blank line
- No italics, bold, or emphasis anywhere in the file
- Bullet points for all lists
- File ends with a trailing newline

### Step 5: Write the Answer section

Write a direct answer under `## Answer`.

Each sentence is its own paragraph.

The answer is your best understanding — the search links exist for the user to verify and extend it.

### Step 6: Write the Search links section

Add 4–6 Google search links under `## Search links` as a bulleted list.

Each link approaches the question from a different angle.

Link text should describe what kind of result to expect.

URL format: `https://www.google.com/search?q=search+terms+separated+by+plus+signs`

### Step 7: Commit

Commit each file to git immediately after creating or updating it.

Commit after each file individually so changes can be reverted one at a time.

Write a short, imperative commit message.

Do not prompt the user before committing.

### Step 8: Handle follow-up additions

If the user points out a missing question or sub-question, add it to the appropriate file and commit again without prompting.
