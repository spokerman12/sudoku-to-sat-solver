import re
from queue import PriorityQueue

def read_sat(s) :
    A = []
    B = []
        
    for line in s.split("\n") :
        if len(line) == 0 : continue
        if line[0] == "c" : continue
        elif line[0] == "p" :
            read_line = line[2:].strip('\n')
            result = re.findall(r'[^\s]+', read_line)
            B.append(int(result[1]))
            A.append([])
        else :
            result = [int(i) for i in re.findall(r'[^\s]+', line)]
            A[-1].append(result)

    return [(B[i], A[i]) for i in range(len(A))]

def simplify(var, clauses) :
    i = 0
    while i < len(clauses) :
        j = 0
        while j != len(clauses[i]) :
            if clauses[i][j] == var :
                clauses.pop(i)
                i -= 1
                break
            elif clauses[i][j] == -var :
                if len(clauses[i]) == 1 :
                    clauses.pop(i)
                    i -= 1
                    break
                else :
                    clauses[i].pop(j)
                    j -= 1
            j +=1
        i += 1
    return clauses

def valid(var, clauses) :
    for clause in clauses :
        if len(clause) == 1 and clause[0] == -var :
            #print("chao", var)
            return False
    return True

def occurrences(var, clauses) :
    ok1 = ok2 = True
    acum = 0
    for clause in clauses :
        for v in clause :
            if len(clause) == 1 :
                if v == var :
                    ok2 = False
                elif v == -var :
                    ok1 = False
            if v == var or v == -var :
                acum += 1
    #print(var, ok1, ok2, acum)

def ssat(nvars, clauses, values=set(), cola=None) :
    #print(clauses)
    if len(clauses) == 0 :
        for i in range(nvars) :
            if not i in  values and not -i in values :
                values.add(i)
    if len(values) == nvars and len(clauses) == 0 :
        #print("gg", values)
        return values
    """
    if cola is None :
        cola = PriorityQueue()
        for i in range(nvars) :
            occurrences(i, clauses)
    """
    for i in range(nvars) :
        if not(valid(i, clauses)) and not(valid(-i, clauses)) :
            #print("RIP")
            return None
        for v in [i, -i] :
            if (not v in values) and (not -v in values) :
                if not valid(v, clauses) : continue
                simple = simplify(v, clauses)
                values.add(v)
                #print(v)
                r = ssat(nvars, simple, values)
                if r : return r
    return None

def format_sat(instance) :
    solution = ssat(instance[0], instance[1])
    if solution :
        return "s cnf 1 " + str(instance[0]) + "\n" + "\n".join(["v "+str(v) for v in solution])
    else :
        return "s cnf 0 " + str(instance[0])

def solve_sat(s) :
    output = ""
    for instance in read_sat(s) :
        output += format_sat(instance) + "\n"
    return output

if __name__ == '__main__':
    s =  "c perro\np cnf 5 5\n 2 -4\n 4\n-3\n"
    #s = ""
    s += "c perro\np cnf 5 5\n-4\n4\n-3"
    ss = "c gato"
    print(solve_sat(s))
    
