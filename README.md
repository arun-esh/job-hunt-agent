# Job-Hunt Agent: Build an AI Agent with Google ADK

A hands-on workshop. You will build an AI agent that helps a student with internship and job searches, using the
[Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini.

You are on **step 7: The brief**. This README covers the setup and steps 1 to 7. Steps 1 to 6 are already done in the code; your job is step 7.

## Prerequisites

| Requirement                  | Notes                                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| Python 3.10 or newer         | Check with `python3 --version`                                                                         |
| Git                          | Check with `git --version`                                                                             |
| A Gemini API key             | Free tier is sufficient. Create one at <https://aistudio.google.com/apikey> (Google account required) |
| A terminal and a code editor | Any editor works                                                                                       |

## Setup

### 1. Get the code

```bash
git clone https://github.com/arun-esh/job-hunt-agent.git job-hunt-agent
cd job-hunt-agent
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and replace `paste-your-key-here` with your key. Do not add quotes or spaces around it.

Your `.env` should look like this (the key below is a fake example; a real key is a similar-looking string
that starts with `AIza`):

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Common mistakes:

```
GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"     <- quotes
GOOGLE_API_KEY = AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     <- spaces around =
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       <- trailing space after the key
GOOGLE_API_KEY=paste-your-key-here                          <- placeholder not replaced
```

`.env` is listed in `.gitignore`, so it is never committed. Never share your key, never paste it into a chat, and
run `git status` before every commit to confirm `.env` is not listed.

### 4. Verify the setup

```bash
python -c "import google.adk; print('ADK installed')"
adk --version
```

Expected: `ADK installed` and a version number.

## Step 1: A bare agent

**Goal:** create the smallest possible ADK agent and talk to it in the browser.

**Concept:** an agent is a **model** (the reasoning engine, here Gemini) plus an **instruction** (who it is and the
rules it follows). This agent has no tools, so it can only answer from what the model already knows.

### 1. Create the package

ADK discovers an agent from a folder that contains an `agent.py` defining `root_agent`. From the repository root:

```bash
mkdir job_hunt_app
touch job_hunt_app/__init__.py job_hunt_app/agent.py
```

### 2. Expose the agent

`job_hunt_app/__init__.py`:

```python
from . import agent
```

### 3. Define the agent

`job_hunt_app/agent.py` (type this in):

```python
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
```

| Field         | Purpose                                                      |
| ------------- | ------------------------------------------------------------ |
| `model`       | The Gemini model that does the reasoning.                    |
| `name`        | Identifier for the agent. Must be a valid Python identifier. |
| `description` | A one-line summary of what the agent is for.                 |
| `instruction` | The system prompt: role, tone and rules.                     |

#### To do: add the model

The `model` line is commented out, so the agent cannot think yet. Uncomment it.

1. In `job_hunt_app/agent.py`, remove the `# ` in front of `model="gemini-3.8-flash",` and delete the `TODO`
   comment above it.
2. Save the file.

If the model name is not available to your key (you will see a `404 ... model not found` error when you run it),
use a different name: see [Finding a model name your key can use](#finding-a-model-name-your-key-can-use).

<details>
<summary>Solution (try it yourself first)</summary>

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-3.8-flash",
    name="job_hunt_agent",
    description="Helps a student find internships and jobs.",
    instruction=(
        "You are a job-search assistant for a university student. "
        "Answer in short, friendly sentences. "
        "Never claim that a job posting exists unless you have actually seen it. "
        "If you do not know something, say so."
    ),
)
```

</details>

### 4. Run it

Run this from the **repository root**: the `job-hunt-agent/` folder, the one that contains `job_hunt_app/`,
`requirements.txt` and `.env`. Do **not** run it from inside `job_hunt_app/`.

```bash
pwd                      # the path must end in job-hunt-agent
ls                       # you should see job_hunt_app, requirements.txt, README.md
adk web .
```

The `.` means "look for agents in the current folder". ADK lists every sub-folder that contains an agent.

Open the address it prints (usually <http://localhost:8000>), select **job_hunt_app** in the drop-down at the top
left, and start a chat.

### 5. Try these prompts

1. `Hi! Who are you and what can you do?`
2. `Which internships are open in Sherbrooke right now?`

**Expected:** the first answer introduces a job-search assistant. For the second, the agent has no way to look
anything up, so it should say that it cannot see current postings. If it lists specific openings, they are
invented, because the agent has no source for them.

Use the **Events** tab in the left panel to see the request sent to the model and its reply.
Stop the server with `Ctrl+C`. If the agent answered, your API key works.

**How the code is organised:** the tools and agents for each step are already written for you. Your job is to
**connect** them: in each step you uncomment a few marked lines (search the code for `STEP 7 TODO`), then
read how the pieces fit together.


## Step 2: Your resume becomes a profile

**Goal:** turn your resume PDF into a small `profile.json` that is safe to send to the model.

**Concept:** a **tool** is a plain Python function. ADK shows the model its name, parameters and docstring; the model
decides *when* to call it, but the function is ordinary code that does exactly what is written. That is why code is
a guarantee and a prompt is only a probability.

### Add your resume

The `data/` folder is yours and **is never committed** (it is in `.gitignore`). Create it and add your resume:

```bash
mkdir -p data
cp /path/to/your/resume.pdf data/resume.pdf     # any file named resume*.pdf works
git status                                      # data/ must NOT appear in this list
```

### What is provided: `job_hunt_app/tools.py`

| Function | What it does |
| --- | --- |
| `read_resume()` | Reads `data/resume*.pdf` with `pypdf`. **Code** removes emails, phone numbers and links from the text. |
| `save_profile(skills, education, experience, projects, interests, location)` | Writes `data/profile.json`. The typed arguments tell the model exactly which fields to fill. There is no field for a name, email or phone. |
| `get_profile()` | Returns the saved profile. Every later agent will use this instead of the resume. |

> **Privacy, honestly:** code can reliably remove emails, phone numbers and links, but not your name. The model reads
> the redacted resume text **once**, to fill in the profile, so that text (name included) goes to Google's API one
> time. After that, only the fields in `profile.json` are used.

### Connect it: `job_hunt_app/agent.py`

Search for `STEP 2 TODO` and uncomment three places: the import, the two instruction lines, and the three tools.
Make sure you also install the new dependency:

```bash
pip install -r requirements.txt
```

### Run it

```bash
adk web .
```

Select **job_hunt_app** and say: `Build my profile from my resume.`

**Expected:** the **Events** tab shows `read_resume` and then `save_profile`. A file `data/profile.json` appears.
Open it: it has skills, education, experience, projects, interests and location, and **no** name, email or phone.
Then ask `What skills are in my profile?` and the agent calls `get_profile`.


## Step 3: Search the web for jobs

**Goal:** let the agent find current postings online, for example "jobs for students in Sherbrooke".

**Concept:** a **specialist agent**. The built-in `google_search` tool runs inside Gemini itself and ADK does not
let it share an agent with your own Python tools, so it gets an agent of its own, `job_searcher`. The main agent calls
it as a tool with `AgentTool`. The specialist saves its answer in **session state** with `output_key`, a shared
notepad that other agents can read.

### What is provided

- `job_hunt_app/sub_agents/job_searcher.py`: the agent. Its tool is `google_search`, its instruction asks for up to
  three current postings with direct links, and `output_key='job_results'` stores the list.
- `job_hunt_app/config.py`: the model name used by every helper agent. If you changed the model name in step 1,
  change it here too.

### Connect it: `job_hunt_app/agent.py`

Search for `STEP 3 TODO` and uncomment: the two imports, the instruction line, and the `AgentTool(agent=job_searcher)`
entry. `AgentTool` wraps an agent so the main agent can call it like a function and stay in charge afterwards.

### Run it

```bash
adk web .
```

Try: `Find student jobs in Sherbrooke that fit my profile.`

**Expected:** the main agent calls `get_profile`, then `job_searcher`, and shows up to three postings with links.
In the **State** tab you can see `job_results`. **Always open the links yourself**: search results can be out of
date, and a posting can be closed.


## Step 4: Read a posting

**Goal:** read the full text of one posting from its link.

**Concept:** **real-world tools need safety rules, and fetched text is untrusted input.** A web page can contain
text like "ignore your instructions". The model must treat page text as *data*. The code also limits what the tool can
reach, so a prompt cannot talk its way past it.

### What is provided: `fetch_posting(url)` in `tools.py`

| Safety rule | Why |
| --- | --- |
| Only `http` and `https` | No `file://` or other schemes. |
| Public addresses only | `localhost` and private networks are refused, including on redirects, so the agent cannot be tricked into reading things on your machine or network. |
| At most 1 MB, 10 seconds, 8000 characters | A huge page cannot stall or flood the agent. |
| HTML turned into plain text | Scripts and styles are dropped. |

### Connect it: `job_hunt_app/agent.py`

Search for `STEP 4 TODO` and uncomment the import, the instruction line, and `fetch_posting` in the tools list.
Install the new dependency with `pip install -r requirements.txt`.

### Run it

```bash
adk web .
```

1. `Read this page and summarize it: <paste the link of a real posting>`
2. `Read http://localhost:8000` and watch it get **blocked**.

**Expected:** the first call returns the page text and a summary. The second shows `status: blocked`.
Some job sites block automated readers or need JavaScript: then the tool returns an error and the agent should say it
could not read the page instead of guessing.


## Step 5: Match a posting to your profile

**Goal:** compare one posting with your profile and see where you fit and where you have gaps.

**Concept:** **shared state.** `resume_matcher` has two tools (`fetch_posting`, `get_profile`) and saves its report
with `output_key='match_report'`. Because the model only receives `profile.json`, your private details never reach it.

### What is provided

`job_hunt_app/sub_agents/resume_matcher.py`. Read its instruction: it lists matching skills, gaps and a fit rating,
forbids adding skills that are not in the profile, and says to write "Could not read the page" instead of guessing.

### Connect it: `job_hunt_app/agent.py`

Search for `STEP 5 TODO` and uncomment the import, the instruction line, and `AgentTool(agent=resume_matcher)`.

### Run it

```bash
adk web .
```

Try: `Compare this posting with my profile: <link of a posting>`

**Expected:** the main agent calls `resume_matcher`, which calls `fetch_posting` and `get_profile`, and you get
matching skills, gaps and a fit rating. The **State** tab shows `match_report`. Check the gaps: are they true?


## Step 6: Work in parallel

**Goal:** search once, then read and match three postings **at the same time**.

**Concept:** **orchestration with plain code.** Search, fetch and match depend on each other, so the parallel part is
across jobs: three workers, one per job.

```
find_jobs  (SequentialAgent: fixed order)
 ├─ 1. job_searcher                    writes state["job_results"]
 └─ 2. job_workers  (ParallelAgent: all at the same time)
        worker_1 ─> fetch + match job 1 ─> state["match_1"]
        worker_2 ─> fetch + match job 2 ─> state["match_2"]
        worker_3 ─> fetch + match job 3 ─> state["match_3"]
```

`ParallelAgent` and `SequentialAgent` are plain code, not a model, so the order and the parallelism are predictable.
Each worker saves to its **own** state key so they never overwrite each other.

### What is provided

`job_hunt_app/sub_agents/workers.py`: a small function builds worker 1, 2 and 3. Each worker's instruction contains
`{job_results?}`: ADK fills it from state before calling the model (the `?` means "empty if missing") and the worker
takes the job with its own number.

### Connect it

1. `job_hunt_app/pipeline.py`: search for `STEP 6 TODO` and uncomment `job_workers` and `find_jobs`.
2. `job_hunt_app/agent.py`: search for `STEP 6 TODO` and uncomment the import, the instruction line, and
   `AgentTool(agent=find_jobs)`.

### Run it

```bash
adk web .
```

Try: `Find student jobs in Sherbrooke.`

**Expected:**
- **Trace** tab: `worker_1`, `worker_2` and `worker_3` start at about the same time and overlap, instead of running
  one after another.
- **State** tab: `job_results`, `match_1`, `match_2`, `match_3`.
- The chat answer is only partly useful in this step, because nothing combines the three reports yet. That is step 7.


## Step 7: The brief

**Goal:** combine everything into one ranked answer for the student.

**Concept:** **fan in.** `brief_writer` runs last and reads `job_results` and `match_1` to `match_3` from state. ADK
fills each `{name}` in its instruction from state before the model is called, so every name must match an `output_key`.

### What is provided

`job_hunt_app/sub_agents/brief_writer.py`: ranks the jobs, gives the link, why it fits, the main gap and a rating, says
plainly if a page could not be read, and ends with a next step.

### Connect it: `job_hunt_app/pipeline.py`

Search for `STEP 7 TODO` and uncomment two things: the import of `brief_writer` and the `brief_writer,` line inside
`find_jobs`. The order of that list is the order the agents run.

### Run it

```bash
adk web .
```

Try: `Find student jobs in Sherbrooke.`

**Expected:** a short ranked brief with links, fit ratings and gaps, based only on what the workers found. Open the
links and check the facts. If a page could not be read, the brief should say so instead of guessing.

## Repository layout

```
job-hunt-agent/
├── job_hunt_app/
│   ├── __init__.py
│   ├── agent.py              the main agent: where you connect things
│   ├── config.py             the model name used by helper agents
│   ├── tools.py              read_resume, save_profile, get_profile, fetch_posting
│   ├── pipeline.py           find_jobs: the fixed order and the parallel step
│   └── sub_agents/
│       ├── job_searcher.py
│       ├── resume_matcher.py
│       ├── workers.py
│       └── brief_writer.py
├── data/                     YOUR private files, never committed (resume.pdf, profile.json)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Finding a model name your key can use

If you get `404 ... model not found`, list the models your key can call. Run this from the repository root
with the virtual environment active. It prints model names only, never your key:

```bash
python - <<'EOF'
from dotenv import load_dotenv
load_dotenv()
from google import genai

for m in genai.Client().models.list():
    if "generateContent" in (m.supported_actions or []):
        print(m.name.removeprefix("models/"))
EOF
```

Pick a name that starts with `gemini-` and contains `flash` (fast and cheap), then copy it exactly into the
`model="..."` line of `job_hunt_app/agent.py` and restart `adk web`.

The official list, with descriptions and limits, is at <https://ai.google.dev/gemini-api/docs/models>.

## Troubleshooting

### `command not found: adk`

The virtual environment is not active. From the repository root run:

```bash
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
```

Your terminal prompt should now start with `(.venv)`. Then run the command again.

### `python3: command not found`

Python is not installed. Install Python 3.10 or newer from <https://www.python.org/downloads/>, open a new
terminal, and check with `python3 --version`.

### `pip install` fails

Check that the virtual environment is active (the prompt starts with `(.venv)`) and that you are in the
repository root, where `requirements.txt` is. Then run `pip install -r requirements.txt` again.

### `job_hunt_app` is missing from the drop-down

You started `adk web` from the wrong folder. Run `pwd`: the path must end in `job-hunt-agent`, not
`job_hunt_app`. Go to the repository root, then run `adk web .` again.

### `404 ... model not found`

The model name in `job_hunt_app/agent.py` is not available to your key. Follow
"Finding a model name your key can use" above, put a name from the list in `model="..."`, and restart `adk web`.

### `403` or `API key not valid`

The key in `.env` is wrong or badly formatted. Compare your `.env` with the example in setup step 3: no quotes,
no spaces around `=`, no trailing space, and the placeholder replaced. If the key still fails, create a new one
at <https://aistudio.google.com/apikey>. Restart `adk web` after any change to `.env`.

### `Missing key inputs argument`

`.env` does not exist, you are not running from the repository root, or `.env` still holds the placeholder.
Repeat setup step 3 and restart `adk web`.

### `No resume found`

The resume must be a PDF named `resume*.pdf` inside the `data/` folder at the repository root, for example
`data/resume.pdf`. Check with `ls data`.

### `The PDF has no readable text`

Your PDF is a scanned image. Export it again as a text PDF from Word or Google Docs.

### `ModuleNotFoundError: No module named 'pypdf'` (or `httpx`)

The virtual environment is not active, or you did not install the new requirements. Run
`source .venv/bin/activate` and `pip install -r requirements.txt`.

### The search returns no jobs, closed jobs, or broken links

The built-in search is only as good as the web it finds. Open every link yourself. Try a more specific request, for
example `student jobs Université de Sherbrooke` or `software internship Sherbrooke`.

### `429` or `RESOURCE_EXHAUSTED`

You used up the free quota for now. Wait a minute and try again, or use a smaller request.

### `status: blocked`

The link is not a public `http(s)` page, so the tool refused it on purpose. That is the safety rule working.

### The page could not be read

Many job sites block automated readers or only show their content with JavaScript. Try the company's own careers page,
or copy the posting text into the chat yourself.

### `Context variable not found: <name>`

A `{name}` in an instruction does not match any state key. Names must match an `output_key` exactly
(`job_results`, `match_1`, `match_2`, `match_3`). Check for typos in the instruction and in `output_key`.

### Only one worker seems to answer in the chat

The chat shows the last answer only. Open the **State** tab to see `match_1`, `match_2` and `match_3`.
