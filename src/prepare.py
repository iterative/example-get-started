import io
import sys
import xml.etree.ElementTree
import random
import re
import os
import errno

if len(sys.argv) != 2:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython prepare.py data\n')
    sys.exit(1)

# Test data set split ratio
split = 0.20
random.seed(20170426)

input = sys.argv[1]
output_train = os.path.join('data', 'prepared', 'train.tsv')
output_test = os.path.join('data', 'prepared', 'test.tsv')

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


def process_posts(fd_in, fd_out_train, fd_out_test, target_tag):
    num = 1
    for line in fd_in:
        try:
            fd_out = fd_out_train if random.random() > split else fd_out_test
            attr = xml.etree.ElementTree.fromstring(line).attrib

            pid = attr.get('Id', '')
            label = 1 if target_tag in attr.get('Tags', '') else 0
            title = re.sub('\s+', ' ', attr.get('Title', '')).strip()
            body = re.sub('\s+', ' ', attr.get('Body', '')).strip()
            text = title + ' ' + body

            fd_out.write(u'{}\t{}\t{}\n'.format(pid, label, text))

            num += 1
        except Exception as ex:
            sys.stderr.write('Skipping the broken line {}: {}\n'.format(num, ex))


mkdir_p(os.path.join('data', 'prepared'))

with io.open(input, encoding='utf8') as fd_in:
    with io.open(output_train, 'w', encoding='utf8') as fd_out_train:
        with io.open(output_test, 'w', encoding='utf8') as fd_out_test:
            process_posts(fd_in, fd_out_train, fd_out_test, u'<python>')

