# _*_ coding: utf-8 _*_

'''
交叉验证划分
'''

import os, random
import sys
from csv import DictReader, DictWriter

# 待分割源文件, 存放目录, 折数
input, output_path, FOLD, id = sys.argv[1:]
FOLD = int(FOLD)
'''
input = '../data/data.csv'
output_path = '../output/k-fold_loop_split'
FOLD = 10
'''

# 创建输出文件夹
print('mkdirs ' + output_path)
if os.path.exists(output_path):
    pass
else:
    os.makedirs(output_path)


# 输出True or False
def isTest():
    return random.randint(0, FOLD - 1) == 0




FILED_train = ['Id', 'Label', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'C1',
               'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
               'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26']

FILED_test = ['Id', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'C1',
              'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
              'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26']

writer_train = DictWriter(open(output_path + '/train.csv', 'w'), fieldnames=FILED_train)
writer_train.writeheader()
writer_test = DictWriter(open(output_path + '/test.csv', 'w'), fieldnames=FILED_test)
writer_test.writeheader()
writer_validation = open(output_path + '/validation.csv', 'w')
writer_validation.write('Id,Label\n')

for t, row in enumerate(DictReader(open(input))):
    if (isTest() == False):
        writer_train.writerow(row)
    else:
        writer_validation.write('%s,%s\n' % (row['Id'], row['Label']))
        del row['Label']
        writer_test.writerow(row)

    if((t+1) % 50000 == 0):
        print(str(t+1) + ' completed !')

print('Worker{id} finished !'.format(id=id))


