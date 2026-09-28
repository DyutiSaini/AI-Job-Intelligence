# AI Job Intelligence

An AI-powered job discovery, matching, and resume-tailoring platform that helps candidates find relevant opportunities and understand why each job matches their profile.

## Overview

AI Job Intelligence combines job aggregation, LLM-based job-description analysis, deterministic candidate-job matching, recommendation ranking, and AI-assisted resume tailoring into a single application.

The current system supports:

- Fetching jobs from the Adzuna API
- Normalizing external job data into a common schema
- Extracting structured information from job descriptions using Gemini
- Storing jobs and candidate profiles in PostgreSQL
- Matching jobs against candidate profiles
- Ranking recommendations using a hybrid scoring model
- Explaining matches through matched skills and potential gaps
- Tailoring resume summaries and experience for individual jobs
- Generating ATS-style skill-alignment analysis
- Evaluating recommendation quality using Precision@K, Recall@K, and NDCG@K
- Providing a React-based dashboard for interacting with recommendations

> **Current scope:** This repository focuses on job intelligence, recommendation, and resume tailoring. Automated applications, referral discovery, email notifications, and application tracking are not currently implemented.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │   Dashboard/Profile  │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ Job         │   │ Job         │   │ Resume      │
      │ Ingestion   │   │ Matching    │   │ Tailoring   │
      └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
             │                 │                 │
             ▼                 ▼                 ▼
        Adzuna API       Matching Engine       Gemini
             │                 │                 │
             ▼                 └────────┬────────┘
      ┌─────────────┐                   │
      │ JD Parser   │◄──────────────────┘
      │   Gemini    │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │ PostgreSQL  │
      └─────────────┘
```

---

## Core Workflow

### 1. Job Discovery

Jobs are fetched from Adzuna using configurable search parameters such as:

- Job keywords
- Location
- Number of results
- Country

The raw external response is normalized into the application's internal `Job` schema.

```text
Adzuna
  ↓
Fetch jobs
  ↓
Normalize
  ↓
Parse JD
  ↓
Store in PostgreSQL
```

### 2. Job Description Intelligence

Gemini analyzes each job description and extracts structured information:

- Role
- Required skills
- Preferred skills
- Experience requirements
- Education requirements

The extraction uses structured Pydantic output and explicit prompts designed to avoid inventing requirements.

### 3. Candidate-Job Matching

Each stored job is compared against a candidate profile.

The current hybrid score consists of:

| Component | Weight |
|---|---:|
| Required skill match | 35% |
| Text similarity | 30% |
| Experience compatibility | 20% |
| Location match | 10% |
| Preferred company match | 5% |

The result includes both the overall score and its individual components.

### 4. Explainable Recommendations

For every recommendation, the system can provide:

- Overall match score
- Skill score
- Text similarity score
- Experience score
- Location score
- Company score
- Matched skills
- Missing skills
- Reasons for the match
- Potential gaps

This allows the candidate to understand why a job was recommended instead of receiving only a black-box score.

### 5. Resume Tailoring

For a selected job, the candidate profile and job description are passed through the resume-tailoring pipeline.

```text
Job Description
      ↓
JD Analysis
      ↓
Skill Alignment
      ↓
Gemini Resume Tailoring
      ↓
Tailored Summary
      +
Tailored Experience
      +
ATS Analysis
```

The tailoring prompt explicitly instructs the model not to fabricate:

- Companies
- Projects
- Technologies
- Responsibilities
- Achievements
- Metrics
- Certifications
- Missing skills

The system therefore focuses on rewriting and emphasizing information that is already supported by the candidate's profile.

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Gemini API
- Adzuna API

### Frontend

- React
- React Router
- Vite
- JavaScript

### Resume Generator

A separate Streamlit-based resume generator is included with:

- Streamlit
- Gemini
- Jinja2
- HTML/CSS resume template
- pdfkit / wkhtmltopdf

### Evaluation

- Precision@K
- Recall@K
- NDCG@K
- scikit-learn

---

## Project Structure

```text
AI-Job-Intelligence/
│
├── backend/
│   ├── app/
│   │   ├── evaluation/
│   │   │   ├── evaluator.py
│   │   │   ├── evaluation_dataset.py
│   │   │   └── run_evaluation.py
│   │   │
│   │   ├── services/
│   │   │   ├── job_ingestion.py
│   │   │   ├── job_normalizer.py
│   │   │   ├── job_parser.py
│   │   │   ├── job_pipeline.py
│   │   │   ├── job_storage.py
│   │   │   ├── job_matcher.py
│   │   │   └── resume_tailor.py
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── FilterBar.jsx
│       │   ├── JobCard.jsx
│       │   └── Navbar.jsx
│       │
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── JobDetails.jsx
│       │   └── Profile.jsx
│       │
│       ├── services/
│       │   └── api.js
│       │
│       └── App.jsx
│
└── resume-generator/
    ├── app.py
    ├── chains.py
    └── templates/
```

---

## API Endpoints

### Health

```text
GET /
GET /health
```

### Jobs

```text
POST /jobs
GET  /jobs
GET  /jobs/{job_id}
GET  /jobs/matches
POST /jobs/ingest
```

### Candidate Profile

```text
POST /profile
GET  /profile/{profile_id}
PUT  /profile/{profile_id}
```

### Resume Tailoring

```text
POST /resume/tailor
```

---

## Matching Example

A candidate profile might contain:

```text
Roles:
Software Engineer Intern

Skills:
Python, Go, PostgreSQL, Docker

Locations:
Bangalore, Delhi NCR

Preferred Companies:
Google, Microsoft
```

A job is then evaluated across multiple dimensions rather than using a single keyword check.

Example output:

```text
Overall Match: 82%

Skill Match:        91%
Text Similarity:    76%
Experience Match:  100%
Location Match:    100%
Company Match:       0%

Matched Skills:
Python
PostgreSQL
Docker

Potential Gaps:
Kubernetes
```

---

## Setup

### Prerequisites

Install:

- Python 3.11+
- Node.js
- PostgreSQL
- A Gemini API key
- An Adzuna API account and credentials

### Backend

Create a virtual environment:

```bash
cd backend

python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=postgresql+psycopg2://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

GEMINI_API_KEY=your_gemini_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs through Vite.

Make sure the backend is running before using the dashboard.

---

## Job Ingestion

Jobs can be ingested through the backend endpoint.

Example:

```text
POST /jobs/ingest?what=software%20engineer%20intern&where=Bangalore&results_per_page=10
```

The pipeline:

1. Fetches jobs from Adzuna
2. Normalizes the raw response
3. Sends job descriptions to Gemini
4. Extracts structured job information
5. Checks for existing jobs
6. Inserts new jobs or updates existing jobs
7. Stores the result in PostgreSQL

---

## Recommendation Evaluation

The repository includes an experimental evaluation pipeline for comparing:

- Skill-based matching
- Text-similarity matching
- Hybrid matching

The evaluation calculates:

```text
Precision@5
Recall@5
NDCG@5
```

The current relevance labels are manually defined for the evaluation dataset. They are intended for experimentation rather than representing a large production benchmark.

---

## Standalone Resume Generator

The `resume-generator/` directory contains a separate Streamlit application for generating a complete PDF resume.

It supports:

- Personal information
- Education
- Technical skills
- Up to two experience entries
- Up to three projects
- Achievements and certifications
- AI-generated professional summary
- AI-assisted experience rewriting
- HTML resume preview
- PDF generation

Run it with:

```bash
cd resume-generator
streamlit run app.py
```

The PDF generation component currently depends on a local `wkhtmltopdf` installation.

---

## Current Limitations

The current implementation does **not** include:

- User authentication
- Multi-user account management
- Automated scheduled job ingestion
- Multiple job-board integrations
- Email notifications
- Automatic job applications
- Application status tracking
- Referral discovery
- Referral outreach
- Gmail integration
- Automated follow-ups
- Browser-based application automation
- Fully autonomous multi-agent orchestration

The recommendation similarity component currently uses local token-based text similarity rather than a production embedding/vector-search architecture.

---

## Roadmap

The project can be extended toward a complete AI job-search agent.

### Phase 1 — Job Intelligence

- [x] Job ingestion
- [x] Job normalization
- [x] JD parsing
- [x] Candidate profiles
- [x] Job matching
- [x] Recommendation ranking
- [x] Match explanations
- [x] Resume tailoring

### Phase 2 — Job Discovery Infrastructure

- [ ] Scheduled ingestion
- [ ] Multiple job sources
- [ ] Deduplication across sources
- [ ] Better job freshness handling
- [ ] Embedding-based retrieval
- [ ] Improved ranking evaluation

### Phase 3 — Candidate Workflow

- [ ] Application database
- [ ] Application status tracking
- [ ] Saved jobs
- [ ] Application history
- [ ] Email notifications
- [ ] Personalized job digests

### Phase 4 — Agentic Job Application

- [ ] Application agent
- [ ] Resume selection/tailoring agent
- [ ] Referral discovery
- [ ] Referral message generation
- [ ] Application form assistance
- [ ] Follow-up agent
- [ ] Human approval before external actions

---

## Design Principles

### 1. Don't fabricate candidate information

AI-generated resume content should only be derived from information supplied by the candidate.

### 2. Explain recommendations

A recommendation should provide enough information for a candidate to understand the underlying match.

### 3. Separate deterministic scoring from generative AI

Where possible:

- AI handles extraction and language generation.
- Deterministic code handles scoring, filtering, and structured business logic.

### 4. Keep external actions controllable

Future automation such as applications and emails should support explicit candidate approval before taking consequential external actions.

---

## Status

**Current stage:** Functional prototype / MVP

The implemented system already covers the core **job intelligence pipeline**:

```text
Discover
   ↓
Parse
   ↓
Match
   ↓
Rank
   ↓
Explain
   ↓
Tailor Resume
```

The next major step is extending this foundation into an end-to-end job-search workflow with applications, referrals, notifications, and application tracking.
