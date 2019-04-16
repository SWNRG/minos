#!/usr/bin/python

# searching inside everyfolder *logs
# find files named *PDR* , assign this file a new name
# based on the folder details (Period, etc.) and copy 
# the newly named file into the folder allGraphDir

import os
from os import system
import fileinput
import sys
import glob
import shutil
from shutil import copyfile, move

if __name__ == '__main__':

    graphsFolderName = "./1.allGraphsFolder"
    if os.path.exists(graphsFolderName): # search the folder for graphs
        print("graph folder found, deleting...")
        shutil.rmtree(graphsFolderName)  # if it exists, remove it, it
        os.makedirs(graphsFolderName) # create it again, EMPTY
    else:
        print('graph folder NOT found, creating...')
        os.makedirs(graphsFolderName) # if it doesnot exist, create it

    #scan the whole directory folder2scan for ALL files inside it
    folder2scan="./"
    #files =os.listdir(folder2scan)

    folders = glob.glob("logs*")
    #print(files)

    allGraphDir = '../1.allGraphsFolder/' #insert all graphs here. REMEMBER: it is not in folder (./Xs-Xf-Xm/)

    folderCounter = 0
    for folder in folders:
        folderCounter+=1
        while os.path.isdir(folder): # exclude directories
            #if folder.startswith("logs"): # not needed !!! glob does the job
            # print(folder)
            os.chdir(folder)
            newName = str(folder)
            for files in glob.glob("*PDR*png"):
                newName = str(files) # that is the detailed name of the folder
                # print (newName)
                copyfile(files, allGraphDir+newName)

        os.chdir('..')
    print("found "+str(folderCounter)+" folders")

       # else:
       #    print("No dirs found")

