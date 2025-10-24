# Category Classification

Scripts in this folder are designed to categorize academic papers into predefined categories based on their abstracts. Various machine learning techniques are employed, including Support Vector Machines (SVM), Cosine Similarity with Sentence Transformers, and fine-tuning of BERT and SciBERT models.

## TOC

- [Support Vector Machines](#support-vector-machines)
- [Cosine Similarity](#cosine-similarity)
- [BERT and SciBERT (Fine-Tuning)](#bert-and-scibert-fine-tuning)
- [BERT and SciBERT (Zero-Shot Evaluation)](#bert-and-scibert-zero-shot-evaluation)
- [Cross-Validation Evaluation](#cross-validation-evaluation)

## Support Vector Machines

The `svm.py` script categorizes new papers based on their abstracts using a multi-label classification model: OneVsRestClassifier with LinearSVC.

It uses TF-IDF vectorization and train a multi-label SVM classifier. The model is trained on existing papers data and then used to predict categories for new papers. The results are then saved to a CSV file.

Example report:

```shell
Classification report:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.00      0.00      0.00         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.00      0.00      0.00         4
     model-construction       0.00      0.00      0.00         2
    multiagent-planning       0.00      0.00      0.00         1
        plan-generation       0.40      0.20      0.27        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.22      0.07      0.11        28
              macro avg       0.05      0.03      0.03        28
           weighted avg       0.14      0.07      0.10        28
            samples avg       0.07      0.07      0.07        28
```

Example console output:

```shell
Loading existing papers data from ../../abstract_adding/updated_papers_data.json...

Model trained successfully.
Classification report:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.00      0.00      0.00         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.00      0.00      0.00         4
     model-construction       0.00      0.00      0.00         2
    multiagent-planning       0.00      0.00      0.00         1
        plan-generation       0.40      0.20      0.27        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.22      0.07      0.11        28
              macro avg       0.05      0.03      0.03        28
           weighted avg       0.14      0.07      0.10        28
            samples avg       0.07      0.07      0.07        28

Loading new papers data from ../data/copy_new_arxiv_papers_20240903_170512.csv...
Categorization complete. Results saved to 'categorized_papers.csv'
```

## Cosine Similarity

The `cosine.py` file uses the existing dataset, process new papers from a CSV file, generate embeddings, and categorizes them based on similarity to existing papers. To further elaborate, the script does the following:

1. Loads existing papers from a JSON file.
2. Loads new papers from a CSV file.
3. Generates embeddings for both existing and new papers using the SentenceTransformer model.
4. Categorizes new papers based on their similarity to existing papers.
5. Tries different thresholds for similarity to categorize papers.
6. Saves the results for all attempted thresholds to a new CSV file.

Two data files were used:

- `../abstract_adding/updated_papers_data.json`: The data file containing existing, categorized papers with their abstracts.
- `./copy_new_arxiv_papers_20240903_170512.csv`: The data file containing new papers to be categorized.

The output of the script is a csv file containing the same data and columns as the `./copy_new_arxiv_papers_20240903_170512.csv` file, with an additional columns `category_{threshold}` containing the category of the paper based on the threshold.
The output file is saved as `output/categorized_papers_multiple_thresholds.csv`.

Potential Challenges:

- Choosing the right similarity threshold to balance between over-classification and under-classification.
- Handling papers that are on the borderline between categories.
- Dealing with new emerging categories that don't exist in the current taxonomy.

Sample Console Output:

```shell
Loading existing papers data at ../../abstract_adding/updated_papers_data.json
Found 140 existing papers
Found 140 existing abstracts
Found 140 existing categories
Loading new papers from ../data/copy_new_arxiv_papers_20240903_170512.csv
Found 48 new papers
Number of unclassified papers (threshold 0.5): 0
Number of unclassified papers (threshold 0.6): 4
Number of unclassified papers (threshold 0.7): 8
Number of unclassified papers (threshold 0.8): 26
Number of unclassified papers (threshold 0.9): 34
Categorization complete. Results saved to 'categorized_papers_multiple_thresholds.csv'
```

## BERT and SciBERT (Fine-Tuning)

Both the `bert.py` and `scibert.py` scripts follow a similar process for categorizing papers. Here's a step-by-step breakdown of what they're doing:

1. Data Loading and Preparation: The script loads both the existing papers from a JSON file and new papers to be categorized from a CSV file. It combines the title and abstract of each paper into a single text. The categories of existing papers are transformed into a multi-label format using scikit-learn's MultiLabelBinarizer.

2. The combined text (title + abstract) is tokenized using the appropriate tokenizer (BERT or SciBERT).

3. The script fine-tunes the model on the existing papers. This process adapts the pre-trained model to the specific categorization task.

4. Class Imbalance Handling: The script uses RandomOverSampler to address potential class imbalance in the dataset. This technique replicates examples from minority classes to ensure all categories are well-represented during training.

5. Categorization of New Papers: For new papers, the script: (1) Tokenizes the combined title and abstract, (2) Feeds this through the fine-tuned model, (3) Applies a threshold to the model's output to determine which categories to assign.

6. The categorized papers are saved to a new CSV file with their assigned categories.

The main difference between the BERT and SciBERT scripts is the base model they use:

- The BERT script uses the 'bert-base-uncased' model, which is pre-trained on a large corpus of general text.
- The SciBERT script uses 'allenai/scibert_scivocab_uncased', which is pre-trained on a large corpus of scientific papers.

## BERT and SciBERT (Zero-Shot Evaluation)

The script, `zero_shot.py`, evaluates the performance of pre-trained BERT and SciBERT models on a multi-label classification task without any fine-tuning. As such, we only perform predictions on the existing labeled dataset to see how well the models can categorize papers based solely on their pre-trained knowledge.

Key observations:

- Overall performance: SciBERT outperformed BERT across all metrics, suggesting its scientific pre-training gives it an edge for our domain-specific task.
- Micro-average F1 scores: BERT achieved 0.08, while SciBERT reached 0.18, indicating SciBERT's superior overall performance.
- Class imbalance: Both models struggled with less represented categories (e.g., 'brain-inspired-planning', 'interactive-planning'), often failing to predict these classes entirely.
- Recall vs Precision: SciBERT showed higher recall (0.57 micro-avg) compared to precision (0.11 micro-avg), suggesting it's more likely to assign categories but with lower confidence.
- Best performing category: 'plan-generation' had the highest F1-score (0.53) with SciBERT, likely due to having the most examples in the dataset.

These results highlight the potential of using SciBERT as a starting point, but also underscore the need for fine-tuning, addressing class imbalance, and potentially collecting more data for underrepresented categories to improve overall classification performance.

Console Output:

```shell
Classification Report for bert-base-uncased:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.04      1.00      0.07         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.00      0.00      0.00         4
     model-construction       0.07      1.00      0.13         2
    multiagent-planning       0.08      1.00      0.15         1
        plan-generation       0.00      0.00      0.00        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.06      0.14      0.08        28
              macro avg       0.02      0.38      0.05        28
           weighted avg       0.01      0.14      0.02        28
            samples avg       0.05      0.14      0.08        28

Classification Report for allenai/scibert_scivocab_uncased:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.04      1.00      0.07         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.14      0.75      0.23         4
     model-construction       0.04      0.50      0.07         2
    multiagent-planning       0.04      1.00      0.07         1
        plan-generation       0.36      1.00      0.53        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.11      0.57      0.18        28
              macro avg       0.08      0.53      0.12        28
           weighted avg       0.15      0.57      0.23        28
            samples avg       0.11      0.57      0.18        28
```

## Cross-Validation Evaluation

The `kfold-evaluation.py` script evaluates the categorization model using cross-validation on existing labeled papers to measure performance. **Note that this script is for model evaluation - it tests how well the categorization approach works using known labels, it does not perform new categorizations.**

Key Components:

1. Data Loading: Loads existing paper data from a JSON file.
2. Embedding Generation: Uses SentenceTransformer to create embeddings for paper abstracts.
3. Categorization: Assigns categories to papers based on similarity to known papers.
4. Cross-Validation: Implements 5-fold cross-validation to assess model performance.
5. Evaluation: Calculates precision, recall, and F1-score for overall and per-category performance.

Assumptions:

1. Input data is in a specific JSON format with 'abstract' and 'category' fields.
2. Categories are treated as multi-label (papers can belong to multiple categories).
3. The similarity threshold (0.7) is appropriate for category assignment.
4. The chosen embedding model (all-MiniLM-L6-v2) is suitable for scientific text.

Outputs:

1. Console output: Overall and per-fold performance metrics, per-category metrics.
2. CSV file: Original paper data with added columns for predicted categories and cross-validation fold.

Limitations:

1. Relies on the quality and comprehensiveness of the existing labeled dataset.
2. Performance may vary with different similarity thresholds or embedding models.
3. Does not handle potential class imbalance issues.

Example console output:

```shell
Found 140 existing papers
Performing 5-fold cross-validation...
Fold 1 - Precision: 0.2178, Recall: 0.7857, F1-score: 0.3411
Fold 2 - Precision: 0.1927, Recall: 0.7500, F1-score: 0.3066
Fold 3 - Precision: 0.1895, Recall: 0.6429, F1-score: 0.2927
Fold 4 - Precision: 0.2165, Recall: 0.7500, F1-score: 0.3360
Fold 5 - Precision: 0.2079, Recall: 0.7500, F1-score: 0.3256

Overall Results:
Precision: 0.2049 (±0.0118)
Recall: 0.7357 (±0.0484)
F1-score: 0.3204 (±0.0182)

Updated data with predictions saved to output/original_papers_with_cross_val_predictions.csv

Per-category Performance:
Unclassified: Precision=0.0000, Recall=0.0000, F1-score=0.0000
brain-inspired-planning: Precision=0.1000, Recall=0.6000, F1-score=0.1714
heuristics-optimization: Precision=0.0847, Recall=0.6250, F1-score=0.1493
interactive-planning: Precision=0.1625, Recall=0.6190, F1-score=0.2574
language-translation: Precision=0.1724, Recall=0.6522, F1-score=0.2727
model-construction: Precision=0.1429, Recall=0.7059, F1-score=0.2376
multiagent-planning: Precision=0.2222, Recall=0.4000, F1-score=0.2857
plan-generation: Precision=0.4182, Recall=0.8679, F1-score=0.5644
tool-integration: Precision=0.2593, Recall=0.8750, F1-score=0.4000
```
