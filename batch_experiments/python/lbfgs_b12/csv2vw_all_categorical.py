# _*_ coding: utf-8 _*_
from csv import DictReader
import sys

data_path = sys.argv[1]
save_path = sys.argv[2]
type = sys.argv[3]

if (type != '-train' and type != '-test'):
    print('wrong arg')
    exit(1)

if(type == '-train'):
    input = data_path + 'train.csv'
    output = save_path + 'train.vw'
else:
    input = data_path + 'test.csv'
    output = save_path + 'test.vw'
    validation = open(data_path + 'validation.csv')

with open(output, 'w') as outfile:
    for t, row in enumerate(DictReader(open(input))):
        categorical_features = []
        for k, v in row.items():
            if k not in ['Id', 'Label']:
                if len(str(v)) > 0:
                    categorical_features.append('{0}={1}'.format(k, v))

        if (type == '-train'):
            if row['Label'] == '1':
                label = 1
            else:
                label = -1

        else:
            if validation.readline().strip().split(',')[1] == '1':
                label = 1
            else:
                label = -1

        outfile.write('{0} \'{1} |categorical {2}\n'.format(label, row['Id'], ' '.join(['{0}'
                                                                                       .format(val) for val in
                                                                                        categorical_features])))
if (type == '-test'):
    validation.close()
