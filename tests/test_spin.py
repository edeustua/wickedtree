from fractions import Fraction
import math

import pytest

from wickedtree.bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        Symbol


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
        Operator("h3c(uoooou)", "pbd qb r ud tbd sb", typs='uoooou',
            weight=1),
        Operator("h3c(ououoo)", "pb qbd r u tbd sbd", typs='ououoo',
            weight=1),

        Operator("h3c(uuouuo)", "pbd qbd r u tb sbd", typs='uuouuo',
            weight=1),
        Operator("h3c(uuouou)", "pbd qbd r u tbd sb", typs='uuouou',
            weight=1),
        Operator("h3c(uouuuo)", "pbd qb rd u tb sbd", typs='uouuuo',
            weight=1),
        Operator("h3c(uououu)", "pbd qb rd ud tb sb", typs='uououu',
            weight=1),
        Operator("h3c(ouuouu)", "pb qbd rd ud tb sb", typs='ouuouu',
            weight=1),

        Operator("h3d(uoouoo)", "pbd qb rb ub tbd sbd", typs='uoouoo',
            weight=Fraction(1,2)),
        Operator("h3d(uuouuo)", "pbd qbd rb ub tb sbd", typs='uuouuo',
            weight=Fraction(1,2)),
        ]

inputs = {
        "aaa": (
            Operator("bra", "c b a k j i"),
            Operator("ket", "id jd kd ad bd cd")
            ),
        "aab": (
            Operator("bra", "cb b a kb j i"),
            Operator("ket", "id jd kbd ad bd cbd")
            ),
        "abb": (
            Operator("bra", "cb bb a kb jb i"),
            Operator("ket", "id jbd kbd ad bbd cbd")
            ),
        "bbb": (
            Operator("bra", "cb bb ab kb jb ib"),
            Operator("ket", "ibd jbd kbd abd bbd cbd")
            )
        }

outputs = ("aaa.txt", "aab.txt", "abb.txt", "bbb.txt")


def run(bra, ket, h):

    # out string
    str_out = ''

    fs = OperatorString(bra * h * ket)

    tree = Node(fs)
    wicks(tree)
    full = collect_fully_contracted(tree)

    new_eqs = []
    new_weights = {}
    if len(full) == 0:
        return str_out

    for i, eq in enumerate(full):
        evs = [x.evaluate() for x in eq.deltas]

        if 0 in evs:
            continue

        mv = h.eval_deltas(eq.deltas)

        new_eqs.append((eq.sign * eq.weight, mv))
        new_weights[mv] = eq.sign * eq.weight

    terms = list(zip(*new_eqs))

    # create box for Hamiltonian term
    if len(terms) > 0:
        uniques = find_equiv(list(terms[1]))
        str_out += "==================================\n"
        str_out += str(h) + "\n"
        str_out += '----------------\n'
        for cnt, term in uniques:
            str_out += str(int(math.sqrt(cnt)) * new_weights[term])
            str_out += " " + str(term)
            str_out += "\n"

        str_out += "==================================\n\n"

    return str_out


@pytest.mark.parametrize("test_input, expected", list(zip(inputs.items(), outputs)))
def test_spin(test_input, expected):

    # get input data
    case = test_input[0]
    bra, ket = test_input[1]

    # read expected output
    with open(expected) as f_in:
        file_data = f_in.read()

    # run wicks theorem
    str_out = ''
    for h in hs:
        str_out += run(bra, ket, h)

    assert file_data == str_out, \
            f"Files don't match in case {case}"
