from app.database import SessionLocal
from app.services.job_ingestion import fetch_jobs
from app.services.job_normalizer import normalize_adzuna_job
from app.services.job_storage import save_job
from app.services.job_parser import parse_job_description


def ingest_jobs(
    country: str = "in",
    what: str = "software engineer intern",
    where: str = "Bangalore",
    results_per_page: int = 10,
) -> dict:

    jobs = fetch_jobs(
        country=country,
        what=what,
        where=where,
        results_per_page=results_per_page,
    )

    db = SessionLocal()

    inserted = 0
    updated = 0
    failed = 0

    try:
        for job in jobs:
            try:
                # Step 1: Normalize raw Adzuna job
                normalized_job = normalize_adzuna_job(job)

                # Step 2: AI analysis using Gemini
                analysis = parse_job_description(
                    description=normalized_job["description"],
                    title=normalized_job["title"],
                )

                # Step 3: Store AI-extracted information
                normalized_job["required_skills"] = (
                    analysis.required_skills
                )

                normalized_job["preferred_skills"] = (
                    analysis.preferred_skills
                )

                normalized_job["experience"] = analysis.experience
                normalized_job["education"] = analysis.education

                # Step 4: Check whether job already exists
                existing_job = None

                if normalized_job["external_job_id"]:
                    from app.models import Job

                    existing_job = (
                        db.query(Job)
                        .filter(
                            Job.external_job_id
                            == normalized_job["external_job_id"]
                        )
                        .first()
                    )

                # Step 5: Save / update job
                save_job(db, normalized_job)

                if existing_job:
                    updated += 1
                else:
                    inserted += 1

            except Exception as error:
                print(
                    f"Failed to process job "
                    f"{job.get('id')}: {error}"
                )
                failed += 1

        return {
            "fetched": len(jobs),
            "inserted": inserted,
            "updated": updated,
            "failed": failed,
        }

    finally:
        db.close()