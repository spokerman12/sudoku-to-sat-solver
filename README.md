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

- Backtracking: One of the go-to techniques to solve this problem. When testing out variable assignments, one must go back to try different paths. Basically, we're transversing a tree, and when we get to a "dead end", we go back. The branches are the many subproblems that we can find in the current input.

- Simplification: We make use of the properties of the disjunction to more easily get rid of variables, as if we are testing P, we can get rid of (T v U v J v K v P).

## New Version Improvements

- Bifurcation Heuristic: Valid allows us to build a priority queue with the elements worth testing where the priority is their 'niceness'. As it gets built, the unasigned variables (which occur in no clause) that have no proposed niceness are implied as 'True'. Valid returns a priority queue; if there's a contradiction among the variables and any clause, it returns an empty queue. Basically, putting a 3 in a column's slot where that column slots' rows also have 3's is a 'nice' assignment, because 3 is more likely to be correct. The niceness of a literal is the number of clauses in which it occurs plus the sum of the multiplicative inverse of the length of the clauses in which it occurs negated. Additionally, if during the backtracking it is found that a literal leads to an unsolvable SAT instance, the negation of the literal is placed on top of the priority queue. This allows the solver to discard unsatisfiable subtrees quicker.

- Unitary Clause Propagation: If a clause that contains a single literal is found, the corresponding variable is assigned to the value of the literal immediately (without backtracking). Backtracking isn't necessary for these assignations because they either are correct for the current subtree or the whole subtree is unsatisfiable.

- Blacklisting: If a literal has been found to lead to an unsatisfiable result for a subproblem, it is added to a 'blacklist' (implemented with a set), these literals are not worth checking for validity in the current subtree. If a literal is 'nice' but blacklisted, it is not considered for testing in that subproblem. If both a variable and its negation are blacklisted, the whole subtree is discarded.

- Simplification: We make use of the properties of the disjunction to more easily get rid of variables, as if we are testing P, we can get rid of (T v U v J v K v P).

## How our solver compares to zChaff
![alt text](https://github.com/spokerman12/sudoku-to-sat-solver/blob/master/new_comparison.png?raw=true)

Here is a graph of how our solver fared against zChaff on all 45 Sudokus in test_input.txt using a time limit of 60s. Needless to say, if it reached 60s then it timed out. Check out report-test_input and oldreport files to see a more detailed summary.

zChaff is a VERY fast SAT solver. Our solver could not handle a decent chunk of the problems. It requires a more detailed analysis on its code and structures.

However, we did find out that most approaches depend on backtracking (such as DPPL). Backtracking was our first choice in implementation.

Also, Python is **not** the best language to write this program in. We chose it on a matter of simplicity and consent among the developers. Python assigns values by references and because it's an interpreted language, it doesn't run its scripts as fast as a compiled program, such as zChaff, which is written in C++.

C++ would've been great. Or perhaps Rust. We considered Haskell but 33% of the team was very rusty on it. It would've been interesting in Prolog... but time was a constraint. 

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
- **A valid Sudoku solution has no repeating digits among its subsections (rows, columns, N x Nsquares)**: `¬Xd_s1 v ¬Xd_s2` for each section 's', these both being either rows, columns or squares. 

### Analyzing resource management

If variables are in a set V, and clauses in a set C

The most important processes in this set of programs, and their time complexity are:

**simplify**: With two nested loops, it takes O(|C|x|V|) = O(C^2). This method gets called by ssat each time the set of valid variables is not empty and it depends on how many variables are per clause. Worst case is every variable is in every clause.

**valid**: Verifying whether the expression is True or False given a set of variable assignments takes O(|V|), as this method calculates the 'niceness' of each variable to decide on what to do next.

**ssat**: This method, firstly ignoring our optimizations, can have a worst case of having to test every variable for each clause. That would be O(2^|V| x (|V|+|C|))

Keep in mind that the number of clauses and variables are:
	
	|V| = N^6
	|C| = N^2 + bin(N^2) x N^4 + 3xN^2xbin(N^2,2)xN^2
	
	O(2 ^ N^6 x (N^6+N^2 + bin(N^2) x N^4 + 3 x N^2 x bin(N^2,2) x N^2)) 

Now, taking into account the techniques and heuristics we used, we can expect that at least |V| x |C| clauses would be cancelled, as there should be at least N^3 of each digit in the grid, but since we are focused on the worst case, we prefer to leave at that.

Still, we could claim that the time complexity of our solver is as follows:

	O(2 x N^6 x (N^6+N^2 + bin(N^2) x N + 3 x bin(N^2,2)x N)) 
	
### Authors:

ShonTitor (Leonardo López)
spokerman12 (Daniel Francis)
LuigiCamilo (Luigi DiMartino)
