import sys, os

def count_items(list_files):


    # save all item to return one big dict
    #'co':co_dict, 'prot':protDICT, 'term':termDICT, 'type_term':type_termDICT,'type_co':type_coDICT,
    #'type':{type1:total, type2:total, type3:total, type4:total}
    big_dict = {} 
    
    # creat info dictionary
    co     = {}
    prot   = {}
    term   = {}

    # creat info dict per type of interaction
    type_term = {}
    type_co   = {}

    # count Type
    int1 = 0
    int2 = 0
    int3 = 0
    int4 = 0

    for file in list_files:
        
      with open(file,'r') as f:

        for line in f:
          line=line.strip()
          if not line or line.startswith("INT") or line.startswith('#') : # ignore these lines
            pass

          else:

            if len(line.split('\t'))==3:             # read lines where info about prot, co, term
              head, body, tail = line.split('\t')    # split to access info

              if head == 'P':
                if body not in prot:
                  prot[body] = tail       # if prot not in dict add prot:total
                elif body in prot:
                  total = prot[body]      # access previous total
                  total = total+tail      # sum with new total ref
                  prot[body]=total        # replace key with updated total repetition

                elif head == 'T':
                  if body not in term:
                    term[body] = tail     # if term not in dict add term:total
                  elif body in term:      
                    total = term[body]    # access previous total
                    total = total + tail  # sum with new total ref
                    term[body]=total      # replace key with updated total repetition
                  
                  
                elif head == 'C':
                  if body not in co:
                    co[body] = tail       # if co-interaction not in dict add co:total
                  elif body in co:
                    total = co[body]      # access previous total
                    total = total + tail  # sum with new total ref
                    co[body] = total      # replace key with updated total repetition
                    
                  
                elif len(line.split('\t'))==4:            # read lines where info about prot, co, term
                  head,Ty, body, tail = line.split('\t')  # split to access info
                  
                  if head == 'TyT':
                     key = f'{Ty}={body}'     # creat key to check for repetition in other files

                     if key not in type_term:      
                       type_term[key] = tail  # if key (Type=Term) not in dict add key:total
                     elif key in type_term:
                       total = type_term[key] # access previous total
                       total = total + tail   # sum with new total ref
                       type_term[key] = total # replace key with updated total repetition
                    
                       
                  elif head == 'TyC':
                     key=f'{Ty}={body}'       # creat key to check for repetition in other files

                     if key not in type_co:
                       type_co[key] = tail    #if co-interaction add (type=co, total)
                     elif key in type_co:
                       total = type_co[body]  # access previous total
                       total = total + tail   # sum with new total ref
                       type_co[key] = total   # replace key with updated total repetition
                       
            if len(line.split('\t'))==2:

              Type, total = line.split('\t')
                
              if Type == "INT_1":
                int1 = int1 + total
              if Type == "INT_2":              
                int2 = int2 + total
              if Type == "INT_1":
                int3 = int3 + total
              if Type == "INT_1":
                int4 = int4 + total
                
            else:
                print (f'error line: {line}')
                  
    # fill big dict
    big_dict['co']   = co
    big_dict['prot'] = prot
    big_dict['term'] = term
    big_dict['type_term'] = type_term
    big_dict['type_co'] = type_co
    Type={}
    Type['int1']=int1
    Type['int2']=int2
    Type['int3']=int3
    Type['int4']=int4
    big_dict['type'] = Type

    
    return big_dict

    

def spread_summary(list_files, output):

    big_dict = count_items(list_files)

    # split big dictionarie in dictionaries
    co   = big_dict['co']
    prot = big_dict['prot']
    term = big_dict['term']
    Type = big_dict['type']

    type_term = big_dict['type_term']
    type_co   = big_dict['type_co']
    
    with open(output,'w') as out:

        # write list of files
        out.write('# List of files used to make this spread summary\n')
        n=0
        for f in list_files:
            n=n+1
            out.write(f'N_{n}\t{f}\n')
        
        # write headers and total of each type of interactions
        out.write(f"# THIS DOCUMENT CONTAINS INFO FROM ALL THE ABOVE FILES JOINED, THEY WERE ACCESSED FROM THE PROVIDED PATH\n# GIVEEN PATH:{path}\n")
        
        out.write(f"# Interaction_type\tTotal\n")
        int1 = Type['int1']
        out.wirte(f"INT_1\t{int1}\n")
        int2 = Type['int2']
        out.write(f"INT_2\t{int2}\n")
        int3 = Type['int3']
        out.write(f"INT_3\t{int3}\n")
        int4 = Type['int4']
        out.write(f"INT_4\t{int4}\n")
        
        # write section

        ### write co-ocurrences
        out.write("\n\n### CO-OCURRENCEs\n\n")
        out.write("# Co-ocurence\t Total\n")
        for key_co, value in co.items():
            out.write(f'C\t{key_co}\t{value}\n')
                  
        ### Write proteins    
        out.write("""\n\n### PROTEINS\n\n""")
        out.write('# Prot\t Total\n')
        for key_prot, value in prot.items():
            out.write(f'P\t{key_prot}\t{value}\n')

        ### Write terms
        out.write("""\n\n### TERMs\n\n""")
        out.write('# Terms\t Total\n')
        for key_term, value in term.items():
            out.write(f'T\t{key_term}\t{value}\n')

        ### Write terms by interaction type
        out.write("""\n\n###\n\n# TERM BY INTERACTION TYPE\n\n""")
        out.write('# Type\t Terms\t Total\n')
        for key_tt, value in type_term.items():
            Type, term = key_tt.split('=')
            out.write(f'TyT\t{Type}\t{term}\t{value}\n')

        ### Write co-interaction by interaction type
        out.write("""\n\n###\n\n# CO-OCURENCE BY TYPE\n\n""")
        out.write('# Type\t Co-ocurrence\t Total\n')
        for key_tc, value in type_co.items():
            Type, coint = key_tc.split('=')
            out.write(f'TyC\t{Type}\t{coint}\t{value}\n')
        



