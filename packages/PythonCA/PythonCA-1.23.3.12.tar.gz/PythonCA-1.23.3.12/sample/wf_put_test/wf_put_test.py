#!python3
from __future__ import print_function

import sys
if sys.version_info > (3,0):
    sys.path.insert(0,"/home/yamamoto/WORK/wf_put_test/PythonCA-1.23.2.2.2/build/lib.linux-x86_64-3.6")
else:
    sys.path.insert(0,"/home/yamamoto/WORK/wf_put_test/PythonCA-1.23.2.2.2/build/lib.linux-x86_64-2.7")

import ca
import random, sys, resource, gc
chname="noboru:TestWF"
print(ca.__file__)

nelm=ca.Get("{chname}.NELM".format(chname=chname), Type=ca.DBF_LONG)
print(nelm)
ch=ca.channel(chname)
ch.wait_conn()
count=0
while True:
    data=[random.gauss(0,1) for i in range(nelm)]
    try:
        ch.put(*data)
        if (count % 1000) == 0:
            print("count:",count)
            print(resource.getrusage(resource.RUSAGE_SELF))
            #print(gc.get_stats())
        elif (count % 500) == 0:
            print (" .",end="")
        elif (count % 100) == 0:
            print (".",end="")
        sys.stdout.flush()
        ch.pend_event(0.05)
        count +=1
    except KeyboardInterrupt:
        sys.exit()
        
