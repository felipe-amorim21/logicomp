"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    pass
    # ======== YOUR CODE HERE ========


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False. """
    
    list_atoms = []
    list_atoms = atoms(formula)
    interpretation = None
    return sat(formula,list_atoms,interpretation)

def sat(formula, list_atoms, interpretation):
    if list_atoms == None:
        if truth_value(formula, interpretation):
            return True
        else:
            return False
    atom = list_atoms.pop()
    interpretation1 = {interpretation}.union({(atom,True)})
    interpretation2 = {interpretation}.union({(atom,False)})
    result = sat(formula, list_atoms, interpretation1)
    if result != False:
        return result
    return sat(formula, list_atoms, interpretation2)


