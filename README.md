# AI Job Intelligence

### Explainable Hybrid Job Recommendation & Resume Tailoring Platform

AI Job Intelligence is a full-stack AI-powered platform that analyzes job opportunities against a candidate's profile, ranks jobs using an explainable hybrid matching system, identifies skill gaps, and generates job-specific resume improvements.

The project combines **deterministic scoring, semantic similarity, Gemini-based job analysis, PostgreSQL, FastAPI, React, and an AI-powered Resume Generator** into a single end-to-end system.

---

## 🚀 Overview

Finding relevant internship and job opportunities can be time-consuming because candidates often need to manually compare job descriptions, required skills, experience requirements, and their own qualifications.

**AI Job Intelligence** automates this analysis by allowing a candidate to maintain a structured profile and receive personalized job recommendations based on:

- Technical skill compatibility
- Semantic similarity between the candidate profile and job description
- Experience requirements
- Location compatibility
- Company preferences
- Skill gaps

The platform also provides:

- Explainable match scores
- Matched and missing skills
- AI-powered job description parsing
- AI-powered resume tailoring
- Standalone AI resume generation
- Recommendation evaluation using ranking metrics

---

## ✨ Key Features

### 1. AI-Powered Job Analysis

Job descriptions are analyzed using **Google Gemini** to extract structured information such as:

- Required technical skills
- Preferred skills
- Experience requirements
- Education requirements

This converts unstructured job descriptions into structured data that can be used by the recommendation engine.

---

### 2. Explainable Hybrid Job Matching

The recommendation engine combines multiple signals instead of relying only on an LLM-generated score.

The current hybrid scoring system uses:

| Signal | Weight |
|---|---:|
| Skill Compatibility | 35% |
| Semantic Similarity | 30% |
| Experience Compatibility | 20% |
| Location Compatibility | 10% |
| Other / Company Signal | 5% |

The final score is calculated programmatically.

This makes recommendations more transparent and allows the system to explain **why a job matches a candidate**.

---

### 3. Skill Gap Detection

For every recommendation, the platform identifies:

- Skills already matched by the candidate
- Required skills that are missing
- Additional preferred skills that may improve compatibility

This helps candidates understand what they may need to learn or strengthen for a particular opportunity.

---

### 4. Semantic Job Matching

The system uses **Gemini Embeddings** to measure semantic similarity between:

- Candidate profile information
- Job descriptions

This allows the system to capture relevant relationships beyond exact keyword matching.

---

### 5. AI Resume Tailoring

Candidates can tailor their resume content for a specific job.

The system:

1. Retrieves the candidate's current profile.
2. Analyzes the selected job description.
3. Calculates deterministic skill alignment.
4. Uses Gemini to rewrite relevant resume sections.
5. Produces a tailored professional summary and experience content.
6. Provides tailoring notes.

The system is designed to avoid inventing qualifications or experience that are not present in the candidate profile.

---

### 6. AI Resume Generator

The repository also contains a standalone **Streamlit-based AI Resume Generator**.

It supports:

- Personal information
- Education
- Skills
- Experience
- Projects
- Achievements and certifications
- AI-generated professional summary
- AI-enhanced experience descriptions
- HTML resume rendering
- PDF generation
- Downloadable resume output

The generated resume uses a structured professional template.

---

### 7. Candidate Profile Management

The platform allows candidates to maintain structured profile information including:

- Name
- Education
- Experience
- Target roles
- Preferred locations
- Skills
- Graduation year
- Work type
- Preferred companies

This profile is used as the basis for personalized recommendations.

---

### 8. Recommendation Evaluation

The project includes an evaluation module for measuring ranking quality using:

- Precision@K
- Recall@K
- NDCG@K

The evaluation framework is designed to compare recommendation quality using labeled job relevance data.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Candidate Profile │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Data / Jobs   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Normalizer    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemini Job Parser │
                    │ Skills / Experience │
                    │ Education Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │      Hybrid Matching Engine     │
              │                                 │
              │ • Skill Compatibility           │
              │ • Semantic Similarity           │
              │ • Experience Compatibility     │
              │ • Location Compatibility       │
              │ • Company / Other Signals      │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Ranked Job List   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌─────────────┐ ┌──────────────┐
        │ Match Score│ │ Skill Gaps  │ │ Job Details  │
        └────────────┘ └─────────────┘ └──────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume Tailoring  │
                    │      with Gemini    │
                    └─────────────────────┘

# AI Job Intelligence

### Explainable Hybrid Job Recommendation & Resume Tailoring Platform

AI Job Intelligence is a full-stack AI-powered platform that analyzes job opportunities against a candidate's profile, ranks jobs using an explainable hybrid matching system, identifies skill gaps, and generates job-specific resume improvements.

The project combines **deterministic scoring, semantic similarity, Gemini-based job analysis, PostgreSQL, FastAPI, React, and an AI-powered Resume Generator** into a single end-to-end system.

---

## 🚀 Overview

Finding relevant internship and job opportunities can be time-consuming because candidates often need to manually compare job descriptions, required skills, experience requirements, and their own qualifications.

**AI Job Intelligence** automates this analysis by allowing a candidate to maintain a structured profile and receive personalized job recommendations based on:

- Technical skill compatibility
- Semantic similarity between the candidate profile and job description
- Experience requirements
- Location compatibility
- Company preferences
- Skill gaps

The platform also provides:

- Explainable match scores
- Matched and missing skills
- AI-powered job description parsing
- AI-powered resume tailoring
- Standalone AI resume generation
- Recommendation evaluation using ranking metrics

---

## ✨ Key Features

### 1. AI-Powered Job Analysis

Job descriptions are analyzed using **Google Gemini** to extract structured information such as:

- Required technical skills
- Preferred skills
- Experience requirements
- Education requirements

This converts unstructured job descriptions into structured data that can be used by the recommendation engine.

---

### 2. Explainable Hybrid Job Matching

The recommendation engine combines multiple signals instead of relying only on an LLM-generated score.

The current hybrid scoring system uses:

| Signal | Weight |
|---|---:|
| Skill Compatibility | 35% |
| Semantic Similarity | 30% |
| Experience Compatibility | 20% |
| Location Compatibility | 10% |
| Other / Company Signal | 5% |

The final score is calculated programmatically.

This makes recommendations more transparent and allows the system to explain **why a job matches a candidate**.

---

### 3. Skill Gap Detection

For every recommendation, the platform identifies:

- Skills already matched by the candidate
- Required skills that are missing
- Additional preferred skills that may improve compatibility

This helps candidates understand what they may need to learn or strengthen for a particular opportunity.

---

### 4. Semantic Job Matching

The system uses **Gemini Embeddings** to measure semantic similarity between:

- Candidate profile information
- Job descriptions

This allows the system to capture relevant relationships beyond exact keyword matching.

---

### 5. AI Resume Tailoring

Candidates can tailor their resume content for a specific job.

The system:

1. Retrieves the candidate's current profile.
2. Analyzes the selected job description.
3. Calculates deterministic skill alignment.
4. Uses Gemini to rewrite relevant resume sections.
5. Produces a tailored professional summary and experience content.
6. Provides tailoring notes.

The system is designed to avoid inventing qualifications or experience that are not present in the candidate profile.

---

### 6. AI Resume Generator

The repository also contains a standalone **Streamlit-based AI Resume Generator**.

It supports:

- Personal information
- Education
- Skills
- Experience
- Projects
- Achievements and certifications
- AI-generated professional summary
- AI-enhanced experience descriptions
- HTML resume rendering
- PDF generation
- Downloadable resume output

The generated resume uses a structured professional template.

---

### 7. Candidate Profile Management

The platform allows candidates to maintain structured profile information including:

- Name
- Education
- Experience
- Target roles
- Preferred locations
- Skills
- Graduation year
- Work type
- Preferred companies

This profile is used as the basis for personalized recommendations.

---

### 8. Recommendation Evaluation

The project includes an evaluation module for measuring ranking quality using:

- Precision@K
- Recall@K
- NDCG@K

The evaluation framework is designed to compare recommendation quality using labeled job relevance data.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Candidate Profile │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Data / Jobs   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Normalizer    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemini Job Parser │
                    │ Skills / Experience │
                    │ Education Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │      Hybrid Matching Engine     │
              │                                 │
              │ • Skill Compatibility           │
              │ • Semantic Similarity           │
              │ • Experience Compatibility     │
              │ • Location Compatibility       │
              │ • Company / Other Signals      │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Ranked Job List   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌─────────────┐ ┌──────────────┐
        │ Match Score│ │ Skill Gaps  │ │ Job Details  │
        └────────────┘ └─────────────┘ └──────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume Tailoring  │
                    │      with Gemini    │
                    └─────────────────────┘

# AI Job Intelligence

### Explainable Hybrid Job Recommendation & Resume Tailoring Platform

AI Job Intelligence is a full-stack AI-powered platform that analyzes job opportunities against a candidate's profile, ranks jobs using an explainable hybrid matching system, identifies skill gaps, and generates job-specific resume improvements.

The project combines **deterministic scoring, semantic similarity, Gemini-based job analysis, PostgreSQL, FastAPI, React, and an AI-powered Resume Generator** into a single end-to-end system.

---

## 🚀 Overview

Finding relevant internship and job opportunities can be time-consuming because candidates often need to manually compare job descriptions, required skills, experience requirements, and their own qualifications.

**AI Job Intelligence** automates this analysis by allowing a candidate to maintain a structured profile and receive personalized job recommendations based on:

- Technical skill compatibility
- Semantic similarity between the candidate profile and job description
- Experience requirements
- Location compatibility
- Company preferences
- Skill gaps

The platform also provides:

- Explainable match scores
- Matched and missing skills
- AI-powered job description parsing
- AI-powered resume tailoring
- Standalone AI resume generation
- Recommendation evaluation using ranking metrics

---

## ✨ Key Features

### 1. AI-Powered Job Analysis

Job descriptions are analyzed using **Google Gemini** to extract structured information such as:

- Required technical skills
- Preferred skills
- Experience requirements
- Education requirements

This converts unstructured job descriptions into structured data that can be used by the recommendation engine.

---

### 2. Explainable Hybrid Job Matching

The recommendation engine combines multiple signals instead of relying only on an LLM-generated score.

The current hybrid scoring system uses:

| Signal | Weight |
|---|---:|
| Skill Compatibility | 35% |
| Semantic Similarity | 30% |
| Experience Compatibility | 20% |
| Location Compatibility | 10% |
| Other / Company Signal | 5% |

The final score is calculated programmatically.

This makes recommendations more transparent and allows the system to explain **why a job matches a candidate**.

---

### 3. Skill Gap Detection

For every recommendation, the platform identifies:

- Skills already matched by the candidate
- Required skills that are missing
- Additional preferred skills that may improve compatibility

This helps candidates understand what they may need to learn or strengthen for a particular opportunity.

---

### 4. Semantic Job Matching

The system uses **Gemini Embeddings** to measure semantic similarity between:

- Candidate profile information
- Job descriptions

This allows the system to capture relevant relationships beyond exact keyword matching.

---

### 5. AI Resume Tailoring

Candidates can tailor their resume content for a specific job.

The system:

1. Retrieves the candidate's current profile.
2. Analyzes the selected job description.
3. Calculates deterministic skill alignment.
4. Uses Gemini to rewrite relevant resume sections.
5. Produces a tailored professional summary and experience content.
6. Provides tailoring notes.

The system is designed to avoid inventing qualifications or experience that are not present in the candidate profile.

---

### 6. AI Resume Generator

The repository also contains a standalone **Streamlit-based AI Resume Generator**.

It supports:

- Personal information
- Education
- Skills
- Experience
- Projects
- Achievements and certifications
- AI-generated professional summary
- AI-enhanced experience descriptions
- HTML resume rendering
- PDF generation
- Downloadable resume output

The generated resume uses a structured professional template.

---

### 7. Candidate Profile Management

The platform allows candidates to maintain structured profile information including:

- Name
- Education
- Experience
- Target roles
- Preferred locations
- Skills
- Graduation year
- Work type
- Preferred companies

This profile is used as the basis for personalized recommendations.

---

### 8. Recommendation Evaluation

The project includes an evaluation module for measuring ranking quality using:

- Precision@K
- Recall@K
- NDCG@K

The evaluation framework is designed to compare recommendation quality using labeled job relevance data.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Candidate Profile │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Data / Jobs   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Normalizer    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemini Job Parser │
                    │ Skills / Experience │
                    │ Education Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │      Hybrid Matching Engine     │
              │                                 │
              │ • Skill Compatibility           │
              │ • Semantic Similarity           │
              │ • Experience Compatibility     │
              │ • Location Compatibility       │
              │ • Company / Other Signals      │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Ranked Job List   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌─────────────┐ ┌──────────────┐
        │ Match Score│ │ Skill Gaps  │ │ Job Details  │
        └────────────┘ └─────────────┘ └──────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume Tailoring  │
                    │      with Gemini    │
                    └─────────────────────┘
Recommendation Pipeline
Candidate Profile
        │
        ▼
Profile Normalization
        │
        ▼
Job Description
        │
        ▼
AI Job Parsing
        │
        ├── Required Skills
        ├── Preferred Skills
        ├── Experience
        └── Education
        │
        ▼
Feature Matching
        │
        ├── Skill Match
        ├── Semantic Match
        ├── Experience Match
        ├── Location Match
        └── Other Signals
        │
        ▼
Hybrid Score
        │
        ▼
Ranked Recommendations
        │
        ├── Matched Skills
        └── Skill Gaps

🧠 Matching Methodology

The recommendation score is calculated using a weighted hybrid approach:

Final Score =
    0.35 × Skill Score
  + 0.30 × Semantic Score
  + 0.20 × Experience Score
  + 0.10 × Location Score
  + 0.05 × Other Score
Skill Compatibility

Skill compatibility compares candidate skills against the required and preferred skills extracted from the job description.

Required skills have greater importance than preferred skills.

Semantic Similarity

Gemini Embeddings are used to calculate semantic similarity between candidate information and the job description.

Experience Compatibility

The system considers the experience requirements of the job against the candidate's profile.

Location Compatibility

Candidate location preferences are compared against the job's available locations.

Explainability

Instead of returning only a numerical score, the platform provides interpretable information such as:

Overall Match: 68%

Skill Match: 40%
Semantic Match: 97%
Location Match: 100%

Matched Skills:
- Python
- C++

Skill Gaps:
- Git
- REST APIs
- SQL
🛠️ Tech Stack
Frontend
React.js
React Router
Vite
JavaScript
HTML
CSS
Backend
Python
FastAPI
SQLAlchemy
Pydantic
Uvicorn
Database
PostgreSQL
AI / Machine Learning
Google Gemini API
Gemini Embeddings
Gemini-based structured job analysis
AI-powered resume tailoring
Semantic similarity
Scikit-learn for recommendation evaluation
Resume Generation
Streamlit
Jinja2
pdfkit
wkhtmltopdf
Development Tools
Git
GitHub
VS Code
Postman
Swagger / OpenAPI
📁 Project Structure
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
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FilterBar.jsx
│   │   │   ├── JobCard.jsx
│   │   │   ├── MatchScore.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── SkillTags.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── JobDetails.jsx
│   │   │   └── Profile.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── resume-generator/
│   ├── prompts/
│   ├── templates/
│   │   └── resume_template.html
│   ├── app.py
│   ├── chains.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
⚙️ Getting Started
Prerequisites

Make sure the following are installed:

Python 3.10+
Node.js
npm
PostgreSQL
Git

You will also need a Google Gemini API key.

1. Clone the Repository
git clone https://github.com/DyutiSaini/AI-Job-Intelligence.git
cd AI-Job-Intelligence
🔧 Backend Setup

Navigate to the backend:

cd backend

Create and activate a virtual environment.

Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create:

backend/.env

Add your local configuration:

DATABASE_URL=your_postgresql_connection_string
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
GEMINI_API_KEY=your_gemini_api_key

Never commit .env files or API keys to GitHub.

PostgreSQL Setup

Create a PostgreSQL database:

CREATE DATABASE ai_job_intelligence;

Update the DATABASE_URL in your .env file according to your local PostgreSQL configuration.

Run the Backend

From the backend directory:

python -m uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
🎨 Frontend Setup

Open another terminal and navigate to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will typically be available at:

http://localhost:5173
📄 Resume Generator Setup

Navigate to:

cd resume-generator

Create a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create:

resume-generator/.env

Add:

GEMINI_API_KEY=your_gemini_api_key

Run the Streamlit application:

streamlit run app.py

The Resume Generator will open in the browser.

🔌 API Overview

The backend exposes REST APIs for the major platform functionality.

Method	Endpoint	Purpose
GET	/	API root
GET	/health	Health check
POST	/jobs	Create a job
GET	/jobs	Retrieve jobs
GET	/jobs/matches	Get personalized job recommendations
GET	/jobs/{job_id}	Get job details
POST	/jobs/ingest	Ingest jobs
POST	/profile	Create candidate profile
GET	/profile/{profile_id}	Retrieve candidate profile
PUT	/profile/{profile_id}	Update candidate profile
POST	/resume/tailor	Generate tailored resume content

Interactive API documentation is available through FastAPI Swagger at:

http://127.0.0.1:8000/docs
🔐 Security

The project follows basic security practices for local development:

API keys are stored in .env files.
.env files are excluded from Git.
Virtual environments are excluded from Git.
Generated and cache files are excluded from Git.
Sensitive credentials are not stored in source code.

Before production deployment, additional security measures such as authentication, authorization, secret management, rate limiting, and production-grade configuration should be implemented.

📊 Evaluation

The project includes an evaluation framework for recommendation ranking.

Implemented metrics:

Precision@K
Recall@K
NDCG@K

The evaluation module is located at:

backend/app/evaluation/

The evaluation dataset contains manually assigned relevance labels for the available job examples.

Because the current evaluation dataset is relatively small, the metrics should be treated as an initial benchmark rather than a production-level evaluation.

💡 Design Principles
Deterministic Scoring

The final recommendation score is calculated programmatically rather than allowing an LLM to directly decide the ranking.

Explainability

Recommendations expose the underlying matching signals and skill gaps.

Structured AI Output

Gemini is used to transform unstructured job descriptions into structured information that can be processed by the backend.

No Qualification Fabrication

Resume tailoring is designed to improve wording and relevance without inventing skills, experience, or qualifications.

Modular Architecture

Job ingestion, normalization, parsing, matching, storage, evaluation, and resume tailoring are separated into dedicated backend services.

📌 Current Status

The following functionality is currently implemented:

 Candidate profile management
 Job ingestion
 Job normalization
 AI-powered job parsing
 PostgreSQL job storage
 Hybrid job matching
 Gemini-based semantic similarity
 Skill compatibility scoring
 Experience compatibility
 Location compatibility
 Explainable match scores
 Matched-skill identification
 Skill-gap detection
 AI resume tailoring
 Standalone AI Resume Generator
 PDF resume generation
 Recommendation evaluation framework
 React dashboard
 Job details page
 Candidate profile page
 FastAPI Swagger documentation
🔮 Future Improvements

Potential future enhancements include:

Embedding caching to reduce repeated API calls
Additional job data sources
Automated job alerts
Email notifications
Saved jobs and application tracking
User authentication and authorization
Recommendation feedback loops
Larger labeled evaluation datasets
Production deployment
More advanced personalization
Background job processing
Production-grade monitoring and logging
🎯 Why This Project?

AI Job Intelligence was designed as an end-to-end demonstration of how AI, information retrieval, recommendation systems, backend engineering, databases, and modern frontend development can be combined into a practical application.

Rather than relying only on keyword matching or an LLM-generated recommendation, the platform combines:

Structured Job Analysis
        +
Skill Matching
        +
Semantic Similarity
        +
Experience Matching
        +
Location Matching
        +
Explainability
        +
AI Resume Tailoring

This creates a more transparent workflow for understanding why a particular job is relevant to a candidate.

👩‍💻 Author

Dyuti Saini

B.Tech — Computer Science Engineering (Artificial Intelligence)
Indira Gandhi Delhi Technical University for Women (IGDTUW)

GitHub:
https://github.com/DyutiSaini
