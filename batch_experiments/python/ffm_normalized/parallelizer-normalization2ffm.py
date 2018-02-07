# _*_ coding: utf-8 _*_

import sys
from common import *

nr_thread = sys.argv[1]
nr_thread = int(nr_thread)
src_path = sys.argv[2]
dst_path = sys.argv[3]

split(src_path, nr_thread, True)

parallel_convert('normalized2ffm.py', [src_path, dst_path], nr_thread)
cat(dst_path, nr_thread)

delete(src_path, nr_thread)
delete(dst_path, nr_thread)

