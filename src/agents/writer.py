
# package for agents
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv()
import os


writer_agent= Agent(
    name="Writer agent",
    model=Gemini(id="gemini-2.5-flash"),
    instructions="Write a detailed report with sources on the topic using planning ",
)

