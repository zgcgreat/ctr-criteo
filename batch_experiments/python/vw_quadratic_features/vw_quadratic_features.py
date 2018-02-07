# _*_ coding: utf-8 _*_

import sys
import subprocess

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

data_path = sys.argv[1]
result_path = sys.argv[2]

cmd = 'python3.5 csv2vw_quadratic.py {0} {1} -train'.format(data_path, result_path)
train = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
cmd = 'python3.5 csv2vw_quadratic.py {0} {1} -test'.format(data_path, result_path)
test = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

train.communicate()
cmd = 'vw {path}train.vw -f {path}model -k -b 21 --loss_function logistic -q AB -q AC --l2 25 --holdout_off'.format(
    path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

test.communicate()
cmd = 'vw {path}test.vw -t -i {path}model -p {path}preds.txt --loss_function logistic --invert_hash {path}look'.format(
    path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

cmd = 'python3.5 vw_to_submission.py {path}'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

cmd = 'rm {path}train.vw {path}test.vw'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
