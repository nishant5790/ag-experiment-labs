"""Innovation Team — Gap Detection + Novel Idea + Cross-Domain Innovation.

Prompt config lives in prompts/teams/innovation.yml.
"""
import asyncio

from research_agent.agents import (
    gap_agent_ag,
    idea_agent_ag,
    cross_domain_agent_ag,
)
from research_agent.teams._base import build_team


innovation_team = build_team(
    prompt_name="innovation",
    members=[
        gap_agent_ag,
        idea_agent_ag,
        cross_domain_agent_ag,
    ],
)


if __name__ == "__main__":
    asyncio.run(innovation_team.aprint_response(
        "Generate research innovations for 'small language models on edge devices'.",
        stream=True,
    ))
