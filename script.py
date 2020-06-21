import sys
import os
import itertools
import numpy as np

from termcolor import colored
from pprint import pprint
from math import factorial

# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()

def combinatorial(n,r):
    return factorial(n) / factorial(r) / factorial(n-r)

class Sudoku():

	def __init__(self, as_string='',order=3):
		self.grid = np.array(np.array_split(read_line,order**2)).reshape((order**2,order**2))
		self.order=order


	def print(self):
		for i in range(self.order**2):
			for j in range(self.order**2):
				if (i//self.order)%2 == 0:
					if (j//self.order)%2 == 0:
						print(colored(self.grid[i,j],'cyan'),' ', end='')
					else:
						print(colored(self.grid[i,j],'yellow'),' ', end='')
				if (i//self.order)%2 != 0:
					if (j//self.order)%2 == 0:
						print(colored(self.grid[i,j],'yellow'),' ', end='')
					else:
						print(colored(self.grid[i,j],'cyan'),' ', end='')
			print('') 
		print('')

	def to_sat(self):
		N = int(self.grid.shape[0]**(1/2))
		if N!=3:
			print('Not yet supported')
			return

		variables = {}

		for k in range((N**2-1)*N**4 + (N**2-1)*N**2 + N**2):
			variables[k] = 0
		# print(variables)
		assert(len(variables.keys()) == N**6)
		

		completeness_clauses = {}
		for i in range(N**2):
			for j in range(N**2):
				slot = []
				for d in range(N**2):
					slot += [i*N**4 + j*N**2 + d]
				completeness_clauses[(i,j)] = slot
		# print(completeness_clauses)
		assert(len(completeness_clauses)== N**2 * N**2)


		unicity_clauses = {}
		for coord in completeness_clauses.keys():
			unicity_clauses[coord] = list(itertools.combinations(completeness_clauses[coord],2))
		assert(len(unicity_clauses)*len(unicity_clauses[(0,0)])==(N**8-N**6)/2)

		column_validity_dict = {}
		for column in range(N**2):
			column_validity_dict[column] = []
			for d in range(N**2):
				slot = []
				for coord in completeness_clauses.keys():
					if coord[1] == column:
						slot += [coord[0]*N**4 + coord[1]*N**2 + d]
					else:
						continue
				column_validity_dict[column] += slot
			column_validity_dict[column] = [array.tolist() for array in np.array_split(column_validity_dict[column],N**2)]

		column_validity_clauses = {}
		for d in range(N**2):
			column_validity_clauses[d] = [key[d] for key in list(column_validity_dict.values())]
			column_validity_clauses[d] = list(itertools.combinations(column_validity_clauses[d],2))	
		# pprint(column_validity_clauses[0])	

		row_validity_dict = {}
		for row in range(N**2):
			row_validity_dict[row] = []
			for d in range(N**2):
				slot = []
				for coord in completeness_clauses.keys():
					if coord[0] == row:
						slot += [coord[0]*N**4 + coord[1]*N**2 + d]
					else:
						continue
				row_validity_dict[row] += slot
			row_validity_dict[row] = [array.tolist() for array in np.array_split(row_validity_dict[row],N**2)]

		row_validity_clauses = {}
		for d in range(N**2):
			row_validity_clauses[d] = [key[d] for key in list(row_validity_dict.values())]
			row_validity_clauses[d] = list(itertools.combinations(row_validity_clauses[d],2))	
		# pprint(row_validity_clauses)	


		square_validity_dict = {}
		for section in list(itertools.product([0,1,2],[0,1,2])):
			square_validity_dict[section] = []
			for d in range(N**2):
				slot = []
				for coord in completeness_clauses.keys():
					if (coord[0]//order,coord[1]//order) == section:
						slot += [coord[0]*N**4 + coord[1]*N**2 + d]
					else:
						continue
				square_validity_dict[section] += slot
			square_validity_dict[section] = [array.tolist() for array in np.array_split(square_validity_dict[section],N**2)]

		square_validity_clauses = {}
		for d in range(N**2):
			square_validity_clauses[d] = [key[d] for key in list(square_validity_dict.values())]
			square_validity_clauses[d] = list(itertools.combinations(square_validity_clauses[d],2))


		num_column_clauses = len(column_validity_clauses[0])*len(column_validity_clauses)
		num_row_clauses = len(row_validity_clauses[0])*len(row_validity_clauses)
		num_square_clauses = len(square_validity_clauses[0])*len(square_validity_clauses)
		
		assert(num_column_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)
		assert(num_row_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)
		assert(num_square_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)

		assert((num_column_clauses+num_row_clauses+num_square_clauses)*N**2 == 3*(N**8-N**6)/2)

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
			sudoku = Sudoku(read_line,order)
			sudoku.print()
			sudoku.to_sat()
			break



