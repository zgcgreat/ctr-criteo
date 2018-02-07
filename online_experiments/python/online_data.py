# _*_ coding: utf-8 _*_
import time
from csv import DictReader, DictWriter

input = '../data/data.csv'
output = '../data'

# 输出validation.csv
validation = open('{0}/validation.csv'.format(output), 'w')
validation.write('Id,Label\n')
for t, row in enumerate(DictReader(open(input))):
    validation.write('%s, %s\n' % (row['Id'], row['Label']))
    if(t % 10000 == 0):
        print('{0} validation data completed !'.format(t))
validation.close()

# csv to vw 全属性转换, 将所有属性都当做分类属性
with open('{0}/online.vw'.format(output), 'w') as outfile:
    for t, row in enumerate(DictReader(open(input))):
        categorical_features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if len(str(v)) > 0:
                    categorical_features.append('{0}={1} '.format(k, v))

        if row['Label'] == '1':
            label = 1
        else:
            label = -1

        outfile.write('{0} \'{1} |categorical {2}\n'.format(label, row['Id'],
                                    ' '.join(['{0}'.format(val) for val in categorical_features])))
        if (t % 10000 == 0):
            print('{0} vw data completed !'.format(t))

    outfile.close()
print('online data prepared !')

