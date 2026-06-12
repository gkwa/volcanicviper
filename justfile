default:
    just --list

# Symlink local skills into ~/.agents/skills/ for local testing
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    for skill_dir in skills/*/; do
        name=$(basename "$skill_dir")
        target="$HOME/.agents/skills/$name"
        rm -rf "$target"
        ln -s "$(pwd)/skills/$name" "$target"
    done

install: setup

# Verify all local skills are symlinked
test:
    #!/usr/bin/env bash
    set -euo pipefail
    failed=0
    for skill_dir in skills/*/; do
        name=$(basename "$skill_dir")
        target="$HOME/.agents/skills/$name"
        if [ ! -L "$target" ]; then
            echo "missing symlink: $target"
            failed=1
        fi
    done
    exit $failed

# Remove symlinks from ~/.agents/skills/
teardown:
    #!/usr/bin/env bash
    set -euo pipefail
    for skill_dir in skills/*/; do
        name=$(basename "$skill_dir")
        target="$HOME/.agents/skills/$name"
        if [ -L "$target" ]; then
            rm "$target"
        fi
    done

uninstall: teardown
