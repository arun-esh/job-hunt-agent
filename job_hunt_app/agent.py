from google.adk.agents.llm_agent import Agent

# STEP 2 TODO: uncomment the lines below (step 2 imports: resume tools)
# from .tools import get_profile, read_resume, save_profile

root_agent = Agent(
    model="gemini-3.8-flash",
    name="job_hunt_agent",
    description="Helps a student find internships and jobs.",
    instruction=(
        "You are a job-search assistant for a university student. "
        "Answer in short, friendly sentences. "
        "Never claim that a job posting exists unless you have actually seen it. "
        "If you do not know something, say so. "
        # STEP 2 TODO: uncomment the lines below (step 2 instruction: resume tools)
        # "To build the student's profile, call read_resume, then call save_profile with the skills, education, experience, projects, interests and preferred location you find in it. Never put the student's name, email, phone number or address in the profile. "
        # "To recall the student's profile, call get_profile. "
    ),
    tools=[
        # STEP 2 TODO: uncomment the lines below (step 2 tool: resume tools)
        # read_resume,
        # save_profile,
        # get_profile,
    ],
)
