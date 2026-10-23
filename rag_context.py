from learning_engine import (
    retrieve_confirmed_cases,
    retrieve_false_positives,
    filter_results_by_similarity
)


SIMILARITY_THRESHOLD = 0.8


def build_query(alert):

    return f"""
Title:
{alert.get('title', '')}

IP:
{alert.get('ip', '')}

User:
{alert.get('user', '')}

Analysis:
{alert.get('analysis', '')}

Raw:
{alert.get('raw', {})}
"""


def title_matches(
    current_title,
    stored_document
):

    current_title = current_title.lower()

    title_keywords = [
        word
        for word in current_title.split()
        if len(word) > 3
    ]

    document_lower = stored_document.lower()

    matches = sum(
        1
        for word in title_keywords
        if word in document_lower
    )

    return matches >= 1


def get_rag_context(alert):

    query = build_query(alert)

    confirmed_results = retrieve_confirmed_cases(
        query,
        n_results=5
    )

    fp_results = retrieve_false_positives(
        query,
        n_results=5
    )

    confirmed_cases = filter_results_by_similarity(
        confirmed_results,
        max_distance=SIMILARITY_THRESHOLD
    )

    false_positive_cases = filter_results_by_similarity(
        fp_results,
        max_distance=SIMILARITY_THRESHOLD
    )

    title = alert.get(
        "title",
        ""
    )

    confirmed_cases = [
        doc
        for doc in confirmed_cases
        if title_matches(title, doc)
    ]

    false_positive_cases = [
        doc
        for doc in false_positive_cases
        if title_matches(title, doc)
    ]

    return {
        "confirmed": confirmed_cases[:3],
        "false_positive": false_positive_cases[:3]
    }