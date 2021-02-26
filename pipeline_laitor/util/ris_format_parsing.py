# -*- coding: utf-8 -*-

import sys, os

### parsing info in file format .ris
def ris_parsing(file, logger):

    new_file = (f"{file}.parsed")

    #iniciate parsing
    if file.endswith('.ris'):
        parsing=[]
        tup=[]

        with open(file, 'r') as fp:            
            
            for line in fp:
                line=line.strip()

                # ignore malformed or not interested line
                if not line or line.startswith("#"):
                    continue

                if line.startswith("AN  - "):
                    AN,ID = line.split("  - ")
                    ID = ID.strip()
                    tup.append(ID)
                    #print (f"ltup_ID={ltup}")
                    #print (f"\n{ID}>")

                if line.startswith("TI  - "):
                    TI,Title = line.split("  - ")
                    Title = Title.strip()
                    tup.append(Title)
                    

                if line.startswith("AB  - "):
                    ab,AB = line.split("  - ")
                    AB = AB.strip()
                    tup.append(AB)


                    tup=tuple(tup)
                    parsing.append(tup)
                    tup=[]
                    
        return (parsing,new_file)
            

# creating file for NLProt format from list created in previous step
def creat_file(parsing_list,new_file):

    with open(new_file,'w') as nf:
        cycles=len(parsing_list)
        i=0

        while i<(cycles):
            ID=str(parsing_list[i][0])
            Title=str(parsing_list[i][1])
            Abstract=str(parsing_list[i][2])
            stg="{}>{} {}\n\n".format(ID,Title,Abstract)
            nf.write(stg)
            i=i+1
            
# listing files in a folder
def get_file(path):
    ListDir = os.listdir(path)
    files=[]

    for file in ListDir:

        if file.endswith('.ris'):
            print(file)
            file = os.path.join(path, file)
            files.append(file)

    return files






########## Going throug fuctions ###################
    
    
"""flag = sys.argv[1]
path = sys.argv[2]
logger = "logger"

if flag=='-p':
    files= get_file(path)
    for f in files:
        #new_file = new_file(f)
        parsing = ris_parsing(f,logger)
        creat_file(parsing)

if flag=='-f':
    #new_file = new_file(path)
    parsing = ris_parsing(path,logger)
    creat_file(parsing)"""





    
    
############# FOR LATER #################################################################
'''except:
                        continue
                logger.info(f'{file} has been parsed successfully, output file > {new_file} ready to NLProt format.')
            except:
                logger.error("Make sure the XML file is a PubMed file")




    else:
        # print ("must be a ris file")
        logger.error('File could not be open, make sure is a ris file. File must be named > NAME.ris')

    logger.info('Parsing is DONE!')
    print('-----------------------------------------------------------------------')
    # print ("DONE!")
    # print()'''

##########################################################################################

