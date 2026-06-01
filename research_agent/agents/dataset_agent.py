"""Dataset Agent — recommends datasets for proposed research ideas.

Prompt config lives in prompts/agents/dataset.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import (
    huggingface_tool,
    paperswithcode_tool,
    kaggle_tool,
)


dataset_agent_ag = build_agent(
    prompt_name="dataset",
    tools=[huggingface_tool, paperswithcode_tool, kaggle_tool],
)


if __name__ == "__main__":
    asyncio.run(dataset_agent_ag.aprint_response(
        "Recommend datasets for evaluating text-to-SQL models.",
        stream=True,
    ))
