import evals

def test_evals():
    paper_id = "01bd7816303809e8a5e58f2e39277f410f4202bd"
    queries = ["signaling", "disease", "FKBP52"]
    results = evals.eval_queries(paper_id, queries)
    print(results)
