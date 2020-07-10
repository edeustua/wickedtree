from wickedtree.main import run
from wickedtree.bintree import Operator

from fractions import Fraction


# Two-body similarity transformed Hamiltonian
h2a = Operator("h2a(oooo)", "p q sd rd", typs='oooo',
        weight=Fraction(1,2))

bra = Operator("bra", "a3 a2 a1 i3 i2 i1")
ket = Operator("ket", "i1d i2d i3d a1d a2d a3d")

exps = run(h2a, bra, ket)

for exp in exps:
    print("--------------")
    print(exp[0])
    print(exp[1], exp[2])
    print("--------------\n")

