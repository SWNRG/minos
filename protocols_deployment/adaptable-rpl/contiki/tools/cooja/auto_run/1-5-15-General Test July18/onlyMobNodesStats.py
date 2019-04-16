#!/usr/bin/python

# to find the average PDR of mobile nodes
# Input needed for the last mobile node number

import os
from os import system
import argparse
import shutil

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
	parser.add_argument('-m', '--lastMobNode', help='Integer Number, the last mobile node',required=True)

	# folders to scan and write
	parser.add_argument('-r', '--folder2scan', help='Folder to Scan for initial logs',required=False)
	parser.add_argument('-w', '--folder2write', help='Folder to write the final logs',required=False)

	args = parser.parse_args()
	#print("folder2scan: {}".format(args.folder2scan))
	#print("folder2write: {}".format(args.folder2write))
	#print("mobile nodes upto: {}".format(args.lastMobNode))
	return args


args = ParseCommandLine()

# ========= EXTRA FOLDER(S) FOR MOBILE NODES STATS ONLY ====================
MobFolder2write = "mobNodeStats-" + (args.folder2write)[10:]
if not os.path.exists(MobFolder2write):  # if it doesn't exist, create it
	os.makedirs(MobFolder2write)
try:  # get ready to create the graph with bars
	# print("copying compareAverageONLY.plt")
	shutil.copy2('./compareAverageONLY.plt', MobFolder2write)
except Exception as e:
	print("Error copy plt: " + str(e))
# ========= EXTRA FOLDER(S) FOR MOBILE NODES STATS ONLY ====================


print
print("\n========== INITIALIZING onlyMobNodesStats.py ============\n")
files =os.listdir(args.folder2scan)
#start converting ALL avaliable log files
for file2Scan in files : # Use ONLY this for file name. No need anywhere else...
	#print("\n==== mobile Node stats from: "+str(file2Scan)+" ============")
	#it should match the incoming number of the last mobile node
	mobNodesCounter = 0
	avgPDR=0.0 #percentage of final average PDR of mobile nodes only

	readFile = args.folder2scan +"/"+ file2Scan
	#print("Reading from file: "+str(readFile))
	#========= EXTRA FILE(S) FOR MOBILE NODES STATS ONLY ====================
	writeMobFileName = "mobNodeStats-"+(file2Scan)[10:]
	#print("writing MOB ONLY STATS: " + str(MobFolder2write) + "/" + str(writeMobFileName) + "\n")
	writeMobFile = open(MobFolder2write + "/" + writeMobFileName, "w+")
	#writeMobFile.write('#Node	PDR\n') #write the first line. It cnfuses things with sorting. Avoid if possible

	with open(readFile, "r") as fp:
		print("=========== open file: " + str(file2Scan) + " ===============")
		for i, line in enumerate(fp.readlines()[0:]):
			#print("Reading line: "+str(line))
			try:
				node = int(line.partition("\t")[0]) #all nodes in the file
				#print("node found: "+str(node)) #printing below only mobile nodes with PDR
			except Exception as e:
				print("Node read problem: "+str(e)+ " in "+ str(line.partition("\t")[0]))

			#print("all nodes:"+str(node))
			if node <= int(args.lastMobNode):
				mobNodesCounter+=1 #count the mobile nodes
				pdr = float(line.rpartition("\t")[2])
				#print('#Mob Node\tPDR')
				line2write = (str(node)+'\t'+str(pdr))
				#print("node,pdr :"+str(line2write))
				writeMobFile.write(line2write+"\n")
				avgPDR = avgPDR + pdr
		if mobNodesCounter > 0: # incoming file has mobile nodes & data to process
			try:
				avgPDR = truncate(avgPDR/mobNodesCounter,2)
				print("Avg PDR: " +str(avgPDR))
				writeMobFile.write("Avg\t" +str(avgPDR))
			except Exception as e:
				print("Error in avgPDR: "+str(e)+", mobNodesCounter="+str(mobNodesCounter))
					#writeMobFile.write('\n')
		else: # file does not have data to process (no mobile nodes, empty file, etc.)
			print("mobNodesCounter is not > 0. Doing nothing....")

		print("total mobile nodes: " + str(mobNodesCounter))
		print("=========== end of file: "+str(file2Scan)+" ===============\n")
	fp.close()
	writeMobFile.close()

# ======================= afterwards run the graph creating file========================
try:
	os.chdir(MobFolder2write)
	#os.system('pwd')
	os.system('gnuplot compareAverageONLY.plt')
	os.chdir('..')
except Exception as e:
	print("error copying compareAverageONLY.plt: "+str(e))



