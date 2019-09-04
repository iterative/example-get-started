import sys
import os

from sklearn.metrics import precision_recall_curve
import sklearn.metrics as metrics

try:
    import cPickle as pickle
except ImportError:
    import pickle

if len(sys.argv) != 4:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython evaluate.py model features output\n')
    sys.exit(1)

model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], 'test.pkl')
metrics_file = sys.argv[3]

with open(model_file, 'rb') as fd:
    model = pickle.load(fd)

with open(matrix_file, 'rb') as fd:
    matrix = pickle.load(fd)

labels = matrix[:, 1].toarray()
x = matrix[:, 2:]

predictions_by_class = model.predict_proba(x)
predictions = predictions_by_class[:, 1]

precision, recall, thresholds = precision_recall_curve(labels, predictions)

auc = metrics.auc(recall, precision)

with open(metrics_file, 'w') as fd:
    fd.write('{:4f}\n'.format(auc))

