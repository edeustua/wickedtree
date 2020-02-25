import pdb

OCCS_FIXED = "ijkl"
UNOCCS_FIXED = "abcd"
OCCS_FREE = "mno"
UNOCCS_FREE = "efgh"
FULL_FREE = "pqrstu"
PRIORITIES = {
        OCCS_FIXED + UNOCCS_FIXED: 10,
        OCCS_FREE + UNOCCS_FREE: 5,
        FULL_FREE: 1
        }

class Symbol:

    cache = {}

    def __new__(cls, label, dummy=True):

        # If fixed symbol, make sure it is not duplicated,
        # and if it is, return it from the cache
        if not dummy:

            cache_sym = cls.cache.get(label)
            if cache_sym:
                return cache_sym
            else:
                sym = super().__new__(cls)
                cls.cache[label] = sym
                return sym

        else:
            sym = super().__new__(cls)
            return sym


    def __init__(self, label, dummy=True):
        self.label = label
        self.dummy = dummy



class ElementaryOperator:
    """Elementary operator, creation/annihilation operator, in second quantization."""

    def __init__(self, symbol, dagger, operator, above=False,
            below=False, dummy=True):

        self.symbol = Symbol(symbol, dummy=dummy)

        self.operator = operator

        self.dagger = dagger
        self.above = above
        self.below = below

    def __str__(self):
        if self.dagger:
            res = "{}†".format(self.symbol.label)
        else:
            res = "{}".format(self.symbol.label)

        return res

    def __repr__(self):
        return self.__str__()


class KroneckerDelta:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def swap(self, ind):

        if ind is self.a or ind is self.b:
            return self.evaluate().symbol.label

        else:
            return None


    def evaluate(self):

        prior_a = None
        prior_b = None
        for key, val in PRIORITIES.items():

            if self.a.symbol.label in key:
                prior_a = val

            if self.b.symbol.label in key:
                prior_b = val

        assert isinstance(prior_a, int) and isinstance(prior_b, int), "Priorities not found"


        if prior_a == prior_b == 10:
            #print(self.a, self.b)
            #print(self.a.symbol, self.b.symbol)
            #pdb.set_trace()
            if self.a.symbol is self.b.symbol:
                return 1
            else:
                return 0

        else:
            if prior_a > prior_b:
                prior = self.a
                notprior = self.b
            else:
                prior = self.b
                notprior = self.a

            return prior


    def __str__(self):
        res = "δ({}{})".format(
                self.a.symbol.label,
                self.b.symbol.label)

        return res

    def __repr__(self):
        return self.__str__()


class MatrixOperator:

    def __init__(self, symbol, lower, upper):
        self.symbol = symbol
        self.lower = lower
        self.upper = upper


    def __str__(self):
        op_str = self.symbol
        op_str += "_{"
        op_str += "".join(self.lower)
        op_str += "}^{"
        op_str += "".join(self.upper)
        op_str += "}"
        return op_str

    def __repr__(self):
        return self.__str__()



class Operator:

    def __init__(self, symbol, indices):
        self.symbol = symbol
        #self.order = order
        self.indices = indices
        self.string = parse_str(indices, self)

        self.upper = []
        self.lower = []

        for ind in self.string:
            if ind.dagger:
                self.lower.append(ind)
            else:
                self.upper.append(ind)

        self.upper = list(reversed(self.upper))

        if 't' in self.symbol:

            self.upper = []
            self.lower = []

            for ind in self.string:
                if ind.above:
                    self.lower.append(ind)
                else:
                    self.upper.append(ind)


    def eval_deltas(self, deltas):

        new_lower = []
        new_upper = []

        for ind_l, ind_u in zip(self.lower, self.upper):

            for delta in deltas:

                tmp = delta.swap(ind_l)
                if tmp is not None:
                    new_lower.append(tmp)

                tmp = delta.swap(ind_u)
                if tmp is not None:
                    new_upper.append(tmp)

        mo = MatrixOperator(self.symbol, new_lower, new_upper)
        return mo


    def __str__(self):
        op_str = ""
        for op in self.string:
            op_str += "{} ".format(op)

        string = "{}({})".format(self.symbol, op_str[:-1])
        return string


    def __repr__(self):
        return self.__str__()


class OperatorString:

    def __init__(self, string, sign=1):

        self.string = string
        self.sign = sign
        self.deltas = []

    def get_dagger(self, end_pos):

        for i, op in enumerate(self.string):
            if op.dagger and i >= end_pos:
                return i, op

        return None, None

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


def full_wicks(node, end_pos = 0):

    if node is None:
        return

    string = node.data
    if len(string) == 0:
        return

    pos, dag = string.get_dagger(end_pos)
    if pos is None:
        return

    if pos == end_pos:
        end_pos += 1
        pos, dag = string.get_dagger(end_pos)
        if pos is None:
            return

    if pos > end_pos:
    #if True:
        left_op = string[pos-1]

        # attempt contraction and load it to the left branch
        if not (dag.dagger and left_op.dagger) \
                and ((dag.above and left_op.above) or (dag.below and
                    left_op.below)) \
                and dag.operator is not left_op.operator:

                    # create new operator product
                    new_string = OperatorString(
                            string[:pos-1] + string[pos+1:],
                            sign=string.sign)

                    # copy deltas
                    new_string.deltas = string.deltas[:]

                    # append new delta
                    new_string.add_contraction(KroneckerDelta(left_op, dag))

                    node.left = Node(new_string)

        # permute operator and load to the right branch
        new_string = OperatorString(
                string[:pos-1] + [dag] + [left_op] + string[pos+1:],
                sign=-string.sign)

        # copy deltas
        new_string.deltas = string.deltas[:]

        node.right = Node(new_string)

        full_wicks(node.left, end_pos)
        full_wicks(node.right, end_pos)


def contract(node):

    if node is None:
        return

    string = node.data
    if len(string) == 0:
        return

    pos, dag = string.get_dagger(0)
    if pos is None:
        return

    if pos > 0:
        left_op = string[pos-1]

        # attempt contraction and load it to the left branch
        if not (dag.dagger and left_op.dagger) \
                and ((dag.above and left_op.above) or (dag.below and
                    left_op.below)) \
                and dag.operator is not left_op.operator:

                    # create new operator product
                    new_string = OperatorString(
                            string[:pos-1] + string[pos+1:],
                            sign=string.sign)

                    # copy deltas
                    new_string.deltas = string.deltas[:]

                    # append new delta
                    new_string.add_contraction(KroneckerDelta(left_op, dag))

                    node.left = Node(new_string)

        # permute operator and load to the right branch
        new_string = OperatorString(
                string[:pos-1] + [dag] + [left_op] + string[pos+1:],
                sign=-string.sign)

        # copy deltas
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
        return ([(string.sign, string.deltas)] + collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))

    else:
        return (collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))

def parse_str(inds, operator=object()):

    string = []
    inds = inds.split()

    for idx in inds:
        above = False
        below = False

        if idx[:1] in OCCS_FIXED + UNOCCS_FIXED:
            dummy = False
        else:
            dummy = True

        if idx[0] in OCCS_FREE + OCCS_FIXED:
            below = True

        elif idx[0] in UNOCCS_FREE + UNOCCS_FIXED:
            above = True

        if "†" in idx or ("d" in idx and len(idx) > 1):
            string.append(ElementaryOperator(idx[:-1], True, operator,
                above=above, below=below, dummy=dummy))
        else:
            string.append(ElementaryOperator(idx, False, operator,
                above=above, below=below, dummy=dummy))

    return string



