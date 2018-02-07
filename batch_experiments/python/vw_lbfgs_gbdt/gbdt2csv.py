# _*_ coding: utf-8 _*_

import sys

from common import *

csv_path = sys.argv[1]
gbdt_path = sys.argv[2]
additional = sys.argv[3]


threshold = 10

# 对每个特征值单独进行哈希, 并输出哈希值

# 出现频率超过10次的特征集合
frequent_feats = read_frequent_feats(threshold)

header = True
with open(additional, 'w') as f:
    for row, line_gbdt in zip(csv.DictReader(open(csv_path)), open(gbdt_path)):
        feats = []
        for feat in gen_feats(row):     # 生成特征向量, 同时将数值特征进行处理
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            # type=I, or C, field=1~39
            if type == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0] + '-less'
            # 生成特征如C1less、C2less
            if type == 'C':
                field += 13
            feats.append((field, feat))

        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i) + '-' + feat))

        if (header == True):
            f.write('Label,Id,' + ','.join(['{0}'.format(feat.split('-')[0]) for (field, feat) in feats]) + '\n')
            header = False

        f.write(row['Label'] + ',' + row['Id'] + ',' + ','.join(
            ['{0}'.format(feat.split('-')[1]) for (field, feat) in feats]) + '\n')
