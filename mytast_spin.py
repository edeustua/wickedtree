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
        Operator("h1a(oo)", "p qd", typs='oo'),
        Operator("h1a(uu)", "pd q", typs='uu'),
        Operator("h1b(oo)", "pb qbd", typs='oo'),
        Operator("h1b(uu)", "pbd qb", typs='uu'),

        Operator("h2a(oooo)", "p q sd rd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("h2a(ouou)", "p qd sd r", typs='ouou',
            weight=1),
        Operator("h2a(uuuu)", "pd qd s r", typs='uuuu',
            weight=Fraction(1,2)),

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

        Operator("h2c(oooo)", "pb qb sbd rbd", typs='oooo',
            weight=Fraction(1,2)),
        Operator("h2c(ouou)", "pb qbd sbd rb", typs='ouou',
            weight=1),
        Operator("h2c(uuuu)", "pbd qbd sb rb", typs='uuuu',
            weight=Fraction(1,2)),

        Operator("h3a(uoouoo)", "pd q r u td sd", typs='uoouoo',
            weight=Fraction(1,2)),
        Operator("h3a(uuouuo)", "pd qd r u t sd", typs='uuouuo',
            weight=Fraction(1,2)),

        Operator("h3b(uoouoo)", "pbd q r u td sbd", typs='uoouoo',
            weight=1),
        Operator("h3b(uooouo)", "pbd q r ud t sbd", typs='uooouo',
            weight=1),
        #Operator("h3b(uoooou)", "pbd q r ud td sb", typs='uoooou',
        #    weight=Fraction(1,2)),
        Operator("h3b(ououoo)", "pb qd r u td sbd", typs='ououoo',
            weight=1),
        Operator("h3b(ouooou)", "pb qd r ud td sb", typs='ouooou',
            weight=1),

        Operator("h3b(uuouuo)", "pbd qd r u t sbd", typs='uuouuo',
            weight=1),
        Operator("h3b(uuouou)", "pbd qd r u td sb", typs='uuouou',
            weight=1),
        Operator("h3b(uouuuo)", "pbd q rd u t sbd", typs='uouuuo',
            weight=1),
        Operator("h3b(uuouuo)", "pbd qd r u t sbd", typs='uuouuo',
            weight=1),



        Operator("h3c(uoouoo)", "pbd qb r u tbd sbd", typs='uoouoo',
            weight=1),
       # Operator("h3c(uooouo)", "pbd qb r ud tb sbd", typs='uooouo',
       #     weight=1),
        Operator("h3c(uoooou)", "pbd qb r ud tbd sb", typs='uoooou',
            weight=1),
        Operator("h3c(ououoo)", "pb qbd r u tbd sbd", typs='ououoo',
            weight=1),
       # Operator("h3c(ouooou)", "pb qbd r ud tbd sb", typs='ouooou',
       #     weight=1),

        Operator("h3c(uuouuo)", "pbd qbd r u tb sbd", typs='uuouuo',
            weight=1),
        Operator("h3c(uuouou)", "pbd qbd r u tbd sb", typs='uuouou',
            weight=1),
        #Operator("h3c(uuoouu)", "pbd qbd r ud tb sb", typs='uuoouu',
        #    weight=1),
        Operator("h3c(uouuuo)", "pbd qb rd u tb sbd", typs='uouuuo',
            weight=1),
        #Operator("h3c(uouuou)", "pbd qb rd u tbd sb", typs='uouuou',
        #    weight=1),
        Operator("h3c(uououu)", "pbd qb rd ud tb sb", typs='uououu',
            weight=1),
        #Operator("h3c(ouuuuo)", "pb qbd rd u tb sbd", typs='ouuuuo',
        #    weight=1),
        #Operator("h3c(ouuuou)", "pb qbd rd u tbd sb", typs='ouuuou',
        #    weight=1),
        Operator("h3c(ouuouu)", "pb qbd rd ud tb sb", typs='ouuouu',
            weight=1),

        Operator("h3d(uoouoo)", "pbd qb rb ub tbd sbd", typs='uoouoo',
            weight=Fraction(1,2)),
        Operator("h3d(uuouuo)", "pbd qbd rb ub tb sbd", typs='uuouuo',
            weight=Fraction(1,2)),
        ]

ht = Operator("h3(ouuouu)", "p qd rd ud t s", typs='ouuouu',
        weight=Fraction(1,2))




def run(h):

    # aaa
    #bra = Operator("bra", "cb b a kb j i")
    #ket = Operator("ket", "id jd kbd ad bd cbd")
    #bra = Operator("bra", "c b a k j i")
    #ket = Operator("ket", "id jd kd ad bd dd")
    #bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
    #ket = Operator("ket", "i1d i2d i6d a1d a5d a6d")
    bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
    ket = Operator("ket", "i1d i6d i2d a1d a5d a6d")
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
    if len(full) == 0:
        return
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

    terms = list(zip(*new_eqs))
    if len(terms) > 0:
        uniques = find_equiv(list(terms[1]))
        print("==================================")
        print(h)
        print('----------------')
        for cnt, term in uniques:
            print(int(math.sqrt(cnt)) * new_weights[term], term)

        print("==================================\n")


#run(hs[0])
for h in hs:
    run(h)
