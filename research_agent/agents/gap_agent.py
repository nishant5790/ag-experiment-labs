"""Gap Detection Agent — identifies open problems in the literature.

Prompt config lives in prompts/agents/gap_detection.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, openalex_tool


gap_agent_ag = build_agent(
    prompt_name="gap_detection",
    tools=[semantic_scholar_tool, openalex_tool],
)


if __name__ == "__main__":
    asyncio.run(gap_agent_ag.aprint_response(
        "Identify research gaps in 'graph neural networks for drug discovery'.",
        stream=True,
    ))
