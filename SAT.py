import re
from queue import PriorityQueue

def read_sat(s) :
    Clauses = []
    Variables = []

    p = False
    p2 = False
    for line in s.split("\n") :
        if len(line) == 0 : continue
        if line[0] == "c" : continue
        else :
            line = line.strip('\n')
            line = re.findall(r'[^\s]+', line)
        for i in range(len(line)) :
            if len(line[i]) == 0 : continue
            if line[i] == "p" :
                p = True
                continue
            if line[i] == "cnf" and p :
                continue
            if p :
                Variables.append(int(line[i]))
                Clauses.append([])
                p = False
                p2 = True
                continue
            elif p2 :
                p2 = False
            else :
                if len(Clauses[-1]) == 0 or line[i] == "0" :
                    Clauses[-1].append([])
                if line[i] != "0" :
                    Clauses[-1][-1].append(int(line[i]))
    instances = [(Variables[i], Clauses[i]) for i in range(len(Clauses))]
    #print(instances)
    return instances

def simplify(var, clauses) :
    nvar = -var
    i = 0
    while i < len(clauses) :
        if len(clauses[i]) == 0 :
            clauses.pop(i)
            i -= 1
            continue
        j = 0
        while j != len(clauses[i]) :
            if clauses[i][j] == var :
                clauses.pop(i)
                i -= 1
                break
            elif clauses[i][j] == nvar :
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

def valid(nvars, clauses, values) :
    #"""
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
                #print("chao", var)
                return PriorityQueue()
                #return set()
            if nvar in valids :
                valids.remove(nvar)

        for v in clause :
            nv = -v
            if niceness[v] :
                niceness[v] = min(niceness[v], len(clause))
            else :
                niceness[v] = len(clause)

            if niceness[nv] :
                niceness[nv] = min(niceness[nv], len(clause))
            else :
                niceness[nv] = len(clause)

    q = PriorityQueue()
    #dontcare = set()
    for i in valids :
        if niceness[i] :
            q.put((niceness[i], i))
        elif i > 0 and niceness[-i] is None  :
            #q.put((0, i))
            #dontcare.add(i)
            values.add(i)
    #return valids
    #print(valids)
    #print("CLAUSES", clauses, "\nNICENESS", niceness, "\nDONTCARE", dontcare)
    #print("\n")
    return q
    """
    valids = set()
    for i in range(1, 1+nvars) :
        ni = -i
        if i in values or ni in values :
            continue
        valids.add(i)
        valids.add(ni)
    for clause in clauses :
        if len(clause) == 1 :
            var = clause[0]
            nvar = -var
            if not var in valids :
                #print("chao", var)
                return set()
            if nvar in valids :
                valids.remove(nvar)
    #print(valids)
    """
    return valids

def ssat(nvars, claus, vals=set(), cola=None) :
    print(len(vals), len(claus))
    if len(claus) <= 20 : print(claus)
    clauses = [i.copy() for i in claus]
    values = vals.copy()
    if len(values) == nvars and len(clauses) == 0 :
        #print("gg")
        return values
    #valuesold = values.copy()
    valids = valid(nvars, clauses, values)
    valuesbackup = values.copy()
    #print(valids, clauses)
    #for v in valids :
    while not valids.empty() :
        v = valids.get()[1]
        #print(v)
        if not v in values and not -v in values :
            #print(v, "hola")
            simple = [i.copy() for i in clauses]
            simple = simplify(v, simple)
            values.add(v)
            r = ssat(nvars, simple, values)
            if r : return r
            #print("bachaqueando", v)
            values = valuesbackup.copy()
    if len(values) == nvars and len(clauses) == 0 :
        #print("gg")
        return values
    return None

def verify(solution, clauses) :
    for clause in clauses :
        for i in range(len(clause)) :
            if clause[i] in solution : break
            if i == len(clause)-1 :
                return False
    return True
        

def format_sat(instance) :
    aaa = [i.copy() for i in instance[1]]
    solution = ssat(instance[0], instance[1], set())
    #print(solution, aaa)
    if solution :
        assert(verify(solution, instance[1]))
        return "s cnf 1 " + str(instance[0]) + "\n" + "\n".join(["v "+str(v) for v in solution])
    else :
        return "s cnf 0 " + str(instance[0])

def solve_sat(s) :
    output = ""
    for instance in read_sat(s) :
        output += format_sat(instance) + "\n"
        break
    return output

if __name__ == '__main__':
    import os
    s =  "c perro\np cnf 5 5 \n -3 0 -2 4  0  -4  0  3 -5"
    #s = ""
    #s += "c perro\np cnf 5 5\n-4\n4 -2\n-3"
    f = open(os.path.join("output", "output1"), "r")
    #s = f.read()
    f.close()
    print(solve_sat(s))
    
