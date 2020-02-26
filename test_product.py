from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        collect_unique

from fractions import Fraction

def vt2_2():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r",
            typs="uoou",
            weight=Rational(1,2))
    t = Operator("t", "ed md fd nd", weight=Rational(1,2))

    full_string = OperatorString(p.string + v.string + t.string,
            weight=Fraction(1/4))

    return p, v, t, full_string

def test_vt2_2p():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r", weight=Fraction(1,2))
    t = Operator("t", "ed md fd nd", weight=Fraction(1,2))

    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    print(v * t)

    #full_string = OperatorString(p.string + v.string + t.string,
    #        weight=Fraction(1/4))

    #return p, v, t, full_string

if __name__ == "__main__":
    test_vt2_2p()

