#!/usr/bin/env bash
# Regenerate the student exercises from the solutions submodule and report what
# needs committing, in which repository.
#
#   pixi run sync-solutions
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"
SOLUTIONS=.course/solutions

if [ ! -e "$SOLUTIONS/python" ]; then
    echo "$SOLUTIONS/ is empty - run: git submodule update --init" >&2
    exit 1
fi

echo "== regenerating exercises =="
pixi run make-exercises || exit 1

echo
echo "== solutions repo =="
if [ -n "$(git -C "$SOLUTIONS" status --porcelain)" ]; then
    git -C "$SOLUTIONS" status --short
    echo "  -> commit and push inside $SOLUTIONS/ FIRST"
else
    echo "  clean"
fi

echo
echo "== course repo =="
if [ -n "$(git status --porcelain)" ]; then
    git status --short
    if git status --porcelain | grep -q "^.M $SOLUTIONS"; then
        echo "  -> '$SOLUTIONS' shown as modified means the submodule pointer moved."
        echo "     Commit it here AFTER pushing inside $SOLUTIONS/."
    fi
else
    echo "  clean"
fi
