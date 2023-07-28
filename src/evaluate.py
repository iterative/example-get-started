import json
import math
import os
import pickle
import sys

import pandas as pd
from sklearn import metrics
from sklearn import tree
from dvclive import Live
from matplotlib import pyplot as plt


def evaluate(model, matrix, split, live, save_path):
    """
    Dump all evaluation metrics and plots for given datasets.

    Args:
        model (sklearn.ensemble.RandomForestClassifier): Trained classifier.
        matrix (scipy.sparse.csr_matrix): Input matrix.
        split (str): Dataset name.
        live (dvclive.Live): Dvclive instance.
        save_path (str): Path to save the metrics.
    """
    labels = matrix[:, 1].toarray().astype(int)
    x = matrix[:, 2:]

    predictions_by_class = model.predict_proba(x)
    predictions = predictions_by_class[:, 1]

    # Use dvclive to log a few simple metrics...
    avg_prec = metrics.average_precision_score(labels, predictions)
    roc_auc = metrics.roc_auc_score(labels, predictions)
    if not live.summary:
        live.summary = {"avg_prec": {}, "roc_auc": {}}
    live.summary["avg_prec"][split] = avg_prec
    live.summary["roc_auc"][split] = roc_auc

    # ... and plots...
    # ... like an roc plot...
    live.log_sklearn_plot("roc", labels, predictions, name=f"roc/{split}")
    # ... and precision recall plot...
    # ... which passes `drop_intermediate=True` to the sklearn method...
    live.log_sklearn_plot(
        "precision_recall",
        labels,
        predictions,
        name=f"prc/{split}",
        drop_intermediate=True,
    )
    # ... and confusion matrix plot
    live.log_sklearn_plot(
        "confusion_matrix",
        labels.squeeze(),
        predictions_by_class.argmax(-1),
        name=f"cm/{split}",
    )


def save_importance_plot(live, model, feature_names):
    """
    Save feature importance plot.

    Args:
        live (dvclive.Live): DVCLive instance.
        model (sklearn.ensemble.RandomForestClassifier): Trained classifier.
        feature_names (list): List of feature names.
    """
    fig, axes = plt.subplots(dpi=100)
    fig.subplots_adjust(bottom=0.2, top=0.95)
    axes.set_ylabel("Mean decrease in impurity")

    importances = model.feature_importances_
    forest_importances = pd.Series(importances, index=feature_names).nlargest(n=30)
    forest_importances.plot.bar(ax=axes)

    live.log_image("importance.png", fig)


def main():
    EVAL_PATH = "eval"

    if len(sys.argv) != 3:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython evaluate.py model features\n")
        sys.exit(1)

    model_file = sys.argv[1]
    train_file = os.path.join(sys.argv[2], "train.pkl")
    test_file = os.path.join(sys.argv[2], "test.pkl")

    # Load model and data.
    with open(model_file, "rb") as fd:
        model = pickle.load(fd)

    with open(train_file, "rb") as fd:
        train, feature_names = pickle.load(fd)

    with open(test_file, "rb") as fd:
        test, _ = pickle.load(fd)

    # Evaluate train and test datasets.
    with Live(EVAL_PATH, dvcyaml=False) as live:
        evaluate(model, train, "train", live, save_path=EVAL_PATH)
        evaluate(model, test, "test", live, save_path=EVAL_PATH)

        # Dump feature importance plot.
        save_importance_plot(live, model, feature_names)


if __name__ == "__main__":
    main()
