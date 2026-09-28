from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, UserProfile as UserProfileModel

from app.schemas import (
    JobCreate,
    JobResponse,
    UserProfile,
    ResumeTailorRequest,
    ResumeTailorResponse,
)

from app.services.job_pipeline import ingest_jobs
from app.services.job_matcher import match_job_to_profile
from app.services.resume_tailor import tailor_resume


app = FastAPI(
    title="AI Job Intelligence",
    description="AI-powered job discovery, matching and recommendation system",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT + HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Job Intelligence API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# ============================================================
# JOB CREATION
# ============================================================

@app.post(
    "/jobs",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    existing_job = (
        db.query(Job)
        .filter(Job.external_job_id == job.external_job_id)
        .first()
    )

    if job.external_job_id and existing_job:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job with this external_job_id already exists.",
        )

    new_job = Job(**job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# ============================================================
# GET JOBS
# ============================================================

@app.get(
    "/jobs",
    response_model=list[JobResponse],
)
def get_jobs(
    db: Session = Depends(get_db),
    company: str | None = Query(
        default=None,
        description="Filter jobs by company",
    ),
    location: str | None = Query(
        default=None,
        description="Filter jobs by location",
    ),
    employment_type: str | None = Query(
        default=None,
        description="Filter jobs by employment type",
    ),
    skill: str | None = Query(
        default=None,
        description="Filter jobs by required skill",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of jobs to return",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of jobs to skip",
    ),
):
    query = db.query(Job)

    if company:
        query = query.filter(
            Job.company.ilike(f"%{company}%")
        )

    if location:
        query = query.filter(
            Job.locations.contains([location])
        )

    if employment_type:
        query = query.filter(
            Job.employment_type.ilike(f"%{employment_type}%")
        )

    if skill:
        query = query.filter(
            Job.required_skills.contains([skill])
        )

    jobs = (
        query
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return jobs


# ============================================================
# AI JOB MATCHES
# IMPORTANT:
# This route must come BEFORE /jobs/{job_id}
# ============================================================

@app.get("/jobs/matches")
def get_job_matches(
    db: Session = Depends(get_db),
    profile_id: int = Query(
        default=2,
        ge=1,
        description="Candidate profile ID",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Number of recommendations to return",
    ),
    min_score: float = Query(
        default=0,
        ge=0,
        le=100,
        description="Minimum match score",
    ),
    location: str | None = Query(
        default=None,
        description="Filter recommendations by location",
    ),
    company: str | None = Query(
        default=None,
        description="Filter recommendations by company",
    ),
    skill: str | None = Query(
        default=None,
        description="Filter recommendations by required skill",
    ),
):
    profile = db.get(UserProfileModel, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found.",
        )

    jobs = (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .all()
    )

    if not jobs:
        return {
            "profile_id": profile_id,
            "total_jobs": 0,
            "filtered_jobs": 0,
            "matches": [],
        }

    matches = []

    for job in jobs:

        # Company filter
        if company:
            if company.lower() not in job.company.lower():
                continue

        # Location filter
        if location:
            job_locations = [
                item.lower()
                for item in job.locations
            ]

            if not any(
                location.lower() in item
                for item in job_locations
            ):
                continue

        # Skill filter
        if skill:
            job_skills = [
                item.lower()
                for item in job.required_skills
            ]

            if not any(
                skill.lower() in item
                for item in job_skills
            ):
                continue

        match_result = match_job_to_profile(
            profile=profile,
            job=job,
        )

        # Minimum score filter
        if match_result["match_score"] < min_score:
            continue

        match_result["url"] = job.url
        match_result["locations"] = job.locations
        match_result["source"] = job.source

        matches.append(match_result)

    # Highest matching jobs first
    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return {
        "profile_id": profile_id,
        "total_jobs": len(jobs),
        "filtered_jobs": len(matches),
        "matches": matches[:limit],
    }


# ============================================================
# RESUME TAILORING
# ============================================================

@app.post(
    "/resume/tailor",
    response_model=ResumeTailorResponse,
)
def tailor_resume_endpoint(
    request: ResumeTailorRequest,
):
    """
    Tailor a candidate resume for a specific job.

    The endpoint:
    1. Parses the target job description.
    2. Calculates deterministic skill alignment.
    3. Generates a tailored summary and experience.
    4. Returns ATS-style analysis and skill gaps.
    """

    try:
        result = tailor_resume(
            name=request.name,
            job_title=request.job_title,
            job_description=request.job_description,
            education=request.education,
            experience=request.experience,
            candidate_skills=request.candidate_skills,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume tailoring failed: {str(exc)}",
        )


# ============================================================
# GET SINGLE JOB
# ============================================================

@app.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {job_id} not found.",
        )

    return job


# ============================================================
# JOB INGESTION
# ============================================================

@app.post("/jobs/ingest")
def ingest_jobs_endpoint(
    what: str = Query(
        default="software engineer intern",
        description="Job search keywords",
    ),
    where: str = Query(
        default="Bangalore",
        description="Job location",
    ),
    results_per_page: int = Query(
        default=10,
        ge=1,
        le=20,
        description="Number of jobs to fetch",
    ),
):
    return ingest_jobs(
        what=what,
        where=where,
        results_per_page=results_per_page,
    )


# ============================================================
# CREATE PROFILE
# ============================================================

@app.post("/profile")
def create_profile(
    profile: UserProfile,
    db: Session = Depends(get_db),
):
    new_profile = UserProfileModel(
        name=profile.name,
        education=profile.education,
        experience=profile.experience,
        roles=profile.roles,
        locations=profile.locations,
        skills=profile.skills,
        graduation_year=profile.graduation_year,
        work_type=profile.work_type,
        companies=profile.companies,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Profile saved successfully",
        "profile_id": new_profile.id,
        "profile": profile.model_dump(),
    }

# ============================================================
# GET PROFILE
# ============================================================

@app.get("/profile/{profile_id}")
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.get(UserProfileModel, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found.",
        )

    return {
        "profile_id": profile.id,
        "name": profile.name,
        "education": profile.education,
        "experience": profile.experience,
        "roles": profile.roles,
        "locations": profile.locations,
        "skills": profile.skills,
        "graduation_year": profile.graduation_year,
        "work_type": profile.work_type,
        "companies": profile.companies,
    }


# ============================================================
# UPDATE PROFILE
# ============================================================

@app.put("/profile/{profile_id}")
def update_profile(
    profile_id: int,
    profile: UserProfile,
    db: Session = Depends(get_db),
):
    existing_profile = db.get(
        UserProfileModel,
        profile_id,
    )

    if existing_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found.",
        )

    existing_profile.name = profile.name
    existing_profile.education = profile.education
    existing_profile.experience = profile.experience
    existing_profile.roles = profile.roles
    existing_profile.locations = profile.locations
    existing_profile.skills = profile.skills
    existing_profile.graduation_year = profile.graduation_year
    existing_profile.work_type = profile.work_type
    existing_profile.companies = profile.companies

    db.commit()
    db.refresh(existing_profile)

    return {
        "message": "Profile updated successfully",
        "profile_id": existing_profile.id,
        "profile": {
            "name": existing_profile.name,
            "education": existing_profile.education,
            "experience": existing_profile.experience,
            "roles": existing_profile.roles,
            "locations": existing_profile.locations,
            "skills": existing_profile.skills,
            "graduation_year": existing_profile.graduation_year,
            "work_type": existing_profile.work_type,
            "companies": existing_profile.companies,
        },
    }