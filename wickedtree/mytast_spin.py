from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted

from fractions import Fraction

import math

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

ht = Operator("h3(ouuouu)", "p qd rd ud t s", typs='ouuouu',
        weight=Fraction(1,2))

braket = (
        (
            Operator("bra", "a3 a2 a1 i3 i2 i1"),
            Operator("ket", "i1d i2d i4d a1d a5d a6d")
            ),
        (
            Operator("bra", "a3 a2 a1 i3 i2 i1"),
            Operator("ket", "i1d i2d i4bd a1d a5d a6bd")
            ),
        # ----
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4bd i3bd a1d a5bd a6bd")
            ),
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i3bd a1d a5d a6bd")
            ),
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4bd i3bd a5d a6bd a3bd")
            ),
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i2d i4d a1d a5d a6d")
            ),
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i3bd a5d a2d a6bd")
            ),
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i3bd a5d a6d a3bd")
            ),

        # ----
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i2bd i4bd a1d a5bd a6bd")
            ),
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i4d i3bd a1d a5d a6bd")
            ),
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4bd i2bd i3bd a5bd a2bd a6bd")
            ),
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i2bd i4bd a5d a2bd a6bd")
            ),
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i4d i3bd a5d a6d a3bd")
            ),
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4d i2bd i3bd a5d a2bd a6bd")
            ),
        # ----
        (
            Operator("bra", "a3b a2b a1b i3b i2b i1b"),
            Operator("ket", "i4d i2bd i3bd a5d a2bd a6bd")
            ),
        (
            Operator("bra", "a3b a2b a1b i3b i2b i1b"),
            Operator("ket", "i1bd i2bd i4bd a1bd a5bd a6bd")
            ),
        # ----
        (
            Operator("bra", "a3 a2 a1 i3 i2 i1"),
            Operator("ket", "i1d i4d i5d a1d a2d a6d")
            ),
        (
            Operator("bra", "a3 a2 a1 i3 i2 i1"),
            Operator("ket", "i1d i4d i5bd a1d a2d a6bd")
            ),
        # ----
        # 19
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i4d i5d i3bd a1d a6d a3bd")
            ),
        # 20
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i5bd a1d a6d a3bd")
            ),
        # 21
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i5d a1d a2d a6d")
            ),
        # 22
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i4d i5bd i3bd a1d a6bd a3bd")
            ),
        # 23
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4d i5bd a1d a2d a6bd")
            ),
        # 24
        (
            Operator("bra", "a3b a2 a1 i3b i2 i1"),
            Operator("ket", "i1d i4bd i5bd a1d a6bd a3bd")
            ),
        # =------
        # 25
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4d i2bd i5bd a6d a2bd a3bd")
            ),
        # 26
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4d i5d i3bd a1d a6d a3bd")
            ),
        # 27
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4d i2bd i5bd a1d a2bd a6bd")
            ),
        # 28
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i4bd i2bd i5bd a6bd a2bd a3bd")
            ),
        # 29
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i4d i5bd a1d a6d a3bd")
            ),
        # 30
        (
            Operator("bra", "a3b a2b a1 i3b i2b i1"),
            Operator("ket", "i1d i4bd i5bd a1d a2bd a6bd")
            ),

        # ---
        # 31
        (
            Operator("bra", "a3b a2b a1b i3b i2b i1b"),
            Operator("ket", "i4d i2bd i5bd a6d a2bd a3bd")
            ),
        # 31
        (
            Operator("bra", "a3b a2b a1b i3b i2b i1b"),
            Operator("ket", "i1bd i4bd i5bd a1bd a2bd a6bd")
            ),

        )



def run(h, bra, ket, python_out):

    # aaa
    #bra = Operator("bra", "cb b a kb j i")
    #ket = Operator("ket", "id jd kbd ad bd cbd")

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
            w = int(math.sqrt(cnt)) * new_weights[term]
            if w < 0:
                str_out = "-" + term.to_python()[1]
            else:
                str_out = term.to_python()[1]

            python_out.append(str_out)

        print("==================================\n")



#run(hs[0])
for idx, bk in enumerate(braket):
    bra, ket = bk
    diffs = get_diff(bra, ket)
    str_out = "\n\n" + str(idx + 1) + " -- " + str(bra) + " " + str(ket) \
            + " -- " + str(diffs)
    print(str_out)
    print("^"*len(str_out))
    python_out = []
    for h in hs[16:]:
        run(h, bra, ket, python_out)

    #for line in python_out:
    #    print(line + ",")
