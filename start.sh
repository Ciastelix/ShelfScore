#!/bin/bash
source ./.venv/bin/activate

cd ./src/app

export DB_URL="sqlite:///./db.sqlite3"
export JWT_SECRET="fJJZNs9LnU356LmyTQA8"
export JWT_ALGORITHM="HS256"


uvicorn main:app --reload