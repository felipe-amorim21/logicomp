from semantics import *
from functions import *


formula7 = Implies((Implies(Not(Atom('p')), Not(Atom('q')))), Implies(Atom('p'), Atom('q'))
                   )  # ((¬(p /\ s)) -> (q /\ r))
formula6 = Or(Not(And(Atom('p'), Atom('s'))), Atom('q'))  # ((¬(p /\ s)) v q)

formula1 = Implies(And(Atom('p'), Atom('q')), Atom('r'))
formula2 = Implies(Not(And(Atom('p'), Atom('q'))), Atom('r'))
formula3 = Implies(Implies(Not(Atom('p')), Not(Atom('q'))), Implies(Atom('p'), Atom('q')))
formula4 = Or(Or(And(Atom('p'), Not(Atom('q'))),Atom('r')),And(Not(Atom('r')),Not(Atom('p'))))

formula = Not(Not(Atom('q')))

def cnf(A):
    b = implication_free(A)
    b = negation_normal_form(b)
    b = distributive(b)
    return b


def implication_free(A):
    if isinstance(A, Implies):
        b1 = implication_free(A.left)
        b2 = implication_free(A.right)
        return (Or(Not(b1), b2))
    if isinstance(A, Or):
        return (Or(implication_free(A.left), implication_free(A.right)))
    if isinstance(A, And):
        return (And(implication_free(A.left), implication_free(A.right)))
    if isinstance(A, Not):
        return Not(implication_free(A.inner))
    if isinstance(A, Atom):
        return A


def negation_normal_form(A):
    if isinstance(A, Not) and isinstance(A.inner,Not):
        return negation_normal_form(A.inner.inner)
    if isinstance(A, Or):
        return (Or(negation_normal_form(A.left), negation_normal_form(A.right)))
    if isinstance(A, And):
        return (And(negation_normal_form(A.left), negation_normal_form(A.right)))
    if isinstance(A, Not) and isinstance(A.inner, And):
        return Or(negation_normal_form(Not(A.inner.left)), negation_normal_form(Not(A.inner.right)))
    if isinstance(A, Not) and isinstance(A.inner, Or):
        return And(negation_normal_form(Not(A.inner.left)), negation_normal_form(Not(A.inner.right)))
    if isinstance(A, Atom) or isinstance(A, Not) and isinstance(A.inner, Atom):
        return A

def distributive(A):
    if isinstance(A, Atom) or isinstance(A, Not) and isinstance(A.inner, Atom):
        return A
    if isinstance(A, And):
        return And(distributive(A.left), distributive(A.right))
    if isinstance(A, Or):
        b1 = distributive(A.left)
        b2 = distributive(A.right)
        if isinstance(b1, And):
            return And(distributive(Or(b1.left, b2)),distributive(Or(b1.right, b2)))
        if isinstance(b2, And):
            return And(distributive(Or(b1, b2.left)),distributive(Or(b1, b2.right)))
    return Or(b1, b2)


"Exemplos"
print(formula4)
print(cnf(formula4))



