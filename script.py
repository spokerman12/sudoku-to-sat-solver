import sys
import os

import numpy as np

if __name__ == '__main__':
	if len(sys.argv) != 1:
		print ("Loading file %s" % (sys.argv[1]))
	else:
		print ("No input provided. Cya")

	try:
		file = open(sys.argv[1],"r")
	except Exception as e:
		print("Could not load file")


	for line in file.readlines():
		print(line)