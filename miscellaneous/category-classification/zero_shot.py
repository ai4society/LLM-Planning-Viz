import json

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def load_existing_papers(file_path):
    with open(file_path, "r") as f:
        papers_data = json.load(f)
    return papers_data


def prepare_data(papers, tokenizer, max_length=512):
    texts = [paper["title"] + " " + paper["abstract"] for paper in papers]
    categories = [
        paper["category"]
        if isinstance(paper["category"], list)
        else [paper["category"]]
        for paper in papers
    ]

    encodings = tokenizer(
        texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt"
    )

    mlb = MultiLabelBinarizer()
    labels = mlb.fit_transform(categories)

    return encodings, labels, mlb


def evaluate_model(model, dataloader, mlb, device):
    model.eval()
    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for input_ids, attention_mask, labels in tqdm(dataloader, desc="Evaluating"):
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            predictions = torch.sigmoid(logits)
            predictions = (predictions > 0.5).int()

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    all_predictions = np.array(all_predictions)
    all_labels = np.array(all_labels)

    report = classification_report(
        all_labels, all_predictions, target_names=mlb.classes_, zero_division=0
    )
    return report, all_predictions


def main():
    # Load existing papers
    existing_papers = load_existing_papers(
        "../abstract_adding/updated_papers_data.json"
    )

    # List of models to test
    models_to_test = ["bert-base-uncased", "allenai/scibert_scivocab_uncased"]

    for model_name in models_to_test:
        print(f"\nTesting model: {model_name}")

        # Initialize tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        num_labels = len(
            set(
                [
                    cat
                    for paper in existing_papers
                    for cat in (
                        paper["category"]
                        if isinstance(paper["category"], list)
                        else [paper["category"]]
                    )
                ]
            )
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )

        # Prepare data
        encodings, labels, mlb = prepare_data(existing_papers, tokenizer)

        # Set up 5-fold cross-validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)

        # Set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        all_fold_predictions = []
        all_fold_indices = []

        for fold, (_, val_indices) in enumerate(kf.split(encodings["input_ids"]), 1):
            print(f"\nFold {fold}")

            # Create datasets
            val_dataset = TensorDataset(
                encodings["input_ids"][val_indices],
                encodings["attention_mask"][val_indices],
                torch.tensor(labels[val_indices], dtype=torch.float),  # type: ignore
            )
            val_dataloader = DataLoader(val_dataset, batch_size=16)

            # Evaluate model
            report, fold_predictions = evaluate_model(
                model, val_dataloader, mlb, device
            )
            print(f"Classification Report for {model_name} (Fold {fold}):")
            print(report)

            all_fold_predictions.extend(fold_predictions)
            all_fold_indices.extend([fold] * len(val_indices))

        # Create DataFrame with results
        results_df = pd.DataFrame(
            {
                "title": [paper["title"] for paper in existing_papers],
                "abstract": [paper["abstract"] for paper in existing_papers],
                "actual_categories": [
                    ", ".join(
                        paper["category"]
                        if isinstance(paper["category"], list)
                        else [paper["category"]]
                    )
                    for paper in existing_papers
                ],
                "predicted_categories": [
                    ", ".join(mlb.classes_[prediction.astype(bool)])
                    for prediction in all_fold_predictions
                ],
                "cross_validation_fold": all_fold_indices,
            }
        )

        # Save results
        if model_name == "bert-base-uncased":
            output_file = "outputs/zero_shot-bert.csv"
        elif model_name == "allenai/scibert_scivocab_uncased":
            output_file = "outputs/zero_shot-scibert.csv"
        else:
            exit("Model not found")
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
