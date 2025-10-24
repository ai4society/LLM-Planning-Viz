# Adding Abstracts

This folder contains scripts and data for adding abstracts to research papers in a given dataset.

The script `get_abstracts.py` is used to get the abstracts of the papers in the [dataset](https://github.com/ai4society/LLM-Planning-Viz/blob/main/papers-data.js) used for ICAPS 2024 paper, "On the Prospects of Incorporating Large Language Models (LLMs) in Automated Planning and Scheduling (APS)".

The script uses the `arxiv` API to get the abstracts and adds them to each paper in the dataset. Since many papers are not on arXiv, some manual work was required to get the abstracts for those papers.

The `paper_data.json` is the original dataset (converted to `json` format) and `updated_papers_data.json` is the dataset with abstracts added.
