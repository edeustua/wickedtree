import sys

from bintree import Operator, OperatorString, \
        Node, contract, collect_fully_contracted, \
        Symbol

from printing import get_utf8_tree


#bra = Operator("bra", "a k j i")
#h1 = Operator("h1", "pd q")
#ket = Operator("ket", "id jd kd ad")
#
#h1.string[0].below = True
#h1.string[1].below = True

bra = Operator("bra", "a i")
h = Operator("h2", "pd q sd r")
ket = Operator("ket", "id ad")

h.string[0].above = True
h.string[1].below = True
h.string[2].below = True
h.string[3].above = True

#bra = Operator("bra", 1, "a b")
#h1 = Operator("h1", 1, "pd q")
#ket = Operator("ket", 1, "ad bd")

#h1.string[0].above = True
#h1.string[1].above = True

fs = OperatorString(bra.string + h.string + ket.string)
print(fs)
print("---------------")


root_node = Node(fs)
contract(root_node)

# Pretty Print
#lines, _, _, _ = get_utf8_tree(root_node)
#for line in lines:
#    print(line)

full = collect_fully_contracted(root_node)
print("==================================\n\n")

#print(full)
#sys.exit()
for i, eq in enumerate(full):
    evs = [x.evaluate() for x in eq[1]]
    #print(eq, evs)
    if 0 in evs:
        continue

    newinds = []
    for ind in h.string:
        for kd in eq[1]:
            ni = kd.swap(ind)
            if ni is not None:
                newinds.append(ni)

    mid = int(len(newinds) / 2)
    newinds = (
            newinds[:mid] +
            list(reversed(newinds[mid:]))
                )
    print(eq[0], "h1(",newinds,")")



print(bra, h, ket)

