#!/usr/bin/python

import os
from os import system
import argparse
import glob


def ParseCommandLine():
	parser = argparse.ArgumentParser(description="Changing RPL parameters dynamically")
	
	# folders to scan and write				
	parser.add_argument('-r', '--folder2scan', help='Folder to Scan for initial logs',required=True)
	parser.add_argument('-w', '--folder2write', help='Folder to write the final logs',required=True)

	args = parser.parse_args()

	#print
	#print("folder2scan: {}".format(args.folder2scan))
	#print("folder2write: {}".format(args.folder2write))

	return args
	
	
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])



# ======================================================================
# ====================== MAIN PROGRAM ==================================
# ======================================================================

print("\n======= START of createAlllogs-new.py =========================")
args = ParseCommandLine()

#scan the whole directory folder2scan for ALL files inside it	
#folder2scan="./initial_logs/"
files =os.listdir(args.folder2scan) 

#print ("Scanning for files inside:  "+str(args.folder2scan))
#print("Writing into folder "+str(args.folder2write))
#print("Also writing into mobOnly* file")

#start converting ALL avaliable log files
for filename in files :
	#print("\n======= Opening file: "+str(filename)+" ===================")
	# Use ONLY this for file name. No need anywhere else...
	file2Scan=filename
	readFile = args.folder2scan +"/"+ file2Scan
	print("\n======= Reading from file: "+str(readFile)+"================")


	#================= Basic Files for ALL NODES STATS =======================
	writeFileName=file2Scan
	folder2write = args.folder2write
	#print("writing to file: "+str(folder2write)+"/"+str(writeFileName))
	
	writeFile = open(folder2write+"/"+writeFileName,"w+")
	writeFile.write('#time(min)	pdr	overhead:(icmp/(icmp+udp))\n')
	
	writeFile.write("time(min)"+"	"+writeFileName+"	"+writeFileName+"\n")
	#================= Basic Files for ALL NODES STATS =======================


	#========= EXTRA FILE(S) FOR MOBILE NODES STATISTICS ONLY ====================
	cumulDataFile = "cumulData-"+str(file2Scan)
	cumulDataFolder = "cumulData-"+args.folder2write

	#writeMobFileName = "mobs_only_"+str(file2Scan)
	#MobFolder2write = "mobs_only_"+args.folder2write

	if not os.path.exists(cumulDataFolder):  #if it doesn't exist, create it
		os.makedirs(cumulDataFolder)

		#print("created mob only file: " + str(MobFolder2write) + "/" + str(writeMobFileName) + "\n")
		print("created cumulative data file: " + str(cumulDataFolder) + "/" + str(cumulDataFile) + "\n")

	writeCumulFile = open(cumulDataFolder + "/" + cumulDataFile, "w+")
	writeCumulFile.write('#Node\tReceived\tSent\tPDR(%)\n')

	#writeMobFile = open(MobFolder2write + "/" + writeMobFileName, "w+")
	#writeMobFile.write('#Node\tReceived\tSent\tPDR(%)\n')
	#========= EXTRA FILE(S) FOR MOBILE NODES STATS ONLY ====================


	# create an array list of all nodes in the experiment
	# will be used later to identify mob nodes and their success rate
	nodes = []
	nodePacketsReceived = []
	nodePacketsSent = []

	started = False
	collected_lines = []

	#print("======= Opening file to read stats: "+str(readFile)+"===========")
	with open(readFile, "r") as fp:

		r_counter=0
		r_next_counter=1
	
		udp_recv_Total=0 #only the sink receives. it DOESNOT send udp
				
		#clients ALREADY ACCUMULATE THESE NUMBERS !!!!!!!!!!!!!!!!!!!!!!!!
		udp_sent_Total=0 # all clients accumulation
		icmp_sent_Total=0
		# again SET TO ZERO AT THE END OF FILE !!!!!!!!!!!!!!
		
		icmp_recv_Total=0
		time_counter=0
	
		for i, line in enumerate(fp.readlines()):
					
			#print("searching Round:"+str(r_counter))
			
			searchString="R:"+str(r_counter)+","
			nextString="R:"+str(r_next_counter)+","
			counter=0

			# ===============Mob Nodes ONLY STATISTICS ========================
			if " from Node:" in line:
				#print("nodes:", nodes)
				#print("Array:nodePacketsReceived", nodePacketsReceived)
				pos = int(line.rpartition('Msg from Node:')[2])
				#print("Node from which packet(s) were received: " + str(pos))
				if pos in nodes:
					index = nodes.index(pos)
					#print("Existing node re-appeared:" + str(pos))
					# increase the 2nd array by one
					nodePacketsReceived[index]+=1
					#print("Node:" + str(pos) + ", total packets Received:" + str(nodePacketsReceived[index]))
				else:  # node is new, just add it in the nodes list
					nodes.append(pos)#expand the array with another new node
					nodePacketsReceived.append(0)#expand the array
					nodePacketsSent.append(0)
			# ===============End of Mob Nodes ONLY STATISTICS =================


			if  searchString in line:
				started = True

				#print "started at line", i # counts from zero !
			
				#process lines for R: r_counter
				collected_lines.append(line.rstrip())
				
				#print("line:"+line.rstrip())

	#======================= UDP PACKETS ================================			
				# Only the Sink collects udp packets
				if "udp_recv:" in line:
					udp_recv=int(line.rpartition('udp_recv:')[2])
					
					#print("udp_recv:  "+str(udp_recv))
										
					#all except sink's are zero, so just take only one >0
					if(udp_recv>0):
						udp_recv_Total=udp_recv
					
					#print("udp_recv_Total:  "+str(udp_recv_Total))
			
				# all EXCEPT sink send udp packets
				if "udp_sent:" in line:
					#print("udp_sent found...")
					udp_sent=int(line.rpartition(":")[2])
					

					
					# clients ALREADY ACCUMULATE THESE NUMBERS !!!!!!!!!!!!!!!!!!!!!!!!
					udp_sent_Total = udp_sent_Total + udp_sent
					# print("udp_sent_Total:  "+str(udp_sent_Total))


	#=============New Entry: For EACH NODE, write the sent packets============
				 	#print(line)
				 	currNode = int(line.split(':')[1])
				 	
					#print("Round: "+str(r_counter))
					#print("currNode:"+str(currNode))
					#print("node:"+str(currNode)+", packts sent:"+str(udp_sent))

					if int(currNode)>1:
						if (currNode not in nodes): # or currNode==1:
							#print("old nodes:",nodes)
							nodes.append(currNode)  # expand the array with another new node
							#print("new nodes:",nodes)
							nodePacketsSent.append(udp_sent)  # expand the array
							nodePacketsReceived.append(0)
						else:
							currIndex =nodes.index(currNode)

							# THIS IS VERY WRONG AS IT TURNS OUT. It shows less sent than received!
							#nodePacketsSent[currIndex] = nodePacketsSent[currIndex] + 1

							# we have the number of sent packets for each node
							nodePacketsSent[currIndex] = udp_sent
							#print
							#print("nodes:               ",nodes)
							#print("nodePacketsSent:     ",nodePacketsSent)
							#print("nodePacketsReceived: ",nodePacketsReceived)
							#print
#=====================================================================================


	#======================= ICMP PACKETS =============================
				if "icmp_sent:" in line:
					icmp_sent=int(line.rpartition('icmp_sent:')[2])

					icmp_sent_Total=icmp_sent_Total+icmp_sent
					#print("icmp_sent_Total:  "+str(icmp_sent_Total))

				if "icmp_recv:" in line:
					icmp_recv=int(line.rpartition('icmp_recv:')[2])
					icmp_recv_Total=icmp_recv_Total+icmp_recv
					#print("icmp_recv_Total:  "+str(icmp_recv_Total))


	#==================================================================
	#=========== END OF CHECKING SPECIFIC LINE FOR DATA================
			
				continue # goto next line

			# nextString="R:"+str(r_next_counter)+","
			if (nextString in line) : #or ("Test ended at simulation time" in line)
				 
				#print "\nend at line", i
				time_counter+=1
				#print("time: "+str(time_counter))
				#print("udp_recv_Total:  "+str(udp_recv_Total))

				#print("udp_sent_Total:  "+str(udp_sent_Total))		
				#print("icmp_sent_Total:  "+str(icmp_sent_Total))
				
				#print("icmp_recv_Total:  "+str(icmp_recv_Total))

	#=========================== PDR CALCULATION ========================		
				if udp_sent_Total>0:
					pdr= (100*float(udp_recv_Total)/float(udp_sent_Total)) #percentage (%)
					pdr=truncate(pdr,3)
				else:
					pdr=0 # stats did not start yet
				#print("time: "+str(time_counter)+" PDR:"+str(pdr)+"%")
				#print(str(time_counter)+"	"+str(pdr)+"%")
				#writeFilePDR.write(str(time_counter)+"	"+str(pdr)+"%\n")
	#====================================================================
			
	#========================== OVERHEAD CALCULATION ====================
				if udp_sent_Total>0 and icmp_sent_Total>0:
					overhead=float(icmp_sent_Total)/(float(icmp_sent_Total)+float(udp_sent_Total))
					overhead=truncate(overhead,3)
				else:
					overhead=0 #stats did not start yet
				#print("time: "+str(time_counter)+" overhead:"+str(overhead))
				#print(str(time_counter)+"	"+str(overhead))
				#writeFileOVERHEAD.write(str(time_counter)+"	"+str(overhead)+"\n")
	#====================================================================
						
				#write to logfile
				writeFile.write(str(time_counter)+"	"+str(pdr)+"	"+str(overhead)+"\n")
				
				# BE careful: RESULTS ALREADY ACCUMULATED IN EVERY CLIENT !!!!
				udp_sent_Total=0
				icmp_sent_Total=0
				
				
#************************* NEXT ROUND ******************************
				#print("\nnext round")
				
				#all lines for R:r_counter are here
				for c_line in collected_lines:
					counter=counter+1

					#print("C:"+str(counter)+":"+c_line)

				#print ("increasing counters")
				collected_lines = []
				r_counter=r_counter+1
				r_next_counter=r_next_counter+1
				
				
				#print("counter:"+str(r_counter)+" ,next_counter:"+str(r_next_counter))
				#break

# ================== Write ONLY MOBILE DATA ========================
		#write the nodes[] data into a file
		print("======= Writing to : "+str(cumulDataFile)+"=============")
		for a,b,c in zip(nodes,nodePacketsReceived, nodePacketsSent):
			mobPDR = truncate(100*float(b)/c,2)
			line2write = str(a)+"\t"+str(b)+"\t"+str(c)+"\t"+mobPDR
			#print(line2write)

			writeCumulFile.write(line2write+"\n")
		writeCumulFile.close()

print("\n======= END OF createAlllogs-new.py =======================\n")
# ==================================================================
	#print 
# sorting the files inside mobile folder is in SEPARATE FILE: ./sortMobStats.py
