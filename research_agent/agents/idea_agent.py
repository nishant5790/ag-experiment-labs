"""Novel Idea Agent — generates concrete novel research ideas.

Prompt config lives in prompts/agents/novel_idea.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, openalex_tool


idea_agent_ag = build_agent(
    prompt_name="novel_idea",
    tools=[semantic_scholar_tool, openalex_tool],
)


if __name__ == "__main__":
    asyncio.run(idea_agent_ag.aprint_response(
        "Propose 3 novel research ideas for federated learning on small edge devices.",
        stream=True,
    ))
