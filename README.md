# LitReviewGym

Contains code and data for LitReviewGym. The goal is to provide an environment to train autonomous agents to perform literature reviews.

## Dataset Creation

The code is documented in `make_dataset.ipynb`.

Broadly, the steps are:
- Query Semantic Scholar to get open access reviews
- Get citation IDs for each paper from Semantic Scholar
- Get full texts and decompose into headings and paragraphs

## Data model

- Documents
	- id
	- title
- DocHeadings
	- doc_id
	- doc_title
	- heading
	- position
- DocParagraphs
	- doc_id
	- doc_title
	- heading_id
	- content
- Citations
    - id
	- doc_id
	- doc_title
	- cited_doc_id
	- cited_doc_title
	- heading_id
	- content_id
	- context

## Running

### Tests

From the root directory, run

`export PYTHONPATH=. && pytest -s`