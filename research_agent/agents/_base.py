"""Shared helper for building Agents — sources settings from configs/."""
from __future__ import annotations

import os
import sys
from typing import Iterable, Optional

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from agno.agent import Agent

from research_agent.configs import agent_config, make_db, make_model
from research_agent.prompts import load_prompt


def build_agent(
    prompt_name: str,
    tools: Optional[Iterable] = None,
    output_schema=None,
) -> Agent:
    """Build an Agent from prompts/agents/<prompt_name>.yml + configs/."""
    p = load_prompt("agents", prompt_name)
    cfg = agent_config(prompt_name)
    a = cfg.get("agent", {})

    return Agent(
        name=p["name"],
        role=p.get("role"),
        description=p.get("description"),
        instructions=list(p.get("instructions", [])),
        model=make_model(cfg["model"]),
        db=make_db(cfg["db"], scope="agent", name=prompt_name),
        tools=list(tools) if tools else None,
        output_schema=output_schema,
        use_json_mode=a.get("use_json_mode", False),
        structured_outputs=a.get("structured_outputs", False),
        markdown=a.get("markdown", True),
        stream_events=a.get("stream_events", True),
    )
