import sys
import os

from Sudoku import Sudoku
from SAT import solve_sat

# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()

if __name__ == '__main__':
	if len(sys.argv) != 1:
		print ("Loading file %s" % (sys.argv[1]))
	else:
		print ("No input provided. Cya")
		sys.exit(1)

	try:
		file = open(sys.argv[1],"r")
	except Exception as e:
		print("Could not load file")
		sys.exit(1)


	for line in file.readlines():
		if line and line[0].isalnum():
			if ((order := int(line[0])) > 6):
				print('Order not supported. Ignoring')
				continue  
			read_line = list(line[2:].strip('\n'))
			for i in range(len(read_line)):
				if read_line[i] == '.':
					read_line[i] = 36
				elif not read_line[i].isdigit():
					read_line[i] = ord(read_line[i])
				elif read_line[i] == ' ':
					continue
				else:
					read_line[i] = int(read_line[i])
			sudoku = Sudoku(read_line,order)
			sudoku.print()

			# This is where the magic happens
			print(sudoku.to_sat()[0:20])
			solve_sat(sudoku.to_sat())

			# Report Solution as Sudoku


