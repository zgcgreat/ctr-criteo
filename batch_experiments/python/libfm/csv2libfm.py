# _*_ coding: utf-8 _*_

import collections
import sys
from csv import DictReader

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

data_path = sys.argv[1]
save_path = sys.argv[2]

THRESHOLD = 10

table = collections.defaultdict(int)

# 建立整数值编号
for i in range(1, 14):
    key = 'I{0}'.format(i)
    table[key] = len(table)


def getIndices(key):
    indices = table.get(key)
    if indices == None:
        indices = len(table)
        table[key] = indices
    return indices


with open(save_path + 'train.sparse', 'w') as outfile:
    for e, row in enumerate(DictReader(open(data_path + 'train.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(getIndices(k), v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        key = v
                        features.append('{0}:1'.format(getIndices(key)))
        if row['Label'] == '1':
            label = 1
        else:
            label = -1

        outfile.write('{0} {1}\n'.format(label, ' '.join('{0}'.format(val) for val in features)))

validation = open(data_path + 'validation.csv')
validation.__next__()

with open(save_path + 'test.sparse', 'w') as outfile:
    for e, row in enumerate(DictReader(open(data_path + 'test.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(getIndices(k), v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        key = v
                        features.append('{0}:1'.format(getIndices(key)))
        if validation.readline().strip().split(',')[1] == '1':
            label = 1
        else:
            label = -1

        outfile.write('{0} {1}\n'.format(label, ' '.join('{0}'.format(val) for val in features)))

validation.close()
