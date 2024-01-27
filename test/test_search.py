import search
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_keyword_search():
    query = "jasplakinolide treatments altered the corral permeability"
    found = search.keyword_search(query)
    print(found[0])
    print(len(found))

