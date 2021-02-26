#usr/bin/python
import sys, time, re
# version 1.0

def taxnomy_info(tax_file):

    stime = time.time() #get starting time

    ### Open file to get TaxID and TaxName
    with open(tax_file,'r') as dmp: 
        
        Dict = {} # creat dictionary
        
        for line in dmp:

            line=line.strip()
            if not line: # # ignore malformed lines
                continue

            ### split line to get colum information,
            tax_id, name, empty1, nclass, empty2  = line.split("|")

            taxID   = int(tax_id.strip()) # Make it number
            name    = name.strip()        # clean edges

            Dict[taxID] = name # add in dictionary


    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime)) # set duration

    ### return dict where taxID : taxName
    print (f'\n\nTaxonomy dict done in {TIME}')
    return Dict




def gene_info(gene_file):
    
    stime = time.time() # get start time

    ### make dict of tuples with gene synonyms
    Dict         = {}
    synonym_list = []
    
    ### open file to get synonyms
    with open(gene_file,'r') as f:

        for line in f:

            line = line.strip()
            if not line or line.startswith("#"): # ignore mal formed lines and header
                continue     


            ### split line to get separeted information
            tax_id, geneID, Symbol, LocusTag, Synonyms, dbXrefs, chromosome, map_location, description, type_of_gene, Symbol_from_nomenclature_authority, Full_name_from_nomenclature_authority, Nomenclature_status, Other_designations, Modification_date, Feature_type = line.split("\t")


            #### ORGANIZE DICTINARIE OF LIST 
            geneID   = int(geneID.strip())                            # make it a number
            Symbol   = Symbol.strip()                                 # clean edges
            synonym_list.append(Symbol)
            
            ### Those are sometimes a list splited by "|"
            Synonyms = Synonyms.split("|")                               # make it a list
            SNA      = Symbol_from_nomenclature_authority.split("|")     # make it a list
            FNNA     = Full_name_from_nomenclature_authority.split("|")  # make it a list
            Other    = Other_designations.split("|")                     # make it a list

            synonyms  = Synonyms + SNA + FNNA + Other  # make one list with all synonyms

            for item in synonyms:
                item = item.strip()
                if item != '-' and item != 'hypothetical protein':
                    synonym_list.append(item) # append all item that are not empty or hypothetical
                    

            Dict[geneID] =  tuple(set(synonym_list)) # add tup to dictionary without repeats
            synonym_list = []           

                            
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime))  # set duration
    
    print (f'Gene info dictionary done in {TIME}')
    ### return Dict of tuple, where key is geneID and tuple has all synonyms
    return Dict




def getaccskey(accs, taxID, taxDict):

    # global variables
    taxName = ""
    accskey = ""

    ### Get tax Name
    if taxID  in taxDict: # check if it exists in dictionary
        taxName = taxDict[taxID]       

    if taxID not in taxDict: # if don't exist creat it
        taxName = "No match"

        
    namelist = taxName.split(" ") # get 1st and 2nd words to creat accskey
    if taxName == "No match":     # if name don't exist
        accskey = f'{accs}_NONE'

    else: # if taxName != "No match":

        if len(taxName) <5: # if name smaller than 5 letters
            sten = taxName.upper()
            accskey = f'{accs}_{sten}'
            
        else:
            try: # if two or more words in name
                st = namelist[0][0:3].upper() # 3 letters from first word
                en = namelist[1][0:2].upper() # 2 letter from second word
                accskey = f'{accs}_{st+en}'
                
            except: # if only one word in name
                sten = namelist[0][0:5].upper()
                accskey = f'{accs}_{sten}'

    ### return created accskey and its related taxName
    return taxName, accskey
            



def unipro_info(tax_file, unip_file):
        
    stime = time.time() # get starting time

    ### get taxonomy info where key is taxID and value is scientific name
    taxDict = taxnomy_info(tax_file) 
    


    ### Creat list of tuple and "tup to be"
    list_tup = []
    tup = []

    ### Global variables
    notTax_count     = 0   # count how many tax are merged or changed and can't be used
    accs_count       = 0   # count how many access are available
    geneID_count     = 0   # count geneID lines to save the latest
    
    accs = "" # save accs for global accs

    ### open file to get uniprot info
    with open(unip_file,'r') as unip:
        
        for line in unip:
            line=line.strip()
            
            if not line: # ignore malformed and unrelated lines
                continue

            ### get uniprot primary accession number 
            if line.startswith('AC '):

                tup = []                   # clean accs if geneID not available
                geneID_count = 0           # start geneID count
                accs_count = accs_count+1  # count access
                
                AC, accs = line.split('   ')
                accs = accs.split(";")
                accs = accs[0]
                    

            ### get TaxID from NCBI 
            elif line.startswith('OX   NCBI_TaxID'):
                OX, taxID = line.split("=")

                if "{" in taxID: # If more that one taxID is cited, get the main taxID 
                    taxID = taxID.split('{')
                    taxID = int(taxID[0].strip())
                    
                    taxName, accskey = getaccskey(accs, taxID, taxDict) # Get taxName and accskey 

                    tup.append(accskey) # add in tup to be
                    tup.append(taxID)   # add in tup to be
                    tup.append(taxName) # add in tup to be

                    if  "_NONE" in accskey: # if NONE, count as tax not to be used
                        notTax_count=notTax_count+1 

                else: # if unique TaxID available, get it
                    taxID = int(taxID.replace(";","").strip())                    
                    taxName, accskey = getaccskey(accs, taxID, taxDict) # Get taxName and accskey

                    tup.append(accskey) # add in tup to be
                    tup.append(taxID)   # add in tup to be
                    tup.append(taxName) # add in tup to be

                    if  "_NONE" in accskey: # if NONE, count as tax not to be used
                        notTax_count=notTax_count+1 

            ### get geneID number, same as synonyms ID
            elif line.startswith('DR   GeneID;'):
                geneID_count = geneID_count+1

                if geneID_count==1: # # for unique or 1st geneID available
                   DR, geneID, other = line.split(';')
                   geneID = int(geneID.strip())
                   tup.append(geneID)               
                   
                elif geneID_count>=2: # replace tup geneID with its last updat --> updated tup
                    DR, geneID, other = line.split(';')
                    geneID  = int(geneID.strip())
                    tup = list(tup)
                    tup[-1] = geneID

            ### ignore lines that are not of interest
            else: 
                continue

            ### Making list of tuple             
            if len(tup) == 4: # if tup compleat, save in list

                if geneID_count==1: # for unique or 1st geneID available
                    tup = tuple(tup)
                    list_tup.append(tup)
                    
                if geneID_count >= 2: # replace last item in list with updated tup
                    tup = tuple(tup)
                    list_tup[-1] = tup
                    
            elif not tup: # if tup empty ignore
                continue
                       
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime))  # set duration


    #print (f'{accs_count} Total uniprot accs in file')
    #print (f'{len(list_tup)} Total items in list')
    #print (f"{notTax_count} Taxonomy IDs are not included due to NCBI's taxonomy merge orother reason\n")
    print (f'UniTax list of dictionary done in {TIME}')

    ### return list tup, where tup in list is (accskey, taxID, taxName, geneID)
    return  list_tup






def make_list(tax_file, unip_file, gene_file):

    stime = time.time() # get start time
    
    ### Uniprot list of tup, where tup in list is (accskey, taxID, taxName, geneID)
    unitax_list  = unipro_info(tax_file, unip_file)
    ### Gene info dict of tuple, where key is geneID and tuple has all synonyms (variable number)
    gene_dict = gene_info(gene_file)

    ### make final list to be used in update sqlite3 format
    mega_dict = []

    for tup in unitax_list:
        accskey = tup[0]
        geneID  = tup[3]
        taxID   = tup[1]
        taxName = tup[2]

        if geneID in gene_dict:
            synonyms = gene_dict[geneID]
            S = []
            for s in synonyms:
                if s not in S:
                    S.append(s)
                    tup = (accskey, geneID, s, taxID, taxName)
                    mega_dict.append(tup)
                else:
                    continue
                    
           
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime))  # set duration

    print (f'Mega_dictionary total running time: {TIME}')
    # return dict of tuples were tup is (accskey, geneID, s, taxID, taxName)
    return mega_dict 
    

#tax_file  = sys.argv[1]
#unip_file = sys.argv[2]
#gene_file = sys.argv[3] 


#make_list(tax_file, unip_file, gene_file)
