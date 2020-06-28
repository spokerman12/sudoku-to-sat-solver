"""

File input helpers

"""
import os

from Sudoku import Sudoku

# Solves all the SUDOKU strings on an input file
def sudoku_to_sat(input_file):

    dirname = os.path.split(os.path.abspath(__file__))[0] + "/output"
    os.makedirs(os.path.dirname(dirname), exist_ok=True)

    path_list = []
    sudoku_list = []
    file_counter = 0
    for line in input_file.readlines():
        if line and line[0].isalnum():
            order = int(line[0])
            if order > 6:
                print("Order not supported. Ignoring")
                continue
            read_line = list(line[2:].strip("\n"))
            for i in range(len(read_line)):
                if read_line[i] == ".":
                    read_line[i] = 36
                elif not read_line[i].isdigit():
                    read_line[i] = ord(read_line[i])
                elif read_line[i] == " ":
                    continue
                else:
                    read_line[i] = int(read_line[i])
            sudoku = Sudoku(read_line, order)
            sudoku_list.append(sudoku)
            sat_sudoku = sudoku.to_sat()

            with open(dirname + "/output" + str(file_counter), "+w") as output_file:
                output_file.write(sat_sudoku)

            path_list.append(dirname + "/output" + str(file_counter))
            file_counter += 1

    return (path_list, sudoku_list)


# Calls up on zChaff to solve a SUDOKU file
def solve_sudoku_zchaff(path, time_limit):
    cmd = "./zchaff64/zchaff " + path + " " + str(time_limit)
    cmd_output = os.popen(cmd).read()
    return cmd_output
