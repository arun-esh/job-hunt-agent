# Job-Hunt Agent: Build an AI Agent with Google ADK

A hands-on workshop. You will build an AI agent that helps a student with internship and job searches, using the
[Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini.

You are on **step 1: a bare agent**. By the end of this README you will have a working agent that you can chat
with in your browser.

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

## Repository layout

```
job-hunt-agent/
├── job_hunt_app/
│   ├── __init__.py
│   └── agent.py
├── .env.example                template for your API key
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
