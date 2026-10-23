import chromadb
import uuid


# ==================================================
# CHROMADB
# ==================================================

client = chromadb.PersistentClient(
    path="knowledge_db"
)

collection = client.get_or_create_collection(
    name="soc_cases"
)


# ==================================================
# STORE KNOWLEDGE
# ==================================================

def save_case_knowledge(
        alert,
        analysis,
        verdict
):

    case_id = str(uuid.uuid4())

    document = f"""
Alert Title:
{alert.get('title', 'N/A')}

IP:
{alert.get('ip', 'N/A')}

User:
{alert.get('user', 'N/A')}

Investigation:
{analysis}

Verdict:
{verdict}
"""

    collection.add(
        ids=[case_id],
        documents=[document],
        metadatas=[
            {
                "verdict": verdict,
                "title": alert.get("title", ""),
                "ip": alert.get("ip", ""),
                "user": alert.get("user", "")
            }
        ]
    )

    return case_id


# ==================================================
# GENERIC RETRIEVAL
# ==================================================

def retrieve_similar_cases(
        query,
        n_results=5
):

    try:

        return collection.query(
            query_texts=[query],
            n_results=n_results
        )

    except:

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }


# ==================================================
# CONFIRMED ATTACKS
# ==================================================

def retrieve_confirmed_cases(
        query,
        n_results=5
):

    try:

        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={
                "verdict":
                "confirmed_attack"
            }
        )

    except:

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }


# ==================================================
# FALSE POSITIVES
# ==================================================

def retrieve_false_positives(
        query,
        n_results=5
):

    try:

        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={
                "verdict":
                "false_positive"
            }
        )

    except:

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }


# ==================================================
# RELEVANCE FILTER
# ==================================================

def filter_results_by_similarity(
        results,
        max_distance=1.0
):

    filtered = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    if not documents:
        return []

    for document, distance in zip(
        documents,
        distances
    ):

        if distance <= max_distance:

            filtered.append(
                document
            )

    return filtered


# ==================================================
# METADATA ACCESS
# ==================================================

def get_all_cases():

    try:

        return collection.get()

    except:

        return {}


# ==================================================
# DASHBOARD STATS
# ==================================================

def get_knowledge_stats():

    return {
        "cases":
        collection.count()
    }
