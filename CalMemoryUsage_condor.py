import glob
import sys

mydir=sys.argv[1] 
print "dir=",mydir

loglist=glob.glob(mydir+'/*.log')
print 'N log file=',len(loglist)

MaxMemory=-1
MaxMemoryFile=''
MinMemory=9999999999999.
MinMemoryFile=''
SumMemory=0

for log in loglist:
    f=open(log,'r')
    lines=f.readlines()
    
    for line in lines:
        #22872  -  MemoryUsage of job (MB)
        #166    MemoryUsage of job (MB)
        if 'MemoryUsage of job (MB)' in line:
            ##Execution time: 16.9294 ms/evt
            #print "Find"
            this_memory=line.replace('MemoryUsage of job (MB)','').replace('-','')
            this_memory=float(this_memory)
            
            

    f.close()
    if this_memory>MaxMemory: 
        MaxMemory=this_memory
        MaxMemoryFile=log
    if this_memory<MinMemory:
        MinMemory=this_memory
        MinMemoryFile=log
    SumMemory+=this_memory

    if this_memory > 1000:
        print '[Over1G memory]',log, this_memory,"MB"




print "Avg Memory =", SumMemory/len(loglist),"MB"
print "Max Memory =", MaxMemory, "MB"
print "Max Memory File =", MaxMemoryFile
print "Min Memory =", MinMemory, "MB"
print "Min Memory File =", MinMemoryFile
