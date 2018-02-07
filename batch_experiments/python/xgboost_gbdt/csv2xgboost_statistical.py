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

# [positive][total][index]
table = collections.defaultdict(lambda: [0, 0, 0])

for i, row in enumerate(DictReader(open('../../data/data.csv'))):
    label = row['Label']
    for j in range(1, 27):
        field = 'C{0}'.format(j)
        value = row[field]
        if label == '1':
            table[field + '-' + value][0] += 1
        table[field + '-' + value][1] += 1
        table[field + '-' + value][2] = len(table) + 13

# 计算某个特征值的点击率（出现该特征值被点击 / 特征值出现的总次数）

with open(save_path + 'train.sparse', 'w') as outfile:
    for e, row in enumerate(DictReader(open(data_path + 'train.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(k.split('I')[1], v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        value = table.get(key)  # 从table中获得值
                        if value is not None:
                            if float(value[1]) > THRESHOLD:  # 特征值出现次数超过10次
                                # 计算某个特征值的点击率（出现该特征值被点击 / 特征值出现的总次数）
                                ratio = float(value[0]) / float(value[1])
                                features.append('{0}:{1}'.format(value[2], round(ratio, 5)))

        outfile.write('{0} {1}\n'.format(row['Label'], ' '.join('{0}'.format(val) for val in features)))

validation = open(data_path + 'validation.csv', 'r')
validation.__next__()
with open(save_path + 'test.sparse', 'w') as outfile:
    for e, row in enumerate(DictReader(open(data_path + 'test.csv'))):
        features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if 'I' in k:
                    if len(str(v)) > 0:
                        features.append('{0}:{1}'.format(k.split('I')[1], v))
                if 'C' in k:
                    if len(str(v)) > 0:
                        key = k + '-' + v
                        value = table.get(key)  # 从table中获得值
                        if value is not None:
                            if float(value[1]) > THRESHOLD:  # 特征值出现次数超过10次
                                # 计算某个特征值的点击率（出现该特征值被点击 / 特征值出现的总次数）
                                ratio = float(value[0]) / float(value[1])
                                features.append('{0}:{1}'.format(value[2], round(ratio, 5)))

        if validation.readline().strip().split(',')[1] == '1':
            label = 1
        else:
            label = 0

        outfile.write('{0} {1}\n'.format(label, ' '.join('{0}'.format(val) for val in features)))
validation.close()
