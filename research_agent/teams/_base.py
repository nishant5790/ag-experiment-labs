"""Shared helper for building Teams — sources settings from configs/."""
from __future__ import annotations

import os
import sys
from typing import List

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agno.agent import Agent
from agno.team import Team

from research_agent.configs import make_db, make_model, team_config
from research_agent.prompts import load_prompt


def build_team(prompt_name: str, members: List[Agent]) -> Team:
    """Build a Team from prompts/teams/<prompt_name>.yml + configs/."""
    p = load_prompt("teams", prompt_name)
    cfg = team_config(prompt_name)
    t = cfg.get("team", {})

    return Team(
        name=p["name"],
        members=members,
        model=make_model(cfg["model"]),
        db=make_db(cfg["db"], scope="team", name=prompt_name),
        description=p.get("description"),
        instructions=list(p.get("instructions", [])),
        markdown=t.get("markdown", True),
        stream_events=t.get("stream_events", True),
        add_datetime_to_context=t.get("add_datetime_to_context", True),
        add_member_tools_to_context=t.get("add_member_tools_to_context", False),
    )
