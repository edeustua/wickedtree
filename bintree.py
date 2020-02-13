import sys

import re
from printing import get_utf8_tree

OCCS_FIXED = "ijk"
UNOCCS_FIXED = "abc"
OCCS_FREE = "mno"
UNOCCS_FREE = "efg"

class LadderOperator:

    def __init__(self, symbol, dagger, operator, above=False,
            below=False):

        self.symbol = symbol
        self.dagger = dagger
        self.operator = operator
        self.above = above
        self.below = below

    def __str__(self):
        if self.dagger:
            res = "{}†".format(self.symbol)
        else:
            res = "{}".format(self.symbol)

        return res

    def __repr__(self):
        return self.__str__()

class KroneckerDelta:

    def __init__(self, a, b):
        self.a = a
        self.b = b


    def __str__(self):
        res = "δ({}{})".format(self.a.symbol, self.b.symbol)
        return res

    def __repr__(self):
        return self.__str__()


class Operator:

    def __init__(self, symbol, order, indices):
        self.symbol = symbol
        self.order = order
        self.indices = indices
        self.string = None

        self._create_string()

    def _create_string(self):


        string = []
        inds = self.indices.split()

        assert len(inds) == 2 * self.order, \
                "Indices don't match order"

        for idx in inds:
            above = False
            below = False

            if idx[0] in OCCS_FREE + OCCS_FIXED:
                below = True
            elif idx[0] in UNOCCS_FREE + UNOCCS_FIXED:
                above = True

            if "†" in idx or ("d" in idx and len(idx) > 1):
                string.append(LadderOperator(idx[:-1], True, self,
                    above=above, below=below))
            else:
                string.append(LadderOperator(idx, False, self,
                    above=above, below=below))



        self.string = string




    def __str__(self):
        op_str = ""
        for op in self.string:
            op_str += "{} ".format(op)

        string = "{}({})".format(self.symbol, op_str[:-1])
        #string += " at {}".format(hex(id(self)))
        return string

    def __repr__(self):
        return self.__str__()


class OperatorString:

    def __init__(self, string, sign=1):

        self.string = string
        self.sign = sign
        self.deltas = []

    def get_dagger(self):

        for i, op in enumerate(self.string):
            if op.dagger:
                return i, op

        return 0, None

    def append(self, item):
        self.string.append(item)

    def add_contraction(self, delta):
        self.deltas.append(delta)

    def __len__(self):
        return len(self.string)

    def __getitem__(self, key):
        return self.string[key]


    def __str__(self):
        out = str(self.string) + " " + str(self.deltas)
        if self.sign == 1:
            return "+" + out
        else:
            return "-" + out


    def __repr__(self):
        return self.__str__()



class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

#    def add(self, data):
#
#        cur = self
#
#        while cur is not None:
#
#            if data < cur.data:
#                if cur.left is None:
#                    cur.left = Node(data)
#                    return
#                cur = cur.left
#            else:
#                if cur.right is None:
#                    cur.right = Node(data)
#                    return
#                cur = cur.right


    def print(self):
        print(self.data)


def contract(node):

    if node is None:
        return

    string = node.data
    if len(string) == 0:
        return

    pos, dag = string.get_dagger()
    if pos > 0:
        left_dag = string[pos-1]

        if not (dag.dagger and left_dag.dagger) \
                and ((dag.above and left_dag.above) or (dag.below and
                    left_dag.below)) \
                and dag.operator is not left_dag.operator:

                    new_string = OperatorString(string[:pos-1] +
                            string[pos+1:])
                    new_string.deltas = string.deltas[:]
                    new_string.add_contraction(KroneckerDelta(left_dag, dag))
                    node.left = Node(new_string)

        new_string = OperatorString(string[:pos-1] + [dag] +
                [left_dag] + string[pos+1:], sign=-string.sign)
        new_string.deltas = string.deltas[:]
        node.right = Node(new_string)

        contract(node.left)
        contract(node.right)






def collect_fully_contracted(node):

    if node is None:
        return []

    string = node.data
    if len(string) == 0:
        #return ([[string.sign] + string.deltas] + collect_fully_contracted(node.left) +
        return ([string.deltas] + collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))

    else:
        return (collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))



def print_tree(node, space=0, char=""):
    pad = 1

    if node is not None:
        print_tree(node.right, space + pad, "/")
        print(space *" " + char + "{}".format(str(node.data)))
        print_tree(node.left, space + pad, "\\")


def vt2_2():

    p = Operator("p", 2, "j b i a")
    v = Operator("v", 2, "pd q sd r")
    t = Operator("t", 2, "ed md fd nd")

    v.string[0].above = True
    v.string[1].below = True
    v.string[2].below = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, full_string

def vt2_2p():

    p = Operator("p", 2, "j b i a")
    v = Operator("v", 2, "pd qd s r")
    t = Operator("t", 2, "ed md fd nd")

    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, full_string

def zc1():
    z = Operator("z", 1, "p q")
    t = Operator("t", 1, "ad id")

    z.string[0].below = True
    z.string[1].above = True

    full_string = OperatorString(z.string + t.string)

    return None, full_string

def vc1():
    v = Operator("v", 2, "p q r s")
    t = Operator("t", 1, "ad id")

    v.string[0].below = True
    v.string[1].below = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(v.string + t.string)

    return None, full_string

# Testing
# -------
#p, full_string = vt2_2()
p, full_string = vt2_2p()
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

for i, eq in enumerate(full):
    print(i, eq)

print("\nCollection")
print("----------")
counts = {}
full_set = set()
if p is not None:
    for i, eq in enumerate(full):
        print(i+1, end="")
        eq_set = []
        for kro in eq:
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
        #print(eq_set)
        full_set.add(eq_set)

        print()
        #print(i+1, eq)

    print(counts)
    print(len(full_set), full_set)
