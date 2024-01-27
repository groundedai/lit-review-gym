import search
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def test_sqlite_search():
    query = "jasplakinolide treatments altered the corral permeability"
    db_path = os.path.join(os.path.dirname(__file__), "../data/citations.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM citations WHERE citations MATCH ?", (query,))
    found = c.fetchall()
    print(found[0:10])
    print(len(found))
    conn.close()


def test_keyword_search():
    query = "jasplakinolide treatments altered the corral permeability"
    found = search.keyword_search(query)
    print(found[0])
    print(len(found))

