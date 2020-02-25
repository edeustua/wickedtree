from bintree import Operator, OperatorString, \
        Node, contract, collect_fully_contracted

def vt2_2():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd q sd r")
    t = Operator("t", "ed md fd nd")

    v.string[0].above = True
    v.string[1].below = True
    v.string[2].below = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, v, t, full_string

def vt2_2p():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r")
    t = Operator("t", "ed md fd nd")

    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, v, t, full_string

def zc1():
    z = Operator("z", "p q")
    t = Operator("t", "ad id")

    z.string[0].below = True
    z.string[1].above = True

    full_string = OperatorString(z.string + t.string)

    return None, full_string

def vc1():
    v = Operator("v", "p q r s")
    t = Operator("t", "ad id")

    v.string[0].below = True
    v.string[1].below = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(v.string + t.string)

    return None, full_string

# Testing
# -------
#p, full_string = vt2_2()
p, v, t, full_string = vt2_2p()
#p, v, t, full_string = vt2_2()
#p, full_string = vc1()
#p, full_string = zc1()
print(full_string)

# Initialize tree
root_node = Node(full_string)

# Contract string
contract(root_node)


# Pretty Print
#lines, _, _, _ = get_utf8_tree(root_node)
#for line in lines:
#    print(line)

#sys.exit()

full = collect_fully_contracted(root_node)
print("==================================\n\n")
print(len(full))

print(v)
for i, eq in enumerate(full):
    evs = [kd.evaluate() for kd in eq[1]]

    #print(eq[1])
    if 0 in evs:
        continue

    #print(eq[1])
    mv = v.eval_deltas(eq[1])
    mt = t.eval_deltas(eq[1])
    print(eq[0], mv, mt)

    #print(i, eq)

print("\nCollection")
print("----------")
counts = {}
full_set = set()
new_eqs = {}
if p is not None:
    for i, eq in enumerate(full):


        print(i+1, end="")
        eq_set = []
        for kro in eq[1]:
            if kro.a.operator is p \
                    or kro.b.operator is p:
                        out = "{}->{}".format(kro.a,
                                kro.b.operator.symbol)
                        if counts.get(out) is None:
                            counts[out] = 0
                        counts[out] += 1
                        eq_set.append(out)
                        print(" ",  out, end="")

        eq_set = frozenset(eq_set)
        new_eqs[eq_set] = eq
        #print(eq_set)
        full_set.add(eq_set)

        print("")
        #print(i+1, eq)

    print(counts)
    print(len(full_set), full_set)

print("\nUniques only")
print("-------------")

for key, eq in new_eqs.items():

    evs = [kd.evaluate() for kd in eq[1]]

    #print(eq[1])
    if 0 in evs:
        continue

    #print(eq[1])
    mv = v.eval_deltas(eq[1])
    mt = t.eval_deltas(eq[1])
    print(eq[0], mv, mt)


