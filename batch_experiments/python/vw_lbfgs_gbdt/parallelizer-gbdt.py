# _*_ coding: utf-8 _*_

import sys
from common import *

nr_thread = sys.argv[1]
nr_thread = int(nr_thread)
src1_path = sys.argv[2]
src2_path = sys.argv[3]
dst_path = sys.argv[4]


split(src1_path, nr_thread, True)
split(src2_path, nr_thread, True)

# 利用pre-a.py根据tr.csv文件生成tr.gbdt.dense和tr.gbdt.sparse两个文件, (或te.*)
parallel_convert('gbdt2csv.py', [src1_path, src2_path, dst_path], nr_thread)
cat_with_header(dst_path, nr_thread)


delete(src1_path, nr_thread)
delete(src2_path, nr_thread)
delete(dst_path, nr_thread)

