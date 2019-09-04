import os
import sys
import errno
import pandas as pd
import numpy as np
import scipy.sparse as sparse

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

try:
    import cPickle as pickle
except ImportError:
    import pickle

np.set_printoptions(suppress=True)

if len(sys.argv) != 3 and len(sys.argv) != 5:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython featurization.py data-dir-path features-dir-path\n')
    sys.exit(1)

train_input = os.path.join(sys.argv[1], 'train.tsv')
test_input = os.path.join(sys.argv[1], 'test.tsv')
train_output = os.path.join(sys.argv[2], 'train.pkl')
test_output = os.path.join(sys.argv[2], 'test.pkl')

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_df(data):
    df = pd.read_csv(
        data,
        encoding='utf-8',
        header=None,
        delimiter='\t',
        names=['id', 'label', 'text']
    )
    sys.stderr.write('The input data frame {} size is {}\n'.format(data, df.shape))
    return df


def save_matrix(df, matrix, output):
    id_matrix = sparse.csr_matrix(df.id.astype(np.int64)).T
    label_matrix = sparse.csr_matrix(df.label.astype(np.int64)).T

    result = sparse.hstack([id_matrix, label_matrix, matrix], format='csr')

    msg = 'The output matrix {} size is {} and data type is {}\n'
    sys.stderr.write(msg.format(output, result.shape, result.dtype))

    with open(output, 'wb') as fd:
        pickle.dump(result, fd, pickle.HIGHEST_PROTOCOL)
    pass


mkdir_p(sys.argv[2])

# Generate train feature matrix
df_train = get_df(train_input)
train_words = np.array(df_train.text.str.lower().values.astype('U'))

bag_of_words = CountVectorizer(stop_words='english',
                               max_features=5000)
bag_of_words.fit(train_words)
train_words_binary_matrix = bag_of_words.transform(train_words)
tfidf = TfidfTransformer(smooth_idf=False)
tfidf.fit(train_words_binary_matrix)
train_words_tfidf_matrix = tfidf.transform(train_words_binary_matrix)

save_matrix(df_train, train_words_tfidf_matrix, train_output)

# Generate test feature matrix
df_test = get_df(test_input)
test_words = np.array(df_test.text.str.lower().values.astype('U'))
test_words_binary_matrix = bag_of_words.transform(test_words)
test_words_tfidf_matrix = tfidf.transform(test_words_binary_matrix)

save_matrix(df_test, test_words_tfidf_matrix, test_output)

