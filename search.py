import os
import json
import logging
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db_path = os.path.join(os.path.dirname(__file__), "data/citations.db")


def _sqlite_search(query: str):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM citations WHERE citations MATCH ?", (query,))
        found = c.fetchall()
    return found


def keyword_search(query: str, limit: int = 100):
    """
    Search the index for the query
    """
    found = _sqlite_search(query)
    found = found[0:limit]
    logger.info(f"Found {len(found)} citations")
    return found
