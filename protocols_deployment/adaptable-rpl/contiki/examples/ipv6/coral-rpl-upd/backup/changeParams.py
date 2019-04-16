#!/usr/bin/python

import os
from os import system
import fileinput
import shutil
import sys
import argparse
import glob


# PARAMETERS TO CHANGE:
# PERIOD 60 means 60 packets per hour
# PERIOD 6 means 600 packets per hour


def ParseCommandLine():
	parser = argparse.ArgumentParser(description="Changing RPL parameters dynamically")

	#Altering freaquency of messages
	parser.add_argument('-mp', '--mobilePeriod', help='Period for sending UDP packets from the MOBILE stations only',required=True)
	parser.add_argument('-fp', '--fixedPeriod', help='Period for sending UDP packets from the FIXED stations only',required=True)
	
	# Altering Idouble				
	parser.add_argument('-mi', '--mobileIdouble', help='Idouble for mobiles. USUALLY, we dont change this',required=False)
	parser.add_argument('-fi', '--fixedIdouble', help='Idouble for statics & server.',required=False)

	args = parser.parse_args()


	print("Mobile Period: {}".format(args.mobilePeriod))
	print("Fixed Stations Period: {}".format(args.fixedPeriod))
	
	if args.mobileIdouble:
		print("Mobile Idouble: {}".format(args.mobileIdouble))
	if args.fixedIdouble:
		print("Fixed Stations Idouble: {}".format(args.fixedIdouble))
	
	return args


if __name__ == '__main__':
	args = ParseCommandLine()

	#scan the whole directory folder2scan for ALL files inside it
	folder2scan="/home/user/contiki/examples/ipv6/coral-rpl-upd/"
	#files =os.listdir(folder2scan)

	files = glob.glob(folder2scan)
	textForPeriod = "#define PERIOD "
	textForIdouble = "#define IDOUBLE "

	for file in files:
		if not os.path.isdir(file): # exclude directories

			if file.startswith("udp-client-mobile"):
				newPeriodText = textForPeriod + str(args.mobilePeriod)
				if args.mobileIdouble:
					newIdoubleText = textForIdouble  + str(args.mobileIdouble)

				tempFile = open(file, 'r+')
				print("opened file: "+str(tempFile))
				for line in fileinput.input(file):
					if textForPeriod in line:
						print("Mobile Period Found: " +textForPeriod+" in file: "+file+" replaced with "+newPeriodText)
						line=newPeriodText+"\n"
						tempFile.write("//PERIOD ALTERED by EXTERNAL PROGRAM\n")
						tempFile.write(line)
					else:
						if args.mobileIdouble:
							if textForIdouble in line:
								print("Mobile Idouble Found: " +textForIdouble+" in file: "+file+" replaced with "+newIdoubleText)
								line=newIdoubleText+"\n"
								tempFile.write("//IDOUBLE ALTERED EXTERNALLY\n")
							tempFile.write(line)
				tempFile.close()

			else:
				if file.startswith("udp-client-static") or file.startswith("udp-server-"):
					newPeriodText = textForPeriod + str(args.fixedPeriod)
					if args.fixedIdouble:
						newIdoubleText = textForIdouble  + str(args.fixedIdouble)

					tempFile = open(file, 'r+')
					print("opened file: " + str(tempFile))
					for line in fileinput.input(file):
						if textForPeriod in line:
							print("Static Period Found: " +textForPeriod+" in file: "+file+" replaced with "+newPeriodText)
							line=newPeriodText+"\n"
							tempFile.write("//PERIOD ALTERED by EXTERNAL PROGRAM\n")
							tempFile.write(line)
						else:
							if args.fixedIdouble:
								if textForIdouble in line:
									print("Static Idouble Found: " +textForIdouble+" in file: "+file+" replaced with "+newIdoubleText)
									line=newIdoubleText+"\n"
									tempFile.write("//IDOUBLE ALTERED EXTERNALLY\n")
								tempFile.write(line)
					tempFile.close()

				else:
					continue


	try:
		# delete all old compiled code. Force fresh compilation
		files = os.listdir(".")
		for file in files:
			if file.endswith(".z1"):
				print("Deleting file: "+str(file))
				os.remove(file)

		os.remove("contiki-z1.*")
		shutil.rmtree("./obj_z1")
	except:
		print ("\nNo file(s) found to delete\n")
