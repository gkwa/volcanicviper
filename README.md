# volcanicviper

TLDR: https://github.com/gkwa/volcanicviper

```
pnpm dlx skills add gkwa/volcanicviper --global
```

Personal agent skills for Claude Code and compatible AI tools.

Skills encode reusable expertise so AI assistants apply consistent standards without repeated correction.

## Skills

- `chrome-extension-multiple-entry-points` — build Chrome extensions with separate Vite configs per entry point to avoid code-splitting issues
- `instagram-to-imgur` — download an Instagram post thumbnail and upload it to Imgur for a permanent URL
- `justfile` — create a justfile with standard setup/test/teardown rules to orchestrate project tasks
- `logging-to-stderr` — set up --verbose flag logging that sends output to stderr (stdout for Chrome extensions)
- `pnpm` — use pnpm instead of npm for package management
- `python-package` — scaffold a new Python package with pyproject.toml, hatchling, ruff, and --version support
- `research-note` — create a cleaned research note from a rough question with an answer and search links
- `return-early-pattern` — apply guard clauses and early returns to reduce nesting and improve readability
- `silence-is-golden` — follow the Unix rule of silence, producing no output on the happy path
- `solid-principles` — write code following SOLID design principles with small focused files
- `txtar` — present multi-file code changes in txtar format as a single code block
- `use-vite` — set up Vite/Vitest with ESM config and vite-plugin-checker for TypeScript projects
- `view-imgur` — fetch and view imgur images via curl when WebFetch is blocked
- `write-readme` — write brief READMEs with a CLI cheatsheet

## Install from GitHub

<!-- install all skills globally -->
```
pnpm dlx skills add gkwa/volcanicviper --global
```

Skills install to `~/.agents/skills/` with symlinks in `~/.claude/skills/`.

## Local testing

<!-- symlink skills into ~/.agents/skills/ for local testing -->
```
just install
```

<!-- remove symlinks when done -->
```
just uninstall
```

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
