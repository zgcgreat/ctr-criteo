# _*_ coding: utf-8 _*_


import sys
from csv import DictReader

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

data_path = sys.argv[1]
result_path = sys.argv[2]



label_path = data_path + 'validation.csv'
predict_path = result_path + 'submission.csv'

label_reader = DictReader(open(label_path))
predict_reader = DictReader(open(predict_path))

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

print('Accuracy: {0}    Precision: {1}    Recall: {2}    F1-Measure: {3}\n'.format(accuracy, precision, recall, f1))
print('logloss: {0}  auc: {1}\n'.format(logloss, auc))

result = open(result_path + 'details.txt', 'w')
result.write('------------------------------------------------------------\n\n')
result.write('Total instances: {count}\n\n\nValidation File: {vafile}\n\nPrediction file: {prefile}\n\n'
             .format(count=count, vafile=label_path, prefile=predict_path))
result.write(
    'Accuracy: {0}\n\nPrecision: {1}\n\nRecall: {2}\n\nF1-Measure: {3}\n\n'.format(accuracy, precision, recall, f1))
result.write('logloss: {0}\n\nauc: {1}\n\n'.format(logloss, auc))
result.write('-------------------------------------------------------------\n\n')
result.close()

# 将结果写入表格
statistics = open(result_path + 'result.csv', 'w')
statistics.writelines('Accuracy,Precision,Recall,F1-Measure,Logloss,AUC\n')
statistics.writelines('{0},{1},{2},{3},{4},{5}'.format(accuracy, precision, recall, f1, logloss, auc))
statistics.close()
