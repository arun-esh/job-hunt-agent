from google.adk.agents.llm_agent import Agent

from .tools import get_profile, read_resume, save_profile

# STEP 3 TODO: uncomment the lines below (step 3 imports: the search agent)
# from google.adk.tools.agent_tool import AgentTool
# from .sub_agents.job_searcher import job_searcher

root_agent = Agent(
    model="gemini-3.8-flash",
    name="job_hunt_agent",
    description="Helps a student find internships and jobs.",
    instruction=(
        "You are a job-search assistant for a university student. "
        "Answer in short, friendly sentences. "
        "Never claim that a job posting exists unless you have actually seen it. "
        "If you do not know something, say so. "
        "To build the student's profile, call read_resume, then call save_profile with the skills, education, experience, projects, interests and preferred location you find in it. Never put the student's name, email, phone number or address in the profile. "
        "To recall the student's profile, call get_profile. "
        # STEP 3 TODO: uncomment the lines below (step 3 instruction: the search agent)
        # "To search the web for jobs, call the job_searcher tool with a short request that includes the student's skills, interests and location. "
    ),
    tools=[
        read_resume,
        save_profile,
        get_profile,
        # STEP 3 TODO: uncomment the lines below (step 3 tool: the search agent)
        # AgentTool(agent=job_searcher),
    ],
)
