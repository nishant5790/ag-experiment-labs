"""
Main application script for the OS app.
"""
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from agno.os import AgentOS
from research_agent.agents.search_agent import search_agent_ag

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

# Create your custom FastAPI app
app = FastAPI(title="AI research assistant")

# Add your custom routes
@app.get("/status")
async def status_check():
    return {"status": "healthy"}

# Pass your app to AgentOS
agent_os = AgentOS(
    agents=[search_agent_ag],

    base_app=app  # Your custom FastAPI app
)

# Get the combined app with both AgentOS and your routes
app = agent_os.get_app()

if __name__ == "__main__":
    """Run the AgentOS application.

    You can see the docs at:
    http://localhost:7777/docs

    """
    agent_os.serve(app="ag-os:app", port=8000, reload=True)