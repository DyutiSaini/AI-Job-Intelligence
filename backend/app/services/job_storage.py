from sqlalchemy.orm import Session

from app.models import Job


def save_job(db: Session, job_data: dict) -> Job:
    """
    Insert a new job or update an existing job using external_job_id.
    """

    external_job_id = job_data.get("external_job_id")

    existing_job = None

    if external_job_id:
        existing_job = (
            db.query(Job)
            .filter(Job.external_job_id == external_job_id)
            .first()
        )

    if existing_job:
        for key, value in job_data.items():
            setattr(existing_job, key, value)

        db.commit()
        db.refresh(existing_job)

        return existing_job

    new_job = Job(**job_data)

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job