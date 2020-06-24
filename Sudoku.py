import itertools
import os

import numpy as np

from termcolor import colored
from pprint import pprint
from math import factorial


# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()

class Sudoku():

	def __init__(self, as_string='',order=3):
		self.grid = np.array(np.array_split(as_string,order**2)).reshape((order**2,order**2))
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
					if (coord[0]//self.order,coord[1]//self.order) == section:
						slot += [coord[0]*N**4 + coord[1]*N**2 + d]
					else:
						continue
				square_validity_dict[section] += slot
			square_validity_dict[section] = [array.tolist() for array in np.array_split(square_validity_dict[section],N**2)]

		square_validity_clauses = {}
		for d in range(N**2):
			square_validity_clauses[d] = [key[d] for key in list(square_validity_dict.values())]
			square_validity_clauses[d] = list(itertools.combinations(square_validity_clauses[d],2))

		# Number of validity clauses
		num_column_clauses = len(column_validity_clauses[0])*len(column_validity_clauses)
		num_row_clauses = len(row_validity_clauses[0])*len(row_validity_clauses)
		num_square_clauses = len(square_validity_clauses[0])*len(square_validity_clauses)
		
		assert(num_column_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)
		assert(num_row_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)
		assert(num_square_clauses==int(factorial(N**2)/factorial(2)/factorial(N**2-2))*N**2)

		assert((num_column_clauses+num_row_clauses+num_square_clauses)*N**2 == 3*(N**8-N**6)/2)

		# Writes non-zeros as conjunctions
		non_zeros = np.nonzero(self.grid)
		sat_variable_list = []
		for index in zip(list(non_zeros[0]),list(non_zeros[1])):
			sat_variable = [index[0]*N**4 + index[1]*N**2 + self.grid[index[0],index[1]]]
			sat_variable_list+=sat_variable


		num_clauses = sum([
			len(completeness_clauses),
			len(unicity_clauses)*len(unicity_clauses[(0,0)]),
				(num_column_clauses+num_row_clauses+num_square_clauses)*N**2
		])

		output = 'p cnf '+str(len(variables.keys()))+' '+str(num_clauses)+'\n'

		# No need for +1 here as it comes from the Sudoku string
		for elem in sat_variable_list:
			output+=str(elem)+' 0\n'

		# From here onwards each digit 'd' should get a +1, as 0's are invalid
		for elem in completeness_clauses.values():
			output+= ' '.join([str(x+1) for x in elem])+' 0\n'

		for elem in unicity_clauses.values():
			clauses = []
			for pair in elem:
				clauses += [('-'+str(pair[0]+1),'-'+str(pair[1]+1))]
			clauses = [str(x[0])+' '+str(x[1]) for x in clauses]
			output += ' 0 '.join(clauses)
			output += ' 0\n'

		num_column_clauses = len(column_validity_clauses[0])*len(column_validity_clauses)
		num_row_clauses = len(row_validity_clauses[0])*len(row_validity_clauses)
		num_square_clauses = len(square_validity_clauses[0])*len(square_validity_clauses)

		for elem in column_validity_clauses.values():
			for clause in elem:
				left = ['-'+str(digit+1) for digit in clause[0]]
				right = ['-'+str(digit+1) for digit in clause[1]]
				demorgan = [str(x[0])+' '+str(x[1]) for x in list(itertools.product(left,right))]
				# print(" 0 ".join(demorgan))
				output += " 0 ".join(demorgan)+'\n'
				output += " 0 "+'\n'


		for elem in row_validity_clauses.values():
			for clause in elem:
				left = ['-'+str(digit+1) for digit in clause[0]]
				right = ['-'+str(digit+1) for digit in clause[1]]
				demorgan = [str(x[0])+' '+str(x[1]) for x in list(itertools.product(left,right))]
				# print(" 0 ".join(demorgan))
				output += " 0 ".join(demorgan)+'\n'
				output += " 0 "+'\n'


		for elem in square_validity_clauses.values():
			for clause in elem:
				left = ['-'+str(digit+1) for digit in clause[0]]
				right = ['-'+str(digit+1) for digit in clause[1]]
				demorgan = [str(x[0])+' '+str(x[1]) for x in list(itertools.product(left,right))]
				# print(" 0 ".join(demorgan))
				output += " 0 ".join(demorgan)+'\n'
				output += " 0 "+'\n'

		return output