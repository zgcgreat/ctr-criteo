# _*_ coding: utf-8 _*_

import os
import shutil
import subprocess
from csv import DictReader

'''
交叉验证
'''

solution = 'ffm_gbdt.py'
FOLD = 10

data_path = '../../output/cross_validation_split/'
results_path = '../../output/results/batch/' + solution.split('.')[0] + '/'


# 先删除已存在的结果文件目录, 这样增加FOLD不会有问题
if os.path.exists(results_path):
    shutil.rmtree(results_path)
# 建立目录
if not os.path.exists(results_path):
    for i in range(FOLD):
        os.makedirs(results_path + 'split_{0}/'.format(i))

# 测试
for i in range(FOLD):
    print('running ' + solution + ', round: ' + str(i))
    cmd = 'python3.5 {solution} {data} {results}'.format(solution=solution, data=data_path + 'split_{0}/'
                                                         .format(i), results=results_path + 'split_{0}/'.format(i))
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

    # 计算性能评价指标
    cmd = 'python3.5 evaluate.py {data} {result}'.format(data=data_path + 'split_{0}/'.format(i),
                                                         result=results_path + 'split_{0}/'.format(i))
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)


# 分析结果汇总输出

accuracy = 0
precision = 0
recall = 0
f1_measure = 0
logloss = 0
auc = 0

for i in range(FOLD):
    for t, row in enumerate(DictReader(open(results_path + 'split_{0}/result.csv'.format(i)))):
        accuracy += float(row['Accuracy'])
        precision += float(row['Precision'])
        recall += float(row['Recall'])
        f1_measure += float(row['F1-Measure'])
        logloss += float(row['Logloss'])
        auc += float(row['AUC'])

accuracy /= FOLD
precision /= FOLD
recall /= FOLD
f1_measure /= FOLD
logloss /= FOLD
auc /= FOLD

avgresult = open(results_path + '{0}-avgresult.csv'.format(solution.split('.')[0]), 'w')
avgresult.write('Accuracy,Precision,Recall,F1-Measure,Logloss,AUC\n')
avgresult.writelines('{0},{1},{2},{3},{4},{5}'.format(accuracy, precision, recall, f1_measure, logloss, auc))
