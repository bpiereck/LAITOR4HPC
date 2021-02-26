#!/usr/lib/python3.8
import sys, os
from .SUMMARY import summary_basic as sb
from .SUMMARY import summary_spread as ss


### get list of laitor.co files and creat list of path
### and create output files name
def list_co_files(path):

    PATH = os.getcwd()                      # get current path
    new_folder = f'{outpath}/SUMMARY_FILES' # name folder to save summary output
    cmd = f'mkdir -p {new_folder}'          # command to creat, if not exists, the above folder
    os.system(cmd)                          # execute command

    
    list_files = []                            # list tup (file, output)
    listdir = os.listdir(path)                 # list all items in directory
    
    for file in listdir: 
       if file.endswith('.co'):                # if file has co-ocurrences (.co)
           co_file = os.path.join(path,file)   # save path
           output  = co_file.split('/')        # get file name without path
           output  = output[-1]
           output  = f'{new_folder}/{output}_summary.basic'  # create output in new SUMMARY folder
           list_files.append((co_file,output))               # add to list_files

    return list_files



### write basic summary file
def run_basic(path):
    
    list_files = list_co_files(path)

    for tup in list_files:
        co_file = tup[0]
        output  = tup[1]
        sb.basic_summary(co_file, output)

      
### get list of file_basic.summary and creat list of path
### and create output files name
def list_basic_files(path):
    
    list_files = []                # list of summary files
    listdir = os.listdir(path)     # list items in directory
    
    try:
        for folder in listdir:
            try:
                if folder.endswith('SUMMARY_FILES'):             # if folder of interest is found
                    folder       = os.path.join(path,folder)     # save folder's path
                    list_summary = os.listdir(folder)            # list files in folder
                    for file in list_summary:
                        if file.endswith('summary.basic'):
                            file = os.path.join(path,file)       # save file's path
                            list_files.append(file)              # append file in list files
            except:
                for f in folder:              # check for branch folders in folder 
                    if f == 'SUMMARY_FILES':  # inside of branch folder look for SUMMARY folder
                        
                        f = os.path.join(folder,item)  # save summary path in brunch folder
                        list_summary = os.listdir(f)   # list files in the above folder

                        for file in list_summary:
                            if file.endswith('summary.basic'):
                                file = os.path.join(path,file)       # save file's path
                                list_files.append(file)              # append file in list files

    except:
        print ('No folder called SUMMARY_FILES was found, check previous steps.')
        pass

    return list_files


### write spread summary file
def run_spread(path, out):
    
    list_files = list_basic_files(path)
    output     = f'{out}_summary.spread'
    ss.spread_summary(list_files, output)       


