"""SWOT Agent — produces a SWOT analysis of a research area.

Prompt config lives in prompts/agents/swot.yml.
"""
import asyncio

from research_agent.agents._base import build_agent


swot_agent_ag = build_agent(
    prompt_name="swot",
    tools=None,
)


if __name__ == "__main__":
    asyncio.run(swot_agent_ag.aprint_response(
        "SWOT analysis for the field of speech-to-text foundation models.",
        stream=True,
    ))
