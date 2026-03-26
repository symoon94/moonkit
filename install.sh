#!/bin/bash
# moonkit skill installer
# Symlinks skills from this repo into your project's .claude/skills/ directory.
#
# Usage:
#   ./install.sh                    # install to current directory
#   ./install.sh /path/to/project   # install to specific project
#   ./install.sh --global           # install to ~/.claude/skills/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

# Parse target
TARGET=""
if [[ "${1:-}" == "--global" ]]; then
    TARGET="$HOME/.claude/skills"
elif [[ -n "${1:-}" ]]; then
    TARGET="$1/.claude/skills"
else
    TARGET="$(pwd)/.claude/skills"
fi

# Validate source
if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "Error: skills/ directory not found at $SKILLS_SRC"
    exit 1
fi

# Create target directory
mkdir -p "$TARGET"

# Install each skill
installed=0
for skill_dir in "$SKILLS_SRC"/*/; do
    skill_name="$(basename "$skill_dir")"
    target_link="$TARGET/$skill_name"

    if [[ -L "$target_link" ]]; then
        # Already a symlink — update it
        rm "$target_link"
        ln -s "$skill_dir" "$target_link"
        echo "  updated: $skill_name -> $skill_dir"
    elif [[ -d "$target_link" ]]; then
        echo "  skipped: $skill_name (directory exists, use --force to overwrite)"
        if [[ "${2:-}" == "--force" || "${1:-}" == "--force" ]]; then
            rm -rf "$target_link"
            ln -s "$skill_dir" "$target_link"
            echo "  forced:  $skill_name -> $skill_dir"
        else
            continue
        fi
    else
        ln -s "$skill_dir" "$target_link"
        echo "  linked:  $skill_name -> $skill_dir"
    fi
    ((installed++))
done

echo ""
echo "Done. $installed skill(s) installed to $TARGET"
echo ""
echo "Available skills:"
for skill_dir in "$SKILLS_SRC"/*/; do
    skill_name="$(basename "$skill_dir")"
    echo "  /$skill_name"
done
