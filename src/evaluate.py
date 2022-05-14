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


live = Live("evaluation")

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py model features\n")
    sys.exit(1)

model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], "test.pkl")

with open(model_file, "rb") as fd:
    model = pickle.load(fd)

with open(matrix_file, "rb") as fd:
    matrix, feature_names = pickle.load(fd)

labels = matrix[:, 1].toarray().astype(int)
x = matrix[:, 2:]

predictions_by_class = model.predict_proba(x)
predictions = predictions_by_class[:, 1]

# Use dvclive to log a few simple plots ...
live.log_plot("roc", labels, predictions)
live.log("avg_prec", metrics.average_precision_score(labels, predictions))
live.log("roc_auc", metrics.roc_auc_score(labels, predictions))

# ... but actually it can be done with dumping data points into a file:
# ROC has a drop_intermediate arg that reduces the number of points.
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html#sklearn.metrics.roc_curve.
# PRC lacks this arg, so we manually reduce to 1000 points as a rough estimate.
precision, recall, prc_thresholds = metrics.precision_recall_curve(labels, predictions)
nth_point = math.ceil(len(prc_thresholds) / 1000)
prc_points = list(zip(precision, recall, prc_thresholds))[::nth_point]
prc_file = os.path.join("evaluation", "plots", "precision_recall.json")
with open(prc_file, "w") as fd:
    json.dump(
        {
            "prc": [
                {"precision": p, "recall": r, "threshold": t}
                for p, r, t in prc_points
            ]
        },
        fd,
        indent=4,
    )


# ... confusion matrix plot
live.log_plot("confusion_matrix", labels.squeeze(), predictions_by_class.argmax(-1))

# ... and finally, we can dump an image, it's also supported:
fig, axes = plt.subplots(dpi=100)
fig.subplots_adjust(bottom=0.2, top=0.95)
importances = model.feature_importances_
forest_importances = pd.Series(importances, index=feature_names).nlargest(n=30)
axes.set_ylabel("Mean decrease in impurity")
forest_importances.plot.bar(ax=axes)
fig.savefig(os.path.join("evaluation", "importance.png"))
