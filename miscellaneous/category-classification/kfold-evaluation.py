import json
import warnings
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import KFold
from sklearn.preprocessing import MultiLabelBinarizer

warnings.simplefilter(action="ignore", category=FutureWarning)


def load_existing_papers(file_path):
    with open(file_path, "r") as f:
        papers_data = json.load(f)
    return papers_data


def generate_embeddings(texts):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts)


def categorize_papers(
    new_embeddings, existing_embeddings, existing_categories, threshold
):
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


def evaluate_performance(true_categories, predicted_categories):
    mlb = MultiLabelBinarizer()
    mlb.fit(true_categories + predicted_categories)
    true_binary = mlb.transform(true_categories)
    pred_binary = mlb.transform(predicted_categories)

    precision, recall, f1, _ = precision_recall_fscore_support(
        true_binary, pred_binary, average="micro"
    )
    return precision, recall, f1, mlb.classes_


def perform_cross_validation(abstracts, categories, n_splits=5, threshold=0.7):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    precisions, recalls, f1_scores = [], [], []
    all_true_categories, all_predicted_categories = [], []
    fold_indices = []

    for fold, (train_index, test_index) in enumerate(kf.split(abstracts), 1):
        # Split the data
        train_abstracts = [abstracts[i] for i in train_index]
        train_categories = [categories[i] for i in train_index]
        test_abstracts = [abstracts[i] for i in test_index]
        test_categories = [categories[i] for i in test_index]

        # Generate embeddings
        train_embeddings = generate_embeddings(train_abstracts)
        test_embeddings = generate_embeddings(test_abstracts)

        # Categorize papers
        predicted_categories = categorize_papers(
            test_embeddings, train_embeddings, train_categories, threshold
        )

        # Evaluate performance
        precision, recall, f1, _ = evaluate_performance(
            test_categories, predicted_categories
        )

        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

        all_true_categories.extend(test_categories)
        all_predicted_categories.extend(predicted_categories)
        fold_indices.extend([(fold, i) for i in test_index])

        print(
            f"Fold {fold} - Precision: {precision:.4f}, Recall: {recall:.4f}, F1-score: {f1:.4f}"
        )

    return (
        np.mean(precisions),
        np.std(precisions),
        np.mean(recalls),
        np.std(recalls),
        np.mean(f1_scores),
        np.std(f1_scores),
        all_true_categories,
        all_predicted_categories,
        fold_indices,
    )


def plot_metrics(precisions, recalls, f1_scores):
    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [precisions, recalls, f1_scores], labels=["Precision", "Recall", "F1-score"]
    )
    plt.title("Distribution of Performance Metrics Across Folds")
    plt.ylabel("Score")

    fig_name: str = "performance_metrics_boxplot.png"

    plt.savefig(fig_name)
    plt.close()
    print(f"Performance metrics boxplot saved as {fig_name}")


def plot_category_distribution(categories, title):
    category_counts = Counter([cat for cats in categories for cat in cats])
    plt.figure(figsize=(12, 6))
    plt.bar(category_counts.keys(), category_counts.values())
    plt.title(title)
    plt.xlabel("Categories")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.tight_layout()

    fig_name = f"{title.lower().replace(' ', '_')}.png"

    plt.savefig(fig_name)
    plt.close()

    print(f"{title} bar plot saved as {fig_name}")


def main():
    # Load existing papers
    existing_papers = load_existing_papers(
        "../abstract_adding/updated_papers_data.json"
    )
    print(f"Found {len(existing_papers)} existing papers")

    # Extract abstracts and categories from existing papers
    abstracts = [
        paper["abstract"]
        for paper in existing_papers
        if paper["abstract"] != "Abstract not found"
    ]
    categories = [
        paper["category"]
        if isinstance(paper["category"], list)
        else [paper["category"]]
        for paper in existing_papers
    ]

    # Create a DataFrame from the existing papers
    df = pd.DataFrame(existing_papers)

    print("Performing 5-fold cross-validation...")
    (
        precision_mean,
        precision_std,
        recall_mean,
        recall_std,
        f1_mean,
        f1_std,
        true_categories,
        predicted_categories,
        fold_indices,
    ) = perform_cross_validation(abstracts, categories)

    print("\nOverall Results:")
    print(f"Precision: {precision_mean:.4f} (±{precision_std:.4f})")
    print(f"Recall: {recall_mean:.4f} (±{recall_std:.4f})")
    print(f"F1-score: {f1_mean:.4f} (±{f1_std:.4f})")

    # Add predicted categories and fold information to the DataFrame
    df["Predicted_Categories"] = [",".join(cats) for cats in predicted_categories]
    df["Cross_Validation_Fold"] = [fold for fold, _ in fold_indices]

    # Save the updated DataFrame to a new CSV file
    output_file = "outputs/kfold-originals.csv"
    df.to_csv(output_file, index=False)
    print(f"\nUpdated data with predictions saved to {output_file}")

    # Calculate and print per-category metrics
    mlb = MultiLabelBinarizer()
    mlb.fit(true_categories + predicted_categories)
    true_binary = mlb.transform(true_categories)
    pred_binary = mlb.transform(predicted_categories)

    precision, recall, f1, _ = precision_recall_fscore_support(
        true_binary, pred_binary, average=None, labels=range(len(mlb.classes_))
    )

    print("\nPer-category Performance:")
    for cls, p, r, f in zip(mlb.classes_, precision, recall, f1):
        print(f"{cls}: Precision={p:.4f}, Recall={r:.4f}, F1-score={f:.4f}")


if __name__ == "__main__":
    main()
