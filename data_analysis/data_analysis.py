# _*_ coding: utf-8 _*_


clks = 0
file = open('../original-data/data.csv', 'r')
next(file)
for line in file:
    s = line.split(',')
    clk = int(s[1])
    clks += clk
file.close()
print(clks)
