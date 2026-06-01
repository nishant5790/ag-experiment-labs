"""Discovery Team — Paper Search + Citation Graph + Trend Analysis.

Prompt config lives in prompts/teams/discovery.yml.
"""
import asyncio

from research_agent.agents import (
    search_agent_ag,
    citation_graph_agent_ag,
    trend_analysis_agent_ag,
)
from research_agent.teams._base import build_team


discovery_team = build_team(
    prompt_name="discovery",
    members=[
        search_agent_ag,
        citation_graph_agent_ag,
        trend_analysis_agent_ag,
    ],
)


if __name__ == "__main__":
    asyncio.run(discovery_team.aprint_response(
        "graph neural networks for drug discovery", stream=True))
