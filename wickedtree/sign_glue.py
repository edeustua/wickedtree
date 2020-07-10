import sys

from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        Symbol

from printing import get_utf8_tree

from fractions import Fraction

import math

import re

IND = re.compile(r"[ai](\d+)")

def get_diff(bra, ket):

    bra_inds = frozenset([ind.symbol.label for ind in bra.string])
    ket_inds = frozenset([ind.symbol.label for ind in ket.string])

    #print(len(bra_inds - ket_inds))

    return len(bra_inds - ket_inds)



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



hs = [
        # h1 aa
        Operator("h1a(oo)", "p qd", typs='oo'),
        Operator("h1a(uu)", "pd q", typs='uu'),

        # h1 bb
        Operator("h1b(oo)", "pb qbd", typs='oo'),
        Operator("h1b(uu)", "pbd qb", typs='uu'),

        # h2 aa
        Operator("h2a(oooo)", "p q sd rd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("h2a(ouou)", "p qd sd r", typs='ouou',
            weight=1),
        Operator("h2a(uuuu)", "pd qd s r", typs='uuuu',
            weight=Fraction(1,2)),

        # h2 ab
        Operator("h2b(oooo)", "p qb sbd rd", typs='oooo',
            weight=1),
        Operator("h2b(ouou)", "p qbd sbd r", typs='ouou',
            weight=1),
        Operator("h2b(ouuo)", "p qbd sb rd", typs='ouuo',
            weight=1),
        Operator("h2b(uoou)", "pd qb sbd r", typs='uoou',
            weight=1),
        Operator("h2b(uouo)", "pd qb sb rd", typs='uouo',
            weight=1),
        Operator("h2b(uuuu)", "pd qbd sb r", typs='uuuu',
            weight=1),

        # h2 bb
        Operator("h2c(oooo)", "pb qb sbd rbd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("h2c(ouou)", "pb qbd sbd rb", typs='ouou',
            weight=1),
        Operator("h2c(uuuu)", "pbd qbd sb rb", typs='uuuu',
            weight=Fraction(1,2)),

        # h3 aaa oou
        Operator("h3a(uoouoo)", "pd q r u td sd", typs='uoouoo',
            weight=Fraction(1,2)),

        # h3 aaa ouu
        Operator("h3a(uuouuo)", "pd qd r u t sd", typs='uuouuo',
            weight=Fraction(1,2)),

        # h3 aab oou
        Operator("h3b(uoouoo)", "pbd q r u td sbd", typs='uoouoo',
            weight=1),
        Operator("h3b(ououoo)", "pb qd r u td sbd", typs='ououoo',
            weight=1),
        Operator("h3b(ouooou)", "pb qd r ud td sb", typs='ouooou',
            weight=1),

        # h3 aab ouu
        Operator("h3b(uuouuo)", "pbd qd r u t sbd", typs='uuouuo',
            weight=1),
        Operator("h3b(uuouou)", "pbd qd r u td sb", typs='uuouou',
            weight=1),
        Operator("h3b(ouuuou)", "pb qd rd u td sb", typs='ouuuou',
            weight=1),



        # h3 abb oou
        Operator("h3c(uoouoo)", "pbd qb r u tbd sbd", typs='uoouoo',
            weight=1),
        Operator("h3c(uoooou)", "pbd qb r ud tbd sb", typs='uoooou',
            weight=1),
        Operator("h3c(oououo)", "pb qb rd ud tb sbd", typs='oououo',
            weight=1),


        Operator("h3c(uououu)", "pbd qb rd ud tb sb", typs='uououu',
            weight=1),
        Operator("h3c(uouuuo)", "pbd qb rd u tb sbd", typs='uouuuo',
            weight=1),
        Operator("h3c(uuouou)", "pbd qbd r u tbd sb", typs='uuouou',
            weight=1),

        # h3 bbb oou
        Operator("h3d(uoouoo)", "pbd qb rb ub tbd sbd", typs='uoouoo',
            weight=Fraction(1,2)),
        # h3 bbb ouu
        Operator("h3d(uuouuo)", "pbd qbd rb ub tb sbd", typs='uuouuo',
            weight=Fraction(1,2)),
        ]






def run(h, bra, ket):

    fs = OperatorString(bra * h * ket)

    root_node = Node(fs)
    wicks(root_node)

    full = collect_fully_contracted(root_node)

    new_eqs = []
    new_weights = {}

    python_out = []

    if len(full) == 0:
        return

    for i, eq in enumerate(full):
        evs = [x.evaluate() for x in eq.deltas]

        if 0 in evs:
            continue

        mv = h.eval_deltas(eq.deltas)

        new_eqs.append((eq.sign * eq.weight, mv))
        new_weights[mv] = eq.sign * eq.weight

    terms = list(zip(*new_eqs))
    if len(terms) > 0:
        uniques = find_equiv(list(terms[1]))
        #print("==================================")
        #print(h)
        #print('----------------')
        for cnt, term in uniques:
            #print(int(math.sqrt(cnt)) * new_weights[term], term)
            w = int(math.sqrt(cnt)) * new_weights[term]
            p = term.to_python()
            if w < 0:
                str_out = "-" + p[1]
            else:
                str_out = p[1]

            python_out.append((p[0], str_out))

        #print("==================================\n")

    return python_out



def prepare_strings(nel, det, dagger):

    op = []
    if not dagger:
        det = reversed(det)
    for ind in det:
        inds = (ind - 1) // 2
        if ind > nel:
            if ind % 2 == 1:
                op.append(f"a{inds}")
            else:
                op.append(f"a{inds}b")
        else:
            if ind % 2 == 1:
                op.append(f"i{inds}")
            else:
                op.append(f"i{inds}b")

    if dagger:
        op = [f"{x}d" for x in op]

    return op

def split_elements(eqs):

    h_elements = {
            1: [],
            2: [],
            3: []
            }

    for eq in eqs:
        drop_ai = IND.sub(r'\1', eq[1])
        h_elements[eq[0]].append(drop_ai)

    return h_elements


def compute_element(nel, bra, ket):

    bra_op = prepare_strings(nel, bra, False)
    ket_op = prepare_strings(nel, ket, True)

    bra_op = Operator("bra", " ".join(bra_op))
    ket_op = Operator("ket", " ".join(ket_op))

    python_out = []
    for h in hs:
        eqs = run(h, bra_op, ket_op)
        if eqs:
            python_out.extend(eqs)

    h_elements = split_elements(python_out)

    return h_elements
