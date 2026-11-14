# Job-Hunt Agent: Build an AI Agent with Google ADK

A hands-on workshop. You will build an AI agent that helps a student with internship and job searches, using the
[Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini.

This branch is **setup only**. By the end of this README your machine is ready to build agents.

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
git clone <repository-url> job-hunt-agent
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

## Repository layout

```
job-hunt-agent/
├── .env.example                template for your API key
├── .gitignore
├── requirements.txt
└── README.md
```

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
