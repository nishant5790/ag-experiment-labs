"""Citation Validator — audits citations in the report.

Prompt config lives in prompts/agents/citation_validator.yml.
"""
import asyncio

from research_agent.agents._base import build_agent
from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
)


citation_validator_ag = build_agent(
    prompt_name="citation_validator",
    tools=[semantic_scholar_tool, openalex_tool, crossref_tool],
)


if __name__ == "__main__":
    asyncio.run(citation_validator_ag.aprint_response(
        "Validate the citation 'Vaswani et al., Attention Is All You Need, 2017'.",
        stream=True,
    ))
