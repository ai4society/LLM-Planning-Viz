import json
import os

import pandas as pd
import torch
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import DataLoader, TensorDataset
from transformers import AdamW, AutoModelForSequenceClassification, AutoTokenizer


# Load existing papers data
def load_existing_papers(file_path):
    print(f"Loading existing papers data from {file_path}...")
    with open(file_path, "r") as f:
        papers_data = json.load(f)
    return papers_data


# Load new papers from CSV
def load_new_papers(file_path):
    print(f"Loading new papers data from {file_path}...")
    return pd.read_csv(file_path)


# Prepare data for SciBERT
def prepare_data(papers, tokenizer, max_length=512):
    texts = [paper["title"] + " " + paper["abstract"] for paper in papers]
    categories = [
        paper["category"]
        if isinstance(paper["category"], list)
        else [paper["category"]]
        for paper in papers
    ]

    # Tokenize texts
    encodings = tokenizer(
        texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt"
    )

    # Binarize labels
    mlb = MultiLabelBinarizer()
    labels = mlb.fit_transform(categories)

    return encodings, labels, mlb


# Train model
def train_model(encodings, labels, mlb, num_epochs=10, batch_size=8):
    # Convert to PyTorch tensors
    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]
    labels = torch.tensor(labels, dtype=torch.float)

    # Create dataset and dataloader
    dataset = TensorDataset(input_ids, attention_mask, labels)
    train_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Initialize model
    model = AutoModelForSequenceClassification.from_pretrained(
        "allenai/scibert_scivocab_uncased", num_labels=len(mlb.classes_)
    )

    for param in model.parameters():
        param.data = param.data.contiguous()

    # Set up optimizer
    optimizer = AdamW(model.parameters(), lr=2e-5)

    # Training loop
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on {device}...")
    model.to(device)
    model.train()

    for epoch in range(num_epochs):
        for batch in train_dataloader:
            batch = tuple(t.to(device) for t in batch)
            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "labels": batch[2],
            }
            outputs = model(**inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        print(f"Epoch {epoch + 1}/{num_epochs} completed")

    return model, mlb


# Save model and MLB
def save_model(model, mlb, model_dir):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the model
    model.save_pretrained(model_dir)

    # Save the MultiLabelBinarizer
    import pickle

    with open(os.path.join(model_dir, "mlb.pkl"), "wb") as f:
        pickle.dump(mlb, f)


# Load model and MLB
def load_model(model_dir):
    # Load the model
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    for param in model.parameters():
        param.data = param.data.contiguous()

    # Load the MultiLabelBinarizer
    import pickle

    with open(os.path.join(model_dir, "mlb.pkl"), "rb") as f:
        mlb = pickle.load(f)

    return model, mlb


# Categorize new papers
def categorize_papers(model, tokenizer, mlb, new_papers, threshold=0.5):
    texts = new_papers["Title"] + " " + new_papers["Abstract"]
    encodings = tokenizer(
        texts.tolist(),
        truncation=True,
        padding=True,
        max_length=512,
        return_tensors="pt",
    )

    model.eval()
    with torch.no_grad():
        outputs = model(
            encodings["input_ids"], attention_mask=encodings["attention_mask"]
        )

    predictions = torch.sigmoid(outputs.logits)
    predictions = (predictions > threshold).int().cpu().numpy()

    return mlb.inverse_transform(predictions)


# Main function
def main():
    model_dir = "scibert_model"

    # Check if model exists
    if os.path.exists(model_dir):
        print("Loading existing model...")
        model, mlb = load_model(model_dir)
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    else:
        print("Training new model...")
        # Load existing papers
        existing_papers = load_existing_papers(
            "../abstract_adding/updated_papers_data.json"
        )

        # Initialize tokenizer
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

        # Prepare data
        encodings, labels, mlb = prepare_data(existing_papers, tokenizer)

        # Handle class imbalance
        ros = RandomOverSampler(random_state=42)
        flat_labels = [
            item for sublist in mlb.inverse_transform(labels) for item in sublist
        ]
        resampled_encodings, resampled_labels = ros.fit_resample(
            pd.DataFrame(
                {
                    "input_ids": encodings["input_ids"].numpy().tolist(),
                    "attention_mask": encodings["attention_mask"].numpy().tolist(),
                }
            ),
            flat_labels,
        )

        # Convert back to tensors
        resampled_input_ids = torch.tensor(resampled_encodings["input_ids"].tolist())
        resampled_attention_mask = torch.tensor(
            resampled_encodings["attention_mask"].tolist()
        )
        resampled_labels = mlb.transform([[label] for label in resampled_labels])

        # Train model
        model, mlb = train_model(
            {
                "input_ids": resampled_input_ids,
                "attention_mask": resampled_attention_mask,
            },
            resampled_labels,
            mlb,
        )

        # Save model
        save_model(model, mlb, model_dir)

    # Load new papers
    new_papers = load_new_papers(
        "../paper-scraping/out/new_arxiv_papers_20240903_170512.csv"
    )

    # Categorize new papers
    new_categories = categorize_papers(model, tokenizer, mlb, new_papers)

    # Add categories to new papers dataframe
    new_papers["Categories"] = [
        ", ".join(cats) if cats else "Unclassified" for cats in new_categories
    ]

    # Save results
    savefile = "outputs/scibert.csv"
    new_papers.to_csv(savefile, index=False)
    print(f"Categorization complete. Results saved to '{savefile}'")


if __name__ == "__main__":
    main()
