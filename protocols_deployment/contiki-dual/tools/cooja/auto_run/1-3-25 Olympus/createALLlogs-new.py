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

print 'TRYFON'
print args.folder2scan
#scan the whole directory folder2scan for ALL files inside it	
#folder2scan="./initial_logs/"
files =os.listdir(args.folder2scan) 


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





	# new file on detailed statistics for EVERY NODE (We care about mobiles)
	mobTimeData = "mobTimeData"+str(file2Scan)+".dat"
	writeMobData = open(folder2write + "/" + mobTimeData, "w+")

	mobNodesNumber = 3 #one more than the last mobile number

	# mobile statistics way down
	mobSentPacks = 0
	mobRecvPacks = 0
	curRes = 0.0







	#========= EXTRA FILE(S) FOR MOBILE NODES STATISTICS ONLY ====================

	cumulDataFile = "cumulData-"+str(file2Scan)
	cumulDataFolder = "cumulData-"+args.folder2write

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
				pos = int(line.rpartition('Msg from Node:')[2])
				#print("Node from which packet(s) were received: " + str(pos))
				if pos in nodes:
					index = nodes.index(pos)
					#print("Existing node re-appeared:" + str(pos))
					# increase the 2nd array by one
					nodePacketsReceived[index]+=1

					#print("Node:" + str(pos) + ", total packets Received:" + str(nodePacketsReceived[index]))

				else:  # node is new, just add it in the nodes list
					#print("node found in moblie statistics: " +str(pos))
					nodes.append(pos)#expand the array with another new node
					nodePacketsReceived.append(1)#expand the array
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
							#print (r_counter)
							#print("nodes:               ",nodes)
							#print("nodePacketsSent:     ",nodePacketsSent)
							#print("nodePacketsReceived: ",nodePacketsReceived)
							#print

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

# =================== UNIQUE time series for each node =================================
				#print (r_counter)
				#print("nodes:               ", nodes)
				#print("nodePacketsSent:     ", nodePacketsSent)
				#print("nodePacketsReceived: ", nodePacketsReceived)
				#print
# =================== UNIQUE time series for each node =================================


# ====== Creating new file with only mobile node stats. Dont forget to set 	mobNodesNumber =================
				for nodeIndex, nodeId in enumerate(nodes):
					if (nodeId < mobNodesNumber): #ONLY MOBILE NODES
						#print (r_counter," Node: ", nodeId, ", P_Snt: ",nodePacketsSent[nodeIndex], "P_rcv: ", nodePacketsReceived[nodeIndex])
						#print("mobRecvPacks: ",nodePacketsReceived[nodeIndex], "mobSentPacks: ",nodePacketsSent[nodeIndex])
						#print ("nodeIndex: ", nodeIndex, ", nodeId: ", nodeId, ", nodePacketsSent: ", nodePacketsSent[nodeIndex],"nodePacketsReceived: ", nodePacketsReceived[nodeIndex])
						mobRecvPacks+=nodePacketsReceived[nodeIndex]
						mobSentPacks+=nodePacketsSent[nodeIndex]
						print("NodeIndex:"+str(nodeIndex)+"  NodeID:"+str(nodeId))
						print("mobRecvPacks:"+str(mobRecvPacks)+"  nodePacketsReceived[nodeIndex]:"+str(nodePacketsReceived[nodeIndex]))
						print("mobSentPacks:"+str(mobSentPacks)+"  nodePacketsSent[nodeIndex]:"+str(nodePacketsSent[nodeIndex]))

				if(mobSentPacks>0):
					mobileNodesPDR = truncate(100*float(mobRecvPacks)/float(mobSentPacks),2)
					print("mobileNodesPDR:"+str(mobileNodesPDR))
				else:
					mobileNodesPDR=0
				mobDataLine = str(r_counter) + "\t"+str(mobileNodesPDR)
				#print(mobDataLine) # mobile nodes only time series for MONROE
				writeMobData.write(mobDataLine+"\n")
				mobRecvPacks = 0 # reset for every round
				mobSentPacks = 0
# ====== Creating new file with only mobile node stats. Dont forget to set 	mobNodesNumber =================


# ================== Write ONLY MOBILE DATA for bars graphs (no time series) ========================
		#write the nodes[] data into a file
		print("======= Writing to : "+str(cumulDataFile)+"=============")
		for a,b,c in zip(nodes,nodePacketsReceived, nodePacketsSent):
			if(c==0):
				c=1 # Just increase it by one, so division is possible
			mobPDR = truncate(100 * float(b) / c, 2)
			line2write = str(a)+"\t"+str(b)+"\t"+str(c)+"\t"+mobPDR
			#print(line2write)

			writeCumulFile.write(line2write+"\n")
		writeCumulFile.close()

	writeMobData.close()
print("\n======= END OF createAlllogs-new.py =======================\n")
# ==================================================================================================

	#print 
# sorting the files inside mobile folder is in SEPARATE FILE: ./sortMobStats.py
