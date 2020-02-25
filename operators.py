import itertools as it
from bintree import Operator, OperatorString, \
        Node, contract, collect_fully_contracted

import sys


def set_fermi(typs, op):

    for i, typ in enumerate(typs):
        if typ == "o":
            op.string[i].below = True
        elif typ == "u":
            op.string[i].above = True


def gen_fermi_onebody():

    ops = [Operator("h1(oo)", "p qd"),
            Operator("h1(uu)", "pd q")]

    set_fermi("oo", ops[0])
    set_fermi("uu", ops[1])

    return ops

def gen_fermi_threebody():

    ops = [Operator("h3(uuouuo)", "pd qd r u t sd")]
    set_fermi("uuouuo", ops[0])

    return ops



def gen_fermi_twobody():

    string = "pqsr"
    c1 = it.permutations("ou")
    c2 = it.permutations("ou", r=2)

    ops = [Operator("h2(oooo)", "p q sd rd")]
    set_fermi("oooo", ops[0])

    for i in it.product(c1, c2):
        s = i[0] + i[1]

        out = []
        for ind, typ in zip(string, s):
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

        op = Operator("h2("+"".join(s) + ")", " ".join(out))
        set_fermi(s, op)
        #print(s)
        #for i in op.string:
        #    print(i.below, i.above)
        #print(op)
        ops.append(op)

    op = Operator("h2(uuuu)", "pd qd s r")
    set_fermi("uuuu", op)
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
        contract(root_node)
        full = collect_fully_contracted(root_node)

        for eq in full:

            evs = [kd.evaluate() for kd in eq[1]]

            #print(eq[1])
            if 0 in evs:
                continue

            #print(eq[1])
            m = op.eval_deltas(eq[1])
            print(eq[0], m)

        print('--------------------------------')



