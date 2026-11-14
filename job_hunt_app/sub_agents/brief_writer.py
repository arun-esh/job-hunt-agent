from google.adk.agents.llm_agent import Agent

from ..config import MODEL

# The last step: reads everything the other agents left in state and writes the answer for the student.
# ADK fills each {name} from session state BEFORE the model is called, so every name must match an output_key.
brief_writer = Agent(
    model=MODEL,
    name='brief_writer',
    description='Writes the final ranked brief for the student.',
    instruction=(
        "You write for a university student looking for a job. Use ONLY the information below. "
        "Write a short brief: rank the jobs from best to worst fit, and for each give the title, company, "
        "the link, why it fits, the main gap, and your fit rating. "
        "If a report says the page could not be read, or a job is missing, say so plainly and do not guess. "
        "End with one sentence on what the student should do next. Keep it under 250 words.\n\n"
        "Job list: {job_results?}\n"
        "Job 1 match: {match_1?}\n"
        "Job 2 match: {match_2?}\n"
        "Job 3 match: {match_3?}"
    ),
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
