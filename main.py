def read_dimacs_file(filename):
    """
    Citește fișierul CNF și extrage clauzele
    """
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue  # Ignorăm comentariile și linia de tip 'p'
            clause = [int(x) for x in line.strip().split() if x != '0']  # Eliminăm 0
            if clause:
                clauses.append(set(clause))  # Folosim set pentru a elimina duplicate
    return clauses

def resolve(ci, cj):
    """
    Aplica rezolutia pe două clauze pentru a obține noi clauze
    """
    resolvents = []
    for literal in ci:
        if -literal in cj:
            new_clause = (ci - {literal}) | (cj - {-literal})
            resolvents.append(frozenset(new_clause))
    return resolvents

def resolution_solver(clauses):
    """
    Rezolvă satisfiabilitatea folosind algoritmul de rezoluție
    """
    clauses = set(frozenset(clause) for clause in clauses)
    new = set()

    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                if not resolvent:
                    return False  # Clauza goală => formula este nesatisfiabilă
                new.add(resolvent)

        if new.issubset(clauses):
            return True  # Nu se mai pot adăuga clauze noi => formula este satisfiabilă

        clauses |= new  # Adăugăm noile clauze la setul de clauze

if __name__ == '__main__':
    # Specifică calea corectă către fișierul CNF
    input_file = r'D:\sat\rezolutie.py\clause_set.cnf'  # Calea corectă către fișier
    clauses = read_dimacs_file(input_file)  # Citește clauzele din fișier
    satisfiable = resolution_solver(clauses)  # Verifică satisfiabilitatea formulei

    if satisfiable:
        print("Formula este satisfiabilă.")
    else:
        print("Formula NU este satisfiabilă.")