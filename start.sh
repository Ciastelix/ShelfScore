#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

source "$PROJECT_ROOT/.venv/bin/activate"

export DB_URL="sqlite:///${PROJECT_ROOT}/src/app/db.sqlite3"
export JWT_SECRET="fJJZNs9LnU356LmyTQA8"
export JWT_ALGORITHM="HS256"
export IMAGE_URL="${PROJECT_ROOT}/shelf/public/images/"

cd "$PROJECT_ROOT/src"
uvicorn app.main:app --port 8000 --reload --reload-dir "$PROJECT_ROOT/src/app"