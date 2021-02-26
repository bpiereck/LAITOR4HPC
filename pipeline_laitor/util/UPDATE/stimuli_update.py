#!/usr/bin/python
import sys, os, time, sqlite3

def get_stimuli(DB):

    stime = time.time() #get starting time

    stimuli_list = [] # creat list of concepts
    
    DB = str(DB) # make DB name readable
    conn = sqlite3.connect(DB) # connect to existed DB or ceat a new one

    ### check connection with DB
    if conn.total_changes == 0:
        print (f"\nConnection with {DB} went ok")
    else:
        print (f"\nconnection with {DB} didn't work")
        sys.exit()

    
    c = conn.cursor() # make it able to execute commands

    rows = c.execute("SELECT * FROM stimuli").fetchall() # get all lines in stimule table

    for r in rows: # get concept in each line
        concept = r[0]
        stimuli_list.append(concept)

    ### return a set of stimuli concepts
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime)) # set duration
    print (f'Stimuli list, done in {TIME}.')
    return set(stimuli_list)

def get_megaDict(DB):

    stime = time.time() #get starting time

    megadict_list = [] # creat list of terms
    
    DB = str(DB) # make DB name readable
    conn = sqlite3.connect(DB) # connect to existed DB or ceat a new one


    ### check connection with DB
    if conn.total_changes == 0:
        print (f"\nConnection with {DB} went ok")
    else:
        print (f"\nconnection with {DB} didn't work")
        sys.exit()
    
    c = conn.cursor() # make it able to execute commands

    rows = c.execute("SELECT * FROM mega_dictionary_taxonomy").fetchall() # get all lines in stimule table

    for r in rows: # get terms in each line
        synonym = r[2]
        megadict_list.append(synonym)

    ### return a set of stimuli concepts
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime)) # set duration
    print (f'Megadict list, done in {TIME}.')
    return set(megadict_list)


def get_mesh(mesh_file):

    stime = time.time() #get starting time

    ### creat list of tuples and tup to be
    mesh_list = []

    with open(mesh_file, 'r') as fp: # read mesh_file lines - actually a XML file (tree format)

        for line in fp:
            line=line.strip()
            
            if not line or line.startswith("#"): # ignore malformed or not interested line
                continue

            if line.startswith("<String>"): # find string line
                S1,L = line.split("<String>")
                L,S2 = L.split("</String>")
                mesh = L

                mesh_list.append(mesh) # append mesh term



    ### return a set of mesh concepts
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime)) # set duration
    print (f'\n\nMesh list, done in {TIME}.')
    return set(mesh_list)


    


# Get rid of terms alread existent in stimuli table by comparing the two lists.
# Get rid of terms that are represented in mega_dictionary 
def make_list(DB,mesh_file):


    ### Get lists to use
    stimuli  = get_stimuli(DB)       # return list of stimuli concepts
    megadict = get_megaDict(DB)      # return list os terms from megadict
    mesh     = get_mesh(mesh_file)   # return list of mesh concept    
    

    ### make list tup and tup to be
    List_tup=[]
    tup=[]

    stime = time.time() #get starting time    
    new_terms = (mesh|megadict) - megadict # new set without elemets from megadict
    new_set = (new_terms|stimuli) - stimuli # new set to be added, containing only new concepts

    for concept in new_set:
        tup.append(concept)
        tup.append('A0')
        tup=tuple(tup)
        List_tup.append(tup)
        tup=[]
    

    ### return a set of mesh concepts
    etime = time.time() # get end time
    TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime)) # set duration
    print (f'\n\nList of tuple for stimuli update, done in {TIME}.')
    return List_tup




    
########### get funtions to work ##########
###########################################
###########################################
    

### Get variables 
#DB = sys.argv[1]
#mesh_file = sys.argv[2]

### list tup of stimuli
#new_stimuli = make_list(DB,mesh_file)

