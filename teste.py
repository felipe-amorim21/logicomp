from formula import *
from functions import *
from semantics import satisfiability_brute_force, truth_value

formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
formula1 = (Atom('p')) # p
formula4 = Not(Atom('p')) # ~p
formula2 = Atom('q')  # q
formula3 = Or(formula1, formula2) # p and q
formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s')))))
formula11 = Not(Not(Not(Atom("p"))))

formula12 = And(Not(Atom("p")), Atom('p'))

print('atomicas of formula7:')
print(atoms(formula8))
for atom in atoms(formula8):
    print(atom)


print(number_of_connectives(formula3))
print(number_of_connectives(formula8))

print(number_of_atoms(formula3))
print(number_of_atoms(formula8))

print(is_literal(formula3))
print(is_literal(formula8))
print(is_literal(formula11))

print('---------------Truth-value------------------')
a = truth_value(formula4, {'p': True})
print(a)
print('----------------_Satisfiability--------------')
print(satisfiability_brute_force(formula8))
print('----------------_Satisfiability--------------')
print(satisfiability_brute_force(formula12))
print(satisfiability_brute_force(formula1))
print(satisfiability_brute_force(formula4))
print(satisfiability_brute_force(formula7))