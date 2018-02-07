# _*_ coding: utf-8 _*_

import sys
from common import *

nr_thread = sys.argv[1]
nr_thread = int(nr_thread)
cvt_path = sys.argv[2]
src_path = sys.argv[3]
dst1_path = sys.argv[4]
dst2_path = sys.argv[5]

split(src_path, nr_thread, True)

# 利用pre-a.py根据tr.csv生成tr.gbdt.dense和tr,gbdt.sparse两个文件,(或te.*)
parallel_convert(cvt_path, [src_path, dst1_path, dst2_path], nr_thread)

cat(dst1_path, nr_thread)
cat(dst2_path, nr_thread)
delete(src_path, nr_thread)
delete(dst1_path, nr_thread)
delete(dst2_path, nr_thread)
