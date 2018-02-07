# _*_ coding: utf-8 _*_

'''
打乱数据集顺序, 这个程序有问题，会产生很大的数据量
'''
import random
import time

start = time.time()

print('shuffling dataset...')

input = open('../data/data.csv', 'r')
output = open('../output/tmp.csv', 'w')

lines = input.readlines()
outlines = []
output.write(lines.pop(0))  # pop()方法, 传递的是待删除元素的index
while lines:
    outlines.append(lines.pop(random.randrange(len(lines))))
    output.write(' '.join(outlines))

input.close()
output.close()

print('dataset shuffled !')

print('Time spent: {0:.2f}s\n\n'.format(time.time() - start))
