from pydantic import BaseModel

class Job(BaseModel):
    title: str
    location: str

class Jobs(BaseModel):
    jobs: list[Job]