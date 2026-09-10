from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Job:
    job_id: str
    conversation_id: str
    status: str = "queued"
    error: str | None = None
    result: dict = field(default_factory=dict)

class InMemoryJobStore:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def create(self, conversation_id: str) -> Job:
        job = Job(job_id=f"job_{len(self.jobs)+1:04d}", conversation_id=conversation_id)
        self.jobs[job.job_id] = job
        return job

    def update(self, job_id: str, status: str, **kwargs):
        job = self.jobs[job_id]
        job.status = status
        for k, v in kwargs.items():
            setattr(job, k, v)
        return job
