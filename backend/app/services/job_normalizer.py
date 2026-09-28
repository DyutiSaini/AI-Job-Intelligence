from datetime import datetime, timezone


def normalize_adzuna_job(job: dict) -> dict:
    """
    Convert an Adzuna job response into our standardized Job format.
    """

    company = job.get("company", {})
    location = job.get("location", {})

    created = job.get("created")

    posted_at = None

    if created:
        posted_at = datetime.fromisoformat(
            created.replace("Z", "+00:00")
        )

    return {
        "external_job_id": str(job.get("id")) if job.get("id") else None,
        "title": job.get("title", "").strip(),
        "company": company.get("display_name", "Unknown").strip(),
        "locations": (
            [location["display_name"]]
            if location.get("display_name")
            else []
        ),
        "employment_type": None,
        "description": job.get("description", "").strip(),
        "required_skills": [],
        "preferred_skills": [],
        "experience": None,
        "education": None,
        "source": "Adzuna",
        "url": job.get("redirect_url", ""),
        "posted_at": posted_at,
    }