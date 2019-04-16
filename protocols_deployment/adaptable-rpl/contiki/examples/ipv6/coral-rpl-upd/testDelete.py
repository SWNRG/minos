#!/usr/bin/python

import os
from os import system
import fileinput
import shutil
import sys
import argparse
import glob


def deleteOldExecs():
	try:
		files = glob.glob("/home/user/contiki/examples/ipv6/coral-rpl-upd/*")
		#print(files)
		for file in files:
			try: # delete all old compiled code. Force fresh compilation
				if file.endswith(".z1"):
					print("Deleting file: " + str(file))
					#os.remove(file)
			except:
				print("\nNo file(s) found to delete\n")
		print("removing contiki-z1.*")
		# os.remove("contiki-z1.*")
		print("removing dir /obj_z1")
	# shutil.rmtree("./obj_z1")
	except:
		print("\nFile(s) error\n")

if __name__ == '__main__':

	#delete all existing complied files inside folder coral-rpl-udp
	deleteOldExecs()

