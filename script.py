import sys
import os
import itertools
import numpy as np

from termcolor import colored
from pprint import pprint

# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()


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
		print('') 
	print('')

def sudoku_to_sat(sudoku):
	N = int(sudoku.shape[0]**(1/2))
	if N!=3:
		print('Not yet supported')
		return

	slot_dict = {}

	for k in range(N*N**4 + N*N**2 + N**2):
		slot_dict[k] = 0
	

	completeness_dict = {}
	for i in range(N**2):
		for j in range(N**2):
			slot = []
			for d in range(N**2):
				slot += [i*N**4 + j*N**2 + d]
			completeness_dict[(i,j)] = slot

	unicity_dict = {}
	for coord in completeness_dict.keys():
		unicity_dict[coord] = list(itertools.combinations(completeness_dict[coord],2))

	validity_dict = {}

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
			if ((order := int(line[0])) > 6):
				print('Order not supported. Ignoring')
				continue  
			read_line = list(line[2:].strip('\n'))
			for i in range(len(read_line)):
				if read_line[i] == '.':
					read_line[i] = 36
				elif not read_line[i].isdigit():
					read_line[i] = ord(read_line[i])
				else:
					read_line[i] = int(read_line[i])
			sudoku = np.array(np.array_split(read_line,order**2)).reshape((order**2,order**2))
			print_sudoku(sudoku)
			sudoku_to_sat(sudoku)
			break



