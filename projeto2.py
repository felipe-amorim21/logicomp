from semantics import *
from functions import *

import csv
import pandas as pd

from pysat.formula import IDPool
from pysat.formula import CNF
from pysat.solvers import Cadical


'''def cnf(A):
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


'''

var_pool = IDPool()


def pretty_formula_printer(formula):
  for clause in formula:
    for literal in clause:
      if literal > 0:
        print(var_pool.obj(literal), ' ',  end = '')
      else:
        print('Not', var_pool.obj(literal*-1), ' ',  end = '')
    print('')



#readind files and getting attributes

directory = './pacientes/column_bin_36a_155p.csv'

with open(directory, mode='r') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)

    attributes = next(leitor_csv)
    attributes.pop()


    #Pegando os pacientes
pd = pd.read_csv(directory)
patientStatus = pd['P'].values.tolist()

patientsNoDisease = pd.loc[pd['P'] == 0]
patientsDisease = pd.loc[pd['P'] == 1]

'''print(patientsNoDisease['LA <= 39.63'].values.tolist())'''

# atomica do tipo Xatributo,regra_atual,regra_aparece_na_formula
m = 8
rules = ['gt', 'le', 's']

def and_all(list_formulas):
    """
    Returns a BIG AND formula from a list of formulas
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    And(And(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: And formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = And(first_formula, formula)
    return first_formula


def or_all(list_formulas):
    """
    Returns a BIG OR of formulas from a list of formulas.
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    Or(Or(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: Or formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = Or(first_formula, formula)
    return first_formula


def numberOfPatientsWithDisease(patient_list):
    count = 0
    for i in patient_list:
        if i == 1:
            count += 1
    return count

def firstRestriction(attributes, m):
    '''Para cada atributo e cada regra, temos exatamente uma das três possibilidades: o atributo aparece
com ≤ na regra, o atributo aparece com > na regra, ou o atributo não aparece na regra.'''
    formulas = []
    a = []
    formula2 = []
    for i in range(1,m+1):
        formula = []
        for j in attributes:
            for k in rules:
                formula.append((var_pool.id('x' + str(j) + '_' + str(i) + '_' + str(k))))
                for c in range(len(rules)-1):
                    if c == 1:
                        formula2.append(((-1*var_pool.id('x' + str(j) + '_' + str(i) + '_' + (rules[c])))))
                        formula2.append(-1*var_pool.id('x' + str(j) + '_' + str(i) + '_' + (rules[2])))
                    else:
                        for v in range(1, len(rules)):
                            formula2.append(((-1*var_pool.id('x' + str(j) + '_' + str(i) + '_' + (rules[c])))))
                            formula2.append(-1*var_pool.id('x' + str(j) + '_' + str(i) + '_' + (rules[v])))
        formulas.append((formula))
        formulas.append(((formula2)))
    return (formulas)



def secondRestrictions(attributes, m):
    formulas = []
    for i in range(1,m+1):
        formula = []
        for j in attributes:
            for k in rules:
                if k == 's':
                    formula.append((-1*var_pool.id('x' + str(j) + '_' + str(i) + '_' + str(k))))
        formulas.append(formula)
    return (formulas)


def thirdRestriction(attributes, m):
    patients = len(patientStatus) - numberOfPatientsWithDisease(patientStatus)
    formula_list = []
    formulas = []
    for i in range(1, m+1):
        for p in range(patients):
            formula = []
            for j in attributes:
                aux_list = patientsNoDisease[j].values.tolist()
                if aux_list[p] == 1: 
                    formula.append(var_pool.id('x' + str(j) + '_' + str(i) + '_' + 'gt'))
                else:
                    formula.append(var_pool.id('x' + str(j) + '_' + str(i) + '_' + 'le'))
            formulas.append(((formula)))
    return (formulas)


def fourthRestriction(attributes, m):
    '''Para cada paciente com patologia, cada regra e cada atributo, se o atributo do paciente não se aplicar
ao da regra, então a regra não cobre esse paciente.'''
    patients = numberOfPatientsWithDisease(patientStatus)
    formula_list = []
    formulas = []
    formula = []
    for i in range(1, m+1):
            for p in range(0, patients):
                for j in attributes:
                    aux_list = patientsDisease[j].values.tolist()
                    if aux_list[p] == 1:
                        formula.append([ -1*(var_pool.id('x' + str(j) + '_'+ str(i) + '_' + 'gt')),(-1*(var_pool.id('c' + str(i) + '_' + str(p+1)))) ])
                    else:
                        formula.append([ -1*(var_pool.id('x' + str(j) + '_'+ str(i) + '_' + 'le')),(-1*(var_pool.id('c' + str(i) + '_' + str(p+1)))) ])
    return (formula)

def fifthRestriction(attributes, m):
    formula_list = []
    formulas = []
    patients = numberOfPatientsWithDisease(patientStatus)
    for p in range(1, patients+1):
        formula = []
        for i in range(1,m+1):
            formula.append(var_pool.id('c' + str(i) + '_' + str(p)))
        formulas.append((formula))
    return (formulas)


clauses1 = firstRestriction(attributes, m)
clauses2 = secondRestrictions(attributes, m)
clauses3 = thirdRestriction(attributes, m)
clauses4 = fourthRestriction(attributes, m)
clauses5 = fifthRestriction(attributes, m)
clauses = clauses1 + clauses2 + clauses3 + clauses4 + clauses5
cnf2 = CNF(from_clauses=clauses)
print(len(cnf2.clauses))
print(cnf2.nv)


solver = Cadical()
solver.append_formula(cnf2.clauses)

print(solver.solve())

print(solver.get_model())


def solution(attributes, m):
    formulas = []
    if solver.solve():
        solution = solver.get_model()
        for i in range(1,m+1):
            formula = []
            for j in attributes:
                for k in rules:
                    if var_pool.id('x' + str(j) + '_' + str(i) + '_' + str(k)) in solution:
                        formula.append((('x' + str(j) + '_' + str(i) + '_' + str(k))))
            formulas.append(formula)
        for i in (formulas):
            print(i)
        print('Time to solve:', solver.time())
    else:
        print("Não há regras que classifiquem todos os pacientes")

solution(attributes, m)