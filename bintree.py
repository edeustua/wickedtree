import pdb
from fractions import Fraction

from printing import get_utf8_tree

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

    def __init__(self, symbol, dagger, operator,
            spin='a',
            above=False,
            below=False,
            dummy=True):

        self.symbol = Symbol(symbol, dummy=dummy)

        self.operator = operator

        self.dagger = dagger
        self.spin = spin
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


def contract(a, b):

    res = not (a.dagger and b.dagger)
    res = res and (
            (a.above and b.above) or
            (a.below and b.below)
            )

    res = res and (a.operator is not b.operator)
    #res = res and (a.spin == b.spin)

    return res


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
        elif prior_a == prior_b == 5:
            if "F" in self.a.operator.symbol or \
                    "V" in self.a.operator.symbol:
                return self.a

            else:
                return self.b

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

    def __init__(self, symbol, indices, typs=None, weight=1):

        self.symbol = symbol
        self.weight = weight
        self.typs = typs

        if isinstance(indices, str):
            self.indices = indices
            self.string = parse_str(indices, self)
        else:
            raise TypeError("indices must be string")
        #elif isinstance(indices, OperatorString):
        #    self.string

        if self.typs:
            self.set_fermi()

        self.upper = []
        self.lower = []


        #if not (ind.above or ind.below):

        #    for ind in self.string:
        #        if ind.dagger:
        #            self.lower.append(ind)
        #        else:
        #            self.upper.append(ind)


            # This might be wrong
        if 't' not in self.symbol:
            self.lower = self.string[:len(self.string)//2]
            self.upper = self.string[len(self.string)//2:]

            #    if ind.dagger:
            #        if ind.above:
            #            self.lower.append(ind)
            #        elif ind.below:
            #            self.upper.append(ind)
            #    else:
            #        if ind.above:
            #            self.upper.append(ind)
            #        elif ind.below:
            #            self.lower.append(ind)

            ##    self.upper = list(reversed(self.upper))

        elif 't' in self.symbol:
            for ind in self.string:
                if ind.above:
                    self.lower.append(ind)
                else:
                    self.upper.append(ind)
        else:
            raise TypeError("operator is not clear for indexing")

        if 't' not in self.symbol:
            self.upper = list(reversed(self.upper))


        self.op_string = OperatorString(self.string,
                weight=self.weight,
                sign=1)

    def set_fermi(self):

        assert len(self.string) == len(self.typs), \
                "Typs and string lenghts don't match"

        for i, typ in enumerate(self.typs):
            if typ == "o":
                self.string[i].below = True
            elif typ == "u":
                self.string[i].above = True
            elif typ == "f":
                self.string[i].above = True
                self.string[i].below = True


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


    def __mul__(self, other):
        res = self.op_string * other
        return res

    def __rmul__(self, other):
        res = other * self.op_string
        return res



    def __str__(self):
        op_str = ""
        for op in self.string:
            op_str += "{} ".format(op)

        string = "{}({})".format(self.symbol, op_str[:-1])
        return string


    def __repr__(self):
        return self.__str__()


class OperatorString:

    def __init__(self, input_string, weight=1, sign=1):

        if isinstance(input_string, list):
            self.string = input_string
            self.sign = sign
            self.weight = weight
            self.deltas = []

        elif isinstance(input_string, OperatorString):
            self.copy_from(input_string)


    def get_dagger(self, end_pos):

        for i, op in enumerate(self.string):
            if op.dagger and i >= end_pos:
                return i, op

        return None, None

    def append(self, item):
        self.string.append(item)

    def add_contraction(self, delta):
        self.deltas.append(delta)


    def __mul__(self, other):
        res = OperatorString(self)
        if isinstance(other, int):
            res.weight *= abs(other)
            res.sign = res.sign if other >= 0 else -res.sign

        elif isinstance(other, Fraction):
            res.weight *= other
            res.sign = res.sign if other >= 0 else -res.sign

        elif isinstance(other, OperatorString):
            res.string = res.string + other.string
            res.weight *= other.weight
            res.sign = res.sign if other.sign >= 0 else -other.sign

        else:
            return NotImplemented

        return res

    def __rmul__(self, other):
        res = OperatorString(self)
        if isinstance(other, int):
            res.weight *= abs(other)
            res.sign = res.sign if other >= 0 else -res.sign

        elif isinstance(other, Fraction):
            res.weight *= other
            res.sign = res.sign if other >= 0 else -res.sign

        elif isinstance(other, OperatorString):
            res.string = other.string + res.string
            res.weight *= other.weight
            res.sign = res.sign if other.sign >= 0 else -other.sign

        return res


    def copy_from(self, other):
        self.string = other.string.copy()
        self.sign = other.sign
        self.weight = other.weight
        self.deltas = other.deltas.copy()


    def __len__(self):
        return len(self.string)

    def __getitem__(self, key):
        return self.string[key]


    def __str__(self):
        out = "+" if self.sign >= 0 else "-"
        out += " " + str(self.weight) + " "
        out += "ops" + str(self.string) + " " \
                + "deltas" + str(self.deltas)
        return out


    def __repr__(self):
        return self.__str__()



class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def print(self):
        lines, _, _, _ = get_utf8_tree(self)
        for line in lines:
            print(line)


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


def wicks(node):

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
        if contract(dag, left_op):

                    # create new operator product
                    new_string = OperatorString(
                            string[:pos-1] + string[pos+1:],
                            sign=string.sign,
                            weight=string.weight)

                    # copy deltas
                    new_string.deltas = string.deltas[:]

                    # append new delta
                    new_string.add_contraction(KroneckerDelta(left_op, dag))

                    node.left = Node(new_string)

        # permute operator and load to the right branch
        new_string = OperatorString(
                string[:pos-1] + [dag] + [left_op] + string[pos+1:],
                sign=-string.sign,
                weight=string.weight)

        # copy deltas
        new_string.deltas = string.deltas[:]

        node.right = Node(new_string)

        wicks(node.left)
        wicks(node.right)



def collect_fully_contracted(node):

    if node is None:
        return []

    string = node.data
    if len(string) == 0:
        #return ([[string.sign] + string.deltas] + collect_fully_contracted(node.left) +
        return ([string] + collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))

    else:
        return (collect_fully_contracted(node.left) +
                collect_fully_contracted(node.right))

cfc = collect_fully_contracted


def collect_unique(p, terms):

    uniq_count = {}
    uniq_set = {}

    for term in terms:

        uniq_term_set = []
        for delta in term.deltas:
            if delta.a.operator is p or delta.b.operator is p:

                # do this to make the various ou instances of the
                # operators equivalent
                target_op = delta.b.operator.symbol
                if "V" in target_op or "F" in target_op:
                    uinds = target_op.count('u')
                    if 1 < uinds < 4 and target_op[0:1] == "V":
                        target_op = f"V({uinds})"
                    elif 1 < uinds < 2 and target_op[0:1] == "F":
                        target_op = f"F({uinds})"
                    else:
                        target_op = target_op[0:1]


                line_str = "{}->{}".format(
                        delta.a,
                        target_op
                        )

                uniq_count.setdefault(line_str, 0)
                uniq_count[line_str] += 1

                uniq_term_set.append(line_str)

        uniq_term_set = frozenset(uniq_term_set)

        uniq_set.setdefault(uniq_term_set, [])
        uniq_set[uniq_term_set].append(term)

    uniq_set_weights = {}
    for key, val in uniq_set.items():
        uniq_set_weights[key] = len(terms) / len(val)

    #print(len(terms))
    #print(uniq_set)

    return uniq_set, uniq_set_weights



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



