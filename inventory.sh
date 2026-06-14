#!/bin/bash
echo "# Sovereign Vedic AGI - Repository Inventory"
echo ""
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "## ${repo%/}"
        echo "- Files: $(find "$repo" -type f -name "*.py" 2>/dev/null | wc -l) Python files"
        echo "- Size: $(du -sh "$repo" 2>/dev/null | cut -f1)"
        if [ -f "$repo/README.md" ]; then
            echo "- Has README: Yes"
        fi
        if [ -f "$repo/setup.py" ] || [ -f "$repo/pyproject.toml" ]; then
            echo "- Installable: Yes"
        fi
        echo ""
    fi
done
