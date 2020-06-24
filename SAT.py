import re
from queue import PriorityQueue

def leer_sat(s) :
    A = []
    B = []
        
    for line in s.split("\n") :
        if line[0] == "c" : continue
        elif line[0] == "p" :
            read_line = line[2:].strip('\n')
            result = re.findall(r'[^\s]+', read_line)
            B.append(int(result[0]))
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

def solve_sat(nvars, clauses, values=set(), cola=None) :
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
                r = solve_sat(nvars, simple, values)
                if r : return r
    return None

def solved_sat(w) :
    r = solve_sat(w[0], w[1])
    if r :
        return "s cnf 1 " + str(w[0]) + "\n" + "\n".join(["v "+str(v) for v in r])
    else :
        return "s cnf 0 " + str(w[0])

if __name__ == '__main__':
    s =  "c perro\np 5 5\n 2 -4\n 4\n-3\n"
    #s = ""
    s += "c perro\np 5 5\n-4\n4\n-3"
    ss = "c gato"
    for w in leer_sat(s) :
        #print(w)
        ss += "\n" + solved_sat(w)
    print(ss)
    
