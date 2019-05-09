import os
import commands



####### Setting #########
##---Which list to check---##
inputfile='Summer16_102X_nAODv4.py'
#inputfile='fall17_102X_nAODv4.py'
#inputfile='Autumn18_102X_nAODv4_v16.py'


##---campaign string in DAS datasetname
campaign='RunIISummer16NanoAODv4'
#campaign='RunIIFall17NanoAODv4'
#campaign='RunIIAutumn18NanoAODv4'
#######End of Setting###########

print "@@"+inputfile+"@@"

f=open(inputfile,'r')
lines=f.readlines()


##updated sample list(dic) 
Samples={}

##line in nAODv4 list python commented out. 
commented_lines=[]
##For ambigious case.
by_hand_list=[]

##--Collect commented lines--##
for line in lines:
    line_nospace=line.replace(" ","")
    #print line_nospace
    ###check unfinished samples###
    if "#Samples" in line_nospace:
        
        #print "+++commented"
        commented_lines.append(line)
        #line=line.replace('#','')
        ##---find 'samples' definition part of this line ---##

        for part in line_nospace.split("#"): 
            if part.startswith('Samples'):
                exec(part) ##define Samples dic 
            else : continue

f.close()
#print "@@key list@@"
#for key in Samples:
#    print key

fnew=open(inputfile+"_new.py",'w') ## new file for updated list -> check commented samples and fill datasetname if production is completed.
for line in lines:
    line_nospace=line.replace(" ","")
    ##Already has datasetname##
    if not "#Samples" in line_nospace:
        fnew.write(line)
        continue
    ###Private samples -> NOT in DAS###
    if 'private' in line.lower():
        fnew.write(line)
        continue
    if 'srmPrefix' in line:
        fnew.write(line)
        continue


    ##scan all unfinished sample and check whetehr this line corresponds to the sample 
    for key in Samples:
        if len(key.replace(' ',''))==0: continue
        if (not "#Samples['"+key+"']" in line_nospace) and (not '#Samples["'+key+'"]' in line_nospace) : continue
        full_datasetname=Samples[key]
        #print full_datasetname['nanoAOD']
        

        ###---Search samples with keyword -> old datasetname/Sample alias/
        datasetname_list=[full_datasetname['nanoAOD'].split('/')[1],  key]
        if 'HZJ_H' in key and 'tautau' in key: datasetname_list.append( key.replace('HZJ_H','ZH')  )
        elif 'HWminusJ_H' in key and 'tautau' in key: datasetname_list.append( key.replace('HWminusJ_H','WminusH')  )
        elif 'HWplusJ_H' in key and 'tautau' in key: datasetname_list.append( key.replace('HWplusJ_H','WplusH')  )
    
        ##To scan all jhugen version## --> remove jhugen version and search
        datasetname_list_noV=[]
        for datasetname in datasetname_list:
            
            name_temp=[]
            for part in datasetname.split('_'): ## <process>_<jhugen>_<mass> :
                if 'jhugen' in part.lower():
                    continue
                if 'M' in part: ##Mass -> search with *M400_*. if using M400, M4000 can be included
                    part=part+"_"
                name_temp.append(part)
            keyword='*'.join(name_temp)
            datasetname_list_noV.append(keyword)##for example ) GluGluHTo2L2Nu*M400
            #print "keyword="+keyword
        datasetname_list=datasetname_list+datasetname_list_noV
        output_list=[]
        for datasetname in datasetname_list:
            ##check das output
            search_phr=datasetname+"*/*"+campaign+"*/NANOAODSIM"
            #For example : 
            #dasgoclient -query="dataset=/GGJets*/*Fall17*/MINI*"
            #print "####Checking-->>>"+datasetname
            dascheck='dasgoclient -query="dataset=/'+search_phr+'"'
            #print dascheck
            #--get das output list
            status, output = commands.getstatusoutput(dascheck)
            if not '/' in output: ## if no output -> searching with next keyword
                continue
            output_list=output_list+output.split('\n')
        output_list=list(set(output_list)) ##removing duplicates
        nsample=len(output_list)
        #print "nsample="+str(nsample)
        if nsample==0: continue
                        
        
        if nsample==1: ## only one corresponding sample
            
            if 'jhugen' in key.lower():
                print key+" updated :) --> !!jhugen version is in latino sample alias...checking..."

                msg_vjhugen_change=''

                vjhugen_das=''
                
                for part in output_list[0].split('_'):
                    if 'jhugen' in part.lower() : 
                        #print '->datasetname in DAS='+part 
                        vjhugen_das=part.lower().replace('jhugen','').replace('v','')
                
                vjhugen_alias=''
                for part in key.split('_'):
                    if 'jhugen' in part.lower() :
                    #print '->datasetname in latino alias='+part
                        vjhugen_alias=part.lower().replace('jhugen','').replace('v','')
                
                if vjhugen_das!=vjhugen_alias :
                    print "!!!!!!!!!Version is not matched. Alias should be fixed!!!.."+vjhugen_alias+"->"+vjhugen_das
                    new_key=[]
                    for part in key.split('_'):
                        if 'jhugen' in part.lower() :
                            part=part.replace(vjhugen_alias,vjhugen_das)
                        new_key.append(part)
                    key='_'.join(new_key)
                    msg_vjhugen_change='vjhugen is changed :'+vjhugen_alias+"->"+vjhugen_das
                else :
                    print '->OK'

                towrite="Samples['"+key+"'] = {'nanoAOD' :'"+output_list[0]+"'} ####Updated! ->"+msg_vjhugen_change
                

            else:
                print key+" updated :)"
                #Format#example#
                #Samples['WgStarLNuEE'] = {'nanoAOD' :'/WGstarToLNuEE_012Jets_13TeV-madgraph/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM'}
                towrite="Samples['"+key+"'] = {'nanoAOD' :'"+output_list[0]+"'} ####Updated! \n"
                fnew.write(towrite)



        elif nsample>1:
            #print "!!!You should choose one of the sample and add it to new sample list python by hand"
            #print "##"+key
            by_hand_list.append("##-----------"+key+" is updated##")
            #print output
            for output_i in output_list:
                towrite="Samples['"+key+"'] = {'nanoAOD' :'"+output_i+"'}"
                by_hand_list.append(towrite)
                #print towrite
            fnew.write(line)
        
                        



fnew.close()


print "@@@@@@@@Choose one of the samples for each process@@@@@@@@@@"
for byhand in by_hand_list:
    print byhand



        