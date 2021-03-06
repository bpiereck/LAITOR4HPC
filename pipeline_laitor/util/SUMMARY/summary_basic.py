import sys, os


### count total number of each type of interaction
def count_interec_type(file):

    int1 = 0
    int2 = 0
    int3 = 0
    int4 = 0

    with open(file,'r') as f:

        for line in f:

            if not line or line.startswith('#'): #ignore malformed or not of interest
                continue

            col = line.strip().split('\t') # get line columns
            
            # accessing info
            Type = col[0] # get column type description

            # counting each type
            if Type == 'INT_1':
                int1 += 1
            elif Type == 'INT_2':
                int2 += 1
            elif Type == 'INT_3':
                int3 += 1
            elif Type == 'INT_4':
                int4 += 1

    return int1,int2,int3,int4


### make list of proteins, terms and co-interactions
def make_list(file):

    co_info  = [] # list of tuples with complete info about interaction
    

    with open(file,'r') as f:

        for line in f:
            line = line.strip()

            if not line or line.startswith('#'): #ignore malformed or not of interest
                continue

            col = line.split('\t') # get line columns

            # accessing info
            Type  = col[0].strip().lower()
            prot1 = col[1].strip().lower()
            prot2 = col[3].strip().lower()
            term  = col[2].strip().lower()

            # creat co-ocurrence info list of tuples
            co  = f"{prot1}/{prot2}"
            tup = (Type, co, term)
            co_info.append(tup)            

    return co_info 

def count_per_type(co_info):

    list_tm = [] # creat list of tup term,type
    list_co = [] # creat list of tupe co-ocurence,type

    count_tm  = [] # save total repetition of each term
    count_co  = [] # save total repetition of co-interactions
    
    for tup in co_info:
        Type         = tup[0] # int1-4
        co           = tup[1] # prot1/prot2
        term         = tup[2].strip().lower # interaction term

        list_tm.append([Type,term])
        list_co.append([Type,co])


    set_tm = set(list_tm) # get onlyt unique terms
    set_co = set(list_co) # get only unique co-ocurrences

    for t in set_tm:
        total = list_tm.count(t) # count repetition
        count_tm.append((t[0],t[1],total)) # save count (type, term, total)

    for c in list_co:
        total = list_co.count(c) # count co-ocurrences
        count_co.append((c[0],c[1],total)) # save count (type, co-ocur, 
        
    return count_tm, count_co


### count number of repetition of prot, tems and co-ocurences
def count_items(co_info):

    list_co = [] # creat list of co ocurences
    list_pr = [] # creat list of proteins
    list_tm = [] # creat list of terms
    
    co_total = [] # creat list tup of (co-ocurences,total_repetition)
    pr_total = [] # creat list tup of (prot, total)
    tm_total = [] # creat list tup of (terms, total)
    
    for tup in co_info:
        co     = (tup[1]).strip().lower() # get co:prot1/prot2
        p1, p2 = co.split('/') # get prot
        term   = tup[2].strip().lower() # get terms

        # add to list
        list_co.append(co) 
        list_pr.append(p1)
        list_pr.append(p2)
        list_tm.append(term)

    # count unique elements of each list
    set_co = set(list_co)
    for co in set_co:
        total = list_co.count(co)
        co_total.append((co,total))
        
    set_pr = set(list_pr)
    for pr in set_pr:
        total = list_pr.count(pr)
        pr_total.append((pr,total))
        
    set_tm = set(list_tm)    
    for tm in set_tm:
        total = (list_tm.count(tm)) 
        tm_total.append((tm,total))

    return co_total, pr_total, tm_total


### creat basic summary files
def basic_summary(file, output):

        
        int1,int2,int3,int4           = count_interac_type(file) # count interactions in file
        co_info                       = make_lists(file) # co_info = (Type, "p1/p2", term)
        co_total, pr_total, tm_total  = count_items(co_info) # list of (co-ocurrence, repetition)
        count_tm, count_co            = count_per_type(co_info) # count by type (type, co/tm, total)
        
        with open(output,'w') as out: # write file info

            # write headers and total of each type of interactions
            out.write(f"\n# {file} SUMMARY \n\n")
            out.write(f"# Interaction_type\tTotal\n")
            out.wirte(f"INT_1\t{int1}\n")
            out.write(f"INT_2\t{int2}\n")
            out.write(f"INT_3\t{int3}\n")
            out.write(f"INT_4\t{int4}")

            # write section
            # write co-ocurrences
            out.write("\n\n### CO-OCURRENCEs\n\n")
            out.write("# Co-ocurence\t Total\n")                
            for tup in co_total:
                co = tup[0]
                total = tup[1]

                if co == Co:
                    out.write(f'C\t{co}\t{total}\n')

            # write proteins                    
            out.write("""\n\n### PROTEINS\n\n""")
            out.write('# Prot\t Total\n')
            for tup in prot_total:
                prot = tup[0]
                total= tup[1]
                out.write(f'P\t{prot}\t{total}\n')

            # write terms
            out.write("""\n\n### TERMs\n\n""")
            out.write('# Terms\t Total\n')
            for tup in terms_total:
                terms = tup[0]
                total= tup[1]
                out.write(f'T\t{terms}\t{total}\n')

            # write terms by interaction type   
            out.write("""\n\n###\n\n# TERM BY INTERACTION TYPE\n\n""")
            out.write('# Type\t Terms\t Total\n')
            for tup in count_term:
                Type  = tup[0]
                term  = tup[1]
                total = typ[2]
                out.write(f'TyT\t{Type}\t{term}\t{total}')

            # write co-interaction by interaction type     
            out.write("""\n\n###\n\n# CO-OCURENCE BY TYPE\n\n""")
            out.write('# Type\t Co-ocurrence\t Total\n')
            for tup in count_co:
                Type  = tup[0]
                co    = tup[1]
                total = typ[2]
                out.write(f'TyC{Type}\t{co}\t{total}')


            
