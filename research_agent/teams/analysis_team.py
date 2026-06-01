"""Analysis Team — Paper Parser + Comparison Matrix + Contradiction + SWOT.

Prompt config lives in prompts/teams/analysis.yml.
"""
import asyncio

from research_agent.agents import (
    parser_agent_ag,
    matrix_agent_ag,
    contradiction_agent_ag,
    swot_agent_ag,
)
from research_agent.teams._base import build_team


analysis_team = build_team(
    prompt_name="analysis",
    members=[
        parser_agent_ag,
        matrix_agent_ag,
        contradiction_agent_ag,
        swot_agent_ag,
    ],
)


if __name__ == "__main__":
    asyncio.run(analysis_team.aprint_response(
        "Analyze recent papers on retrieval-augmented generation.", stream=True))
