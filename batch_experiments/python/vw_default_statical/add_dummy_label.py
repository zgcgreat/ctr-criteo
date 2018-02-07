# _*_ coding: utf-8 _*_

import csv
import sys

'''
插入Label， 并全部为0
'''

csv_path = sys.argv[1]
out_path = sys.argv[2]

f = csv.writer(open(out_path, 'w'))
for i, row in enumerate(csv.reader(open(csv_path))):
    if i == 0:
        row.insert(1, 'Label')
    else:
        row.insert(1, '0')
    f.writerow(row)
