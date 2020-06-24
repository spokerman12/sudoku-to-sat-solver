# main.pyimport sys
import os
import sys

from Sudoku import Sudoku
from SAT import SAT

# Windows needs this to print the colors
if os.name == 'nt':
	import colorama
	colorama.init()


def sudoku_to_sat(file, filename, write_to_file=False):

	if write_to_file:
		dirname = os.path.split(os.path.abspath(__file__))[0]+'/'+filename
		os.makedirs(os.path.dirname(dirname), exist_ok=True)

	sudoku_list = []
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
			sat_sudoku = sudoku.to_sat()
			if write_to_file:
				with open(dirname+'/'+filename+str(file_counter),'+w') as file:
					file.write(sat_sudoku)
				print('^This^ Sudoku written as SAT to file',filename+'_'+str(file_counter))
				file_counter+=1
		
			sudoku_list.append(sat_sudoku)
	return(sudoku_list)

def solve_sudoku_zchaff(filename):
	cmd = './zchaff64/zchaff '+sudoku.to_sat()+' 1000'
	so = os.popen(cmd).read()
	print(so)
	# sat.solve(sudoku.to_sat())
	return
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
			sudoku_list = sudoku_to_sat(file, filename)
			# print(sudoku_list)
			for sudoku in sudoku_list:
				new_sat = SAT()
				print(new_sat.solve_sat(sudoku))

		elif sys.argv[1] == 'solve_sudoku_zchaff':
			pass
		elif sys.argv[1] == 'sudoku_to_sat':
			if len(sys.argv) == 4 and sys.argv[3] == 'save':
				sudoku_to_sat(file, filename, write_to_file=True)
			else:
				sudoku_to_sat(file, filename)

		elif sys.argv[1] == 'sat_to_sudoku':
			pass
		elif sys.argv[1] == 'solve_sat':
			pass
		else:
			print('42')
