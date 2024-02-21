import logging
from . import db
from . import search
from . import util

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_true_pos(hit_ids: list[str], target_ids: list[str]):
    return list(set(hit_ids).intersection(set(target_ids)))


def get_false_pos(hit_ids: list[str], target_ids: list[str]):
    return list(set(hit_ids).difference(set(target_ids)))


def calc_recall(true_pos: list[str], target_ids: list[str]):
    return len(true_pos) / (len(target_ids) + 1e-8)


def calc_precision(true_pos: list[str], hit_ids: list[str]):
    return len(true_pos) / (len(hit_ids) + 1e-8)


def calc_f1(precision: float, recall: float):
    return 2 * precision * recall / (precision + recall + 1e-8)

from functools import lru_cache

# @lru_cache(maxsize=2000)
def eval_query(paper_id: str, query: str, target_ids: list[str] = None):
    """
    Evaluate accuracy of a query in fetching the relevant citations from the mock search engine
    """
    hits = search.keyword_search(query)
    hit_ids = [doc["doc_id"] for doc in hits]
    target_ids = target_ids or db.get_citations(paper_id)
    true_pos = get_true_pos(hit_ids, target_ids)
    false_pos = get_false_pos(hit_ids, target_ids)
    recall = calc_recall(true_pos, target_ids)
    precision = calc_precision(true_pos, hit_ids)
    f1 = calc_f1(precision, recall)
    results = {
        "query": query,
        "hit_ids": hit_ids,
        "target_ids": target_ids,
        "true_pos": true_pos,
        "false_pos": false_pos,
        "n_returned": len(hits),
        "n_targets": len(target_ids),
        "n_true_pos": len(true_pos),
        "n_false_pos": len(false_pos),
        "recall": recall,
        "precision": precision,
        "f1": f1,
    }
    return results


def eval_queries(paper_id: str, queries: list[str]):
    """
    Evaluate query list
    """
    if len(queries) == 0:
        return {}
    query_results = []
    target_ids = db.get_citations(paper_id)
    for query in queries:
        r = eval_query(paper_id, query, target_ids=target_ids)
        query_results.append(r)
    all_hit_ids = [r["hit_ids"] for r in query_results]
    all_true_pos = [r["true_pos"] for r in query_results]
    all_false_pos = [r["false_pos"] for r in query_results]
    hit_ids = list(set(util.flatten(all_hit_ids)))
    true_pos = list(set(util.flatten(all_true_pos)))
    false_pos = list(set(util.flatten(all_false_pos)))
    recall = calc_recall(true_pos, target_ids)
    precision = calc_precision(true_pos, hit_ids)
    f1 = calc_f1(precision, recall)
    # Remove redundant fields
    for r in query_results:
        del r["target_ids"]
        del r["n_targets"]
    results = {
        "queries": query_results,
        "hit_ids": hit_ids,
        "target_ids": target_ids,
        "true_pos": true_pos,
        "false_pos": false_pos,
        "n_returned": len(hit_ids),
        "n_targets": len(target_ids),
        "n_true_pos": len(true_pos),
        "n_false_pos": len(false_pos),
        "recall": recall,
        "precision": precision,
        "f1": f1,
    }
    return results
