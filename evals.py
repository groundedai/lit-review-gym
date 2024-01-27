import logging
import db
import search

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def eval_queries(paper_id: str, queries: list[str]):
    """
    Evaluate accuracy of a query list in fetching the relevant citations from the mock search engine
    """
    found = search.multi_keyword_search(queries)
    found_ids = [doc["doc_id"] for doc in found]
    target_ids = db.get_citations(paper_id)
    logger.info(f"Found {len(found)} citations")
    logger.info(f"True positives: {len(target_ids)}")
    results = {}
    results["n_found"] = len(found)
    results["n_true_positives"] = len(target_ids)
    hits = len(set(found_ids).intersection(set(target_ids)))
    results["hits"] = hits
    recall = hits / len(target_ids)
    results["recall"] = recall
    precision = hits / len(found_ids)
    results["precision"] = precision
    return results
