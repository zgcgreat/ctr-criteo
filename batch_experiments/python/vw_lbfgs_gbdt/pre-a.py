# _*_ coding: utf-8 _*_

import sys
import csv
from common import *

csv_path = sys.argv[1]
dense_path = sys.argv[2]
sparse_path = sys.argv[3]

# 类别属性中出现频率最高的26个特征
target_cat_feats = ['C9-a73ee510', 'C22-', 'C17-e5ba7672', 'C26-', 'C23-32c7478e', 'C6-7e0ccccf', 'C14-b28479f6',
                    'C19-21ddcdc9', 'C14-07d13a8f', 'C10-3b08e48b', 'C6-fbad5c96', 'C23-3a171ecb', 'C20-b1252a9d',
                    'C20-5840adea', 'C6-fe6b92e5', 'C20-a458ea53', 'C14-1adce6ef', 'C25-001f3601', 'C22-ad3062eb',
                    'C17-07c540c4', 'C6-', 'C23-423fab69', 'C17-d4bb7bd8', 'C2-38a947a1', 'C25-e8b83407', 'C9-7cc72ec2']

with open(dense_path, 'w') as f_d, open(sparse_path, 'w') as f_s:
    for row in csv.DictReader(open(csv_path)):
        feats = []
        for j in range(1, 14):
            val = row['I{0}'.format(j)]
            # 若数值缺失, 则为-10
            if val == '':
                val = -10
            feats.append('{0}'.format(val))
        # 将数值属性放入.dense文件中
        f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')

        cat_feats = set()
        for j in range(1, 27):
            field = 'C{0}'.format(j)
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        # 将最常见的26个类别属性编码放入sparse文件中
        f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')

