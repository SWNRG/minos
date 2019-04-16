#!/usr/bin/python

import os
from os import system

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


#scan the whole directory folder2scan for ALL files inside it	
folder2scan="./initial_logs/"
files =os.listdir(folder2scan) 
   
print 
#start converting ALL avaliable log files
for filename in files :

	# Use ONLY this for file name. No need anywhere else...
	file2Scan=filename

	readFile = folder2scan + file2Scan
	print("Reading from file: "+str(readFile))

	writeFileName=file2Scan
	print("writing to file: ./logs/"+str(writeFileName)+"\n")
	
	writeFile = open("./logs/"+writeFileName,"w+")
	writeFile.write('#time(min)	pdr	overhead:(icmp/(icmp+udp))\n')
	
	writeFile.write("time(min)"+"	"+writeFileName+"	"+writeFileName+"\n")
	
	started = False
	collected_lines = []

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

			if  searchString in line:
				started = True

				#print "started at line", i # counts from zero !
			
				# process lines for R: r_counter
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
					udp_sent=int(line.rpartition('udp_sent:')[2])
										
					#clients ALREADY ACCUMULATE THESE NUMBERS !!!!!!!!!!!!!!!!!!!!!!!!
					udp_sent_Total=udp_sent_Total+udp_sent					
					
					#print("udp_sent_Total:  "+str(udp_sent_Total))

	#===================================================================

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
			
				continue	
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

	#writeFile.close()

# creating all graphs with gnuplot scripts
# system('./runPlts-logs')


