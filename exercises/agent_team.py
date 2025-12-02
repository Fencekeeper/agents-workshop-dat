import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="model-deployment-name",
    model="model-name",
    api_version="2024-10-21",
    azure_endpoint="https://mdir-workshop.openai.azure.com/",
    api_key=os.getenv("API_KEY"),
)

async def main():
    # Opprett agenter
    coder = AssistantAgent("coder", model_client=model_client)
    reviewer = AssistantAgent("reviewer", model_client=model_client)
    
    # Opprett team
    team = RoundRobinGroupChat(
        participants=[coder, reviewer],
        termination_condition=MaxMessageTermination(6)
    )
    
    # Kjør oppgave
    task = "Write and review a Python function to sort a list"
    await Console(team.run_stream(task=task))

# Kjør hovedfunksjonen
asyncio.run(main())