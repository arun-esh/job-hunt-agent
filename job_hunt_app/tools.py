"""Tools: plain Python functions the agent can call.

ADK shows the model each function's NAME, its PARAMETERS and its DOCSTRING. The model decides WHEN to call a
tool, but the function itself is ordinary code that does exactly what is written here. No model runs inside it.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"                 # your private files (git-ignored)
PROFILE = DATA / "profile.json"      # the small profile the model will see


# ---------------------------------------------------------------- step 2: the resume and the profile
def _redact(text: str) -> str:
    """Removes emails, phone numbers and web links before the text is shown to the model.
    This is plain code, so it is a guarantee: the model never sees them, whatever any prompt says."""
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email removed]", text)
    text = re.sub(r"https?://\S+|www\.\S+|linkedin\.com/\S+|github\.com/\S+", "[link removed]", text)
    text = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[phone removed]", text)
    return text


def read_resume() -> dict:
    """Reads the student's resume PDF (data/resume*.pdf) and returns its text with emails, phone numbers
    and links removed. Call this once to build the student's profile."""
    from pypdf import PdfReader  # imported here so the earlier steps work before pypdf is installed

    found = sorted(DATA.glob("resume*.pdf"))
    if not found:
        return {"status": "error", "message": "No resume found. Put your resume PDF in the data/ folder (data/resume.pdf)."}
    try:
        text = "\n".join((page.extract_text() or "") for page in PdfReader(str(found[0])).pages)
    except Exception as e:  # a tool must never crash: return the problem instead
        return {"status": "error", "message": f"Could not read the resume: {e}"}
    text = _redact(text).strip()
    if not text:
        return {"status": "error", "message": "The PDF has no readable text (a scanned image?). Export it again as a text PDF."}
    return {"status": "ok", "file": found[0].name, "resume_text": text}


def save_profile(skills: list[str], education: list[str], experience: list[str], projects: list[str],
                 interests: list[str], location: str) -> dict:
    """Saves the student's profile to data/profile.json. Use ONLY facts written in the resume.
    Never include the student's name, email, phone number or address.
    skills: technical and soft skills. education: one short line per degree. experience: one short line per job
    or internship. projects: one short line per project. interests: kinds of work the student wants.
    location: the city or region where the student wants to work."""
    profile = {"skills": skills, "education": education, "experience": experience,
               "projects": projects, "interests": interests, "location": location}
    DATA.mkdir(exist_ok=True)
    PROFILE.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"status": "ok", "saved_to": "data/profile.json"}


def get_profile() -> dict:
    """Returns the student's saved profile (skills, education, experience, projects, interests, location).
    If there is no profile yet, it says so: then read_resume and save_profile must be used first."""
    if not PROFILE.is_file():
        return {"status": "error", "message": "No profile yet. Build it first with read_resume and save_profile."}
    return {"status": "ok", "profile": json.loads(PROFILE.read_text(encoding="utf-8"))}
