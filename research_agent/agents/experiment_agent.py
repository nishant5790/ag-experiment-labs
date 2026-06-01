"""Experiment Design Agent — produces detailed experimental protocols.

Prompt config lives in prompts/agents/experiment_design.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, paperswithcode_tool


experiment_agent_ag = build_agent(
    prompt_name="experiment_design",
    tools=[semantic_scholar_tool, paperswithcode_tool],
)


if __name__ == "__main__":
    asyncio.run(experiment_agent_ag.aprint_response(
        "Design an experiment comparing LoRA vs full fine-tuning on a small reasoning benchmark.",
        stream=True,
    ))
