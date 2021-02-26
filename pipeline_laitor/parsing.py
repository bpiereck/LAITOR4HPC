#!/usr/lib/python3.8
import argparse, logging, os
from inspect import getmembers, isfunction # to check function available in module

from util import update as up
from util import xml_beautifulsoap as xml
from util import ris_format_parsing as ris
from util import exec_laitor as laitor

from util import summary as smy
print (getmembers(smy,isfunction)) # print function available in module

#from util import loggerinitializer as utl

### Initialize log object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#utl.initialize_logger(os.getcwd(), logger)



def main():
    parser = argparse.ArgumentParser(description="A Tool to parse XML and RIS files from PubMed and extract in NLProt txt format", usage='python3 parsing.py [option]')

    subparsers = parser.add_subparsers(title='Programs',
                                       description='valid actions',
                                       dest='command')
                                       



    #########################  X M L . P A R S I N G #########################

    XML = subparsers.add_parser('xml_parsing',
                                help='Do the parsing of a XML format file.',
                                #argument_default='SUPPRESS',
                                description='This parsing is meant to PubMed XML tree and will extract PMID, Title and Abstract of all papers available in the given file.',
                                usage='python3 parsing.py xml_parsing [option]')

    XML.add_argument("-f", "--file",
                            dest="xml_file",
                            type=str,
                            action="store",
                            default=None,
                            required=False,
                            help="Name of document.xml file to be parsed. In case of none, all directory will be listed and all XML will be cath to run")

    XML.add_argument("-p", "--path",
                            dest="xml_path",
                            type=str,
                            action="store",
                            required=False,
                            default='./',
                            help="write path to file, default is the present path, in this case all XML files will be parsed recursively")

    XML.add_argument("-i", "--pmid",
                     dest="pmid",
                     action="store_true",
                     required=False,
                     default=False,
                     help="Save a list of PMIDs parsed")

    #########################  R I S . P A R S I N G #########################

    RIS = subparsers.add_parser('ris_parsing',
                                help='Do the parsing of a RIS format file.',
                                description='This parsing is meant to PubMed RIS file type and will extract PMID, Title and Abstract of all papers available in the given file.',
                                usage= 'python3 parsing.py ris_parsing [option]')

    RIS.add_argument("-f", "--file",
                            dest="ris_file",
                            type=str,
                            action="store",
                            default=None,
                            required=False,
                            help="Name of document.xml file to be parsed. In case of none, all directory will be listed and all XML will be cath to run")

    RIS.add_argument("-p", "--path",
                     dest="ris_path",
                     type=str,
                     action="store",
                     required=False,
                     default='./',
                     help="write path to file, default is the present path, in this case all XML files will be parsed recursively")

    RIS.add_argument("-i", "--pmid",
                     dest="pmid",
                     action="store_true",
                     required=False,
                     default=False,
                     help="Save a list of PMIDs parsed")
                     
    

    
    #########################     S U M M A R Y     #########################

    summary = subparsers.add_parser('summary',
                                    help='Counts how many proteins, co-ocurrences and terms were tagged in the analysis.',
                                    argument_default='SUPPRESS',
                                    description= 'This option will build a table with a summary of all proteins, co-ocurrences and terms. There are two option available: (1) Basic; to acces results from LAITOR4HPC in one folder. (2) Spread; to access results of LAITOR4HPC in more than one folder.',
                                    usage='python3 parsing.py summary [option]')
    
    summary.add_argument("-b", "--basic",
                         dest='co',
                         action='store_true',
                         default=False,
                         required=False)
    
    summary.add_argument("-s", "--spread",
                         dest='full',
                         action='store_true',
                         default=False,
                         required=False)

    summary.add_argument("-p", "--path",
                         dest='path',
                         type = str,
                         action='store',
                         default='./',
                         required=True)

    summary.add_argument("-o", "--output",
                         dest='out',
                         type=str,
                         action='store',
                         default='JOINED',
                         required=False)
    

    
    #########################     UPDATE     #########################

    update = subparsers.add_parser('update',
                                    help='Runs laitor DB updates',
                                    description= '...',
                                    usage='[option]')
    

    update.add_argument("--sup","--stimuli",
                        dest='sup',
                        action='store_true',
                        default=False,
                        required=False)
    
    update.add_argument("--mup","--megadict",
                        dest='mup',
                        action='store_true',
                        default=False,
                        required=False)

    update.add_argument("-b","--both",
                        dest='both',
                        action='store_true',
                        default=False,
                        required=False)

    update.add_argument("--fl","--file_list",
                        dest='file_list',
                        type=str,
                        action='store',
                        default=False,
                        required=False)



    
    #########################     NLProt     #########################

    nlprot = subparsers.add_parser('nlprot',
                                    help='Runs nlprot program',
                                    description= 'This option will allow you tu run NLProt parsing to tag all abstracts/text given in a path list.',
                                    usage='python3 parsing.py nlprot [option]')
    

    nlprot.add_argument("-n","--nlprot",
                         dest='nlprot',
                         action='store_true',
                         default=False,
                         required=False) 

    
    #####################  LAITOR4HPC  #####################

    laitor = subparsers.add_parser('laitor4hpc',
                                    help='Runs LAITRO4HPC program',
                                    description= 'This option will allow you tu run LAITOR4HPC to get all abstracts/text interactions.',
                                    usage='python3 parsing.py laitor4hpc [option]')
    

    laitor.add_argument("-f","--file",
                         dest='laitor_file',
                         type = str,
                         action='store',
                         default=False,
                         required=False)


    
    ### RUN PIPELINE
    ###############################################################

    args = parser.parse_args()

    
    ### Initialize log object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    #utl.initialize_logger(os.getcwd(), logger)

    ### RUN XML PARSING
    ######################################### 
    if hasattr(args,'xml_file') == True or hasattr(args, 'xml_path') == True:
        
        if hasattr(args, 'xml_file') and args.xml_file is not None:
            xml_file = args.xml_file
            xml.xml_parsing(xml_file, logger)
            

        else:
            xml_path = args.xml_path
            files    = xml.get_file(xml_path)
            for f in files:
                xml.xml_parsing(f, logger)

    ### RUN RIS PARSING            
    ######################################### 
    elif hasattr(args, 'ris_file') == True or hasattr(args, 'ris_path') == True: # parsing ris file

        if hasattr(args, 'ris_file') and args.ris_file is not None:
            ris_file = args.ris_file
            logger = 'logger'
            parsing,new_file = ris.ris_parsing(ris_file,logger)
            ris.creat_file(parsing,new_file)


        else:
            ris_path = args.ris_path
            files    = ris.get_file(ris_path)
            logger   = 'logger'
            for f in files:
                parsing,new_file = ris.ris_parsing(f,logger)
                ris.creat_file(parsing,new_file)


    ### RUN SUMMARY
    ######################################### RUN SUMMARY
    elif hasattr(args,'co') == True or hasattr(args,'full') == True:

        smr_path = args.path
        out      = args.out
        basic    = args.co
        spread   = args.full

        if basic is True:
            smy.run_basic(smy_path)
        elif spread is True:
            smy.run_spread(smy_path, out)
        

    ######################################### RUN LAITOR DATABASE UPDATE
    elif hasattr(args,'file_list'): 
        print ('update')

        if hasattr(args, 'sup') and args.sup is True:
            column_type = 'sup'
            file_list=Path(args.file_list)
            
            dict_data = up.updating(file_list, column_type)

        if hasattr(args, 'mup') and args.mup is True:
            column_type = 'mup'
            file_list=Path(args.file_list)
            
            dict_data = up.updating(file_list, column_type)
            

        if hasattr(args, 'both') and args.both is True:
            column_type = 'both'
            file_list=args.file_list
            
            dict_data = up.updating(file_list, column_type)

    ######################################### RUN NLPROT
    elif hasattr(args,'nlprot') == True:
        print ('nlprot')

    ######################################### RUN LAITOR4HPC
    elif hasattr(args,'laitor') == True:
        print ('laitor4hpc')

        


if __name__ == "__main__":
    main()
                     
