import itertools as it

from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted

from fractions import Fraction

import sys


def set_fermi(typs, op):

    for i, typ in enumerate(typs):
        if typ == "o":
            op.string[i].below = True
        elif typ == "u":
            op.string[i].above = True


def gen_fermi_onebody(label):

    ops = [
            Operator(label+"(oo)", "p qd", typs="oo"),
            Operator(label+"(ou)", "p q", typs="ou"),
            Operator(label+"(uo)", "pd qd", typs="uo"),
            Operator(label+"(uu)", "pd q", typs="uu")
            ]

    return ops

def gen_fermi_threebody():

    ops = [Operator("h3(uuouuo)", "pd qd r u t sd")]
    set_fermi("uuouuo", ops[0])

    return ops



def gen_fermi_twobody(label):

    string = "pqsr"

    ops = []

    for i in range(4+1):
        for j in it.combinations(range(4), i):
            typs = ['o'] * 4
            for indx in j:
                typs[indx] = 'u'

            typs = "".join(typs)

            out = []
            for ind, typ in zip(string, typs):

                if typ == 'o':
                    if ind in "pq":
                        out.append(ind)
                    elif ind in "sr":
                        out.append(ind + "d")

                elif typ == 'u':
                    if ind in "pq":
                        out.append(ind + "d")
                    elif ind in "sr":
                        out.append(ind)


            op = Operator(label+f"({typs})", " ".join(out),
                    typs=typs,
                    weight=Fraction(1,2))
            set_fermi(typs, op)
            ops.append(op)

    return ops




if __name__ == "__main__":

    ops = gen_fermi_onebody()
    #ops = gen_fermi_twobody()
    #ops = gen_fermi_threebody()

    bra = Operator("bra", "c b a k j i")
    ket = Operator("ket", "id jd kd ad bd dd")


    #sys.exit()

    for op in ops:
        print('--------', op, '-----------')
        fs = OperatorString(bra.string + op.string + ket.string)
        root_node = Node(fs)
        wicks(root_node)
        full = collect_fully_contracted(root_node)

        for eq in full:

            evs = [kd.evaluate() for kd in eq[1]]

            if 0 in evs:
                continue

            m = op.eval_deltas(eq[1])
            print(eq[0], m)

        print('--------------------------------')



