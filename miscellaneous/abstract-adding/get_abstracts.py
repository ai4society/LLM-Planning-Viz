import json
import xml.etree.ElementTree as ET

import requests


def get_abstract(arxiv_id):
    base_url = "http://export.arxiv.org/api/query?id_list="
    url = base_url + arxiv_id
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        # The default namespace is defined in the 'feed' tag
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        summary = root.find(".//atom:entry/atom:summary", namespace)
        if summary is not None:
            return summary.text.strip()  # type: ignore
    else:
        print(f"Abstract not found for {arxiv_id}")
        return "Abstract not found"


# Load the existing data
with open("papers_data.json", "r") as f:
    papers_data = json.load(f)

# Update each paper with its abstract
for paper in papers_data:
    arxiv_id = paper["link"].split("/")[-1]
    print(f"Getting abstract for {paper['title']} with arXiv ID {arxiv_id}")
    abstract = get_abstract(arxiv_id)
    paper["abstract"] = abstract


# Save the updated data
with open("updated_papers_data.json", "w") as f:
    json.dump(papers_data, f, indent=4)

print("Papers data updated with abstracts.")
