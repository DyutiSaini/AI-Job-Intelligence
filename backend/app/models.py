from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    external_job_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    locations: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    required_skills: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False
    )

    preferred_skills: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False
    )

    experience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    education: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # Resume information
    name = Column(String(255), nullable=True)
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)

    # Job preferences
    roles = Column(JSONB, nullable=False, default=list)
    locations = Column(JSONB, nullable=False, default=list)
    skills = Column(JSONB, nullable=False, default=list)

    graduation_year = Column(Integer, nullable=True)

    work_type = Column(JSONB, nullable=False, default=list)
    companies = Column(JSONB, nullable=False, default=list)