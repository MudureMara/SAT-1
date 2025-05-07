def read_dimacs_file(filename):
    
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue 
            clause = [int(x) for x in line.strip().split() if x != '0']  
            if clause:
                clauses.append(set(clause))  
    return clauses

def resolve(ci, cj):
    
    resolvents = []
    for literal in ci:
        if -literal in cj:
            new_clause = (ci - {literal}) | (cj - {-literal})
            resolvents.append(frozenset(new_clause))
    return resolvents

def resolution_solver(clauses):
  
    clauses = set(frozenset(clause) for clause in clauses)
    new = set()

    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                if not resolvent:
                    return False 
                new.add(resolvent)

        if new.issubset(clauses):
            return True  

        clauses |= new 

if __name__ == '__main__':
 
    input_file = r'D:\sat\rezolutie.py\clause_set.cnf'
    clauses = read_dimacs_file(input_file)  
    satisfiable = resolution_solver(clauses)  

    if satisfiable:
        print("Formula este satisfiabilă.")
    else:
        print("Formula NU este satisfiabilă.")
