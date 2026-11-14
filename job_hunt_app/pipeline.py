from google.adk.agents import ParallelAgent, SequentialAgent

from .sub_agents.job_searcher import job_searcher
from .sub_agents.workers import worker_1, worker_2, worker_3
from .sub_agents.brief_writer import brief_writer

# Step 6: the three workers run AT THE SAME TIME. This is plain code, no model decides it.
job_workers = ParallelAgent(
    name='job_workers',
    sub_agents=[worker_1, worker_2, worker_3],
)

# Steps run in a fixed ORDER: search first, then the workers, then the brief.
find_jobs = SequentialAgent(
    name='find_jobs',
    description="Finds 3 current job postings for the student, compares each with the student's profile "
                "and reports. Input: a short request with the student's skills, interests and location.",
    sub_agents=[
        job_searcher,
        job_workers,
        brief_writer,
    ],
)
