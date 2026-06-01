"""Comparison Matrix Agent — builds side-by-side method comparisons.

Prompt config lives in prompts/agents/comparison_matrix.yml.
"""
import asyncio

from research_agent.agents._base import build_agent


matrix_agent_ag = build_agent(
    prompt_name="comparison_matrix",
    tools=None,
)


if __name__ == "__main__":
    asyncio.run(matrix_agent_ag.aprint_response(
        "Build a comparison matrix of three transformer-based summarization models.",
        stream=True,
    ))
