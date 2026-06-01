"""Research Workflow — orchestrates the five teams end-to-end.

Pipeline:
    user topic
        -> Discovery Team
        -> Analysis Team
        -> Innovation Team
        -> Experiment Team
        -> Writing Team
        -> final research report

Prompt config lives in prompts/workflows/research.yml.
Runtime config lives in configs/ (defaults.yml + workflows.yml).
"""
from __future__ import annotations

import asyncio
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from agno.workflow import Step, Workflow

from research_agent.configs import make_db, workflow_config
from research_agent.prompts import load_prompt
from research_agent.teams import (
    analysis_team,
    discovery_team,
    experiment_team,
    innovation_team,
    writing_team,
)


_PROMPT_NAME = "research"
_meta = load_prompt("workflows", _PROMPT_NAME)
_cfg = workflow_config(_PROMPT_NAME)
_wf = _cfg.get("workflow", {})


research_workflow = Workflow(
    name=_meta["name"],
    description=_meta.get("description"),
    db=make_db(_cfg["db"], scope="workflow", name=_PROMPT_NAME),
    steps=[
        Step(name="Discovery", team=discovery_team,
             description="Surface the relevant literature, citation graph, and trends for the topic."),
        Step(name="Analysis", team=analysis_team,
             description="Parse the corpus, build a comparison matrix, find contradictions, run SWOT."),
        Step(name="Innovation", team=innovation_team,
             description="Detect gaps, generate novel ideas, and cross-domain inspirations."),
        Step(name="Experiment", team=experiment_team,
             description="Turn the chosen ideas into datasets, experiment designs, and evaluation plans."),
        Step(name="Writing", team=writing_team,
             description="Draft Abstract, Methods, Results, and audit citations into a final report."),
    ],
    stream_events=_wf.get("stream_events", True),
)


if __name__ == "__main__":
    topic = (
        "Produce a full research report on the topic: "
        "'large language model agents for autonomous scientific research'."
    )
    asyncio.run(research_workflow.aprint_response(topic, stream=True))
