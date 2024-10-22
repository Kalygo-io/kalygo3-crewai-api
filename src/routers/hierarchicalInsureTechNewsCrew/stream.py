from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.routers.hierarchicalInsureTechNewsCrew.helpers.format_news_for_email import format_news_for_email
from src.routers.hierarchicalInsureTechNewsCrew.helpers.send_email import send_email_ses
from src.core.schemas.HierarchicalCrew.RunCrewPrompt import RunCrewPrompt
from crewai import Agent, Crew, Task, Process
import json
from fastapi.responses import StreamingResponse
from src.deps import jwt_dependency
from crewai_tools import ScrapeWebsiteTool
from src.pydantic.HaitianNewsCrew.NewsResults import NewsResults

scrape_web_tool = ScrapeWebsiteTool()

limiter = Limiter(key_func=get_remote_address)

from dotenv import load_dotenv
import uuid

load_dotenv()

callbacks = []

router = APIRouter()

async def generator(sessionId: str, prompt: str, crewConfig: dict):

    def manager_step_callback(step):
        print('___ --- ___')
        print('manager_step_callback', step)
        
        print("step.thought", step.thought)
        print("step.tool", step.tool)
        print("step.tool_input", step.tool_input)
        # print("step.text", step.text)
        
        # thought: str
        # tool: str
        # tool_input: str
        # text: str
        # result: str

        print('___ --- ___')

    def manager_callback(step):
        print('___ --- ___')
        print('manager_callback', step)
        print('___ --- ___')

    def worker_step_callback(step):
        print('___ --- ___')
        print('worker_step_callback', step)
        print('___ --- ___')

    def worker_callback(step):
        print('___ --- ___')
        print('worker_callback', step)
        print('___ --- ___')

    def crew_step_callback(step):
        print('___ --- ___')
        print('crew_step_callback', step)
        print('___ --- ___')

    def crew_callback(step):
        print('___ --- ___')
        print('crew_callback', step)
        print('___ --- ___')

    def task_step_callback(step):
        print('___ --- ___')
        print('task_step_callback', step)
        print('___ --- ___')

    def task_callback(step):
        print('___ --- ___')
        print('task_callback', step)
        print('___ --- ___')

    manager_agent = Agent(
        role=crewConfig["managerAgent"]["role"],
        goal=crewConfig["managerAgent"]["goal"],
        backstory=crewConfig["managerAgent"]["backstory"],
        step_callback=(lambda step: manager_step_callback(step)),
        callback=(lambda step: manager_callback(step))
    )

    worker_agents = []

    for workerAgent in crewConfig["workerAgents"]:
        worker_agents.append(
            Agent(
                role=workerAgent["role"],
                goal=workerAgent["goal"],
                backstory=workerAgent["backstory"],
                verbose=True,
                step_callback=(lambda step: worker_step_callback(step)),
                tools=[scrape_web_tool],
                callback=(lambda step: worker_callback(step))
            )
        )

    research_task = Task(
        description="""
Conduct a thorough research about Haiti across the websites provided.
    
    - Le Nouvelliste (https://lenouvelliste.com/) & make sure research is done by the Le Nouvelliste reporter.
    - Loop News Haiti (https://haiti.loopnews.com/) & make sure research is done by the Loop News Haiti reporter.
    - The Haitian Times (https://haitiantimes.com/) & make sure research is done by the Haitian Times reporter.
    - Ayibopost (https://ayibopost.com/) & make sure research is done by the Ayibopost reporter.
    - Radio France Internationale (https://www.rfi.fr/en/tag/haiti/) & make sure research is done by the Radio France Internationale reporter.
    - New York Times (https://www.nytimes.com/topic/destination/haiti) & make sure research is done by the New York Times reporter.
    - CNN (https://www.cnn.com/search?q=Haiti&from=0&size=10&page=1&sort=newest&types=all&section=) & make sure research is done by the CNN reporter.

    Make sure you find any interesting and relevant information given the current date is 10-21-2024.
        """,
        expected_output="""
5 Bulletpoints of the top 5 events representing the most important developments retrieved from the various news outlets. Include a summary of 
event and include detailed sources and citations so that the information can be verified.
Include links to the sources in the final output. Finally, generate a solution-oriented question to
pose to social media to addresss any problems being raised by the most prominent of the developments.
        """,
        step_callback=(lambda step: task_step_callback(step)),
        callback=(lambda step: task_callback(step)),
        output_pydantic=NewsResults
    )

    crew = Crew(
        agents=worker_agents,
        manager_agent=manager_agent,
        tasks=[research_task],
        process=Process.hierarchical,
        verbose=True,
        step_callback=(lambda step: crew_step_callback(step)),
        callback=(lambda step: crew_callback(step))
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

@router.post("/stream")
@limiter.limit("10/minute")
def streamHierarchical(prompt: RunCrewPrompt, jwt: jwt_dependency, request: Request):
    return StreamingResponse(generator(prompt.sessionId, prompt.content, prompt.crewConfig), media_type='text/event-stream')