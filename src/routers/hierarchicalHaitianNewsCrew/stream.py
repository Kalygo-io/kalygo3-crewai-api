from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.routers.hierarchicalHaitianNewsCrew.helpers.format_news_for_email import format_news_for_email
from src.routers.hierarchicalHaitianNewsCrew.helpers.send_email import send_email_ses
from src.core.schemas.HierarchicalHaitianNewsCrew.RunCrewPrompt import RunCrewPrompt
from crewai import Agent, Crew, Task, Process
import json
from fastapi.responses import StreamingResponse
from src.deps import jwt_dependency
from crewai_tools import ScrapeWebsiteTool
from src.pydantic.HaitianNewsCrew.NewsResults import NewsResults
import os

import yaml
tasks_yaml = None
with open("src/routers/hierarchicalHaitianNewsCrew/config/tasks.yaml", 'r') as file:
    tasks_yaml = yaml.safe_load(file)

agents_yaml = None
with open("src/routers/hierarchicalHaitianNewsCrew/config/agents.yaml", 'r') as file:
    agents_yaml = yaml.safe_load(file)

scrape_web_tool = ScrapeWebsiteTool()

limiter = Limiter(key_func=get_remote_address)

from dotenv import load_dotenv
import uuid

load_dotenv()

callbacks = []

router = APIRouter()

async def generator(sessionId: str):
    
    def manager_callback(step):
        print('___ -!-!- ___')
        print('manager_callback', step)
        print("step.thought", step.thought)
        print("step.tool", step.tool)
        print("step.tool_input", step.tool_input)
        # print("step.text", step.text)

        yield json.dumps({
            "event": "manager_callback",
            "data": "manager_callback",
            "id": str(uuid.uuid4())
        }, separators=(',', ':'))

    def crew_step_callback(step):
        print('___ -!-!- ___')
        print('crew_step_callback', step)
        print("step.thought", step.thought)
        print("step.tool", step.tool)
        print("step.tool_input", step.tool_input)
        # print("step.text", step.text)

        yield json.dumps({
            "event": "crew_step_callback",
            "data": "crew_step_callback",
            "id": str(uuid.uuid4())
        }, separators=(',', ':'))
        
        # thought: str
        # tool: str
        # tool_input: str
        # text: str
        # result: str

        print('___ --- ___')

    def worker_step_callback(step):
        print('___ -!-!- ___')
        print('worker_step_callback', step)
        print("step.thought", step.thought)
        print("step.tool", step.tool)
        print("step.tool_input", step.tool_input)
        yield json.dumps({
            "event": "worker_step_callback",
            "data": "worker_step_callback",
            "id": str(uuid.uuid4())
        }, separators=(',', ':'))

    def task_callback(step):
        print('___ --- ___')
        print('task_callback', step)
        print('___ --- ___')

    manager = Agent(
        role=agents_yaml["manager"]["role"],
        goal=agents_yaml["manager"]["goal"],
        backstory=agents_yaml["manager"]["backstory"],
        verbose=True,
        step_callback=(lambda step: manager_callback(step)),
        callback=(lambda step: manager_callback(step))
    )

    workers = []
    
    for worker in agents_yaml["workers"]:
        workers.append(
            Agent(
                role=agents_yaml["workers"][worker]["role"],
                goal=agents_yaml["workers"][worker]["goal"],
                backstory=agents_yaml["workers"][worker]["backstory"],
                verbose=True,
                step_callback=(lambda step: worker_step_callback(step)),
                tools=[scrape_web_tool],
            )
        )

    research_task = Task(
        description=tasks_yaml["research_task"]["description"],
        expected_output=tasks_yaml["research_task"]["expected_output"],
        # callback=(lambda step: task_callback(step)),
        output_pydantic=NewsResults
    )

    crew = Crew(
        agents=workers,
        manager_agent=manager,
        tasks=[research_task],
        process=Process.hierarchical,
        verbose=True,
        # step_callback=(lambda step: crew_step_callback(step)),
        # task_callback=(lambda step: crew_step_callback(step)),
    )

    crew_output = crew.kickoff()

    print()
    print('FINAL OUTPUT')
    print()
    print(crew_output)
    print(crew_output.pydantic)
    print()

    send_email_ses(["tad@cmdlabs.io"], format_news_for_email(crew_output.pydantic))

    yield json.dumps({
        "event": "crew_final_output",
        "data": crew_output.raw,
        "id": str(uuid.uuid4())
    }, separators=(',', ':'))

    # yield json.dumps({
    #     "event": "crew_final_output",
    #     "data": "DONE",
    #     "id": str(uuid.uuid4())
    # }, separators=(',', ':'))

@router.post("/stream")
@limiter.limit("10/minute")
def streamHierarchical(prompt: RunCrewPrompt, jwt: jwt_dependency, request: Request):
    return StreamingResponse(generator(prompt.sessionId), media_type='text/event-stream')