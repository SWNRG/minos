#!/usr/bin/python

import os
from os import system
import argparse
import glob


	
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

if 1:
	#print("\n======= Opening file: "+str(filename)+" ===================")
	# Use ONLY this for file name. No need anywhere else...
	readFile = "COOJA.testlog"
	print("\n======= Reading from file: "+str(readFile)+"================")

	#================= Basic Files for ALL NODES STATS =======================
	writeFileName="OlymposPDR.log"
	
	writeFile = open("output/"+writeFileName,"w+")
	writeFile.write('#time(min)	pdr	overhead:(icmp/(icmp+udp))\n')
	
	writeFile.write("time(min)"+"	"+writeFileName+"	"+writeFileName+"\n")
	#================= Basic Files for ALL NODES STATS =======================

	# new file on detailed statistics for EVERY NODE (We care about mobiles)
	mobTimeData = "mobTimeDataOlympos.dat"
	writeMobData = open("output/" + mobTimeData, "w+")

	maxnodes = 27  # USER enter number of network nodes 
	modnodes = [2]  # enter mobile node IDs

	# mobile statistics way down
	mobSentPacks = 0
	mobRecvPacks = 0
	curRes = 0.0

	#========= EXTRA FILE(S) FOR MOBILE NODES STATISTICS ONLY ====================

	cumulDataFile = "Total.log"
	cumulDataFolder = "output"

	writeCumulFile = open(cumulDataFolder + "/" + cumulDataFile, "w+")
	writeCumulFile.write('#Node\tReceived\tSent\tPDR(%)\n')
	#========= EXTRA FILE(S) FOR MOBILE NODES STATS ONLY ====================

	# create an array list of all nodes in the experiment
	# will be used later to identify mob nodes and their success rate
	nodes = []
	nodePacketsReceived = []
	nodePacketsSent = []

	for i in range(1,maxnodes+1):
		nodes.append(i)#expand the array with another new node
		nodePacketsReceived.append(0)#expand the array
		nodePacketsSent.append(0)
		#print("Tryfon i:"+str(i))
		#print("Tryfon node[i]:"+str(nodes[i-1]))

	started = False

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
			searchString="R:"+str(r_counter)+","
			nextString="R:"+str(r_next_counter)+","
			counter=0
			# ===============Mob Nodes ONLY STATISTICS ========================
			if " from Node:" in line:
				pos = int(line.rpartition('Msg from Node:')[2])
				nodePacketsReceived[pos-1]+=1
			# ===============End of Mob Nodes ONLY STATISTICS =================

			if  searchString in line:
				started = True

				#print "started at line", i # counts from zero !
				
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

					#========New Entry: For EACH NODE, write the sent packets============
				 	currNode = int(line.split(':')[1])
					if int(currNode)>1:
						nodePacketsSent[int(currNode)-1] = udp_sent

				#============== ICMP PACKETS SEND =============================
				if "icmp_sent:" in line:
					icmp_sent=int(line.rpartition('icmp_sent:')[2])
					icmp_sent_Total=icmp_sent_Total+icmp_sent

				#============== ICMP PACKETS RECEIVE===========================
				if "icmp_recv:" in line:
					icmp_recv=int(line.rpartition('icmp_recv:')[2])
					icmp_recv_Total=icmp_recv_Total+icmp_recv

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
	#====================================================================
			
	#========================== OVERHEAD CALCULATION ====================
				if udp_sent_Total>0 and icmp_sent_Total>0:
					overhead=float(icmp_sent_Total)/(float(icmp_sent_Total)+float(udp_sent_Total))
					overhead=truncate(overhead,3)
				else:
					overhead=0 #stats did not start yet
	#====================================================================
						
				#write to logfile
				writeFile.write(str(time_counter)+"	"+str(pdr)+"	"+str(overhead)+"\n")
				
				# BE careful: RESULTS ALREADY ACCUMULATED IN EVERY CLIENT !!!!
				udp_sent_Total=0
				icmp_sent_Total=0

#************************* NEXT ROUND ******************************
				r_counter=r_counter+1
				r_next_counter=r_next_counter+1

# ====== Creating new file with only mobile node stats. Dont forget to set mobNodesNumber 
				for i in range(1,maxnodes+1):
					if i in modnodes:
						mobRecvPacks+=nodePacketsReceived[i-1]
						mobSentPacks+=nodePacketsSent[i-1]	
						print("NodeIndex:"+str(i-1)+"  NodeID:"+str(i))
						print("mobRecvPacks:"+str(mobRecvPacks)+"  nodePacketsReceived[nodeIndex]:"+str(nodePacketsReceived[i-1]))
						print("mobSentPacks:"+str(mobSentPacks)+"  nodePacketsSent[nodeIndex]:"+str(nodePacketsSent[i-1]))

				if mobRecvPacks > mobSentPacks:
 					mobileNodesPDR = 100
				else:
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
			if float(b) > float(c):
				b = c  # avoid numbers above 100
			mobPDR = truncate(100 * float(b) / c, 2)
			line2write = str(a)+"\t"+str(b)+"\t"+str(c)+"\t"+mobPDR
			#print(line2write)

			writeCumulFile.write(line2write+"\n")
		writeCumulFile.close()

	writeMobData.close()
print("\n======= END OF createAlllogs-new.py =======================\n")
# ==================================================================================================

