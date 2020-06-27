# Sudoku-to-SAT-solver
Transforms a Sudoku to a boolean SAT problem and solves it 

## Installation:
- Clone this repository, say in `~/sudoku-to-sat-solver`
- Create a virtualenv, if you care about your current Python installation.
- Do `pip install -r requirements.txt`
- Install zChaff from https://www.princeton.edu/chaff/zchaff.html. You may need to fix an import. It's easy.
- Make sure that the zchaff64 dir is in `~/sudoku-to-sat-solver`

## Instructions

You can use this program like so:

	python main.py <command> <input_file> <time_limit>

### Input types:

**SUDOKU file**: A file where each line is formatted like this:

	3 000400009020980030093000840000000000200008067160300002049000650600003000000059010

Where "3" is the size of the Sudoku board and the rest are the existing digits, read from left to right and top to bottom, 0 being a blank space and the other numbers being themselves.

**DIMACS SAT INPUT**: A file formatted like this:
	
	c Example file
	c
	p cnf 4 3
	1 3 -4 0
	4 0 2
	-3

Where:
- Lines starting with 'c' are comments and will be ignored
- Lines starting with p contain the form (cnf is the only supported one), number of variables and number of lines
- Other lines with each variable number, where '-' represents negation and 0 represents conjunction.

This "Example file" represents the boolean expression: φ = (X1 ∨ X3 ∨ ¬X4) ∧ X4 ∧ (X2 ∨ ¬X3).

The ∧ / 0's separate each clause. In the file, these can be broken in different lines, like in the example.


### Commands:
- **sudoku_to_sat**:  Takes a file with 'n' SUDOKU strings and produces 'n' DIMACS SAT INPUT files in `output/`

- **solve_sat**: Takes a DIMACS SAT INPUT file, solves it using our solver and reports the solution as a Sudoku.

- **full_solve**: Takes a file with 'n' SUDOKU strings, produces 'n' DIMACS SAT INPUT files in `output/`, and solves each of them using our solver. Reports the results.

- **full_solve_zchaff**: Takes a file with 'n' SUDOKU strings, produces 'n' DIMACS SAT INPUT files in `output/`, and solves each of them using zChaff. Reports the results.

- **compare_solvers**: Takes a file with 'n' SUDOKU strings, produces 'n' DIMACS SAT INPUT files in `output/`, and solves each of them using both solvers. Reports time.

### Time limit:

You can set a timeout value for the algorithm you wish to execute. The default is 100 seconds.


## About our implementation:

### Our Solver

![alt text](https://github.com/spokerman12/sudoku-to-sat-solver/blob/daniel/comparison.png?raw=true)

### Translating Sudokus to SAT

Thanks to the clauses proposed by the course's teachers, 