# _*_ coding: utf-8 _*_

import subprocess
import sys

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

data_path = sys.argv[1]
save_path = sys.argv[2]

NR_THREAD = 8

# -----------------------------------gbdt--------------------------------------------

cmd = 'python3.5 add_dummy_label.py {data}test.csv {data}test.tmp.csv'.format(data=data_path)
subprocess.call(cmd, shell=True)
print('dummy label to test.csv added !\n')

cmd = 'python3.5 parallelizer-a.py {nr_thread} pre-a.py {data}train.csv {save}tr.gbdt.dense {save}tr.gbdt.sparse'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('train set to dense and sparse format completed !\n')

cmd = 'python3.5 parallelizer-a.py {nr_thread} pre-a.py {data}test.tmp.csv {save}te.gbdt.dense {save}te.gbdt.sparse'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('test set to dense and sparse format completed !\n')

cmd = './gbdt -t 30 -s {nr_thread} {save}te.gbdt.dense {save}te.gbdt.sparse {save}tr.gbdt.dense {save}tr.gbdt.sparse ' \
      '{save}te.gbdt.out {save}tr.gbdt.out'.format(nr_thread=NR_THREAD, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features generated !\n')

cmd = 'rm -f {path}te.gbdt.dense {path}te.gbdt.sparse {path}tr.gbdt.dense {path}tr.gbdt.sparse'.format(path=save_path)
subprocess.call(cmd, shell=True)

# tr.csv 原始特征, tr.gbdt.out 增强(gbdt)特征
cmd = 'python3.5 parallelizer-b.py {nr_thread} pre-b.py {data}train.csv {save}tr.gbdt.out {save}tr.ffm'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features added to train dataSet !\n')

cmd = 'python3.5 parallelizer-b.py {nr_thread} pre-b.py {data}test.tmp.csv {save}te.gbdt.out {save}te.ffm'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features added to test dataSet !\n')

# -----------------------------------gbdt--------------------------------------------

print('gbdt process completed !\n')

# train & test
cmd = './ffm -k 4 -t 11 -s {nr_thread} {save}te.ffm {save}tr.ffm'.format(nr_thread=NR_THREAD, save=save_path)
subprocess.call(cmd, shell=True)

with open(save_path + 'submission.csv', 'w') as f:
    f.write('Id,Predicted\n')
    for i, row in enumerate(open(save_path + 'te.ffm.out')):
        f.write('{0},{1}'.format(i, row))

# 删除中间文件
cmd = 'rm -f {data}test.tmp.csv {save}tr.gbdt.out {save}te.gbdt.out {save}tr.ffm {save}te.ffm {save}te.ffm.out'.format(
    data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
