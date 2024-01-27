import os
import json
import logging
import search

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def eval_queries(paper_id: str, queries: list[str]):
    """
    Evaluate accuracy of a query list in fetching the relevant citations from the mock search engine
    """
    # Run mock searches
    found = []
    for query in queries:
        found += search.keyword_search(query)
    found_ids = [doc["paperId"] for doc in found]
    # Get true positives
    details = paper_details[paper_id]
    true_ids = [citation["paperId"] for citation in details["citations"]]
    # Calculate precision and recall
    logger.info(f"Found {len(found)} citations")
    logger.info(f"True positives: {len(true_ids)}")
    results = {}
    results["n_found"] = len(found)
    results["n_true_positives"] = len(true_ids)
    hits = len(set(found_ids).intersection(set(true_ids)))
    results["hits"] = hits
    recall = hits / len(true_ids)
    results["recall"] = recall
    precision = hits / len(found_ids)
    results["precision"] = precision
    return results