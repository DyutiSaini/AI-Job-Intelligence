from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from app.config import settings


class JobAnalysis(BaseModel):
    role: str = Field(
        description="The primary role or job title."
    )

    required_skills: list[str] = Field(
        description=(
            "Technical skills, programming languages, frameworks, "
            "tools, databases, platforms, APIs, or technologies "
            "that the job description explicitly states or clearly "
            "indicates are needed for the role."
        )
    )

    preferred_skills: list[str] = Field(
        description=(
            "Technical skills, technologies, tools, or platforms "
            "that the job description explicitly describes as "
            "preferred, optional, nice-to-have, bonus, or additional."
        )
    )

    experience: str | None = Field(
        description=(
            "Explicit experience requirement such as 0 years, "
            "1-2 years, internship experience, or similar. "
            "Return null if not mentioned."
        )
    )

    education: str | None = Field(
        description=(
            "Explicit education requirement such as degree, "
            "field of study, or graduation requirement. "
            "Return null if not mentioned."
        )
    )


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def parse_job_description(
    description: str,
    title: str = "",
) -> JobAnalysis:

    prompt = f"""
You are an expert job-description information extraction system.

Analyze the following job posting and extract structured information.

JOB TITLE:
{title}

JOB DESCRIPTION:
{description}

IMPORTANT EXTRACTION RULES:

1. Extract only information that is explicitly present
   or clearly supported by the job description.

2. REQUIRED SKILLS:
   Include technologies and technical skills that the job
   description presents as relevant, necessary, expected,
   or part of the work.

   This includes:
   - Programming languages
   - Frameworks
   - Libraries
   - Databases
   - APIs
   - Cloud platforms
   - Developer tools
   - Software technologies
   - Technical concepts

   IMPORTANT:
   A skill does NOT need to appear under a heading such as
   "Required Skills" to be included.

   For example, if the description says:
   "Build backend services using Python and PostgreSQL"
   then Python and PostgreSQL should be extracted.

3. PREFERRED SKILLS:
   Include skills explicitly described as:
   - preferred
   - optional
   - nice to have
   - bonus
   - plus
   - additional

4. Do NOT invent technologies that are not mentioned
   or clearly supported by the job description.

5. Keep skill names concise and standardized.
   Examples:
   - Python
   - C++
   - PostgreSQL
   - React
   - Node.js
   - REST APIs
   - Docker
   - Git

6. EXPERIENCE:
   Extract the explicit experience requirement.
   Examples:
   - "0 years"
   - "1-2 years"
   - "Freshers"
   - "Internship experience"

   If no experience requirement is mentioned, return null.

7. EDUCATION:
   Extract only explicit education requirements.
   If none are mentioned, return null.

8. Do not include general soft skills such as:
   - communication
   - teamwork
   - leadership
   - enthusiasm
   - curiosity

   unless they are specifically technical skills.

Return the structured result according to the provided schema.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JobAnalysis,
        ),
    )

    if response.parsed is None:
        raise ValueError(
            "Gemini returned an invalid job analysis."
        )

    return response.parsed