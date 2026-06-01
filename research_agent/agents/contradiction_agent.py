"""Contradiction Agent — surfaces disagreements across papers.

Prompt config lives in prompts/agents/contradiction.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, openalex_tool


contradiction_agent_ag = build_agent(
    prompt_name="contradiction",
    tools=[semantic_scholar_tool, openalex_tool],
)


if __name__ == "__main__":
    asyncio.run(contradiction_agent_ag.aprint_response(
        "Find contradictions across recent papers on chain-of-thought prompting.",
        stream=True,
    ))
