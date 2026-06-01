"""Method Writer — writes the Methods section.

Prompt config lives in prompts/agents/method_writer.yml.
"""
import asyncio

from research_agent.agents._base import build_agent


method_writer_ag = build_agent(
    prompt_name="method_writer",
    tools=None,
)


if __name__ == "__main__":
    asyncio.run(method_writer_ag.aprint_response(
        "Write the Methods section for a paper on retrieval-augmented code generation.",
        stream=True,
    ))
