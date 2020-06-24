"""
sudoku_to_sat.py

Translates a file with a Sudoku per line
	into SAT instances, each one in a file


Use as follows:

$ python sudoku_to_sat.py <input_file> <output_filename (optional)>

"""

import sys
import os

from Sudoku import Sudoku

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

	if len(sys.argv) > 2:
		filename = sys.argv[2]
	else:
		filename = 'output'

	dirname = os.path.split(os.path.abspath(__file__))[0]+'/'+filename

	os.makedirs(os.path.dirname(dirname), exist_ok=True)

	output = ''
	file_counter = 0
	for line in file.readlines():
		if line and line[0].isalnum():
			order = int(line[0])
			if order > 6:
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
			with open(dirname+'/'+filename+str(file_counter),'+w') as file:
				file.write(sudoku.to_sat())
			print('^This^ Sudoku written as SAT to file',filename+'_'+str(file_counter))
			file_counter+=1


