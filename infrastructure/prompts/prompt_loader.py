from __future__ import annotations

from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(prompt_filename: str) -> str:
    prompt_path = PROMPTS_DIR / prompt_filename
    return prompt_path.read_text(encoding="utf-8")

