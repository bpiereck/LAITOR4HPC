# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import os

def xml_parsing(file, logger):

    new_file = f"{file}.parsed"
   
    if file.endswith('.xml'):
        print (f"Running file: {file}")
        logger.info(f"{file} is open and it is going to be parsed")
        contents = (open(file,'r')).read()
        with open(new_file, 'w') as f:

            try:
                soup = bs(contents,'xml')
                medlines = soup.find_all('MedlineCitation')

                for medline in medlines:
                    pmid = medline.PMID.get_text()
                    title = medline.ArticleTitle.get_text()

                    try:
                        f.write("\n"+pmid+"> "+title)
                        for abs in medline.Abstract.find_all():
                            if abs.attrs:
                                f.write(abs)
                            else:
                                f.write(abs.get_text())
                    except:
                        continue
                logger.info(f'{file} has been parsed successfully, output file > {new_file} ready to NLProt format.')
            except:
                logger.error("Make sure the XML file is a PubMed file")


    else:
        logger.error('File could not be open, make sure is a XML file. File must be named > NAME.xml')

    logger.info('Parsing is DONE!')
    #print('----------------------------------------------------------------')


def get_file(path):
    
    ListDir = os.listdir(path)
    files=[]

    for file in ListDir:

        if file.endswith('.xml'):
            file = os.path.join(path, file)
            files.append(file)

    return files
