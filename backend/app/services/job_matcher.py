# import math

# from google import genai
# from google.genai import types

# from app.config import settings


# # ---------------------------------------------------------
# # Gemini Embedding Client
# # ---------------------------------------------------------

# embedding_client = genai.Client(
#     api_key=settings.GEMINI_API_KEY
# )

# EMBEDDING_MODEL = "gemini-embedding-001"


# # ---------------------------------------------------------
# # Skill Matching
# # ---------------------------------------------------------

# def normalize_skill(skill: str) -> str:
#     return skill.strip().lower()


# def calculate_skill_match(candidate_skills, required_skills) -> dict:
#     candidate = {
#         normalize_skill(skill)
#         for skill in candidate_skills
#         if skill and skill.strip()
#     }

#     required = {
#         normalize_skill(skill)
#         for skill in required_skills
#         if skill and skill.strip()
#     }

#     if not required:
#         return {
#             "score": 0.0,
#             "matched_skills": [],
#             "missing_skills": [],
#         }

#     matched = candidate.intersection(required)
#     missing = required - candidate

#     score = (len(matched) / len(required)) * 100

#     return {
#         "score": round(score, 2),
#         "matched_skills": sorted(matched),
#         "missing_skills": sorted(missing),
#     }


# # ---------------------------------------------------------
# # Location Matching
# # ---------------------------------------------------------

# def calculate_location_match(candidate_locations, job_locations) -> float:
#     candidate = {
#         location.strip().lower()
#         for location in candidate_locations
#         if location and location.strip()
#     }

#     job = {
#         location.strip().lower()
#         for location in job_locations
#         if location and location.strip()
#     }

#     if not candidate or not job:
#         return 0.0

#     if candidate.intersection(job):
#         return 100.0

#     if "remote" in candidate and "remote" in job:
#         return 100.0

#     return 0.0


# # ---------------------------------------------------------
# # Experience Matching
# # ---------------------------------------------------------

# def calculate_experience_match(
#     candidate_experience,
#     job_experience
# ) -> float:

#     if not job_experience:
#         return 100.0

#     if not candidate_experience:
#         return 50.0

#     candidate = candidate_experience.lower().strip()
#     job = job_experience.lower().strip()

#     if candidate == job:
#         return 100.0

#     if candidate in job or job in candidate:
#         return 100.0

#     return 50.0


# # ---------------------------------------------------------
# # Pure Python Cosine Similarity
# # ---------------------------------------------------------

# def cosine_similarity(vector_a, vector_b) -> float:

#     if not vector_a or not vector_b:
#         return 0.0

#     if len(vector_a) != len(vector_b):
#         return 0.0

#     dot_product = sum(
#         a * b for a, b in zip(vector_a, vector_b)
#     )

#     norm_a = math.sqrt(
#         sum(a * a for a in vector_a)
#     )

#     norm_b = math.sqrt(
#         sum(b * b for b in vector_b)
#     )

#     if norm_a == 0 or norm_b == 0:
#         return 0.0

#     return dot_product / (norm_a * norm_b)


# # ---------------------------------------------------------
# # Gemini Semantic Similarity
# # ---------------------------------------------------------

# def calculate_semantic_similarity(
#     candidate_text: str,
#     job_text: str
# ) -> float:

#     if not candidate_text.strip() or not job_text.strip():
#         return 0.0

#     result = embedding_client.models.embed_content(
#         model=EMBEDDING_MODEL,
#         contents=[
#             candidate_text,
#             job_text,
#         ],
#         config=types.EmbedContentConfig(
#             task_type="SEMANTIC_SIMILARITY"
#         ),
#     )

#     embeddings = result.embeddings

#     if not embeddings or len(embeddings) < 2:
#         return 0.0

#     similarity = cosine_similarity(
#         embeddings[0].values,
#         embeddings[1].values
#     )

#     # Gemini cosine similarity is in approximately [-1, 1].
#     # Convert to a 0-100 score.
#     score = ((similarity + 1) / 2) * 100

#     return round(
#         max(0.0, min(100.0, score)),
#         2
#     )


# # ---------------------------------------------------------
# # Hybrid Match Score
# # ---------------------------------------------------------

# def calculate_hybrid_match_score(
#     skill_score,
#     semantic_score,
#     experience_score,
#     location_score,
#     other_score=100.0
# ) -> float:

#     final_score = (
#         skill_score * 0.35
#         + semantic_score * 0.30
#         + experience_score * 0.20
#         + location_score * 0.10
#         + other_score * 0.05
#     )

#     return round(final_score, 2)


# # ---------------------------------------------------------
# # Match Explanation
# # ---------------------------------------------------------

# def generate_match_explanation(
#     skill_result,
#     semantic_score,
#     experience_score,
#     location_score,
#     company_score
# ) -> dict:

#     reasons = []
#     gaps = []

#     if skill_result["matched_skills"]:
#         reasons.append(
#             "Matched skills: "
#             + ", ".join(skill_result["matched_skills"])
#         )

#     if semantic_score >= 70:
#         reasons.append(
#             "Strong semantic similarity with the job description."
#         )

#     elif semantic_score >= 50:
#         reasons.append(
#             "Moderate semantic similarity with the job description."
#         )

#     if location_score == 100:
#         reasons.append(
#             "Location preference matches the job."
#         )

#     if experience_score == 100:
#         reasons.append(
#             "Experience requirements are compatible."
#         )

#     if company_score == 100:
#         reasons.append(
#             "Company matches the preferred company list."
#         )

#     if skill_result["missing_skills"]:
#         gaps.extend(
#             skill_result["missing_skills"]
#         )

#     if experience_score < 100:
#         gaps.append(
#             "Experience requirement may need review."
#         )

#     if location_score == 0:
#         gaps.append(
#             "Job location does not match preferences."
#         )

#     return {
#         "why_it_matches": reasons,
#         "potential_gaps": gaps,
#     }


# # ---------------------------------------------------------
# # Main Job Matching Function
# # ---------------------------------------------------------

# def match_job_to_profile(profile, job) -> dict:

#     skill_result = calculate_skill_match(
#         candidate_skills=profile.skills,
#         required_skills=job.required_skills,
#     )

#     candidate_text = " ".join(
#         [
#             *profile.roles,
#             *profile.skills,
#             *profile.locations,
#             *profile.work_type,
#             *profile.companies,
#         ]
#     )

#     job_text = " ".join(
#         [
#             job.title,
#             job.company,
#             job.description,
#             *job.required_skills,
#             *job.preferred_skills,
#             *job.locations,
#         ]
#     )

#     semantic_score = calculate_semantic_similarity(
#         candidate_text=candidate_text,
#         job_text=job_text,
#     )

#     experience_score = calculate_experience_match(
#         candidate_experience=None,
#         job_experience=job.experience,
#     )

#     location_score = calculate_location_match(
#         candidate_locations=profile.locations,
#         job_locations=job.locations,
#     )

#     candidate_companies = {
#         company.strip().lower()
#         for company in profile.companies
#         if company and company.strip()
#     }

#     job_company = job.company.strip().lower()

#     if not candidate_companies:
#         company_score = 100.0

#     elif job_company in candidate_companies:
#         company_score = 100.0

#     else:
#         company_score = 0.0

#     final_score = calculate_hybrid_match_score(
#         skill_score=skill_result["score"],
#         semantic_score=semantic_score,
#         experience_score=experience_score,
#         location_score=location_score,
#         other_score=company_score,
#     )

#     explanation = generate_match_explanation(
#         skill_result=skill_result,
#         semantic_score=semantic_score,
#         experience_score=experience_score,
#         location_score=location_score,
#         company_score=company_score,
#     )

#     return {
#         "job_id": job.id,
#         "title": job.title,
#         "company": job.company,
#         "match_score": final_score,
#         "skill_score": skill_result["score"],
#         "semantic_score": semantic_score,
#         "experience_score": experience_score,
#         "location_score": location_score,
#         "company_score": company_score,
#         "matched_skills": skill_result["matched_skills"],
#         "missing_skills": skill_result["missing_skills"],
#         "why_it_matches": explanation["why_it_matches"],
#         "potential_gaps": explanation["potential_gaps"],
#     }


import math
import re
from collections import Counter


def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


def calculate_skill_match(candidate_skills, required_skills) -> dict:
    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
        if skill and skill.strip()
    }

    required = {
        normalize_skill(skill)
        for skill in required_skills
        if skill and skill.strip()
    }

    if not required:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = candidate.intersection(required)
    missing = required - candidate

    score = (len(matched) / len(required)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
    }


def calculate_location_match(candidate_locations, job_locations) -> float:
    candidate = {
        location.strip().lower()
        for location in candidate_locations
        if location and location.strip()
    }

    job = {
        location.strip().lower()
        for location in job_locations
        if location and location.strip()
    }

    if not candidate or not job:
        return 0.0

    if candidate.intersection(job):
        return 100.0

    if "remote" in candidate and "remote" in job:
        return 100.0

    return 0.0


def calculate_experience_match(candidate_experience, job_experience) -> float:
    if not job_experience:
        return 100.0

    if not candidate_experience:
        return 50.0

    candidate = candidate_experience.lower().strip()
    job = job_experience.lower().strip()

    if candidate == job:
        return 100.0

    if candidate in job or job in candidate:
        return 100.0

    return 50.0


def tokenize(text: str):
    if not text:
        return []

    return re.findall(r"[a-zA-Z0-9+#.]+", text.lower())


def calculate_text_similarity(text_a: str, text_b: str) -> float:
    """
    Lightweight local TF-IDF-style cosine similarity.

    This avoids external native ML libraries such as
    torch/scikit-learn, so it works with Smart App Control ON.
    """

    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)

    if not tokens_a or not tokens_b:
        return 0.0

    counter_a = Counter(tokens_a)
    counter_b = Counter(tokens_b)

    vocabulary = set(counter_a) | set(counter_b)

    total_a = len(tokens_a)
    total_b = len(tokens_b)

    vector_a = {}
    vector_b = {}

    for term in vocabulary:
        tf_a = counter_a.get(term, 0) / total_a
        tf_b = counter_b.get(term, 0) / total_b

        document_frequency = 0

        if term in counter_a:
            document_frequency += 1

        if term in counter_b:
            document_frequency += 1

        idf = math.log((2 + 1) / (document_frequency + 1)) + 1

        vector_a[term] = tf_a * idf
        vector_b[term] = tf_b * idf

    dot_product = sum(
        vector_a[term] * vector_b[term]
        for term in vocabulary
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a.values())
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    similarity = dot_product / (magnitude_a * magnitude_b)

    return round(
        max(0.0, min(100.0, similarity * 100)),
        2,
    )


def calculate_semantic_similarity(candidate_text, job_text) -> float:
    """
    Local semantic-style text similarity.

    No external API call is made during dashboard refresh.
    """

    return calculate_text_similarity(
        candidate_text,
        job_text,
    )


def calculate_hybrid_match_score(
    skill_score,
    semantic_score,
    experience_score,
    location_score,
    other_score=100.0,
) -> float:

    final_score = (
        skill_score * 0.35
        + semantic_score * 0.30
        + experience_score * 0.20
        + location_score * 0.10
        + other_score * 0.05
    )

    return round(final_score, 2)


def generate_match_explanation(
    skill_result,
    semantic_score,
    experience_score,
    location_score,
    company_score,
):
    reasons = []
    gaps = []

    if skill_result["matched_skills"]:
        reasons.append(
            f"Matched skills: "
            f"{', '.join(skill_result['matched_skills'])}"
        )

    if semantic_score >= 70:
        reasons.append(
            "Strong similarity with the job description."
        )
    elif semantic_score >= 50:
        reasons.append(
            "Moderate similarity with the job description."
        )

    if location_score == 100:
        reasons.append(
            "Location preference matches the job."
        )

    if experience_score == 100:
        reasons.append(
            "Experience requirements are compatible."
        )

    if company_score == 100:
        reasons.append(
            "Company matches the preferred company list."
        )

    if skill_result["missing_skills"]:
        gaps.extend(skill_result["missing_skills"])

    if experience_score < 100:
        gaps.append(
            "Experience requirement may need review."
        )

    if location_score == 0:
        gaps.append(
            "Job location does not match preferences."
        )

    return {
        "why_it_matches": reasons,
        "potential_gaps": gaps,
    }


def match_job_to_profile(profile, job):

    skill_result = calculate_skill_match(
        candidate_skills=profile.skills,
        required_skills=job.required_skills,
    )

    candidate_text = " ".join(
        [
            *profile.roles,
            *profile.skills,
            *profile.locations,
            *profile.work_type,
            *profile.companies,
            profile.education or "",
            profile.experience or "",
        ]
    )

    job_text = " ".join(
        [
            job.title,
            job.company,
            job.description,
            *job.required_skills,
            *job.preferred_skills,
            *job.locations,
            job.experience or "",
            job.education or "",
        ]
    )

    semantic_score = calculate_semantic_similarity(
        candidate_text=candidate_text,
        job_text=job_text,
    )

    # Profile currently stores general candidate experience,
    # while jobs store requirement text.
    experience_score = calculate_experience_match(
        candidate_experience=profile.experience,
        job_experience=job.experience,
    )

    location_score = calculate_location_match(
        candidate_locations=profile.locations,
        job_locations=job.locations,
    )

    candidate_companies = {
        company.strip().lower()
        for company in profile.companies
        if company and company.strip()
    }

    job_company = job.company.strip().lower()

    if not candidate_companies:
        company_score = 100.0
    elif job_company in candidate_companies:
        company_score = 100.0
    else:
        company_score = 0.0

    final_score = calculate_hybrid_match_score(
        skill_score=skill_result["score"],
        semantic_score=semantic_score,
        experience_score=experience_score,
        location_score=location_score,
        other_score=company_score,
    )

    explanation = generate_match_explanation(
        skill_result=skill_result,
        semantic_score=semantic_score,
        experience_score=experience_score,
        location_score=location_score,
        company_score=company_score,
    )

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "match_score": final_score,
        "skill_score": skill_result["score"],
        "semantic_score": semantic_score,
        "experience_score": experience_score,
        "location_score": location_score,
        "company_score": company_score,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "why_it_matches": explanation["why_it_matches"],
        "potential_gaps": explanation["potential_gaps"],
    }