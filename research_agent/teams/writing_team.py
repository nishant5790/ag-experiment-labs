"""Writing Team — Abstract + Method + Results + Citation Validator.

Prompt config lives in prompts/teams/writing.yml.
"""
import asyncio

from research_agent.agents import (
    abstract_writer_ag,
    method_writer_ag,
    results_writer_ag,
    citation_validator_ag,
)
from research_agent.teams._base import build_team


writing_team = build_team(
    prompt_name="writing",
    members=[
        abstract_writer_ag,
        method_writer_ag,
        results_writer_ag,
        citation_validator_ag,
    ],
)


if __name__ == "__main__":
    asyncio.run(writing_team.aprint_response(
        "Draft a research report on retrieval-augmented code generation.",
        stream=True,
    ))
