from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted, \
        collect_unique

from fractions import Fraction

def vt2_2():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r",
            typs="uoou",
            weight=Fraction(1,2))
    t = Operator("t", "ed md fd nd", weight=Fraction(1,2))

    full_string = OperatorString(p.string + v.string + t.string,
            weight=Fraction(1/4))

    return p, v, t, full_string

def vt2_2p():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r", weight=Fraction(1,2))
    t = Operator("t", "ed md fd nd", weight=Fraction(1,2))

    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string,
            weight=Fraction(1/4))

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
p, v, t, full_string = vt2_2()
#p, v, t, full_string = vt2_2p()
#p, v, t, full_string = vt2_2()
#p, full_string = vc1()
#p, full_string = zc1()
print(full_string)

# Initialize tree
tree = Node(full_string)

# Contract string
wicks(tree)

full = collect_fully_contracted(tree)


# Pretty Print
#lines, _, _, _ = get_utf8_tree(root_node)
#for line in lines:
#    print(line)

#sys.exit()

print("==================================\n\n")

print(v)
for i, eq in enumerate(full):
    evs = [kd.evaluate() for kd in eq.deltas]

    #print(eq[1])
    if 0 in evs:
        continue

    #print(eq[1])
    mv = v.eval_deltas(eq.deltas)
    mt = t.eval_deltas(eq.deltas)
    print(eq.sign * eq.weight, mv, mt)

    #print(i, eq)

print("\nUniques only")
print("-------------")

new_eqs, new_eqs_weights = collect_unique(p, full)
for key, eqs in new_eqs.items():

    eq = eqs[0]

    evs = [kd.evaluate() for kd in eq.deltas]

    #print(eq[1])
    if 0 in evs:
        continue

    #print(eq[1])
    mv = v.eval_deltas(eq.deltas)
    mt = t.eval_deltas(eq.deltas)
    equiv = new_eqs_weights[key]
    print(equiv)
    print(eq.sign * eq.weight * equiv, mv, mt)


