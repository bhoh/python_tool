import glob
import sys

mydir=sys.argv[1] 
print "dir=",mydir

outlist=glob.glob(mydir+'/*.out')
print 'N out file=',len(outlist)

SumTime=0
Nvalid=0
for out in outlist:
    f=open(out,'r')
    lines=f.readlines()
    isValid=False
    for line in lines:
        if 'Execution time' in line:
            ##Execution time: 16.9294 ms/evt
            #print "Find"
            this_time=line.replace('Execution time:','').replace('ms/evt','')
            SumTime+=float(this_time)
            isValid=True
            break
    if isValid:
        Nvalid+=1
    f.close()

print "Avg Execution =", SumTime/Nvalid,'ms/evt'
