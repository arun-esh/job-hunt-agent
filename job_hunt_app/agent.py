from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    # TODO: uncomment the next line (remove the "# " in front of it)
    # model="gemini-3.8-flash",
    name="job_hunt_agent",
    description="Helps a student find internships and jobs.",
    instruction=(
        "You are a job-search assistant for a university student. "
        "Answer in short, friendly sentences. "
        "Never claim that a job posting exists unless you have actually seen it. "
        "If you do not know something, say so."
    ),
)
