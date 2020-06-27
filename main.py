# main.pyimport sys
import os
import sys
import re

import matplotlib.pyplot as plt

from timeit import default_timer as timer
from func_timeout import func_timeout, FunctionTimedOut
from Sudoku import Sudoku
from SAT import solve_sat_timeout

# Windows needs this to print the colors
if os.name == "nt":
    import colorama
    colorama.init()

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
def solve_sudoku_zchaff(path,time_limit):
    cmd = "./zchaff64/zchaff " + path + " "+str(time_limit)
    cmd_output = os.popen(cmd).read()
    return cmd_output

# Main procedure.
# Please refer to README.md for better info on how to use this
# program.
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Loading file %s" % (sys.argv[2]))
    else:
        print("No input provided. For instructions, please read README.md")
        sys.exit(1)

    filename = sys.argv[2]

    # Set the timeout value
    if len(sys.argv) == 4:
        try:
            time_limit = int(sys.argv[3])
            print('Time limit is',time_limit,'seconds')
        except Exception as e:
            print('Could not read time limit',e)
    else:
        time_limit = 100

    with open(filename) as file:

        # sudoku_to_sat: Translates a single file of 'n' sudokus to
        #               'n' DIMACS SAT files
        if sys.argv[1] == "sudoku_to_sat":
            path_list, _ = sudoku_to_sat(file)

        # solve_sat: Solves a single SAT from a DIMACS SAT input file
        elif sys.argv[1] == "solve_sat":
            output = solve_sat(file.read())
            all_the_digits = [
                int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
            ]

            digit_list = []
            for digit in all_the_digits:
                if digit > 0:
                    digit_list.append(int(digit))
            # print(len(digit_list))
            # print(digit_list,len(digit_list))
            # sudoku = Sudoku()
            # sudoku.solution_from_output(digit_list)
            # print("Solved")
            # sudoku.print()

        # full_solve: Solves all sudokus from an input file
        elif sys.argv[1] == "full_solve":
            path_list, sudoku_list = sudoku_to_sat(file)
            i = 0
            print("Solving with our solver")
            for sudoku in path_list:
                print("Sudoku #", i)
                print("Unsolved")
                sat_sudokus[i].print()
                start = timer()
                output = solve_sat_timeout(file.read(),time_limit)
                end = timer()
                all_the_digits = [
                    int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
                ]

                digit_list = []
                for digit in all_the_digits:
                    if digit > 0:
                        digit_list.append(int(digit))
                # print(len(digit_list))
                # print(digit_list,len(digit_list))
                # sudoku = Sudoku()
                # sudoku.solution_from_output(digit_list)
                # print("Solved in ",str(end-start),'seconds')
                # sudoku.print()

                break
                i += 1

        # full_solve_zchaff: Using zChaff, solves all sudokus from an input file
        elif sys.argv[1] == "full_solve_zchaff":
            path_list, sat_sudokus = sudoku_to_sat(file)
            i = 0
            print("Solving with zChaff")
            for path in path_list:
                print("Sudoku #", i)
                print("Unsolved")
                sat_sudokus[i].print()
                
                start = timer()
                try:# This block handles timeout and whether it's satisfiable or not
                    solution = func_timeout(time_limit,solve_sudoku_zchaff,args=(path,time_limit))
                    if "Unsatisfiable" in solution:
                        print("Unsatisfiable!")
                        continue
                except FunctionTimedOut:
                    print ( "Time out.\n")
                except Exception as e:
                    print ( "Error occurred,",e)
                end = timer()

                solution = solution.split("Random Seed Used")[0]
                solution = solution.split("Instance Satisfiable")[1]
                digit_list = []
                all_the_digits = re.findall("-?\d+", solution)

                for digit in all_the_digits:
                    if int(digit) > 0:
                        digit_list.append(int(digit))
                sudoku = Sudoku()
                sudoku.solution_from_sat(digit_list)
                print("Solved in ", str(end - start), "seconds")
                sudoku.print()
                break

                i += 1

        # compare_solvers: Solves all sudokus from an input file using
        #                   zChaff and our solver. Compares results and
        #                   plots them.
        elif sys.argv[1] == "compare_solvers":
            path_list, sat_sudokus = sudoku_to_sat(file)
            i = 0
            zchaff_times = []
            our_solver_times = []
            for path in path_list:
                print("Sudoku #", i)
                # print("Unsolved")
                # sat_sudokus[i].print()
                
                # zChaff
                print("Solving with zChaff")
                start = timer()
                try: # This block handles timeout and whether it's satisfiable or not
                    solution = func_timeout(time_limit,solve_sudoku_zchaff,args=(path,time_limit))
                    if "Unsatisfiable" in solution:
                        print("Unsatisfiable! Time elapsed:",str(end-start))
                        continue
                except FunctionTimedOut:
                    print ( "Time out.\n")
                except Exception as e:
                    print ( "Error occurred,",e)
                end = timer()

                solution = solution.split("Random Seed Used")[0]
                solution = solution.split("Instance Satisfiable")[1]
                digit_list = []
                all_the_digits = re.findall("-?\d+", solution)

                for digit in all_the_digits:
                    if int(digit) > 0:
                        digit_list.append(int(digit))
                sudoku = Sudoku()
                sudoku.solution_from_sat(digit_list)
                print("zChaff solved in ", str(end - start), "seconds")
                zchaff_times.append(end-start)

                # Our solver
                print("Solving with our solver")
                file = open(path,'r')

                start = timer()
                # try # This block handles timeout and whether it's satisfiable or not
                # output = solve_sat_timeout(file.read(),time_limit)
                # Ver el estado de la solucion
                end = timer()
                # all_the_digits = [
                #     int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
                # ]

                # digit_list = []
                # for digit in all_the_digits:
                #     if digit > 0:
                #         digit_list.append(int(digit))                

                # sudoku = Sudoku()
                # sudoku.solution_from_sat(digit_list)
                print("Our solver solved in ", str(end - start), "seconds")
                our_solver_times.append(end-start)


                # sudoku.print()

                i += 1

            plt.plot(list(range(i)),our_solver_times, label='Our solver')
            plt.plot(list(range(i)),zchaff_times, label='zChaff')
            plt.xlabel('Sudoku #')
            plt.ylabel('Time elapsed in seconds')
            plt.legend(loc='best')
            plt.show()
        else:
            print("42")
