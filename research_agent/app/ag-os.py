"""Main application script for the AgentOS app."""
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from fastapi import FastAPI
from agno.os import AgentOS

from research_agent.agents import (
    search_agent_ag,
    citation_graph_agent_ag,
    trend_analysis_agent_ag,
    parser_agent_ag,
    matrix_agent_ag,
    contradiction_agent_ag,
    swot_agent_ag,
    gap_agent_ag,
    idea_agent_ag,
    cross_domain_agent_ag,
    dataset_agent_ag,
    experiment_agent_ag,
    evaluation_agent_ag,
    abstract_writer_ag,
    method_writer_ag,
    results_writer_ag,
    citation_validator_ag,
)
from research_agent.teams import (
    discovery_team,
    analysis_team,
    innovation_team,
    experiment_team,
    writing_team,
)
from research_agent.workflows import research_workflow


app = FastAPI(title="AI research assistant")


@app.get("/status")
async def status_check():
    return {"status": "healthy"}


agent_os = AgentOS(
    agents=[
        search_agent_ag,
        citation_graph_agent_ag,
        trend_analysis_agent_ag,
        parser_agent_ag,
        matrix_agent_ag,
        contradiction_agent_ag,
        swot_agent_ag,
        gap_agent_ag,
        idea_agent_ag,
        cross_domain_agent_ag,
        dataset_agent_ag,
        experiment_agent_ag,
        evaluation_agent_ag,
        abstract_writer_ag,
        method_writer_ag,
        results_writer_ag,
        citation_validator_ag,
    ],
    teams=[
        discovery_team,
        analysis_team,
        innovation_team,
        experiment_team,
        writing_team,
    ],
    workflows=[research_workflow],
    base_app=app,
)

app = agent_os.get_app()


if __name__ == "__main__":
    """Run the AgentOS application. Docs at http://localhost:8000/docs"""
    agent_os.serve(app="ag-os:app", port=8000, reload=True)
