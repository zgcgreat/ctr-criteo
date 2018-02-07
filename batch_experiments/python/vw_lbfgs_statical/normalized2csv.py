# _*_ coding: utf-8 _*_

import sys
import argparse
from common import *

# csv_path = sys.argv[1]
# out_path = sys.argv[2]

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()

parser.add_argument('csv_path', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())


threshold = 10

# 不包含gbdt特征, 只利用其数值分箱, 频繁类别筛选

# 出现频率超过10次的特征集合
frequent_feats = read_frequent_feats(threshold)

header = True
with open(args['out_path'], 'w') as f:
    for t, row in enumerate(csv.DictReader(open(args['csv_path']))):
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

        if (header == True):
            f.write('Label,Id,' + ','.join(['{0}'.format(feat.split('-')[0]) for (field, feat) in feats]) + '\n')
            header = False

        f.write(row['Label'] + ',' + row['Id'] + ',' + ','.join(
            ['{0}'.format(feat.split('-')[1]) for (field, feat) in feats]) + '\n')
