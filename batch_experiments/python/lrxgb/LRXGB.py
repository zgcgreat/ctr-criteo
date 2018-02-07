# _*_ coding: utf-8 _*_

import sys
import subprocess
import xgboost as xgb

if len(sys.argv) != 3:
    print('wrong arg')
    exit(1)

data_path = sys.argv[1]
result_path = sys.argv[2]

cmd = 'python3.5 csv2xgboost_onehotencoding.py {0} {1}'.format(data_path, result_path)
subprocess.call(cmd, shell=True, stdout=sys.stdout)

train_data = xgb.DMatrix(result_path + 'train.sparse')
test_data = xgb.DMatrix(result_path + 'test.sparse')

param = {'silent': 1, 'objective': 'binary:logistic', 'booster': 'gblinear', 'lambda': 25, 'eval_metric': 'logloss'}

param['nthread'] = 8
plst = param.items()
evallist = [(train_data, 'train')]

num_round = 25

bst = xgb.train(plst, train_data, num_round, evallist)

bst.dump_model(result_path + 'dump.raw.txt')

y_pred = bst.predict(test_data)

output = open(result_path + 'submission.csv', 'w')
output.write('Id,Predicted\n')
for p in y_pred:
    output.write('{0},{1}\n'.format('anything', p))

output.close()

cmd = 'rm {path}train.sparse {path}test.sparse'.format(path=result_path)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

print(y_pred)
