from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

from ..config import MODEL

# A specialist agent. Its only tool is Google Search, which runs inside Gemini itself.
# (ADK does not let a built-in tool like google_search share an agent with your own Python tools,
# which is one more reason to give it an agent of its own.)
# output_key saves the final answer in session state under the name "job_results", a shared notepad
# that other agents can read later.
job_searcher = Agent(
    model=MODEL,
    name='job_searcher',
    description='Searches the web for current job postings that fit a student.',
    instruction=(
        "You find job postings for a university student. The request describes the student's skills, interests "
        "and location. Use Google Search to find up to 3 CURRENT postings that fit. "
        "Answer with a numbered list. For each job give: title, company, location, the DIRECT link to the posting "
        "page, and one line on why it fits. Use only what the search results show; never invent a posting or a link. "
        "If you find fewer than 3, list only those you found and say so."
    ),
    tools=[google_search],
    output_key='job_results',
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
