#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "Project virtual environment not found: $PYTHON" >&2
    exit 1
fi

exec "$PYTHON" -m behave --no-capture "$SCRIPT_DIR/features" "$@"
