import csv
from semantics import *
from functions import *
import pandas as pd

#readind files and getting attributes

directory = './pacientes/column_bin_3a_4p.csv'

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
m = 2
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
    formula_list = []
    formula2 = []
    formulas = []
    n = 0
    for i in range(1,m+1):
        for j in attributes:
            for k in rules:
                formula =  (Atom('x' + str(j) + '_' + str(i) + '_' + str(k)))
                formula_list.append(formula)
                for c in range(len(rules)-1):
                    if c == 1:
                        formula2.append(Not(And(Atom('x' + str(j) + '_' + str(i) + '_' + rules[c]),Atom('x' + str(j) + '_' + str(i) + '_' + rules[2]))))
                    else:
                        for v in range(1, len(rules)):
                            formula2.append(Not(And(Atom('x' + str(j) + '_' + str(i) + '_' + rules[c]),Atom('x' + str(j) + '_' + str(i) + '_' + rules[v])))) 
        formulas.append(or_all(formula_list))
        formulas.append(and_all(list( dict.fromkeys(formula2))))
        formula_list.clear()
        formula2.clear()
    return and_all(formulas)



def secondRestriction(attributes, m):
    '''Cada regra deve ter algum atributo aparecendo nela.'''
    formula_list = []
    formulas = []
    for i in range(1,m+1):
        for j in attributes:
            for k in rules:
                if k == 's':
                    formula =  Not(Atom('x' + str(j) + '_' + str(i) + '_' + str(k)))
                    formula_list.append(formula)
        formulas.append(or_all(formula_list))
        formula_list.clear()
    return and_all(formulas)



def thirdRestriction(attributes, m):
    '''Para cada paciente sem patologia e cada regra, algum atributo do paciente não pode ser aplicado à
regra.'''
    '''formula_list = []
    formulas = []
    for i in range(1,m+1):
        for j in attributes:
'''
    patients = len(patientStatus) - numberOfPatientsWithDisease(patientStatus)
    formula_list = []
    formulas = []
    for i in range(1, m+1):
        for p in range(patients):
            for j in attributes:
                aux_list = patientsNoDisease[j].values.tolist()
                if aux_list[p] == 1: 
                    formula =  Atom('x' + str(j) + '_' + str(i) + '_' + 'gt')
                    formula_list.append(formula)
                else:
                    formula =  Atom('x' + str(j) + '_' + str(i) + '_' + 'le')
                    formula_list.append(formula)
            formulas.append(or_all((formula_list)))
            formula_list.clear()
    return and_all(formulas)



def fourthRestriction(attributes, m):
    '''Para cada paciente com patologia, cada regra e cada atributo, se o atributo do paciente não se aplicar
ao da regra, então a regra não cobre esse paciente.'''
    patients = numberOfPatientsWithDisease(patientStatus)
    formula_list = []
    formulas = []
    for i in range(1, m+1):
            for p in range(0, patients):
                for j in attributes:
                    aux_list = patientsDisease[j].values.tolist()
                    if aux_list[p] == 1:
                        formula = Implies(Atom('x' + str(j) + '_'+ str(i) + '_' + 'gt'),Not(Atom('c' + str(i) + '_' + str(p+1))))
                        formula_list.append(formula)
                    else:
                        formula = Implies(Atom('x' + str(j) + '_'+ str(i) + '_' + 'le'),Not(Atom('c' + str(i) + '_' + str(p+1))))
                        formula_list.append(formula)
            formulas.append(and_all(formula_list))
            formula_list.clear()
    return and_all(formulas)


def fifthRestriction(attributes, m):
    '''Cada paciente com patologia deve ser coberto por alguma das regras.'''
    formula_list = []
    formulas = []
    patients = numberOfPatientsWithDisease(patientStatus)
    for p in range(1, patients+1):
        for i in range(1,m+1):
            formula =  Atom('c' + str(i) + '_' + str(p))
            formula_list.append(formula)
        formulas.append(or_all(formula_list))
        formula_list.clear()
    return and_all(formulas)
        

def isSatisfactory(first, second, third, fourth, fifth):
    formula = []    
    formula.extend([first, second, third, fourth, fifth])
    return satisfiability_brute_force(and_all(formula))

'''print(isSatisfactory(firstRestriction(attributes, m), secondRestriction(attributes, m), thirdRestriction(attributes, m), fourthRestriction(attributes, m), fifthRestriction(attributes, m)))
'''

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

print(thirdRestriction(attributes, m))
print(cnf(thirdRestriction(attributes, m)))
