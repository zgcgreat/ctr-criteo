# fi1 = open('../../original-data/dac_sample.txt', 'r')
# fi2 = open('../data/data.csv', 'r')
# l1 = fi1.readlines()
# l2 = fi2.readlines()
# print(len(l1))
# print(len(l2))

from csv import DictReader
label_reader = DictReader(open('../output/day2_valid.csv'))
for t, row in enumerate(label_reader):
    print(t, row)
