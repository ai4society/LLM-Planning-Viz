import json

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")


def load_existing_papers(file_path):
    """
    Load existing papers data from a JSON file.
    @param file_path: Path to the JSON file.
    @return: List of dictionaries, where each dictionary represents a paper.
    """
    print(f"Loading existing papers data from {file_path}...")
    with open(file_path, "r") as f:
        papers_data = json.load(f)
    return papers_data


def load_new_papers(file_path):
    """
    Load new papers data from a CSV file.
    @param file_path: Path to the CSV file.
    @return: DataFrame containing new papers data.
    """
    print(f"Loading new papers data from {file_path}...")
    return pd.read_csv(file_path)


def preprocess_text(text):
    """
    Preprocess text data by removing stopwords, punctuation, and converting to lowercase.
    @param text: Text data to preprocess.
    @return: Preprocessed text.
    """
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text.lower())
    return " ".join([w for w in word_tokens if w not in stop_words and w.isalnum()])


def prepare_data(papers):
    """
    Prepare data for training the model.
    @param papers: List of dictionaries, where each dictionary represents a paper.
    @return: X, y where X is a list of preprocessed abstracts and y is a list of categories.
    """
    X = [preprocess_text(paper["abstract"]) for paper in papers]
    y = [
        paper["category"]
        if isinstance(paper["category"], list)
        else [paper["category"]]
        for paper in papers
    ]
    return X, y


def train_model(X, y):
    """
    Train a multi-label classification model using LinearSVC.
    @param X: List of preprocessed abstracts.
    @param y: List of categories.
    @return: Trained model and classification report.
    """
    mlb = MultiLabelBinarizer()
    y_encoded = mlb.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=5000)),
            ("clf", OneVsRestClassifier(LinearSVC())),
        ]
    )

    pipeline.fit(X_train, y_train)

    # Evaluate model
    y_pred = pipeline.predict(X_test)

    return (
        pipeline,
        mlb,
        classification_report(y_test, y_pred, target_names=mlb.classes_),
    )


# Categorize new papers
def categorize_papers(model, mlb, new_papers):
    """
    Categorize new papers using the trained model.
    @param model: Trained model.
    @param mlb: MultiLabelBinarizer object.
    @param new_papers: DataFrame containing new papers data.
    @return: List of predicted categories for each new paper.
    """
    preprocessed_abstracts = [
        preprocess_text(abstract) for abstract in new_papers["Abstract"]
    ]
    predictions = model.predict(preprocessed_abstracts)
    return mlb.inverse_transform(predictions)


# Main function
def main():
    # Load existing papers
    existing_papers = load_existing_papers(
        "../abstract_adding/updated_papers_data.json"
    )

    # Prepare data
    X, y = prepare_data(existing_papers)

    # Train model
    model, mlb, class_report = train_model(X, y)
    print("Model trained successfully.")
    print("Classification report:")
    print(class_report)

    # Load new papers
    new_papers = load_new_papers(
        "../paper-scraping/out/new_arxiv_papers_20240903_170512.csv"
    )

    # Categorize new papers
    new_categories = categorize_papers(model, mlb, new_papers)

    # Add categories to new papers dataframe
    new_papers["Categories"] = [", ".join(cats) for cats in new_categories]

    # Save results
    out_file = "outputs/svm-categorized.csv"
    new_papers.to_csv(out_file, index=False)
    print(f"Categorization complete. Results saved to '{out_file}'")


if __name__ == "__main__":
    main()
