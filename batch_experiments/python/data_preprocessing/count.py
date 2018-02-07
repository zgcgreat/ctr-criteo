# _*_ coding: utf-8 _*_

import argparse, csv, sys, collections
from common import *
import time

# 创建一个默认字典
counts = collections.defaultdict(lambda: [0, 0, 0])

for i, row in enumerate(csv.DictReader(open('../data/data.csv')), start=1):
    label = row['Label']
    for j in range(1, 27):
        field = 'C{0}'.format(j)
        value = row[field]
        if label == '0':
            counts[field + ',' + value][0] += 1
        else:
            counts[field + ',' + value][1] += 1
        counts[field + ',' + value][2] += 1
    if (i % 1000000 == 0):
        print('{0}m\n'.format(int(i / 1000000)))

print(counts)

output = open('../output/fc.trav.t10.txt', 'w')
output.write('Field,Value,Neg,Pos,Total,Ratio\n')

for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
    if total < 10:
        continue
    ratio = round(float(pos) / total, 5)
    # print(key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio))
    output.write(key + ',' + str(neg) + ',' + str(pos) + ',' + str(total) + ',' + str(ratio) + '\n')
