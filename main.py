def read_dimacs_file(filename):
   
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue 
            clause = [int(x) for x in line.strip().split() if x != '0']  # Eliminăm 0
            if clause:
                clauses.append(clause)
    return clauses


def unit_propagation(clauses):
    
    assignments = {}
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1]  
        if not unit_clauses:
            break

        for clause in unit_clauses:
            unit_literal = clause[0]
            if unit_literal not in assignments:
                assignments[unit_literal] = True
            elif unit_literal in assignments and assignments[unit_literal] is False:
                return None, False  
            clauses = [c for c in clauses if unit_literal not in c]  
            clauses = [list(filter(lambda x: x != -unit_literal, c)) for c in clauses] 
    return clauses, assignments


def davis_putnam(clauses, variables):
    
    clauses, assignments = unit_propagation(clauses)
    if clauses == []:
        return True  
    if any(len(clause) == 0 for clause in clauses):
        return False 

    if not variables:
        return True  

    var = variables.pop()

   
    new_clauses = [list(filter(lambda x: x != var, clause)) for clause in clauses]
    if davis_putnam(new_clauses, variables.copy()):
        return True

    
    new_clauses = [list(filter(lambda x: x != -var, clause)) for clause in clauses]
    if davis_putnam(new_clauses, variables.copy()):
        return True

    return False  


if __name__ == '__main__':
    input_file = r'D:\sat\rezolutie.py\dpll\clause_set.cnf'  
    clauses = read_dimacs_file(input_file)  
    variables = set(abs(literal) for clause in clauses for literal in clause)  

    satisfiable = davis_putnam(clauses, list(variables))

    if satisfiable:
        print("Formula este satisfiabilă.")
    else:
        print("Formula NU este satisfiabilă.")