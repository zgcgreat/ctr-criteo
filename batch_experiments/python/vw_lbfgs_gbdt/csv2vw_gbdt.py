# _*_ coding: utf-8 _*_

import subprocess
import sys
from csv import DictReader

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

NR_THREAD = 8

data_path = sys.argv[1]
save_path = sys.argv[2]

# -----------------------------gbdt-----------------------------------------

cmd = 'python3.5 add_dummy_label.py {data}test.csv {data}test.tmp.csv'.format(data=data_path)
subprocess.call(cmd, shell=True)
print('dummy label to test.csv added !\n')

cmd = 'python3.5 parallelizer-a.py {nr_thread} pre-a.py {data}train.csv {save}tr.gbdt.dense {save}tr.gbdt.sparse'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('train set to dense and sparse format completed !\n')

cmd = 'python3.5 parallelizer-a.py {nr_thread} pre-a.py {data}test.tmp.csv {save}te.gbdt.dense {save}te.gbdt.sparse' \
    .format(nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('test set to dense and sparse format completed !\n')

# 生成gbdt特征
cmd = './gbdt -t 30 -s {nr_thread} {save}te.gbdt.dense {save}te.gbdt.sparse {save}tr.gbdt.dense {save}tr.gbdt.sparse ' \
      '{save}te.gbdt.out {save}tr.gbdt.out'.format(nr_thread=NR_THREAD, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features generated !\n')

# 删除中间数据文件
#


# tr.csv原始特征, tr.gbdt.out增强(gbdt)特征
cmd = 'python3.5 parallelizer-gbdt.py {nr_thread} {data}train.csv {save}tr.gbdt.out {save}tr.addition' \
    .format(nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features added to train dataset !\n')

cmd = 'python3.5 parallelizer-gbdt.py {nr_thread} {data}test.tmp.csv {save}te.gbdt.out {save}te.addition' \
    .format(nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('gbdt features added to test dataset !\n')

# cmd = 'rm {data}test.tmp.csv'.format(data=data_path)
# subprocess.call(cmd, shell=True)

# -----------------------------gbdt-----------------------------------------

print('gbdt process completed !')

with open(save_path + 'train.vw', 'w') as outfile:
    for t, row in enumerate(DictReader(open(save_path + 'tr.addition'))):
        categorical_features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if len(str(v)) > 0:
                    categorical_features.append('{0}={1}'.format(k, v))

        if row['Label'] == '1':
            label = 1
        else:
            label = -1
        outfile.write('{0} \'{1} |features {2}\n'.format(label, row['Id'],
                                                         ' '.join(['{0}'.format(val) for val in categorical_features])))

validation = open(data_path + 'validation.csv', 'r')
validation.__next__()

with open(save_path + 'test.vw', 'w') as outfile:
    for t, row in enumerate(DictReader(open(save_path + 'te.addition'))):
        categorical_features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if len(str(v)) > 0:
                    categorical_features.append('{0}={1}'.format(k, v))

        if validation.readline().strip().split(',')[1] == '1':
            label = 1
        else:
            label = -1
        outfile.write('{0} \'{1} |features {2}\n'.format(label, row['Id'], ' '.join(
            ['{0}'.format(val) for val in categorical_features])))

validation.close()

# cmd = 'rm {save}tr.gbdt.out {save}te.gbdt.out {save}tr.addition {save}te.addition'.format(save=save_path)
# subprocess.call(cmd, shell=True)
