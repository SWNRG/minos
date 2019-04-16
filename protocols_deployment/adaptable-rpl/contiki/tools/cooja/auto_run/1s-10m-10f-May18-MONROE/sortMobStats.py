#!/usr/bin/python

# sorting file as fileinput
# it will look into all folders named mob*,
# open all files inside it, sort all numeric lines
#  write back the sorted list into the file and close it

import os
from os import system
import argparse
import glob
import csv
import fileinput
import re

def sort_human(l):
  convert = lambda text: float(text) if text.isdigit() else text
  alphanum = lambda key: [ convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key) ]
  l.sort( key=alphanum )
  return l

print("\n===== INITIALIZING sortMobStats.py: Sort all cum* folders ============")
# Trying to sort the files inside mobile folder
folders = glob.glob("cum*")
print("found "+str(len(folders))+" cum* folders. Sorting all...")
for folder in folders:
	while os.path.isdir(folder):  # only directories
		os.chdir(folder)
		newName = str(folder)
		for files in glob.glob("*log"):
			print("sorting file: "+str(files))
			listA = []
			newName = str(files)  # that is the detailed name of the folder
			with open (files) as f:
				for line in f:
					#line = sorted (line)
					#print line
					if line.split()[0]<>"#Node":
						#print line.split()[0]
						listA.append(line)
				#print listA
				listA=sort_human(listA)
				#print ("sorted list: "+str(files))
				#for item in listA:
				#   print item
				#print("end of lines")
				#print ("sorted: "+str(files))
			f.close()
			file2write = open(files, 'w')
			for item in listA:
				file2write.write("%s" % item)
			file2write.close()

	os.chdir('..')
	print("===== ENDING sortMobStats.py: Sorted all cum* folders ==============")

	#print("sorted folder: "+str(folder))
	# ATTENTION: Needed number of mobile nodes -m !!!!!!!!!!!!!!!!!!
	os.system("./onlyMobNodesStats.py -r " + folder + " -w" + folder + "AVG" + " -m" + "11")
