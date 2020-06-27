# main.pyimport sys
import os
import sys

from Sudoku import Sudoku

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
			print('Sudoku written as SAT to file','output'+str(file_counter))
			file_counter+=1
		
		path_list.append(dirname+'/output'+str(file_counter))
			
	return (path_list,sudoku_list)

def solve_sudoku_zchaff(path):
	cmd = './zchaff64/zchaff '+path+' 1000'
	cmd_output = os.popen(cmd).read()
	return cmd_output

def solve_sudoku():
	return
def sat_to_sudoku():
	return
def solve_sat():
	return




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
			print(solve_sudoku_zchaff(filename))

		elif sys.argv[1] == 'sudoku_to_sat':
			path_list, _ = sudoku_to_sat(file)

		elif sys.argv[1] == 'sat_to_sudoku':
			pass
		elif sys.argv[1] == 'solve_sat':
			# solve sat
			pass

		elif sys.argv[1] == 'full_solve':
			path_list, sudoku_list = sudoku_to_sat(file)
			
			print(path_list)
			for sudoku in path_list:

				# solve sat
				pass
		elif sys.argv[1] == 'full_solve_zchaff':
			# solve sat
			pass
		else:
			print('42')
