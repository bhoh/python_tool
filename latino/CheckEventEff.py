import ROOT
import os
def MakeYield(conf):
    ##--Load configuration
    #filepath=conf['filepath']
    #lumi=conf['lumi']
    #vname=conf['vname']
    #process=conf['process']
    #runmode=conf['runmode']
    for k in conf:
        exec(k+"=conf['"+k+"']")
        
    myfile=ROOT.TFile.Open(filepath,"READ")
    histopath="/".join([cutname,vname,'histo_'+process])
    print histopath
    myhisto=myfile.Get(histopath)
    nEvent=myhisto.Integral()
    print "nEvent=",nEvent
    myfile.Close()


    f=open(dirpath+'/Integral.txt','w')
    f.write(str(nEvent))
    f.close()
    return nEvent

def MakeEff(conf):
    for k in conf:
        exec(k+"=conf['"+k+"']")
        
    ##read yield
    f=open(dirpath+'/Integral.txt','r')
    lines=f.readlines()
    
    nEvent=float(lines[0])

    f.close()

    nGenEvent=float(lumi)*float(xsec)*1000
    

    Eff=nEvent/nGenEvent
    print Eff
    f=open(dirpath+'/Efficiency.txt','w')
    f.write(str(Eff))

    return Eff
def MakeStoB_DirBase(sdirs,bdirs,savedir): ##signal dir bkg dir
    sdirlist=sdirs.split(',')
    bdirlist=bdirs.split(',')

    NSIG=0.
    NBKG=0.
    for sdir in sdirlist:
        f=open(sdir+'/Integral.txt','r')
        lines=f.readlines()
        N=float(lines[0])
        f.close()
        NSIG+=N
    for bdir in bdirlist:
        f=open(bdir+'/Integral.txt','r')
        lines=f.readlines()
        N=float(lines[0])        
        f.close()
        NBKG+=N

    StoB=NSIG/NBKG
    os.system('mkdir -p '+savedir)
    f=open(savedir+'/StoB.txt','w')
    f.write(str(StoB))
    f.close()
    print "---",savedir,'---'
    print StoB
    return StoB

if __name__ == '__main__':


    
    import optparse
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option("-f", "--filepath", dest="filepath" , help="histogram path")
    parser.add_option("-l", "--lumi",   dest="lumi", help="target lumi")
    parser.add_option("-v", "--vname",   dest="vname", help="variable name eg. Event")
    parser.add_option("-p", "--process",   dest="process", help="process name, eg. top")
    parser.add_option("-r", "--runmode",   dest="runmode", help="runmode")
    parser.add_option("-c", "--cutname",   dest="cutname", help="cutname")
    parser.add_option("-x", "--xsec",   dest="xsec", help="xsec")
    parser.add_option("-a", "--alias",   dest="alias", help="alias")
    
    (options, args) = parser.parse_args()
    #args=parser.parse_args()
    filepath=options.filepath
    lumi=options.lumi
    vname=options.vname
    process=options.process
    runmode=options.runmode
    cutname=options.cutname
    xsec=options.xsec
    alias=options.alias
    #filepath="rootFile_2016_SigBkgEfficiency_Boosted_HMFull_V11_cprime1.0BRnew0.0_DeepAK8WP2p5_dMchi2Resolution_SR/hadd.root"
    #lumi=35.9*1000 ##in /pb (1 fb = 0.0001 pb, 1 fb-1 = 1000pb-1)
    #nGenEvent=(6.296492010211201e-06)*lumi
    #myfile=ROOT.TFile.Open(filepath,"READ")
    #___Boosted__SR__METOver40__PtOverM04______
    #cutname="___Boosted__SR__METOver40__PtOverM04______"
    #vname="Event"
    #process="ggHWWlnuqq_M3000_S"
    

    dirpath='EventEfficiency/'+alias+'/Yield/'+process+'/'+cutname
    os.system('mkdir -p '+dirpath)
    conf={
        'filepath':filepath,
        'lumi':lumi,
        'vname':vname,
        'process':process,
        'cutname':cutname,
        'runmode':runmode,
        'dirpath':dirpath,
        'xsec':xsec,
        'alias':alias
    }
    if runmode=='yield':
        MakeYield(conf)
    
    if MakeEff=='efficiency':
        MakeEff(conf)

    #histopath="/".join([cutname,vname,'histo_'+process])
    #print histopath
    #myhisto=myfile.Get(histopath)
    #nEvent=myhisto.Integral()
   
    #eff=float(nEvent)/float(nGenEvent)
    #print eff
