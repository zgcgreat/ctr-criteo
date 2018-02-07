# _*_ coding: utf-8 _*_

import subprocess
import sys

data_path = sys.argv[1]
result_path = sys.argv[2]

cmd = 'python3.5 csv2vw_normalized_categorical.py {0} {1}'.format(data_path, result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

# 训练
cmd = 'vw {path}train.vw -f {path}model --bfgs -c -k --passes 25 -b 20 --quiet --loss_function logistic --l2 25 ' \
      '--termination 1e-5 --holdout_off'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

# 测试
cmd = 'vw {path}test.vw -t -i {path}model -p {path}preds.txt --quiet --loss_function logistic'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

# 删除中间数据文件
cmd = 'rm {path}train.vw {path}test.vw {path}train.vw.cache'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

# 转换格式
cmd = 'python3.5 vw_to_submission.py {path}'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
