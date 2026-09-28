from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    external_job_id: str | None = Field(
        default=None,
        max_length=255
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    company: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    locations: list[str] = Field(
        default_factory=list
    )

    employment_type: str | None = Field(
        default=None,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=1
    )

    required_skills: list[str] = Field(
        default_factory=list
    )

    preferred_skills: list[str] = Field(
        default_factory=list
    )

    experience: str | None = Field(
        default=None,
        max_length=255
    )

    education: str | None = Field(
        default=None,
        max_length=255
    )

    source: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    url: str = Field(
        ...,
        min_length=1
    )

    posted_at: datetime | None = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserProfile(BaseModel):
    name: str | None = None
    education: str | None = None
    experience: str | None = None

    roles: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)

    graduation_year: int | None = None

    work_type: list[str] = Field(default_factory=list)
    companies: list[str] = Field(default_factory=list)


# ============================================================
# Resume Tailoring Schemas
# ============================================================

class ResumeTailorRequest(BaseModel):
    """
    Input data required to tailor a resume for a specific job.
    """

    name: str = Field(
        ...,
        min_length=1
    )

    job_title: str = Field(
        ...,
        min_length=1
    )

    job_description: str = Field(
        ...,
        min_length=1
    )

    education: str = Field(
        default=""
    )

    experience: str = Field(
        default=""
    )

    candidate_skills: list[str] = Field(
        default_factory=list
    )


class ATSAnalysisResponse(BaseModel):
    """
    Deterministic ATS-style skill alignment analysis.
    """

    ats_score: float

    required_matches: list[str] = Field(
        default_factory=list
    )

    required_gaps: list[str] = Field(
        default_factory=list
    )

    preferred_matches: list[str] = Field(
        default_factory=list
    )

    required_score: float

    preferred_score: float


class JobAnalysisResponse(BaseModel):
    """
    Structured information extracted from the target job.
    """

    role: str

    required_skills: list[str] = Field(
        default_factory=list
    )

    preferred_skills: list[str] = Field(
        default_factory=list
    )

    experience: str | None = None

    education: str | None = None


class ResumeTailorResponse(BaseModel):
    """
    Final response returned by the resume tailoring API.
    """

    job_title: str

    job_analysis: JobAnalysisResponse

    tailored_summary: str

    tailored_experience: str

    tailoring_notes: list[str] = Field(
        default_factory=list
    )

    ats_analysis: ATSAnalysisResponse