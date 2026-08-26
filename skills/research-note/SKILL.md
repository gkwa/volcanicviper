---
name: research-note
description: Create a research note from a rough question. Cleans the question, splits into separate files if multiple questions, records the source URL, and adds answers with Google search links per topic. Also covers adding follow-up questions to an active research note. Use when the user has a question they want documented as a note.
---

## Research Note Workflow

When the user gives you a rough question to document as a research note, follow these steps exactly.

### Step 0: Check for the cooking how-to exception

A how-to note about cooking or roasting is not a research note.

Use the [[recipe-cleanup]] format instead: YAML frontmatter with `tags: recipe`, ingredients as checked checkboxes with wikilinks, a Prep section, and instructions as plain paragraphs that start lowercase, carry no trailing period, and give each sentence its own paragraph.

Omit the creator, pic, and source fields when there is no external source.

The rest of these steps do not apply in that case.

### Step 1: Clean the question

Rewrite the question so it is clear, precise, and self-contained enough to copy-paste into any LLM.

Rules:

- Remove references to prior conversation or context another model would not have — inline any necessary background
- Remove ambiguity — choose the most likely reading or restructure
- Fix grammar, spelling, and punctuation
- Use plain, direct language — cut filler words
- Each sentence of the question is its own paragraph, separated by a blank line
- Define scope — narrow a question too broad to answer usefully, widen one too narrow to stand alone
- Separate the parts clearly when the question has more than one
- Do not answer the question during this step

Preserve the motivating context rather than reducing the question to an abstract one.

Keep named examples, specific tools, proposed workflows, and stated constraints.

The goal is clarity and portability, not brevity at the cost of the concrete detail that makes the note useful months later.

These rewriting rules are duplicated in the question-cleanup command, at /Users/mtm/.claude/commands/question-cleanup.md, which is generated from the chezmoi template command-question-cleanup. This skill keeps its own copy because it installs onto machines with no copy of that commands directory. Change both together.

### Step 2: Count distinct questions

If the input contains multiple independently answerable questions, split them — one file per question.

Two questions are distinct if they address different aspects of the topic and can be answered without reference to each other.

### Step 3: Name the file by renaming the source

Rename the source file to the descriptive target name rather than creating a new file and deleting the old one.

Renaming treats the source as the same artifact being refined, and it keeps git history on tracked files.

Use `git mv "Untitled NNNN.md" "descriptive name.md"` for git-tracked files, or `mv` for untracked ones, then write the note content into the renamed file in place.

Filename rules:

- All lowercase
- Words separated by spaces, not hyphens or underscores
- Descriptive of the specific question
- Extension `.md`

Example: `lamination fold what builds strength.md`

When Step 2 produced more than one note, only one of them can be the renamed source; create the rest as new files and see Step 9.

### Step 4: Write the file

Structure:

1. YAML frontmatter with `tags: [voice-memo-research]`
2. A context block (if the source file contains Obsidian wikilinks) — preserve any `[[wikilinks]]` verbatim before the question text
3. The cleaned question — no label, no header, just the question text
4. `## Source` section, when a URL was provided
5. One `##` section per topic, each holding its own answer and search links
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

### Step 5: Write the Source section

Record the URL where the user encountered the topic — the article, newsletter, or page they were reading, not the project's own homepage or source repository.

The point is to be able to return to the original context and re-read it.

Skip this section only when no URL was part of the request.

### Step 6: Write one section per topic

Give each distinct angle or sub-topic its own `##` section, named for that angle.

Examples of section names: `## Conflict of interest`, `## Cost comparison`, `## Alternatives`, `## Online sentiment`.

Write the answer content for that angle in the section, each sentence its own paragraph.

The answer is your best understanding — the search links exist for the user to verify and extend it.

Put that angle's search links at the bottom of its own section.

Never collect every link into a single `## Search links` block at the end of the note.

Per-section links let any one section grow later without spawning a new document that links back to this one.

A note that genuinely covers a single angle has a single section, which is fine.

### Step 7: Format the search links

Add 4–6 Google search links per section as a bulleted list.

Each link approaches that section's topic from a different angle.

Every entry must be a clickable markdown link, never a bare URL.

Format each bullet as `- [descriptive link text](https://www.google.com/search?q=search+terms+separated+by+plus+signs)`.

The link text describes what kind of result to expect, and is never the URL itself.

Search terms in the URL are separated by plus signs.

This is a deliberate exception to the general vault convention that URLs sit bare on their own line for Obsidian to auto-link.

Example:

```
## Swallowing and coughing

- [clinical term for coughing triggered by swallowing](https://www.google.com/search?q=coughing+while+eating+medical+term+oropharyngeal+dysphagia)
- [how penetration and aspiration differ](https://www.google.com/search?q=laryngeal+penetration+vs+aspiration+difference)
```

Before finishing the file, reread every section's links and confirm each bullet uses the bracket-and-parenthesis form.

### Step 8: Write the Original request section

Append a `## Original request` section at the bottom of the note containing the verbatim original content of the source file.

Do not discard any text from the source file, even if it looks like stray wikilinks, copied text, or app-generated messages.

The user may have collected that content intentionally as context or raw material, even if it does not look like a clean question.

### Step 9: Delete the source file only when splitting

A single research note needs no deletion, because Step 3 renamed the source into the note.

When Step 2 split the input across several notes, the source cannot be renamed into all of them, so delete it after every output file is committed.

Do not prompt the user before deleting.

Commit the deletion immediately after, before proceeding.

### Step 10: Commit

Commit each file to git immediately after creating or updating it.

Commit after each file individually so changes can be reverted one at a time.

Write a short, imperative commit message.

Do not prompt the user before committing.

### Step 11: Handle follow-up questions

Any time the user asks a question during a research conversation, add it to the active note as a new `##` header phrased as the question, with the answer in the body below it.

Do this immediately, and never ask whether to update the note.

A header rather than a loose paragraph gives the question room to grow when more context arrives later.

Commit after each such addition, following Step 10.

The same applies when the user points out a missing question or sub-question — add it to the appropriate file and commit without prompting.
