# SATurday Night Solver
## a Sudoku-to-SAT solver
Transforms a Sudoku to a boolean SAT problem and solves it 

## Installation:
- Clone this repository, say in `~/sudoku-to-sat-solver`
- Create a virtualenv, if you care about your current Python installation.
- Do `pip install -r requirements.txt`
- Install zChaff from https://www.princeton.edu/~chaff/zchaff.html. You may need to fix an import. It's easy.
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

Our solver is based on the following methods:

- read_sat: Reads a DIMACS_SAT format file and creates a list of subproblems.

- simplify: Eliminates all clauses where the variable being tested 'P' occurs, likewise with all occurences of '¬P'

- valid: Obtains the 'niceness' of each variable for the given clause. This would be the minimum length of the clause 'C' so that the variable occurs in 'C'.

- ssat: Attempts to solve a SAT problem, backtracking and carrying over a blacklist of up-to-no-good variables. Read next section for more on these terms.
- verify: With a set of variable assignments, checks out whether the given clauses are True or False. 

- format_sat: Returns a solution in DIMACS SAT format.

- solve_sat: The main procedure for the solver. Attempts to solve a SAT problem.

- solve_sat_timeout: Same as solve_sat, only that it imposes a process timeout to make sure that the program finishes.

## Techniques

- Niceness: Valid allows us to build a priority queue with the elements worth testing where the priority is their 'niceness'. As it gets built, the unasigned variables (which occur in no clause) that have no proposed niceness are implied as 'True'. Valid returns a priority queue; if there's a contradiction among the variables and any clause, it returns None.

- Backtracking: One of the go-to techniques to solve this problem. When testing out variable assignments, one must go back to try different paths. Basically, we're transversing a tree, and when we get to a "dead end", we go back. The branches are the many subproblems that we can find in the current input.

- Blacklisting: Some variables are not worth checking for validity in a new subproblem. If a variable is 'nice' but is blacklisted, it is not considered for testing in that subproblem.

- Simplification: We make use of the properties of the disjunction to more easily get rid of variables, as if we are testing P, we can get rid of (T v U v J v K v P).

## How our solver compares to zChaff
![alt text](https://github.com/spokerman12/sudoku-to-sat-solver/blob/master/comparison.png?raw=true)

For more details, check out `report-test_input.txt`

### Translating Sudokus to SAT

Thanks to the clauses proposed by the course's teachers, it wasn't too hard to translate the Sudokus to and from DIMACS SAT formats.

The clauses were modeled using Python dictionaries and using a Numpy matrix as a grid.

A SAT variable 'D' can be transformed into a Sudoku digit 'd' using the formula:

	D = N**4 * i + N**2 * j + d

Where 'N' is the order of the Sudoku (3 is default) 'i' are the rows and 'j' are the columns. There are N^6 variables.

Knowing that, Xd_ij represents the digit 'd' on row 'i' and column 'j'...

we modeled the following sets of clauses (conjunctions):
- **A valid Sudoku solution has no empty slots**: `Disjunction for all Xd_ij for 1<=d<=N^2`. There are N^2 clauses of this kind.
- **A valid Sudoku solution has only one number per slot**: `¬Xd_ij v ¬Xd'_ij`. There are bin(N^2,2) x N^4 clauses of this kind.
- **A valid Sudoku solution has no repeating digits among its subsections (rows, columns, N x Nsquares)**: `¬Xd_s1 v ¬Xd_s2'` for each section 's', these both being either rows, columns or squares. 

