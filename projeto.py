import csv
from semantics import *
from functions import *

#readind files and getting attributes
with open('./pacientes/column_bin_5a_3p.csv', mode='r') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)

    attributes = next(leitor_csv)
    attributes.pop()

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
    return formulas 

for i in secondRestriction(attributes, m):
    print(i)
    print('------------------------')


def thirdRestriction(attribute, m):
    '''Para cada paciente sem patologia e cada regra, algum atributo do paciente não pode ser aplicado à
regra.'''
