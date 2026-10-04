# volcanicviper

TLDR: https://github.com/gkwa/volcanicviper

```
pnpm dlx skills add gkwa/volcanicviper --global
```

Personal agent skills for Claude Code and compatible AI tools.

Skills encode reusable expertise so AI assistants apply consistent standards without repeated correction.

## Skills

- `chrome-extension-multiple-entry-points` — build Chrome extensions with separate Vite configs per entry point to avoid code-splitting issues
- `distinctdeer` — claim an unused project name and create an empty git repo for it under the project root
- `grafana-bake-annotation` — extract annotatable events from a Zephyr bake log, run the Grafana annotation CLI, and write the command into the bake log
- `social-to-imgur` — download a social media post thumbnail (Instagram, Facebook, or any yt-dlp-supported platform) and upload it to Imgur for a permanent URL
- `islandiguana` — search the Obsidian vault by YAML front matter using islandiguana and yq expressions
- `justfile` — create a justfile with standard setup/test/teardown rules to orchestrate project tasks
- `outline-headings` — reformat a vault note so every line sits under a short heading for Obsidian Outline: remove the TOC, head orphan text, move the abstract first, nest dated entries, and shorten long headings nothing links to
- `pnpm` — use pnpm instead of npm for package management
- `python-package` — scaffold a new Python package with pyproject.toml, hatchling, ruff, and --version support
- `research-note` — create a cleaned research note from a rough question with an answer and search links
- `thesourdoughjourney-method-check` — judge whether Tom Cucuzza's two-factor bulk fermentation method (from The Sourdough Journey) fits a sourdough recipe, and which way the error swings if not
- `transcript-cleanup` — clean up raw transcripts from output/ and write to a timestamped file in cleaned/
- `transcribe-voice-memos` — run the valorousverdin pipeline end to end: transcribe the waiting recordings, route the Zephyr and Fulcrum entries into the vault, and leave the cleaned transcripts on the clipboard
- `tsconfig` — add a tsconfig.json for TypeScript projects using Vite and/or Chrome extensions
- `use-vite` — set up Vite/Vitest with ESM config and vite-plugin-checker for TypeScript projects
- `view-imgur` — fetch and view imgur images via curl when WebFetch is blocked
- `voice-memo-triage` — take the newest N entries in the aggregate voice memo file, turn the ones that are questions into research notes, and remove exactly those entries with byte accounting proving nothing was lost
- `write-readme` — write brief READMEs with a CLI cheatsheet
- `zephyr` — the Zephyr sourdough bake tagging scheme: find bake logs by Zephyr key, read entries to extract event times, add event_time tags, and fill the Starter peak duration block
- `zephyr-grafana-links` — build or refresh the overall and bulk ferment Grafana dashboard links in a bake log
- `zephyr-routing` — route Zephyr entries from any document to their proper bake logs, deduplicated and in reverse chronological order

## Triggering a skill

A skill fires on its `description` frontmatter, which is the only part loaded into the agent's context.

The phrasings below are examples of what reaches `distinctdeer`, not a list the agent consults:

- Let's create a new project
- Start a new project
- Set up a fresh project directory
- I need a name for a new project
- Claim a project name
- Give me a project name and a repo for it
- Make a new repo under the project root

Any wording that names starting a project, needing a project name, or creating a project directory reaches it.

The phrasings below are examples of what reaches `outline-headings`, each naming a note by its absolute path:

- Run outline-headings on /Users/mtm/Documents/Obsidian Vault/your kitchen lab easy sourdough crepes.md
- Use the outline-headings skill on this note
- Outline-headings this note
- Fix the outline of this note
- Fix the outline of /Users/mtm/Documents/Obsidian Vault/your kitchen lab easy sourdough crepes.md
- Clean up the outline for this note
- Make this note outline-friendly
- Make this note work with Obsidian Outline
- Make this note easier to navigate in the outline sidebar
- Get this note ready for outline mode
- I rely on Obsidian Outline now, update this note for it
- Remove the TOC from this note
- Remove the table of contents from this note
- Delete the table-of-contents block in this note
- I don't need the TOC in this note anymore
- This note still has a TOC, get rid of it
- Strip the table of contents and fix the headings
- Shorten the headings in this note
- The headings in this note wrap in the sidebar, shorten them
- Make the section headings in this note shorter
- Tighten up the headings in this note
- Rename the long headings in this note if nothing links to them
- Put everything in this note under a section
- Make sure everything in this note is within a section
- This note has text above the first heading, give it a section
- Add a heading for the stuff at the top of this note
- Find text that is not in any section and give it a heading
- Give the intro of this note a heading
- Move the abstract to the top of this note
- Put the abstract in the first section
- Make the first section the reason I would read this note
- Let me jump to the abstract from the outline
- Let me jump to the motivating question from the outline
- Nest the dated entries in this note under one heading
- Put the cook log entries under a single parent heading
- Group the dated sections in this note under one section
- Fix the heading levels in this note so the log collapses
- Reformat this note for the outline
- Reformat the headings in this note
- Restructure this note so the outline works
- Do the outline pass on this note
- Run the outline pass on every note I name
- Apply the outline policy to this note
- Check this note against the outline rules
- Which headings in this note can be shortened without breaking links
- Check whether anything links to the headings in this note, then shorten them
- Do the outline cleanup on the note I have open
- Do the outline cleanup on the note I just edited

Any wording that names the Outline sidebar, a table of contents to remove, or text sitting outside a section reaches it.

## Install from GitHub

<!-- install all skills globally -->
```
pnpm dlx skills add gkwa/volcanicviper --global
```

Skills install to `~/.agents/skills/` with symlinks in `~/.claude/skills/`.

## Update

<!-- check for updates -->
```
pnpm dlx skills check
```

<!-- apply updates -->
```
pnpm dlx skills update
```

## Skill structure

Each skill is a folder containing:

```
skills/<name>/
├── SKILL.md     # instructions and trigger terms
└── tile.json    # metadata for the skills CLI installer
```
