"""Evaluation Agent — defines metrics, benchmarks, and pitfalls per experiment.

Prompt config lives in prompts/agents/evaluation.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import paperswithcode_tool, semantic_scholar_tool


evaluation_agent_ag = build_agent(
    prompt_name="evaluation",
    tools=[paperswithcode_tool, semantic_scholar_tool],
)


if __name__ == "__main__":
    asyncio.run(evaluation_agent_ag.aprint_response(
        "Define an evaluation methodology for code-generation language models.",
        stream=True,
    ))
