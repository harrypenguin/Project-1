import sys
import subprocess
p = subprocess.getoutput("{} ./adventure.py < gameplay1.txt".format(sys.executable))
print(p)
