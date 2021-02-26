#usr/bin/python
import  time, sqlite3, sys
from .UPDATE import mega_dict_update as mup
from .UPDATE import stimuli_update as sup

def check_files(dict_data, columns_type):

    checkinn_sup = {'tax_file': 'TAXONOMY FILE ', 'unip_file':'UNIPROT FILE  ', 'gene_file':'GENE INFO FILE', 'DB':'DATABASE PATH '}
    checkinn_mup = {'mesh_file':'MESH TERMS FILE', 'DB': 'DATABESE PATH '}
    
    if columns_type == 'sup' or columns_type == 'both':

        for key,value in checkinn_sup.items() :
            if key in dict_data:
                pass
            else:
                print (f'\n{value} missing or not recognized')

    if columns_type == 'mup' or columns_type == 'both':

        for key,value in checkinn_mup.items() :
            if key in dict_data:
                pass
            else:
                print (f'\n{value} missing or not recognized')
    

### get path to files
def get_path(files_list, columns_type):

    dict_data = {}
    if columns_type == "mup" or columns_type == "both":
        
        with open(files_list,'r') as f:

            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

            if 'taxonomy file' in line:
                header, tax_file = line.split('=')
                tax_file = str(tax_file.strip())
                dict_data['tax_file'] = tax_file

            elif 'uniprot file' in line:
                header, unip_file = line.split("=")
                unip_file = str(unip_file.strip())
                dict_data['unip_file'] = unip_file

            elif 'gene_info file' in line:
                header, gene_file = line.split('=')
                gene_file = str(gene_file.strip())
                dict_data['gene_file'] = gene_file

            elif 'DB name' in line:
                header, DB = line.split('=')
                DB = str(DB.strip())
                dict_data['DB'] = DB

            else:                
                if columns_type == "both":
                    pass #continue

                else:
                    print ("\nCheck the spelling, and organization. It should look similar to this:\n    taxonomy file  = path/to/name.dmp\n    uniprot file   = path/to/uniprot_sprot.dat\n    gene_info file = path/to/all_data.gene_info\n    DB          = path/to/DB_name.db\n\nWRONG LINE, THE FOLLOWING LINE IS GOING TO BE IGNORED:")
                    print (line)
                    print ("\nWRONG LINE,\nLines that start with '#' are ignored, do this for lines that don't need to be read by the program\n\n")


    if columns_type == "sup" or columns_type == "both":
        
        with open(files_list,'r') as f:

            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

            if 'DB name' in line:
                header, DB = line.split('=')
                DB = str(DB.strip())
                dict_data['DB'] = DB

            elif 'mesh file' in line:
                header, mesh_file = line.split("=")
                mesh_file = str(mesh_file.strip())
                dict_data['mesh_file'] = mesh_file

            else:
                if columns_type == "both":
                    pass #continue
                
                else:
                    print ("\nCheck the spelling, and organization. It should look similar to this:\n    mesh file  = path/to/name.dmp\n    DB          = path/to/DB_name.db\n\nWRONG LINE, THE FOLLOWING LINE IS GOING TO BE IGNORED:")
                    print (line)
                    print ("\nWRONG LINE,\nLines that start with '#' are ignored, do this for lines that don't need to be read by the program\n\n")


    check_files(dict_data, columns_type)
    return dict_data



  ### Insert lines in columns of stimuli table
def insert_stimuli(list_tup, DB):
    conn = sqlite3.connect(DB) # creat a new or connect to an existent DB
    c = conn.cursor() # creat a cursos to execute commands

    ### check connection with DB
    if conn.total_changes == 0:
      print (f"\nConnection with {DB} went ok, starting update of Stimuli (concepts table)")
    else:
      print (f"\nconnection with {DB} didn't work")
      sys.exit()

      insert = (""" INSERT INTO stimuli (synonym, word) VALUES (?,?)""")
      for value in list_tup:
        c.execute(insert,value)

      conn.commit() # save changes
      c.close()     # close DB
      print ("\n\nStimuli (dictioinary of concepts) Update is Done!")






        
  ### Insert lines in columns of Mega dictionary table
def insert_megaDict(list_tup, DB):
    conn = sqlite3.connect(DB) # creat a new or connect to an existent DB
    c = conn.cursor() # creat a cursos to execute commands

    ### check connection with DB
    if conn.total_changes == 0:
      print (f"\nConnection with {DB} went ok, starting update of Mega dictionary ")
    else:
      print (f"\nconnection with {DB} didn't work")
      sys.exit()

      ### check if mega_dictionary_taxonomy exist

      drop = "DROP TABLE IF EXISTS mega_dictionary_taxonomy;"
      c.execute(drop)

      create = """CREATE TABLE IF NOT EXISTS mega_dictionary_taxonomy (
                        GeneID varchar(255) DEFAULT NULL, 
                        name varchar(255) DEFAULT NULL COLLATE NOCASE, 
                        synonym varchar DEFAULT NULL COLLATE NOCASE, 
                        tax_id varchar(255) DEFAULT NULL, 
                        name_txt TEXT);"""

      c.execute(create)

      index = ['CREATE INDEX IF NOT EXISTS idex_GeneID ON "mega_dictionary_taxonomy" (GeneID);', 'CREATE INDEX IF NOT EXISTS idex_name ON "mega_dictionary_taxonomy" (name);', 'CREATE INDEX IF NOT EXISTS idex_syn ON "mega_dictionary_taxonomy" (synonym);', 'CREATE INDEX IF NOT EXISTS idex_tax ON "mega_dictionary_taxonomy" (tax_id);', 'CREATE INDEX IF NOT EXISTS idex_nameTXT ON "mega_dictionary_taxonomy" (name_txt);']

      for i in index:
        c.execute(i)

        insert = """ INSERT INTO mega_dictionary_taxonomy (geneID, name, synonym, tax_id, name_txt) VALUES (?,?,?,?,?)"""

        for value in list_tup:
          c.execute(insert,value)

          
        conn.commit() # save changes
        c.close()     # close DB
        print ("\n\nMega dictionary Update is Done!")





        
                
  #### Inserting items without the hirarchical tree number
  # A python script is generate to run sqlite3 connection and insertion
def updating(files_list, columns_type):

    dict_data = get_path(files_list, columns_type)

    ### if updating stimuli table
    if columns_type == "sup" or columns_type == "both" :
      stime = time.time() #get starting time

      try:
          mesh_file = dict_data['mesh_file'] # Mesh terms file
          DB        = dict_data['DB'] # Laitor4HPC DB name

          print ('\n\n--------------\nPARSING DATA FOR STIMULI UPDATE\n--------------')
          list_tup  = sup.make_list(DB, mesh_file)
          insert_stimuli(list_tup, DB)

          etime = time.time() # get end time
          TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime))
          print ('Stimule updated in {TIME}')

      except:
          print ("\n\nIf file is missing or not recognized STIMULI update can't be done")
          


    ### if updating mega_dictionary
    if columns_type == "mup" or columns_type == "both":

      stime = time.time() #get starting time
      try:
          tax_file  = dict_data['tax_file'] # NCBI taxonomy name.dmp file
          unip_file = dict_data['unip_file'] # uniprot uniprot_sprot.dat file
          gene_file = dict_data['gene_file'] # NCBI all_data.gene_info file
          DB        = dict_data['DB'] # Laitor4HPC DB name

          print ('\n\n--------------\nPARSING DATA FOR MEGA DICTIONARY UPDATE\n--------------')
          list_tup  = mup.make_list(tax_file, unip_file, gene_file)
          insert_megaDict(list_tup, DB)
          etime = time.time() # get end time
          TIME  = time.strftime("%H:%M:%S", time.gmtime(etime-stime))
          print ('Mega dictionary updated in {TIME}')
                

      except:
          print ("\n\nIf file is missing or not recognized MEGA DICTIONARY update can't be done")


