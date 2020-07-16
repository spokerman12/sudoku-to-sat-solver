import re
import time


import multiprocessing

from queue import PriorityQueue

from timeit import default_timer as timer

from Sudoku import Sudoku


def read_sat(s):
    Clauses = []
    Variables = []

    p = False
    p2 = False
    for line in s.split("\n"):
        if len(line) == 0:
            continue
        if line[0] == "c":
            continue
        else:
            line = line.strip("\n")
            line = re.findall(r"[^\s]+", line)
        for i in range(len(line)):
            if len(line[i]) == 0:
                continue
            if line[i] == "p":
                p = True
                continue
            if line[i] == "cnf" and p:
                continue
            if p:
                Variables.append(int(line[i]))
                Clauses.append([])
                p = False
                p2 = True
                continue
            elif p2:
                p2 = False
            else:
                if len(Clauses[-1]) == 0 or line[i] == "0":
                    Clauses[-1].append([])
                if line[i] != "0":
                    Clauses[-1][-1].append(int(line[i]))
    instances = [(Variables[i], Clauses[i]) for i in range(len(Clauses))]
    return instances


def simplify(varss, clauses):
    if len(clauses) < 500:
        print(len(clauses))
    clauses = [i.copy() for i in clauses]
    i = 0
    while i < len(clauses):
        if len(clauses[i]) == 0:
            clauses.pop(i)
            i -= 1
            continue
        j = 0
        while j != len(clauses[i]):
            if clauses[i][j] in varss :
                clauses.pop(i)
                i -= 1
                break
            elif -clauses[i][j] in varss :
                if len(clauses[i]) == 1:
                    return None
                    clauses.pop(i)
                    i -= 1
                    break
                else:
                    clauses[i].pop(j)
                    j -= 1
            j += 1
        i += 1
    return clauses


def valid(nvars, clauses, values) :
    valids = set()
    niceness = {}
    for i in range(1, nvars+1) :
        ni = -i
        niceness[i] = None
        niceness[ni] = None
        if i in values or ni in values :
            continue
        valids.add(i)
        valids.add(ni)
    
    for clause in clauses :
        if len(clause) == 0 : continue
        var = clause[0]
        nvar = -var
        
        if len(clause) == 1 :
            if not var in valids :
                return PriorityQueue()
            if nvar in valids :
                valids.remove(nvar)

        for v in clause :
            if niceness[v] :
                niceness[v] = min(niceness[v], len(clause))
            else :
                niceness[v] = len(clause)

    q = PriorityQueue()
    for i in valids :
        if niceness[i] :
            if i < 0 and niceness[i] > 1 :
                niceness[i] += 1
            q.put((niceness[i], i))
        elif i > 0 and niceness[-i] is None  :
            values.add(i)
    return q


def ssat(nvars, claus, vals=set(), blacklist=set()):
    #print(len(vals), len(claus))
    #if len(claus) <= 20 : print(claus)
    clauses = [i.copy() for i in claus]
    values = vals.copy()
    blacklist = blacklist.copy()
    if len(values) == nvars and len(clauses) == 0:
        return values
    
    valids = valid(nvars, clauses, values)

    # deducting loop
    fresh = True
    while (not valids.empty()) and fresh :
        
        peek = valids.get()
        if peek[0] == 1 :
            v = peek[1]
            fresh = False
        elif fresh :
            valids.put(peek)
            break
        else :
            fresh = True
            valids = valid(nvars, clauses, values)
            continue

        if -v in values or v in blacklist :
            return None
        values.add(v)
        clauses = simplify({v}, clauses)
        if clauses is None : return None

    # backtracking loop ##################
    while not valids.empty():
        print('loop2') 
        # print(valids.queue)
        v = valids.get()[1]
        if v in blacklist:
            continue
        if not v in values and not -v in values:
            simple = simplify({v}, clauses)
            if simple is None :
                #print(len(vals), "susto", v)
                if -v in blacklist:
                    return None
                else:
                    blacklist.add(v)
                continue
            values.add(v)
            r = ssat(nvars, simple, values, blacklist)
            if r:
                return r
            values.remove(v)
            if -v in blacklist:
                return None
            else:
                blacklist.add(v)
    if len(values) == nvars and len(clauses) == 0:
        return values
    return None


def verify(solution, clauses):
    for clause in clauses:
        for i in range(len(clause)):
            if clause[i] in solution:
                break
            if i == len(clause) - 1:
                print(clause)
                return False
    return True


def format_sat(instance):
    aaa = [i.copy() for i in instance[1]]
    solution = ssat(instance[0], instance[1], set())
    #print(solution)
    if solution:
        assert(verify(solution, instance[1]))
        return (
            "s cnf 1 "
            + str(instance[0])
            + "\n"
            + "\n".join(["v " + str(v) for v in solution])
        )
    else:
        return "s cnf 0 " + str(instance[0])


def solve_sat(s, return_dict):
    output = ""
    for instance in read_sat(s):
        output += format_sat(instance) + "\n"
        break
    return_dict["solve_sat"] = output
    return output


def solve_sat_timeout(s, time_limit):
    try:
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        process = multiprocessing.Process(target=solve_sat, args=(s, return_dict))
        process.start()
        process.join(time_limit)
        if process.is_alive():
            process.terminate()
            return 0
        else:
            return return_dict["solve_sat"]
    except Exception as e:
        print("Error occurred,", e)


if __name__ == '__main__':
    file = open('sudo3.txt').read()
    print(solve_sat(file,{}))
