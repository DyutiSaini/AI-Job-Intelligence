from app.services.resume_tailor import tailor_resume


result = tailor_resume(
    name="Dyuti Saini",
    job_title="Software Engineer Intern",
    job_description="""
    We are looking for a Software Engineer Intern to work on
    backend services and web applications.

    Responsibilities include developing APIs, working with
    databases, writing Python code, and collaborating with
    engineering teams.

    Required skills:
    Python, FastAPI, PostgreSQL, Git

    Preferred:
    Docker, React
    """,
    education="B.Tech in Computer Science Engineering with specialization in Artificial Intelligence",
    experience="""
    Built full-stack web applications using React and Python.
    Developed backend APIs using FastAPI.
    Worked with PostgreSQL and MongoDB.
    Built projects involving AI-powered financial analytics.
    """,
    candidate_skills=[
        "Python",
        "FastAPI",
        "PostgreSQL",
        "React",
        "MongoDB",
    ],
)


print("\n===== TAILORED SUMMARY =====")
print(result["tailored_summary"])

print("\n===== TAILORED EXPERIENCE =====")
print(result["tailored_experience"])

print("\n===== ATS ANALYSIS =====")
print(result["ats_analysis"])

print("\n===== TAILORING NOTES =====")
for note in result["tailoring_notes"]:
    print("-", note)