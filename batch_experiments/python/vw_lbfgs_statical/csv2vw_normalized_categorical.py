# _*_ coding: utf-8 _*_

from datetime import datetime
from csv import DictReader
import sys, subprocess

NR_THREAD = 8

data_path = sys.argv[1]
save_path = sys.argv[2]

'''
对特征进行标准化处理

数值特征, 大于2的, v < -|_log(v)**2_|, 变为分类特征
分类特征, 出现次数少于10次的转化为特殊值
pre-c

'''

# ---------------------------normalize------------------------------------------

# 增加Label, 全为0
cmd = 'python3.5 add_dummy_label.py {data}test.csv {data}test.tmp.csv'.format(data=data_path)
subprocess.call(cmd, shell=True)
print('dummy label to test.csv added !\n')

# tr.csv原始特征, tr.gbdt.out增强(gbdt)特征
cmd = 'python3.5 parallelizer_normalization2csv.py {nr_thread} {data}train.csv {save}tr.normalized' \
    .format(nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('normalized features added to train dataset\n')

cmd = 'python3.5 parallelizer_normalization2csv.py {nr_thread} {data}test.tmp.csv {save}te.normalized' \
    .format(nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('normalized features added to test dataset\n')

# 删除文件
cmd = 'rm {data}test.tmp.csv'.format(data=data_path)
subprocess.call(cmd, shell=True)

# ---------------------------normalize------------------------------------------

print('gbdt process completed !')

with open(save_path + 'train.vw', 'w') as outfile:
    for t, row in enumerate(DictReader(open(save_path + 'tr.normalized'))):
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

validation = open(data_path + 'validation.csv')
validation.__next__()

with open(save_path + 'test.vw', 'w') as outfile:
    for t, row in enumerate(DictReader(open(save_path + 'te.normalized'))):
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
