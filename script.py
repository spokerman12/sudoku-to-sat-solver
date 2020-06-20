import sys
import os

import numpy as np

from termcolor import colored



def print_sudoku(sudoku, order=3):
	for i in range(order**2):
		for j in range(order**2):
			if (i//order)%2 == 0:
				if (j//order)%2 == 0:
					print(colored(sudoku[i,j],'cyan'),' ', end='')
				else:
					print(colored(sudoku[i,j],'yellow'),' ', end='')
			if (i//order)%2 != 0:
				if (j//order)%2 == 0:
					print(colored(sudoku[i,j],'yellow'),' ', end='')
				else:
					print(colored(sudoku[i,j],'cyan'),' ', end='')
		print('\n',end='') 
	print('')

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
		if line and line[0].isalnum():
			# Mind this if we implement order 6 sudokus
			# order = line[0]
			read_line = list(line[2:].strip('\n'))
			sudoku = np.array(np.array_split(read_line,9)).reshape((9,9))
			print_sudoku(sudoku)