import os
import re
from typing import Set

from dotenv import load_dotenv

load_dotenv()

ALLOWED_LABELS: Set[str] = {
    "frontend",
    "backend",
    "ui",
    "validation",
    "authentication",
    "documentation",
    "testing",
}


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta a variável de ambiente: {name}")
    return value


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text