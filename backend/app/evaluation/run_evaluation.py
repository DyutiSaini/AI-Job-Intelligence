from app.database import SessionLocal
from app.models import Job, UserProfile
from app.services.job_matcher import (
    calculate_semantic_similarity,
    calculate_skill_match,
    match_job_to_profile,
)
from app.evaluation.evaluator import evaluate_ranking
from app.evaluation.evaluation_dataset import RELEVANCE_LABELS


def build_candidate_text(profile):
    return " ".join(
        [
            *profile.roles,
            *profile.skills,
            *profile.locations,
            *profile.work_type,
            *profile.companies,
        ]
    )


def build_job_text(job):
    return " ".join(
        [
            job.title,
            job.company,
            job.description,
            *job.required_skills,
            *job.preferred_skills,
            *job.locations,
        ]
    )


def evaluate_method(
    jobs,
    scores,
    method_name,
    k=5,
):
    ranked_jobs = sorted(
        zip(jobs, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    ranked_labels = [
        RELEVANCE_LABELS[job.id]
        for job, score in ranked_jobs
    ]

    ranked_scores = [
        score
        for job, score in ranked_jobs
    ]

    metrics = evaluate_ranking(
        relevance_labels=ranked_labels,
        predicted_scores=ranked_scores,
        k=k,
    )

    return {
        "method": method_name,
        **metrics,
    }


def main():
    db = SessionLocal()

    try:
        profile = db.get(UserProfile, 2)

        if profile is None:
            raise ValueError(
                "Profile with ID 2 was not found."
            )

        jobs = (
            db.query(Job)
            .order_by(Job.id)
            .all()
        )

        if not jobs:
            raise ValueError(
                "No jobs found in the database."
            )

        candidate_text = build_candidate_text(profile)

        skill_scores = []
        semantic_scores = []
        hybrid_scores = []

        for job in jobs:

            # -----------------------------
            # 1. Skill-based score
            # -----------------------------
            skill_result = calculate_skill_match(
                candidate_skills=profile.skills,
                required_skills=job.required_skills,
            )

            skill_scores.append(
                skill_result["score"]
            )

            # -----------------------------
            # 2. Semantic score
            # -----------------------------
            job_text = build_job_text(job)

            semantic_score = calculate_semantic_similarity(
                candidate_text=candidate_text,
                job_text=job_text,
            )

            semantic_scores.append(
                semantic_score
            )

            # -----------------------------
            # 3. Hybrid score
            # -----------------------------
            hybrid_result = match_job_to_profile(
                profile=profile,
                job=job,
            )

            hybrid_scores.append(
                hybrid_result["match_score"]
            )

        results = [
            evaluate_method(
                jobs,
                skill_scores,
                "Skill-Based",
            ),
            evaluate_method(
                jobs,
                semantic_scores,
                "Semantic",
            ),
            evaluate_method(
                jobs,
                hybrid_scores,
                "Hybrid",
            ),
        ]

        print("\n" + "=" * 60)
        print("AI JOB INTELLIGENCE - RECOMMENDATION EVALUATION")
        print("=" * 60)

        print(f"\nProfile ID: {profile.id}")
        print(f"Jobs evaluated: {len(jobs)}")
        print("Evaluation metric: K = 5")

        print("\n" + "-" * 60)
        print(
            f"{'Method':<18}"
            f"{'Precision@5':<15}"
            f"{'Recall@5':<15}"
            f"{'NDCG@5':<15}"
        )
        print("-" * 60)

        for result in results:
            print(
                f"{result['method']:<18}"
                f"{result['precision_at_k']:<15}"
                f"{result['recall_at_k']:<15}"
                f"{result['ndcg_at_k']:<15}"
            )

        print("-" * 60)

        print("\nEvaluation completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
    