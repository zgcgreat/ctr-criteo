# _*_ coding: utf-8 _*_

'''
准备数据：将txt格式转化为csv格式
这里用了小数据dac_sample.txt，只有100000条记录
'''

input = '../../original-data/dac_sample.txt'
file = open('../../original-data/dac_sample.txt')
line = file.readlines()
file.close()
print('file length:', len(line))

output = '../data/data.csv'

count = 0
id = 0

header = 'Id,Label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,' \
         'C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26'

with open(output, 'w') as file:
    file.write(header + '\n')
    for line in open(input, 'r'):
        line = line.replace('\t', ',')
        if (count % 10000 == 0):
            print(count, 'processed !')
        #file.write(str(id) + ',' + line.replace('\n', '\r\n'))
        file.write(str(id) + ',' + line)
        count += 1
        id += 1
file.close()
print(id)
print('dataset prepared !')
