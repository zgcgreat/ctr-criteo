# _*_ coding: utf-8 _*_

import sys
from common import *

nr_thread =sys.argv[1]
nr_thread = int(nr_thread)
cvt_path = sys.argv[2]
src1_path = sys.argv[3]
src2_path = sys.argv[4]
dst_path = sys.argv[5]

# src1 原始特征
split(src1_path, nr_thread, True)
# src2 为gbdt特征
split(src2_path, nr_thread, True)

parallel_convert(cvt_path, [src1_path, src2_path, dst_path], nr_thread)
cat(dst_path, nr_thread)

delete(src1_path, nr_thread)
delete(src2_path, nr_thread)
delete(dst_path, nr_thread)
