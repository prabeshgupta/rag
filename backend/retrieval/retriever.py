from retrieval import hybrid_search


def retrieve(query, limit=5):
    return hybrid_search(query, limit)