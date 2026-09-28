import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# LOAD RESUME-GENERATOR ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)


# =========================================================
# GEMINI API KEY
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to resume-generator/.env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# HELPER
# =========================================================

def generate_ai_content(prompt: str) -> str:
    """
    Generate content using Gemini in JSON mode.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# =========================================================
# GENERATE RESUME CONTENT
# =========================================================

def generate_resume_content(
    name: str,
    job_role: str,
    education: str,
    experience: str,
) -> dict:
    """
    Generate both professional summary and experience
    using ONE Gemini API request.
    """

    prompt = f"""
You are a professional resume writer.

Create resume content for the candidate using ONLY
the information explicitly provided below.

Candidate name:
{name}

Target job role:
{job_role}

Education:
{education}

Original experience:
{experience}

Requirements for the professional summary:
- Write 2 to 3 concise sentences.
- Make it professional and ATS-friendly.
- Focus on the candidate's background and target role.
- Do not invent skills, experience, achievements,
  technologies, companies, numbers, or qualifications.
- Use only the information provided.
- Do not mention that you are an AI.
- Do not use first person.

Requirements for the experience:
- If no experience is provided, return an empty string.
- Preserve the factual meaning of the original experience.
- Improve clarity and professional wording.
- Use strong professional action verbs where appropriate.
- Do not invent responsibilities.
- Do not invent technologies.
- Do not invent metrics or achievements.
- Do not add experience that was not provided.
- Keep it concise.
- If multiple experience entries are provided,
  preserve their information without mixing them.

Return ONLY valid JSON in exactly this format:

{{
    "summary": "Professional summary here",
    "experience": "Improved experience content here"
}}
"""

    result = generate_ai_content(prompt)

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        cleaned_result = result.strip()

        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result[7:]

        elif cleaned_result.startswith("```"):
            cleaned_result = cleaned_result[3:]

        if cleaned_result.endswith("```"):
            cleaned_result = cleaned_result[:-3]

        cleaned_result = cleaned_result.strip()

        try:
            data = json.loads(cleaned_result)
        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned an invalid JSON response. "
                "Please try again."
            )

    summary = data.get("summary", "").strip()
    experience_content = data.get("experience", "").strip()

    if not summary:
        raise ValueError(
            "Gemini did not return a professional summary."
        )

    return {
        "summary": summary,
        "experience": experience_content,
    }


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

def generate_summary(
    name: str,
    job_role: str,
    education: str,
) -> str:
    """
    Kept for compatibility with existing code.

    NOTE:
    Prefer generate_resume_content() because it uses
    only ONE Gemini API request.
    """

    result = generate_resume_content(
        name=name,
        job_role=job_role,
        education=education,
        experience="",
    )

    return result["summary"]


def generate_experience(
    name: str,
    experience: str,
) -> str:
    """
    Kept for compatibility with existing code.

    NOTE:
    Prefer generate_resume_content() because it uses
    only ONE Gemini API request.
    """

    if not experience.strip():
        return ""

    result = generate_resume_content(
        name=name,
        job_role="",
        education="",
        experience=experience,
    )

    return result["experience"]