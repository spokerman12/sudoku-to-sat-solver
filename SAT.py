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
            result = [i for i in re.findall(r'[^\s]+', line)]
            A[-1].append(result)

    return [(B[i], A[i]) for i in range(len(A))]

def simplify(var, clauses) :
    if var[0] == "-" :
        nvar = var[1:]
    else :
        nvar = "-"+var
    i = 0
    while i < len(clauses) :
        j = 0
        while j != len(clauses[i]) :
            if clauses[i][j] == str(var) :
                clauses.pop(i)
                i -= 1
                break
            elif clauses[i][j] == str(nvar) :
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

# supone que se le pasa un entero no negativo
"""
def valid(var, clauses) :
    var = str(var)
    mvar = "-"+var
    okpos = True
    okneg = True
    valids = []
    for clause in clauses :
        if not(okpos or okneg) : break
        if len(clause) == 1 :
            if clause[0] == var :
                okpos = False
                #print("chao", var)
            elif clause[0] == mvar :
                okneg = False
                #print("chao", mvar)
    if okpos : valids.append(var)
    if okneg : valids.append(mvar)
    #print(valids, okpos, okneg)
    return valids
"""
def valid(nvars, clauses, values) :
    valids = set()
    for i in range(nvars) :
        i = str(i)
        ni = "-"+i
        if i in values or ni in values :
            continue
        valids.add(i)
        valids.add(ni)
    for clause in clauses :
        if len(clause) == 1 :
            var = clause[0]
            if var[0] == "-" :
                nvar = var[1:]
            else :
                nvar = "-"+var
                
            if not var in valids :
                return set()
            if nvar in valids :
                valids.remove(nvar)
    return valids

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

def ssat(nvars, claus, vals=set(), cola=None) :
    clauses = [i.copy() for i in claus]
    values = vals.copy()
    #print(len(values), len(clauses))
    #print(nvars, clauses, values)
    #if len(clauses) == 0 :
    #    for i in range(nvars) :
    #        if not i in  values and not -i in values :
    #            values.add(str(i))
    if len(values) == nvars and len(clauses) == 0 :
        #print("gg")
        return values
    """
    if cola is None :
        cola = PriorityQueue()
        for i in range(nvars) :
            occurrences(i, clauses)
    """
    valids = valid(nvars, clauses, values)
    #print(valids, clauses)
    for v in valids :
        if v[0] == "-" :
            nv = v[1:]
        else :
            nv = '-'+v
        if not v in values and not nv in values :
            #print(v, "hola")
            #if not valid(v, clauses) : continue
            simple = [i.copy() for i in clauses]
            simple = simplify(v, simple)
            values.add(v)
            r = ssat(nvars, simple, values)
            if r : return r
            #print("bachaqueando", v)
            values.remove(v)
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
    return output

if __name__ == '__main__':
    s =  "c perro\np cnf 5 5\n 2 -4\n 4\n-3\n"
    #s = ""
    s += "c perro\np cnf 5 5\n-4\n4 -2\n-3"
    ss = "c gato"
    print(solve_sat(s))
    
