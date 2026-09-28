from sklearn.metrics import ndcg_score


def precision_at_k(
    relevance_labels: list[int],
    k: int,
    relevant_threshold: int = 1,
) -> float:
    """
    Calculate Precision@K.

    A job is considered relevant if its relevance label
    is greater than or equal to relevant_threshold.
    """

    if k <= 0:
        return 0.0

    top_k = relevance_labels[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(
        1
        for label in top_k
        if label >= relevant_threshold
    )

    return round(relevant_count / len(top_k), 4)


def recall_at_k(
    relevance_labels: list[int],
    k: int,
    relevant_threshold: int = 1,
) -> float:
    """
    Calculate Recall@K.
    """

    if k <= 0:
        return 0.0

    total_relevant = sum(
        1
        for label in relevance_labels
        if label >= relevant_threshold
    )

    if total_relevant == 0:
        return 0.0

    top_k = relevance_labels[:k]

    relevant_in_top_k = sum(
        1
        for label in top_k
        if label >= relevant_threshold
    )

    return round(
        relevant_in_top_k / total_relevant,
        4,
    )


def ndcg_at_k(
    relevance_labels: list[int],
    predicted_scores: list[float],
    k: int,
) -> float:
    """
    Calculate NDCG@K using graded relevance labels.

    Relevance:
    0 = Not relevant
    1 = Relevant
    2 = Highly relevant
    """

    if k <= 0:
        return 0.0

    if not relevance_labels or not predicted_scores:
        return 0.0

    if len(relevance_labels) != len(predicted_scores):
        raise ValueError(
            "relevance_labels and predicted_scores "
            "must have the same length."
        )

    true_relevance = [relevance_labels]

    predicted_scores_array = [predicted_scores]

    score = ndcg_score(
        true_relevance,
        predicted_scores_array,
        k=k,
    )

    return round(float(score), 4)


def evaluate_ranking(
    relevance_labels: list[int],
    predicted_scores: list[float],
    k: int = 5,
) -> dict:
    """
    Evaluate a job ranking using Precision@K,
    Recall@K and NDCG@K.
    """

    if len(relevance_labels) != len(predicted_scores):
        raise ValueError(
            "relevance_labels and predicted_scores "
            "must have the same length."
        )

    return {
        "k": k,
        "precision_at_k": precision_at_k(
            relevance_labels,
            k,
        ),
        "recall_at_k": recall_at_k(
            relevance_labels,
            k,
        ),
        "ndcg_at_k": ndcg_at_k(
            relevance_labels,
            predicted_scores,
            k,
        ),
    }