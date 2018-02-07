# _*_ coding: utf-8 _*_

import subprocess
import sys
from csv import DictReader
from common import *

nr_bins = int(1e+6)
threshold = 10
csv_path = sys.argv[1]
gbdt_path = sys.argv[2]
out_path = sys.argv[3]


# 对每个特征值单独进行哈希, 并输出哈希值
def gen_hashed_fm_feats(feats, nr_bins):
    feats = [(field, hashstr(feat, nr_bins)) for (field, feat) in feats]
    feats.sort()
    feats = ['{0}'.format(idx) for (field, idx) in feats]
    return feats


# 出现频率超过10次的特征值集合
frequent_feats = read_frequent_feats(threshold)

writeheader = True
with open(out_path, 'w') as f:
    for row, line_gbdt in zip(DictReader(open(csv_path)), open(gbdt_path)):
        feats = []
        for feat in gen_feats(row):
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            # type=I or C, field=1~39
            if type == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0] + 'less'
            # 生成特征如C1less, C2less
            if type == 'C':
                field += 13
            feats.append((field, feat))

        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i) + ':' + feat))

        # 将结合的特征向量进行哈希
        feats = gen_hashed_fm_feats(feats, nr_bins)
        f.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
