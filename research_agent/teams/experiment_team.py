"""Experiment Team — Dataset + Experiment Design + Evaluation.

Prompt config lives in prompts/teams/experiment.yml.
"""
import asyncio

from research_agent.agents import (
    dataset_agent_ag,
    experiment_agent_ag,
    evaluation_agent_ag,
)
from research_agent.teams._base import build_team


experiment_team = build_team(
    prompt_name="experiment",
    members=[
        dataset_agent_ag,
        experiment_agent_ag,
        evaluation_agent_ag,
    ],
)


if __name__ == "__main__":
    asyncio.run(experiment_team.aprint_response(
        "Plan experiments for evaluating LoRA fine-tuning on math reasoning benchmarks.",
        stream=True,
    ))
