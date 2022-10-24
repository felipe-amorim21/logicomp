from formula import *
from functions import *

formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
formula1 = Atom('p')  # p
formula2 = Atom('q')  # q
formula3 = And(formula1, formula2)
formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s')))))

print('atomicas of formula7:')
print(atoms(formula8))
for atom in atoms(formula8):
    print(atom)