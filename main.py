# main.pyimport sys
import os
import sys
import re

import matplotlib.pyplot as plt
import unittest 
import threading

from timeit import default_timer as timer
from Sudoku import Sudoku
from SAT import solve_sat_timeout
from file_helpers import sudoku_to_sat, solve_sudoku_zchaff 
from pprint import pprint

# Windows needs this to print the colors
if os.name == "nt":
    import colorama
    colorama.init()


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
        time_limit = 120
        print("Using default time of",time_limit,"seconds")

    with open(filename) as file:

        # sudoku_to_sat: Translates a single file of 'n' sudokus to
        #               'n' DIMACS SAT files
        if sys.argv[1] == "sudoku_to_sat":
            path_list, _ = sudoku_to_sat(file)

        # solve_sat: Solves a single SAT from a DIMACS SAT input file
        elif sys.argv[1] == "solve_sat":
            start = timer()
            output = solve_sat_timeout(file.read(),time_limit)
            end = timer()

            if type(output) != type('string'):
                result ='Time out. Moving on.'
                our_time = time_limit
            else:
                all_digits = [
                    int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
                ]

                digit_list = []
                for digit in all_digits:
                    if digit > 0:
                        digit_list.append(int(digit))                

                our_sudoku = Sudoku()
                our_sudoku.solution_from_output(digit_list)
                our_time = round(end - start,6)
                percent_diff = round(abs(zchaff_time-our_time)/zchaff_time,2)
                result = "Our solver solved in "+str(our_time)+" seconds, "+str(percent_diff)+"% of zChaff"
                our_sudoku.print()
            
            print(result)
            

        # full_solve: Solves all sudokus from an input file
        elif sys.argv[1] == "full_solve":
            path_list, sat_sudokus = sudoku_to_sat(file)
            i = 0
            print("Solving with our solver")
            for path in path_list:
                print("- - - Sudoku #"+str(i)+"- - -")
                sat_sudokus[i].print(to_console=True)
                file = open(path,'r')

                start = timer()
                output = solve_sat_timeout(file.read(),time_limit)
                end = timer()


                if output == (0):
                    result ='Time out. Moving on.'
                    our_time = time_limit
                elif output is None or "s cnf 0" in output:
                    result = "Unsatisfiable (Or could not satisfy?)"
                else:
                    all_digits = [
                        int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
                    ]

                    digit_list = []
                    for digit in all_digits:
                        if digit > 0:
                            digit_list.append(int(digit))                

                    our_sudoku = Sudoku()
                    our_sudoku.solution_from_output(digit_list)
                    our_time = round(end - start,6)
                    result = "Our solver solved in "+str(our_time)+" seconds."
                    our_sudoku.print(to_console=True)
                
                print(result)
                i += 1
                if i == 7:
                    break

        # full_solve_zchaff: Using zChaff, solves all sudokus from an input file
        elif sys.argv[1] == "full_solve_zchaff":
            path_list, sat_sudokus = sudoku_to_sat(file)
            i = 0
            print("Solving with zChaff")
            for path in path_list:
                print("- - - Sudoku #"+str(i)+"- - -")
                sat_sudokus[i].print(to_console=True)
                
                start = timer()
                solution = solve_sudoku_zchaff(path,time_limit)
                end = timer()
                zchaff_time = round(end - start,6)
                if "Unsatisfiable" in solution:
                    result="Unsatisfiable! Time elapsed:"+str(zchaff_time)+'\n'
                    continue
                else:
                    solution = solution.split("Random Seed Used")[0]
                    solution = solution.split("Instance Satisfiable")[1]
                    digit_list = []
                    all_digits = re.findall("-?\d+", solution)

                    for digit in all_digits:
                        if int(digit) > 0:
                            digit_list.append(int(digit))
                    zchaff_sudoku = Sudoku()
                    zchaff_sudoku.solution_from_sat(digit_list)
                    result ="zChaff solved in "+ str(zchaff_time)+" seconds"
                    sudoku.print()
                print(result)
                i += 1

        # compare_solvers: Solves all sudokus from an input file using
        #                   zChaff and our solver. Compares results and
        #                   plots them.
        elif sys.argv[1] == "compare_solvers":
            report_text = ''
            with open('report-'+sys.argv[2]+'.txt','w') as report:
                path_list, sat_sudokus = sudoku_to_sat(file)
                i = 0
                zchaff_times = []
                our_solver_times = []
                for path in path_list:
                    print("- -  -  Sudoku #"+str(i)+'  -  - -')
                    sat_sudokus[i].print(to_console=True)
                    report_text += "- - -  Sudoku #"+str(i)+'  - - -'+'\n'

                    # zChaff
                    start = timer()
                    solution = solve_sudoku_zchaff(path,time_limit)
                    end = timer()
                    zchaff_time = round(end - start,6)
                    if "Unsatisfiable" in solution:
                        result="Unsatisfiable! Time elapsed:"+str(zchaff_time)+'\n'
                        report_text += result
                        continue
                    else:
                        try:
                            solution = solution.split("Random Seed Used")[0]
                            solution = solution.split("Instance Satisfiable")[1]
                            digit_list = []
                            all_digits = re.findall("-?\d+", solution)

                            for digit in all_digits:
                                if int(digit) > 0:
                                    digit_list.append(int(digit))
                            zchaff_sudoku = Sudoku()
                            zchaff_sudoku.solution_from_sat(digit_list)
                            result ="zChaff solved in "+ str(zchaff_time)+" seconds"
                        except:
                            result+= "Time out. Moving on'\n'"
                    
                    print(result)
                    report_text += result
                    zchaff_times.append(zchaff_time)


                    # Our solver
                    file = open(path,'r')
                    start = timer()
                    output = solve_sat_timeout(file.read(),time_limit)
                    end = timer()
        
                    if output is None or "s cnf 0" in output:
                        result = "Unsatisfiable (Or could not satisfy?)"
                    elif output == (0):
                        result ='Time out. Moving on.'
                        our_time = time_limit
                        report_text += str(result)
                    else:
                        all_digits = [
                            int(x.strip("v ")) + 1 for x in re.findall("v -?\d+", output)
                        ]

                        digit_list = []
                        for digit in all_digits:
                            if digit > 0:
                                digit_list.append(int(digit))                

                        our_sudoku = Sudoku()
                        our_sudoku.solution_from_output(digit_list)
                        our_time = round(end - start,6)
                        percent_diff = round(abs(zchaff_time-our_time)/zchaff_time,2)
                        result = "Our solver solved in "+str(our_time)+" seconds, "+str(percent_diff)+"% of zChaff\n"
                        
                        # zchaff_sudoku.print()
                        # our_sudoku.print()

                        j,k =0,0 
                        for j in range(9):
                            for k in range(9):
                                assert(our_sudoku.grid[j][k]==zchaff_sudoku.grid[j][k])    
                        
                        report_text += zchaff_sudoku.print()
                        report_text += str(result)
                    
                    print(result)
                    zchaff_sudoku.print(to_console=True)
                    our_solver_times.append(our_time)

                    i += 1
                    print('')
                    if i == 3:
                        break

                summary='Summary:\n'
                summary+='Using a time limit of '+str(time_limit)+' seconds.\n'
                for j in range(i):
                    summary+='Sudoku #'+str(j)+': zChaff:'+str(zchaff_times[j])+'s'+' | Our Solver:'+str(our_solver_times[j])+'s |'+'\n'
                print(summary)
                plt.plot(list(range(i)),our_solver_times, label='Our solver',color='blue')
                plt.plot(list(range(i)),zchaff_times, label='zChaff',color='orange')
                plt.xlabel('Sudoku #')
                plt.ylabel('Time elapsed in seconds')
                plt.legend(loc='best')
                plt.savefig('comparison.png')
                report_text+=summary
                report.write(report_text)
        else:
            print("42")
