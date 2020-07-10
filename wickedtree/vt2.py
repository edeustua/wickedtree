import sys

from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        Symbol

from printing import get_utf8_tree

from fractions import Fraction

import math


def find_equiv(terms):

    tmp_terms = list(zip(*terms))
    new_terms = list(zip(*terms))

    uniques = []
    while True:

        pivot_l = tuple([frozenset([term.symbol] + term.lower) for term in
            tmp_terms[0]])
        pivot_u = tuple([frozenset([term.symbol] + term.upper) for term in
            tmp_terms[0]])

        #pivot_l = set(tmp_terms[0].lower)
        #pivot_u = set(tmp_terms[0].upper)
        pivot_l = set(pivot_l)
        pivot_u = set(pivot_u)

        cnt = 0
        for term in tmp_terms:
            t_l = tuple([frozenset([t_term.symbol] + t_term.lower) for t_term in
                term])
            t_u = tuple([frozenset([t_term.symbol] + t_term.upper) for t_term in
                term])

            if \
                    pivot_l == set(t_l) and \
                    pivot_u == set(t_u):

                new_terms.remove(term)
                cnt += 1

        uniques.append((cnt, tmp_terms[0]))



        if len(new_terms) == 0:
            break

        tmp_terms = new_terms[:]

    return uniques





hs = [
        Operator("va(oooo)", "p q sd rd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("va(ouou)", "p qd sd r", typs='ouou',
            weight=1),
        Operator("va(oouu)", "p q s r", typs='oouu',
            weight=Fraction(1,2)),
        Operator("va(uuuu)", "pd qd s r", typs='uuuu',
            weight=Fraction(1,2)),

        Operator("vb(oooo)", "p qb sbd rd", typs='oooo',
            weight=1),
        Operator("vb(ouou)", "p qbd sbd r", typs='ouou',
            weight=1),
        Operator("vb(ouuo)", "p qbd sb rd", typs='ouuo',
            weight=1),
        Operator("vb(uoou)", "pd qb sbd r", typs='uoou',
            weight=1),
        Operator("vb(uouo)", "pd qb sb rd", typs='uouo',
            weight=1),
        Operator("vb(uuuu)", "pd qbd sb r", typs='uuuu',
            weight=1),

        Operator("vc(oooo)", "pb qb sbd rbd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("vc(ouou)", "pb qbd sbd rb", typs='ouou',
            weight=1),
        Operator("vc(uuuu)", "pbd qbd sb rb", typs='uuuu',
            weight=Fraction(1,2)),

        ]

ts = [
        Operator("t2a", "ed md fd nd", weight=Fraction(1,2)),
        Operator("t2b", "ed md fbd nbd", weight=1),
        Operator("t2c", "ebd mbd fbd nbd", weight=Fraction(1,2)),
        ]



def run(h):

    # aaa
    bra = Operator("bra", "c b a k j i")
    ket = Operator("ket", "id jd kd ad bd cd")
    #bra = Operator("bra", "b a j i")
    #bra = Operator("bra", "j b i a")
    #bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
    #ket = Operator("ket", "i1d i2d i6d a1d a5d a6d")
    #bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
    #ket = Operator("ket", "i1d i2d i6d a1d a5d a6d")
    #ket = Operator("ket", "i1d i2d i3d a1d a2d a6d")

    # aab
    #bra = Operator("bra", "cb b a kb j i")
    #ket = Operator("ket", "id jd kbd ad bd cbd")

    # abb
    #bra = Operator("bra", "cb bb a kb jb i")
    #ket = Operator("ket", "id jbd kbd ad bbd cbd")

    # bbb
    #bra = Operator("bra", "cb bb ab kb jb ib")
    #ket = Operator("ket", "ibd jbd kbd abd bbd cbd")

    #bra = Operator("bra", "cb b a kb j i")
    #ket = Operator("ket", "id jd kbd ad bd cbd")

    for t in ts:

        fs = OperatorString(bra * h * t * ket)

        root_node = Node(fs)
        wicks(root_node)

        # Pretty Print
        #lines, _, _, _ = get_utf8_tree(root_node)
        #for line in lines:
        #    print(line)

        #print(root_node.right.right.right.right.left.data)

        #print(fs)
        #root_node.print()
        full = collect_fully_contracted(root_node)

        #print(full)
        #sys.exit()
        new_eqs = []
        new_weights = {}
        if len(full) == 0:
            continue

        for i, eq in enumerate(full):
            evs = [x.evaluate() for x in eq.deltas]

            if 0 in evs:
                continue

            mv = h.eval_deltas(eq.deltas)
            mt = t.eval_deltas(eq.deltas)
            #equiv = new_eqs_weights[key]
            #print(equiv)
            #print(eq.deltas)
            #print(eq.sign * eq.weight, mv)

            new_eqs.append((eq.sign * eq.weight, mv, mt))
            new_weights[(mv, mt)] = eq.sign * eq.weight

        terms = list(zip(*new_eqs))
        #print(terms)
        if len(terms) > 0:
            uniques = find_equiv(list(terms[1:]))
            print("==================================")
            print(h)
            print('----------------')
            for cnt, term in uniques:
                print(int(math.sqrt(cnt)) * new_weights[term], term)

            print("==================================\n")



#run(hs[0])
for h in hs:
    run(h)
