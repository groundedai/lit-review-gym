import db


def test_get_citations():
    paper_id = "01bd7816303809e8a5e58f2e39277f410f4202bd"
    citations = db.get_citations(paper_id)
    print(citations)