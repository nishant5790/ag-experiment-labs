"""Abstract Writer — drafts a publication-quality abstract.

Prompt config lives in prompts/agents/abstract_writer.yml.
"""
import asyncio

from research_agent.agents._base import build_agent


abstract_writer_ag = build_agent(
    prompt_name="abstract_writer",
    tools=None,
)


if __name__ == "__main__":
    asyncio.run(abstract_writer_ag.aprint_response(
        "Write an abstract for a paper on retrieval-augmented code generation.",
        stream=True,
    ))
