# Make sqlite FTS index for the citation database

import os
import json
import jsonlines
import logging
import sqlite3
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(message)s")

papers_path = os.path.join(os.path.dirname(__file__), "data/papers.json")
with open(papers_path, "r") as f:
    papers = json.load(f)

db_path = os.path.join(os.path.dirname(__file__), "data/citations.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS documents")
logging.info("Populating FTS documents index")
c.execute(
    """CREATE VIRTUAL TABLE documents USING fts5(
    doc_id UNINDEXED,
    title,
    abstract
)"""
)

for paper in tqdm(papers):
    c.execute(
        """INSERT INTO documents VALUES (
        :paperId,
        :title,
        :abstract
    )""",
        {"paperId": paper["paperId"], "title": paper["title"], "abstract": None}
    )
conn.commit()

paper_details_path = os.path.join(os.path.dirname(__file__), "data/paper_details.jsonl")
with jsonlines.open(paper_details_path) as f:
    for line in tqdm(f):
        if not "paperId" in line:
            continue
        paper_id = line["paperId"]
        citations = line["citations"]
        for citation in citations:
            citation["doc_id"] = paper_id
            c.execute(
                """INSERT INTO documents VALUES (
                :paperId,
                :title,
                :abstract
            )""",
                citation,
            )
conn.commit()


logging.info("Populating citations table")
c.execute("DROP TABLE IF EXISTS citations")
c.execute(
    """CREATE TABLE citations (
    doc_id TEXT,
    cited_doc_id TEXT,
    FOREIGN KEY(doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY(cited_doc_id) REFERENCES documents(doc_id)
)"""
)
with jsonlines.open(paper_details_path) as f:
    for line in tqdm(f):
        if not "paperId" in line:
            continue
        paper_id = line["paperId"]
        citations = line["citations"]
        for citation in citations:
            cited_doc_id = citation["paperId"]
            c.execute(
                """INSERT INTO citations VALUES (
                :doc_id,
                :cited_doc_id
            )""",
                {"doc_id": paper_id, "cited_doc_id": cited_doc_id},
            )

conn.commit()

c.execute("SELECT COUNT(*) FROM documents")
logging.info(f"Number of documents: {c.fetchone()[0]}")
c.execute("SELECT COUNT(*) FROM citations")
logging.info(f"Number of citations: {c.fetchone()[0]}")
c.execute("SELECT COUNT(DISTINCT doc_id) FROM citations")
logging.info(f"Number of documents with citations: {c.fetchone()[0]}")

conn.close()