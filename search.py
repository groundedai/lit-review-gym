import db
import logging

logging.basicConfig(level=logging.INFO)


def keyword_search(query: str, limit: int = 100):
    """
    Search the index for the query
    """
    found = db.document_fts(query)
    found = found[0:limit]
    logging.info(f"keword_search: found {len(found)} results")
    return found


def multi_keyword_search(queries: list[str], limit: int = None, **kwargs):
    """
    Search the index for the query
    """
    found = []
    for query in queries:
        found += keyword_search(query, **kwargs)
    if limit:
        found = found[0:limit]
    logging.info(f"multi_keyword_search: found {len(found)} results")
    return found