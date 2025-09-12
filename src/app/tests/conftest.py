import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ.setdefault("DB_URL", f"sqlite:///{ROOT}/src/app/db.sqlite3")
os.environ.setdefault("JWT_SECRET", "fJJZNs9LnU356LmyTQA8")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("IMAGE_URL", f"{ROOT}/shelf/public/images")
