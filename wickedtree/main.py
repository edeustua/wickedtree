from .bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted

from fractions import Fraction

import math

def find_equiv(terms):

    tmp_terms = terms.copy()
    new_terms = terms.copy()

    uniques = []
    while True:

        pivot_l = set(tmp_terms[0].lower)
        pivot_u = set(tmp_terms[0].upper)

        cnt = 0
        for term in tmp_terms:
            if pivot_l == set(term.lower) and \
                    pivot_u == set(term.upper):
                new_terms.remove(term)
                cnt += 1

        uniques.append((cnt, tmp_terms[0]))


        if len(new_terms) == 0:
            break

        tmp_terms = new_terms[:]

    return uniques

def collect_unique(fully_contracted, operator):

    unique_eqs = []
    unique_weights = {}

    if len(fully_contracted) == 0:
        return

    for i, eq in enumerate(fully_contracted):

        evs = [x.evaluate() for x in eq.deltas]

        if 0 in evs:
            continue

        mv = operator.eval_deltas(eq.deltas)

        unique_eqs.append((eq.sign * eq.weight, mv))
        unique_weights[mv] = eq.sign * eq.weight

    unique_eqs = list(zip(*unique_eqs))

    if len(unique_eqs) > 0:
        uniques = find_equiv(list(unique_eqs[1]))

        res = []

        for cnt, term in uniques:
            w = int(math.sqrt(cnt)) * unique_weights[term]
            res.append((operator, w, term))

        return res

    else:
        return None


def run(operator, bra, ket):
    """
    Obtain all fully contracted expressions.
    """

    full_string = OperatorString(bra * operator * ket)
    root_node = Node(full_string)

    wicks(root_node)
    fully_contracted = collect_fully_contracted(root_node)

    exps = collect_unique(fully_contracted, operator)

    return exps



