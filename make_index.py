# Make sqlite FTS index for the citation database

import os
import json
import logging
import sqlite3
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

paper_details_path = os.path.join(os.path.dirname(__file__), "data/paper_details.json")
with open(paper_details_path, "r") as f:
    paper_details = json.load(f)

all_citations = []
for paper_id, details in paper_details.items():
    all_citations += details["citations"]


logger.info(f"Loaded {len(all_citations)} citations from {len(paper_details)} papers")

db_path = os.path.join(os.path.dirname(__file__), "data/citations.db")

conn = sqlite3.connect(db_path)

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS citations")

c.execute(
    """CREATE VIRTUAL TABLE citations USING fts5(
    paperId,
    title,
    abstract
)"""
)
logger.info("Created FTS index")

logger.info("Populating FTS index")
for citation in tqdm(all_citations):
    c.execute(
        """INSERT INTO citations VALUES (
        :paperId,
        :title,
        :abstract
    )""",
        citation,
    )

conn.commit()
conn.close()

logger.info("Done")
