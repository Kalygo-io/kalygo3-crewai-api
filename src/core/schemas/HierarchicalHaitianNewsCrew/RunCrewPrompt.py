from pydantic import BaseModel

class RunCrewPrompt(BaseModel):
    sessionId: str
    crewConfig: dict
    emails: str