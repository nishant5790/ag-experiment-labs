# package for agents
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv()
import os


content_planner= Agent(
    name="Content planner",
    model=Gemini(id="gemini-2.5-flash"),
    instructions=[
        "Plan a queries for the  topic and research content",
        "Ensure that I have detailed sources with relevant links",
        "only return the topic names in dict format [{category_name : [queries]}]"
    ]
)

