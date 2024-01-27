import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), "data/citations.db")


def safe_query(query: str):
    return query.replace("'", "''").replace('"', '""').replace("%", "%%")


def get_document(doc_id: str):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM documents WHERE doc_id = ?", (doc_id,))
        found = c.fetchone()
        found = dict(found)
    return found


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


def get_doc_ids_with_citations():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT doc_id FROM citations")
        citations = c.fetchall()
        citations = [citation[0] for citation in citations]
        citations = list(set(citations))
    return citations