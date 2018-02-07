# _*_ coding: utf-8 _*_

'''
交叉验证划分
'''

import os
import subprocess

FOLD = 10
src = '../data/data.csv'

rootdir = '../output/cross_validation_split/'
if os.path.exists(rootdir):
    pass
else:
    os.makedirs(rootdir)

workers = []

# 并行运行

for i in range(FOLD):
    cmd = 'python split_worker.py {src_file} {dest_path} {fold} {id}'.format(src_file=src, dest_path=rootdir + 'split_{id}/'
                                                                        .format(id=i), fold=FOLD, id=i)
    worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    workers.append(worker)

for worker in workers:
    print(worker.communicate())

