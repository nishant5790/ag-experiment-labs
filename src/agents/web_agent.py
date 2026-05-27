# package for agents
from agno.agent import Agent
from agno.vectordb.qdrant import Qdrant
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from dotenv import load_dotenv
load_dotenv()
import os

web_agent= Agent(
    name="Web agent",
    model=Gemini(
        id="gemini-2.5-flash"
    ),
    tools= [WebSearchTools()],
    role = "Search the web for the latest news and trends",
    db=SqliteDb(
        session_table="web_session",
        db_file = "tmp/web.db",
    ),
    add_history_to_context=True,
)