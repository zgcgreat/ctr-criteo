# _*_ coding: utf-8 _*_

import subprocess
import time
from csv import DictReader
import math
from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

output = '../output/online_lbfgs/'

records = 100000  # 总的记录条数
oneday = 20000  # 一天的记录条数

'''
将数据等分，写入不同文件
'''

TRAIN = ['Id', 'Label', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'C1', 'C2',
         'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
         'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26']
TEST = ['Id', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'C1', 'C2', 'C3',
        'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20',
        'C21', 'C22', 'C23', 'C24', 'C25', 'C26']

'''
将数据划分成训练集, 测试集和验证集, 并转换为vw格式
'''


def day_split():
    last = 0
    train = open('../output/online_lbfgs/day1_train.vw', 'w')
    validation = open('../output/online_lbfgs/day1_valid.csv', 'w')
    validation.write('Id,Label' + '\n')

    for t, row in enumerate(DictReader(open('../data/data.csv'))):
        this = int(t / oneday)
        if last != this:
            print('got! this={0} last={1}'.format(this, last))
            train.close()
            last = this
            train = open('../output/online_lbfgs/day{0}_train.vw'.format(this + 1), 'w')

            validation.close()
            validation = open('../output/online_lbfgs/day{0}_valid.csv'.format(this + 1), 'w')
            validation.write('Id,Label' + '\n')
            print('day{0} completed !'.format(this))

        categorical_features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if len(str(v)) > 0:
                    categorical_features.append('{0}={1} '.format(k, v))

        if row['Label'] == '1':
            label = 1
        else:
            label = -1

        train.write('{0} \'{1} |categorical {2}\n'.format(label, row['Id'],
                                                          ' '.join(
                                                              ['{0}'.format(val) for val in categorical_features])))

        validation.write('{0},{1}\n'.format(row['Id'], row['Label']))


start = time.time()

print('records / oneday:', records / oneday)
print('int(records / oneday):', int(records / oneday))
day_split()
print('it took {0}s to generate vw data !'.format(round(time.time() - start, 2)))

for i in range(int(records / oneday)):
    if i == 0:
        # 训练第一天
        cmd = 'vw {path}day{this}_train.vw -f {path}model{this} --bfgs -c -k --passes 30 -b 20 --quiet ' \
              '--loss_function logistic --l2 17.5 --termination 1e-5 --holdout_off' \
            .format(path=output, this=i + 1)
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    elif i != 0:
        # 检验性能
        cmd = 'vw {path}day{this}_train.vw -t -i {path}model{last} -p {path}pred{this}.txt ' \
              '--loss_function logistic -P 20000'.format(path=output, this=i + 1, last=i)
        print(cmd)
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

        # 不训练最后一天
        if i != (int(records / oneday) - 1):
            print('day{0} completed !'.format(i + 1))
            cmd = 'vw {path}day{this}_train.vw -i {path}model{last} -f {path}model{this} --bfgs -c -k ' \
                  '--passes 30 --quiet --loss_function logistic --l2 17.5 --termination 1e-5 ' \
                  '--holdout_off'.format(path=output, this=i + 1, last=i)
            subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)


#
def sigmod(x):
    return 1 / (1 + math.exp(-x))


result_path = '{0}details.txt'.format(output)
result = open(result_path, 'w')
result.write('online_lbfgs result:\n\n')

for i in range(2, 6):
    with open('../output/online_lbfgs/predict{0}.txt'.format(i), 'w') as outfile:
        outfile.write('Id,Predicted\n')
        for line in open('../output/online_lbfgs/pred{0}.txt'.format(i), 'r'):
            row = line.strip().split(' ')
            pro = sigmod(float(row[0]))
            outfile.write('%s,%f\n' % (row[1], pro))

    label_reader = DictReader(open('../output/online_lbfgs/day{0}_valid.csv'.format(i)))
    predict_reader = DictReader(open('../output/online_lbfgs/predict{0}.txt'.format(i)))
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

    auc = roc_auc_score(y_true, y_scores)
    logloss = log_loss(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print('day{0}:'.format(i))
    print('Accuracy: {0}    Precision: {1}    Recall: {2}    F1-Measure: {3}\n'.format(accuracy, precision, recall, f1))

    result.write('------------------------------------------------------------\n\n')
    result.write('day{0}:\n\n'.format(i))
    result.write(
        'Accuracy: {0}\n\nPrecision: {1}\n\nRecall: {2}\n\nF1-Measure: {3}\n\n'.format(accuracy, precision, recall, f1))
    result.write('logloss: {0}\n\nauc: {1}\n\n'.format(logloss, auc))
    result.write('------------------------------------------------------------\n\n')

result.close()
