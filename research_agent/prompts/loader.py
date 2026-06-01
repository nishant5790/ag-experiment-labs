"""Simple YAML prompt loader.

Each prompt file lives under prompts/<kind>/<name>.yml and contains:
    name: str
    role: str
    description: str
    instructions:
      - str
      - ...

Usage:
    from research_agent.prompts import load_prompt
    p = load_prompt("agents", "search")
    Agent(name=p["name"], role=p["role"], description=p["description"],
          instructions=p["instructions"], ...)
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict

import yaml

_PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def load_prompt(kind: str, name: str) -> Dict[str, Any]:
    """Load a prompt YAML file from prompts/<kind>/<name>.yml."""
    path = os.path.join(_PROMPTS_DIR, kind, f"{name}.yml")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Normalize defaults
    data.setdefault("instructions", [])
    return data
