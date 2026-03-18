# volcanicviper

TLDR: https://github.com/gkwa/volcanicviper

```
pnpm dlx skills add gkwa/volcanicviper --global
```

Personal agent skills for Claude Code and compatible AI tools.

Skills encode reusable expertise so AI assistants apply consistent standards without repeated correction.

## Skills

- `python-package` — scaffold a new Python package with pyproject.toml, hatchling, ruff, and --version support
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
