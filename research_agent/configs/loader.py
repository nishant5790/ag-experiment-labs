"""Centralized config loader for agents, teams, and workflows.

Defaults live in configs/defaults.yml. Per-component overrides live in
configs/<scope>.yml (scope ∈ {agents, teams, workflows}) keyed by the
component's prompt_name.

Public API:
    agent_config(name)      -> dict {model, db, agent}
    team_config(name)       -> dict {model, db, team}
    workflow_config(name)   -> dict {db, workflow}
    make_model(cfg["model"])
    make_db(cfg["db"], scope, name)
"""
from __future__ import annotations

import os
from copy import deepcopy
from functools import lru_cache
from typing import Any, Dict

import yaml

_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CONFIG_DIR, "../../"))


def _read_yaml(path: str) -> Dict[str, Any]:
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive dict merge — override wins; nested dicts merged, not replaced."""
    out = deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


@lru_cache(maxsize=1)
def _defaults() -> Dict[str, Any]:
    return _read_yaml(os.path.join(_CONFIG_DIR, "defaults.yml"))


@lru_cache(maxsize=None)
def _scope_overrides(scope: str) -> Dict[str, Any]:
    return _read_yaml(os.path.join(_CONFIG_DIR, f"{scope}.yml"))


def _component_config(scope: str, name: str) -> Dict[str, Any]:
    overrides = _scope_overrides(scope).get(name, {}) or {}
    return _deep_merge(_defaults(), overrides)


def agent_config(name: str) -> Dict[str, Any]:
    return _component_config("agents", name)


def team_config(name: str) -> Dict[str, Any]:
    return _component_config("teams", name)


def workflow_config(name: str) -> Dict[str, Any]:
    return _component_config("workflows", name)


# ---------- factories ----------

def make_model(model_cfg: Dict[str, Any]):
    provider = (model_cfg.get("provider") or "google").lower()
    model_id = model_cfg.get("id")
    kwargs: Dict[str, Any] = {"id": model_id}
    if model_cfg.get("temperature") is not None:
        kwargs["temperature"] = model_cfg["temperature"]

    if provider == "google":
        from agno.models.google import Gemini
        return Gemini(**kwargs)
    if provider == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(**kwargs)
    if provider == "anthropic":
        from agno.models.anthropic import Claude
        return Claude(**kwargs)
    raise ValueError(f"Unsupported model provider: {provider}")


def make_db(db_cfg: Dict[str, Any], scope: str, name: str):
    db_type = (db_cfg.get("type") or "sqlite").lower()
    if db_type != "sqlite":
        raise ValueError(f"Unsupported db type: {db_type}")

    from agno.db.sqlite import SqliteDb

    db_file = db_cfg.get("file", "research_agent/storage/research_agent.db")
    if not os.path.isabs(db_file):
        db_file = os.path.join(_PROJECT_ROOT, db_file)
    os.makedirs(os.path.dirname(db_file), exist_ok=True)

    return SqliteDb(
        db_file=db_file,
        session_table=f"{scope}_{name}_session",
    )
