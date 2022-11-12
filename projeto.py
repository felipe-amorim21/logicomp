import csv
from semantics import *
from functions import *
import pandas as pd

#readind files and getting attributes
with open('./pacientes/column_bin_5a_3p.csv', mode='r') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)

    attributes = next(leitor_csv)
    attributes.pop()


    #Pegando os pacientes
pd = pd.read_csv('./pacientes/column_bin_5a_3p.csv')
patientStatus = pd['P'].values.tolist()

patientsNoDisease = pd.loc[pd['P'] == 0]
'''print(patientsNoDisease['PI <= 42.09'].values)'''

# atomica do tipo Xatributo,regra_atual,regra_aparece_na_formula
m = 4
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

def firstRestriction():
    '''Para cada atributo e cada regra, temos exatamente uma das três possibilidades: o atributo aparece
com ≤ na regra, o atributo aparece com > na regra, ou o atributo não aparece na regra.'''


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
            for j in attributes:
                if patientsNoDisease[j].values == 1: 
                    formula =  Atom('x' + str(j) + '_' + str(i) + '_' + 'gt')
                    formula_list.append(formula)
                else:
                    formula =  Atom('x' + str(j) + '_' + str(i) + '_' + 'le')
                    formula_list.append(formula)
            formulas.append(or_all(formula_list))
            formula_list.clear()
    return and_all(formulas)

print(thirdRestriction(attributes,m))




def fourthRestriction(attributes, m):
    '''Para cada paciente com patologia, cada regra e cada atributo, se o atributo do paciente não se aplicar
ao da regra, então a regra não cobre esse paciente.'''
    patients = numberOfPatientsWithDisease(patientStatus)
    formula_list = []
    formulas = []
    for i in range(1, m+1):
        for k in range(5):
            for p in range(1, patients+1):
                for j in attributes:
                    formula = Implies(Atom('x' + str(j) + '_'+ str(i) + '_' + str(k)),Not(Atom('c' + str(i) + '_' + str(p))))
                    formula_list.append(formula)
        formulas.append(and_all(formula_list))
        formula_list.clear()
    return and_all(formulas)


def fifthRestriction(m):
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
        