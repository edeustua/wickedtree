import sys

from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        Symbol

from printing import get_utf8_tree

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





hs = [
        Operator("h1(oo)", "p qd", typs='oo'),
        Operator("h1(uu)", "pd q", typs='uu'),
        Operator("h2(oooo)", "p q sd rd", typs='oooo',
            weight=Fraction(1,2)),
        #Operator("h2(ouou)", "p qd sd r", typs='ouou',
        #    weight=1),
        Operator("h2(ouuo)", "p qd s rd", typs='ouuo',
            weight=1),
        #Operator("h2(uouo)", "pd q s rd", typs='uouo',
        #    weight=1),
        #Operator("h2(uoou)", "pd q sd r", typs='uoou',
        #    weight=1),
        Operator("h2(uuuu)", "pd qd s r", typs='uuuu',
            weight=Fraction(1,2)),
        Operator("h3(uoouoo)", "pd q r u td sd", typs='uoouoo',
            weight=Fraction(1,2)),
        Operator("h3(uuouuo)", "pd qd r u t sd", typs='uuouuo',
            weight=Fraction(1,2)),
        ]

ht = Operator("h3(ouuouu)", "p qd rd ud t s", typs='ouuouu',
        weight=Fraction(1,2))




def run(h):
    print("==================================")
    print(h)

    bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
    #ket = Operator("ket", "id jd kd ad bd dd")
    ket = Operator("ket", "i1d i2d i4d a1d a4d a5d")

    fs = OperatorString(bra * h * ket)

    root_node = Node(fs)
    wicks(root_node)

    # Pretty Print
    #lines, _, _, _ = get_utf8_tree(root_node)
    #for line in lines:
    #    print(line)

    #print(root_node.right.right.right.right.left.data)

    full = collect_fully_contracted(root_node)

    #print(full)
    #sys.exit()
    new_eqs = []
    new_weights = {}
    for i, eq in enumerate(full):
        evs = [x.evaluate() for x in eq.deltas]

        if 0 in evs:
            continue

        mv = h.eval_deltas(eq.deltas)
        #equiv = new_eqs_weights[key]
        #print(equiv)
        #print(eq.deltas)
        #print(eq.sign * eq.weight, mv)

        new_eqs.append((eq.sign * eq.weight, mv))
        new_weights[mv] = eq.sign * eq.weight

    print('----------------')
    terms = list(zip(*new_eqs))
    if len(terms) > 0:
        uniques = find_equiv(list(terms[1]))
        for cnt, term in uniques:
            print(int(math.sqrt(cnt)) * new_weights[term], term)

    print("==================================\n")


#run(hs[0])
for h in hs:
    run(h)
