# _*_ coding: utf-8 _*_

import sys
from common import *

nr_thread = int(sys.argv[1])
data_path = sys.argv[2]
save_path = sys.argv[3]

split(data_path, nr_thread, True)
parallel_convert('normalized2csv.py', [data_path, save_path], nr_thread)
cat_with_header(save_path, nr_thread)

delete(data_path, nr_thread)

delete(save_path, nr_thread)

