"""Results Writer — writes the Results & Discussion section.

Prompt config lives in prompts/agents/results_writer.yml.
"""
import asyncio

from research_agent.agents._base import build_agent


results_writer_ag = build_agent(
    prompt_name="results_writer",
    tools=None,
)


if __name__ == "__main__":
    asyncio.run(results_writer_ag.aprint_response(
        "Write a Results section comparing our method against three baselines on HumanEval.",
        stream=True,
    ))
