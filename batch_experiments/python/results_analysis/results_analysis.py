# _*_ coding: utf-8 _*_

import os
import matplotlib.pyplot as plt
from csv import DictReader

results_path = '../../output/results/batch/'

methods = []
accuracy = []
precision = []
recall = []
f1 = []
logloss = []
auc = []

for i in range(0, len(os.listdir(results_path))):
    dir_name = os.listdir(results_path)[i]
    methods.append(dir_name)
    for t, row in enumerate(DictReader(open(results_path + '{0}/{0}-avgresult.csv'.format(dir_name), 'r'))):
        accuracy.append(row['Accuracy'])
        precision.append(row['Precision'])
        recall.append(row['Recall'])
        f1.append(row['F1-Measure'])
        logloss.append(row['Logloss'])
        auc.append(row['AUC'])

result = open('result.xls', 'w')
result.write('experiments,accuracy,precision,recall,f1-measure,logloss,auc\n')
for i in range(len(methods)):
    result.write(methods[i] + ',' + str(accuracy[i]) + ',' + str(precision[i]) + ',' + str(recall[i]) + ',' + str(
        f1[i]) + ',' + str(logloss[i]) + ',' + str(auc[i]) + '\n')

arg = ['accuracy', 'precision', 'recall', 'f1-measure', 'logloss', 'auc']
args = [accuracy, precision, recall, f1, logloss, auc]
for i in range(len(args)):
    fig, ax = plt.subplots()
    plt.plot(args[i])
    plt.title('{0} of algorithms'.format(arg[i]))
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation='vertical')
    plt.savefig('{0} of algorithms'.format(arg[i]))
    plt.show()
