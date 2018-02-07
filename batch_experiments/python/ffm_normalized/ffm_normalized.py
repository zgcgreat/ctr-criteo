# _*_ coding: utf-8 _*_

import subprocess
import sys

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

NR_THREAD = 8

data_path = sys.argv[1]
save_path = sys.argv[2]

'''
对特征进行标准化处理

数值属性, 大于2的, v < -|_log(v)**2_|, 变为分类属性
分类属性, 出现次数少于10的转为特殊值
pre-c
'''

# -------------------------------normalize---------------------------------------

cmd = 'python3.5 add_dummy_label.py {data}test.csv {data}test.tmp.csv'.format(data=data_path)
subprocess.call(cmd, shell=True)
print('dummy label to test.csv added! \n')

# tr.csv原始特征, tr.gbdt.out增强(gbdt)特征
cmd = 'python3.5 parallelizer-normalization2ffm.py {nr_thread} {data}train.csv {save}tr.ffm'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)

cmd = 'python3.5 parallelizer-normalization2ffm.py {nr_thread} {data}test.tmp.csv {save}te.ffm'.format(
    nr_thread=NR_THREAD, data=data_path, save=save_path)
subprocess.call(cmd, shell=True)
print('normalized features added to train dataSet!\n')

# -------------------------------normalize---------------------------------------

print('gbdt process completed !\n')

# 训练并预测，输出文件 te.ffm.out
cmd = './ffm -k 4 -t 11 -s {nr_thread} {save}te.ffm {save}tr.ffm'.format(nr_thread=NR_THREAD, save=save_path)
subprocess.call(cmd, shell=True)

# # 训练
# cmd = './ffm-train -k 4 -t 11 -s {nr_thread} -p {save}te.ffm {save}tr.ffm model'.format(nr_thread=NR_THREAD,
#                                                                                       save=save_path)
# subprocess.call(cmd, shell=True)
# # 预测
# cmd = './ffm-predict {save}te.ffm model {save}te.out'.format(save=save_path)
# subprocess.call(cmd, shell=True)

with open(save_path + 'submission.csv', 'w') as f:
    f.write('Id,Predicted\n')
    for i, row in enumerate(open(save_path + 'te.ffm.out')):
        f.write('{0},{1}'.format(i, row))

# 删除中间文件
# cmd = 'rm {data}test.tmp.csv {save}tr.ffm {save}te.ffm {save}te.ffm.out'.format(data=data_path, save=save_path)
# subprocess.call(cmd, shell=True)

