
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from agno.os import AgentOS
from workflow_research import content_creation_workflow
# Create your custom FastAPI app
app = FastAPI(title="My Custom App")

# Mount the static UI directory
import os
ui_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
# app.mount("/ui", StaticFiles(directory=ui_dir, html=True), name="ui")

# Add your custom routes
@app.get("/status")
async def status_check():
    return {"status": "healthy"}

# Pass your app to AgentOS
agent_os = AgentOS(
    workflows=[content_creation_workflow],
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