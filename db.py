import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), "data/citations.db")


def document_fts(query: str):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM documents WHERE documents MATCH ?", (query,))
        found = c.fetchall()
        found = [dict(row) for row in found]
    return found


def get_citations(paper_id: str):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT cited_doc_id FROM citations WHERE doc_id = ?", (paper_id,))
        citations = c.fetchall()
        citations = [citation[0] for citation in citations]
    return citations
