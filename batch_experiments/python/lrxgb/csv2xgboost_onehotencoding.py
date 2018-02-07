# _*_ coding: utf-8 _*_

from csv import DictReader
import sys
import collections

data_path = sys.argv[1]
save_path = sys.argv[2]

THRESHOLD = 10

# 给整个数据集生成一个编号默认字典 [index]
table = collections.defaultdict(lambda: 0)

for i, row in enumerate(DictReader(open('../../data/data.csv'))):
    label = row['Label']
    for j in range(1, 27):
        field = 'C{0}'.format(j)
        value = row[field]
        table[field + '-' + value] = len(table) + 13


with open(save_path + 'train.sparse', 'w') as outfile:
    for t, row in enumerate(DictReader(open(data_path + 'train.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(k.split('I')[1], v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        value = table.get(key)
                        features.append('{0}:1'.format(value))

        outfile.write('{0} {1}\n'.format(row['Label'], ' '.join('{0}'.format(val) for val in features)))

validation = open(data_path + 'validation.csv', 'r')
validation.__next__()

with open(save_path + 'test.sparse', 'w') as outfile:
    for t, row in enumerate(DictReader(open(data_path + 'test.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(k.split('I')[1], v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        value = table.get(key)
                        features.append('{0}:1'.format(value))

        if validation.readline().strip().split(',')[1] == '1':
            label = 1
        else:
            label = 0
        outfile.write('{0} {1}\n'.format(label, ' '.join('{0}'.format(val) for val in features)))

validation.close()
