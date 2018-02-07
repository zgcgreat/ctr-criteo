# _*_ coding: utf-8 _*_

import math
import os
import subprocess
import time
from csv import DictReader

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

# 开始计时
start = time.time()

output = '../output/vw_ftrl'

# 创建输出文件夹, 第一次运行取消注释, 以后注释掉
# os.makedirs(output)
if os.path.exists(output):
    pass
else:
    os.makedirs(output)


# 1. 训练并预测结果
cmd = 'vw ../data/online.vw -p {path}/preds.txt -P 20000 --ftrl --loss_function logistic'.format(path=output)
subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

# 2. 转换格式
submission = '{0}/submission.csv'.format(output)
preds = '{0}/preds.txt'.format(output)

def sigmod(x):
    return 1 / (1 + math.exp(-x))

with open(submission, 'w') as outfile:
    outfile.write('Id,Predicted\n')
    for line in open(preds):
        row = line.strip().split(' ')
        pro = sigmod(float(row[0]))
        outfile.write('%s,%s\n' % (row[1], pro))


# 3. 验证结果
validation = '../data/validation.csv'
result_path = '{0}/details.txt'.format(output)

label_reader = DictReader(open(validation))
predict_reader = DictReader(open(submission))

count = 0
y_true = []
y_pred = []
y_scores = []
for t, row in enumerate(label_reader):
    predict = predict_reader.__next__()
    actual = float(row['Label'])
    predicted = float(predict['Predicted'])

    y_true.append(actual)
    y_scores.append(predicted)

    # 大于阈值的即视为点击
    if (predicted >= 0.5):
        y_pred.append(1)
    else:
        y_pred.append(0)

    count += 1

# 计算性能指标
auc = roc_auc_score(y_true, y_scores)
logloss = log_loss(y_true, y_pred)
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# 结束计时
end = time.time()


print('Accuracy: {0}    Precision: {1}    Recall: {2}    F1-Measure: {3}\n'.format(accuracy, precision, recall, f1))
print('logloss: {0}  auc: {1}\n'.format(logloss, auc))
print('Time spent: {0:.2f}s'.format(end - start))

result = open(result_path, 'w')
result.write('vw_ftrl result:\n\n')
result.write('------------------------------------------------------------\n\n')
result.write('Total instances: {count}\n\nTrain and Test File: {ttfile}\n\nValidation File: {vafile}\n\nPrediction '
             'file: {prefile}\n\n'.format(count=count, ttfile='../data/online.vw', vafile=validation, prefile=submission))
result.write('Accuracy: {0}\n\nPrecision: {1}\n\nRecall: {2}\n\nF1-Measure: {3}\n\n'.format(accuracy, precision, recall, f1))
result.write('logloss: {0}\n\nauc: {1}\n\n'.format(logloss, auc))
result.write('------------------------------------------------------------\n\n')
result.write('Time spent: {0:.2f}s\n\n'.format(end - start))
result.close()



