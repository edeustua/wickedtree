import sys
sys.path.append("../")
print(sys.path)


import pytest

from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        Symbol

from printing import get_utf8_tree

from fractions import Fraction

import math


master = ["""==================================
h1(oo)(p q†)
----------------
-1 h1(oo)_{i}^{i}
-1 h1(oo)_{j}^{j}
-1 h1(oo)_{k}^{k}
==================================""",
"""==================================
h1(uu)(p† q)
----------------
1 h1(uu)_{a}^{a}
1 h1(uu)_{b}^{b}
1 h1(uu)_{c}^{c}
==================================""",
"""==================================
h2(oooo)(p q s† r†)
----------------
1 h2(oooo)_{ji}^{ji}
1 h2(oooo)_{ki}^{ki}
1 h2(oooo)_{kj}^{kj}
==================================""",
"""==================================
h2(ouuo)(p q† s r†)
----------------
-1 h2(ouuo)_{ia}^{ia}
-1 h2(ouuo)_{ja}^{ja}
-1 h2(ouuo)_{ka}^{ka}
-1 h2(ouuo)_{ib}^{ib}
-1 h2(ouuo)_{jb}^{jb}
-1 h2(ouuo)_{kb}^{kb}
-1 h2(ouuo)_{ic}^{ic}
-1 h2(ouuo)_{jc}^{jc}
-1 h2(ouuo)_{kc}^{kc}
==================================""",
"""==================================
h2(uuuu)(p† q† s r)
----------------
1 h2(uuuu)_{ab}^{ab}
1 h2(uuuu)_{ac}^{ac}
1 h2(uuuu)_{bc}^{bc}
==================================""",
"""==================================
h3(uoouoo)(p† q r u t† s†)
----------------
1 h3(uoouoo)_{aji}^{jia}
1 h3(uoouoo)_{aki}^{kia}
1 h3(uoouoo)_{akj}^{kja}
1 h3(uoouoo)_{bji}^{jib}
1 h3(uoouoo)_{bki}^{kib}
1 h3(uoouoo)_{bkj}^{kjb}
1 h3(uoouoo)_{cji}^{jic}
1 h3(uoouoo)_{cki}^{kic}
1 h3(uoouoo)_{ckj}^{kjc}
==================================""",
"""==================================
h3(uuouuo)(p† q† r u t s†)
----------------
-1 h3(uuouuo)_{abi}^{iab}
-1 h3(uuouuo)_{abj}^{jab}
-1 h3(uuouuo)_{abk}^{kab}
-1 h3(uuouuo)_{aci}^{iac}
-1 h3(uuouuo)_{acj}^{jac}
-1 h3(uuouuo)_{ack}^{kac}
-1 h3(uuouuo)_{bci}^{ibc}
-1 h3(uuouuo)_{bcj}^{jbc}
-1 h3(uuouuo)_{bck}^{kbc}
=================================="""]

#print(master)

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
    #print("==================================")
    #print(h)
    out_str = "==================================\n"
    out_str += str(h) + "\n"

    bra = Operator("bra", "c b a k j i")
    ket = Operator("ket", "id jd kd ad bd cd")

    fs = OperatorString(bra * h * ket)

    root_node = Node(fs)
    wicks(root_node)

    full = collect_fully_contracted(root_node)

    new_eqs = []
    new_weights = {}
    for i, eq in enumerate(full):
        evs = [x.evaluate() for x in eq.deltas]

        if 0 in evs:
            continue

        mv = h.eval_deltas(eq.deltas)

        new_eqs.append((eq.sign * eq.weight, mv))
        new_weights[mv] = eq.sign * eq.weight

    #print('----------------')
    out_str += '----------------\n'
    terms = list(zip(*new_eqs))
    uniques = find_equiv(list(terms[1]))
    for cnt, term in uniques:
        #print(int(math.sqrt(cnt)) * new_weights[term], term)
        out_str += str(int(math.sqrt(cnt)) * new_weights[term]) + \
				" " + str(term) + "\n"

    #print("==================================\n")
    out_str += "=================================="

    return out_str

@pytest.mark.parametrize("test_input,expected",
        list(zip(hs, master)))
def test_hbar(test_input, expected):
    out = run(test_input)
    assert out == expected

    #for i, h in enumerate(hs):
    #    out = run(h)
