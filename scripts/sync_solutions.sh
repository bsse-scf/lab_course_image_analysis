#!/usr/bin/env bash
# Regenerate the student exercises from the solutions submodule and report what
# needs committing, in which repository.
#
#   pixi run sync-solutions
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if [ ! -e solutions/python ]; then
    echo "solutions/ is empty - run: git submodule update --init" >&2
    exit 1
fi

echo "== regenerating exercises =="
pixi run make-exercises || exit 1

echo
echo "== solutions repo =="
if [ -n "$(git -C solutions status --porcelain)" ]; then
    git -C solutions status --short
    echo "  -> commit and push inside solutions/ FIRST"
else
    echo "  clean"
fi

echo
echo "== course repo =="
if [ -n "$(git status --porcelain)" ]; then
    git status --short
    if git status --porcelain | grep -q '^.M solutions'; then
        echo "  -> 'solutions' shown as modified means the submodule pointer moved."
        echo "     Commit it here AFTER pushing inside solutions/."
    fi
else
    echo "  clean"
fi
