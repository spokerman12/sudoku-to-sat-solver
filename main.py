# main.pyimport sys
import os
import sys
import re

from time import sleep
from Sudoku import Sudoku
from SAT import solve_sat

# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()


def sudoku_to_sat(input_file):

	dirname = os.path.split(os.path.abspath(__file__))[0]+'/output'
	os.makedirs(os.path.dirname(dirname), exist_ok=True)

	path_list = []
	sudoku_list = []
	file_counter = 0
	for line in input_file.readlines():
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
			sudoku_list.append(sudoku)
			sat_sudoku = sudoku.to_sat()
		
			with open(dirname+'/output'+str(file_counter),'+w') as output_file:
				output_file.write(sat_sudoku)
		
			path_list.append(dirname+'/output'+str(file_counter))
			file_counter+=1
			
	return (path_list,sudoku_list)

def solve_sudoku_zchaff(path):
	cmd = './zchaff64/zchaff '+path+' 1000'
	cmd_output = os.popen(cmd).read()
	return cmd_output

def solve_sudoku():
	return
def sat_to_sudoku():
	return
# def solve_sat(file):
# 	so
# 	return




if __name__ == '__main__':
	if len(sys.argv) != 1:
		print ("Loading file %s" % (sys.argv[2]))
	else:
		print ("No input provided. For instructions, please read README.md")
		sys.exit(1)

	filename = sys.argv[2]

	with open(filename) as file:
		if sys.argv[1] == 'solve_sudoku':
			path_list, _ = sudoku_to_sat(file)
			print(path_list)
			for sudoku in path_list:
				# solve sat
				pass

		elif sys.argv[1] == 'solve_sudoku_zchaff':
			solution = solve_sudoku_zchaff(filename)
			solution = solution.split('Random Seed Used')[0]
			solution = solution.split('Instance Satisfiable')[1]
			digit_list = []
			all_the_digits = re.findall('-?\d+',solution)

			for digit in all_the_digits:
				if int(digit) > 0:
					digit_list.append(int(digit))
			sudoku = Sudoku()
			sudoku.solution_from_sat(digit_list)
			sudoku.print()

		elif sys.argv[1] == 'sudoku_to_sat':
			path_list, _ = sudoku_to_sat(file)

		elif sys.argv[1] == 'sat_to_sudoku':
			pass
		elif sys.argv[1] == 'solve_sat':
			solve_sat(sys.argv[2])
			pass

		elif sys.argv[1] == 'full_solve':
			path_list, sudoku_list = sudoku_to_sat(file)
			for sudoku in path_list:
				# print sudoku
				# solve sat
				# print solved sat as sudoku
				pass
		elif sys.argv[1] == 'full_solve_zchaff':
			path_list, sat_sudokus = sudoku_to_sat(file)
			i = 0 
			for path in path_list:
				print('Sudoku #',i)
				print('Unsolved')
				sat_sudokus[i].print()
				solution = solve_sudoku_zchaff(path)
				solution = solution.split('Random Seed Used')[0]
				solution = solution.split('Instance Satisfiable')[1]
				digit_list = []
				all_the_digits = re.findall('-?\d+',solution)

				for digit in all_the_digits:
					if int(digit) > 0:
						digit_list.append(int(digit))
				sudoku = Sudoku()
				sudoku.solution_from_sat(digit_list)
				print("Solved")
				sudoku.print()
				break

				i+=1
		else:
			print('42')
