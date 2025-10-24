import json

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load existing papers data
def load_existing_papers(file_path):
    """
    Load existing papers data from a JSON file
    :param file_path: Path to the JSON file. Should contain the abstract field.
    Sample value:
    {
        {
            "title": "Plansformer: Generating symbolic plans using transformers",
            "category": "plan-generation",
            "link": "https://arxiv.org/abs/2212.08681",
            "authors": "Pallagani, Vishal ...",
            "year": "2022",
            "abstract": "Large Language Models (LLMs) have been ..."
        },
    }
    :return: List of dictionaries containing paper data
    """
    print(f"Loading existing papers data at {file_path}")
    with open(file_path, "r") as f:
        papers_data = json.load(f)
    return papers_data


# Load new papers from CSV
def load_new_papers(file_path):
    """
    Load new papers from a CSV file
    :param file_path: Path to the CSV file.
    :return: DataFrame containing new papers data
    """
    print(f"Loading new papers from {file_path}")
    return pd.read_csv(file_path)


# Generate embeddings
def generate_embeddings(texts):
    """
    Generate embeddings for a list of texts
    :param texts: List of texts
    :return: Numpy array of embeddings
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts)


# Calculate similarity and assign categories
def categorize_papers(
    new_embeddings, existing_embeddings, existing_categories, threshold
):
    """
    Calculate cosine similarity between new and existing embeddings and assign categories to new papers.
    Note that multiple categories can be assigned to a paper.
    :param new_embeddings: Numpy array of embeddings for new papers
    :param existing_embeddings: Numpy array of embeddings for existing papers
    :param existing_categories: List of categories for existing papers
    :param threshold: Threshold for similarity
    :return: List of categories for new papers. Contains 'Unclassified' if no category is assigned
    """
    similarities = cosine_similarity(new_embeddings, existing_embeddings)
    categories = []
    for sim in similarities:
        paper_categories = set()
        for i, s in enumerate(sim):
            if s > threshold:
                paper_categories.update(existing_categories[i])
        categories.append(
            list(paper_categories) if paper_categories else ["Unclassified"]
        )
    return categories


# Main function
def main():
    # Load existing papers
    existing_papers = load_existing_papers(
        "../abstract_adding/updated_papers_data.json"
    )
    print(f"Found {len(existing_papers)} existing papers")

    # Extract abstracts and categories from existing papers
    existing_abstracts = [
        paper["abstract"]
        for paper in existing_papers
        if paper["abstract"] != "Abstract not found"
    ]
    print(f"Found {len(existing_abstracts)} existing abstracts")

    existing_categories = [
        paper["category"]
        if isinstance(paper["category"], list)
        else [paper["category"]]
        for paper in existing_papers
    ]
    print(f"Found {len(existing_categories)} existing categories")

    # Generate embeddings for existing papers
    existing_embeddings = generate_embeddings(existing_abstracts)

    # Load new papers
    new_papers = load_new_papers(
        "../paper-scraping/out/new_arxiv_papers_20240903_170512.csv"
    )
    print(f"Found {len(new_papers)} new papers")

    # Generate embeddings for new papers
    new_embeddings = generate_embeddings(new_papers["Abstract"].tolist())

    # Categorize new papers for different thresholds
    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]

    for threshold in thresholds:
        new_categories = categorize_papers(
            new_embeddings, existing_embeddings, existing_categories, threshold
        )
        new_papers[f"Categories_{threshold}"] = new_categories
        print(
            f"Number of unclassified papers (threshold {threshold}): {new_categories.count(['Unclassified'])}"
        )

    # Save results
    out_file_name = "outputs/cosine-categorized.csv"
    new_papers.to_csv(out_file_name, index=False)
    print(f"Categorization complete. Results saved to '{out_file_name}'")


if __name__ == "__main__":
    main()
