# _*_ coding: utf-8 _*_

import subprocess
import sys
from datetime import datetime


print('Start the batch experiments !')

# start = datetime.now()
# cmd = 'ffm_gbdt/cross_validator.py'
# subprocess.call(cmd, shell=True, stdout=sys.stdout)
# end = datetime.now()
# print('Time spent {0:.2f}'.format(end - start))

start = datetime.now()
cmd = 'python3.5 ffm_normalized/cross_validator.py'
subprocess.call(cmd, shell=True, stdout=sys.stdout)
end = datetime.now()
print('Time spent {0}'.format(end - start))
