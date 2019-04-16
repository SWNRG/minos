#!/usr/bin/python

import os
from os import system
import argparse


def truncate(f, n):
	'''Truncates/pads a float f to n decimal places without rounding'''
	s = '{}'.format(f)
	if 'e' in s or 'E' in s:
		return '{0:.{1}f}'.format(f, n)
	i, p, d = s.partition('.')
	return '.'.join([i, (d + '0' * n)[:n]])

def ParseCommandLine():
	parser = argparse.ArgumentParser(description="Find the received packets of ONLY MOBILE NODES")
	
	# number of mobile nodes
	parser.add_argument('-m', '--lastMobNode', help='Integer Number, the last mobile node',required=False)

	# folders to scan and write
	parser.add_argument('-r', '--folder2scan', help='Folder to Scan for initial logs',required=False)
	parser.add_argument('-w', '--folder2write', help='Folder to write the final logs',required=False)

	args = parser.parse_args()

	print("folder2scan: {}".format(args.folder2scan))
	print("folder2write: {}".format(args.folder2write))
	print("mobile nodes upto: {}".format(args.lastMobNode))

	return args
	
	
args = ParseCommandLine()
#scan the whole directory folder2scan for ALL files inside it	
#folder2scan="./initial_logs/"
files =os.listdir(args.folder2scan) 
   
print 
#start converting ALL avaliable log files
for filename in files :

	# Use ONLY this for file name. No need anywhere else...
	file2Scan=filename
	readFile = args.folder2scan +"/"+ file2Scan
	print("Reading from file: "+str(readFile))
	
# ========= EXTRA FILE(S) FOR MOBILE NODES STATS ONLY ====================
	writeMobFileName = "mobFINALSTATS"+file2Scan
	MobFolder2write = "mobFINALSTATS"+args.folder2write
	if not os.path.exists(MobFolder2write):  #if it doesn't exist, create it
		os.makedirs(MobFolder2write)
	print("writing MOB ONLY STATS: " + str(MobFolder2write) + "/" + str(writeMobFileName) + "\n")

	writeMobFile = open(MobFolder2write + "/" + writeMobFileName, "w+")
	writeMobFile.write('#Node	PDR\n')

# ========= EXTRA FILE(S) FOR MOBILE NODES STATS ONLY ====================
	# to find the average PDR of mobile nodes
	mobNodesCounter = 0
	avgPDR=0.0 #percentage

	with open(readFile, "r") as fp:
		for i, line in enumerate(fp.readlines()[1:]):
			#node = line.rpartition(" ")[0]
			#print("node:"+str(node))
			#print line.partition("\t")

			node = int(line.partition("\t")[0]) #all nodes in the file
			#print("all nodes:"+str(node))
			if node <= int(args.lastMobNode):
				mobNodesCounter+=1 #count the mobile nodes
				pdr = float(line.rpartition("\t")[2])
				print('#Mob Node\tPDR')
				line2write = (str(node)+'\t'+str(pdr))
				print(line2write)
				writeMobFile.write(line2write+"\n")
				avgPDR = avgPDR + pdr
		avgPDR = truncate(avgPDR/mobNodesCounter,2)
		print("Avg PDR: " +str(avgPDR))
		writeMobFile.write("Avg PDR:\t" +str(avgPDR))
				#writeMobFile.write('\n')
				
				
				
	
