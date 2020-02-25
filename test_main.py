from bintree import Operator, OperatorString, \
        Node, contract, collect_fully_contracted

def vt2_2p():

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r")
    t = Operator("t", "ed md fd nd")

    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, full_string

def test_vt2_2p():

    p, full_string = vt2_2p()

    # Initialize tree
    root_node = Node(full_string)

    # Contract string
    contract(root_node)

    #
    full = collect_fully_contracted(root_node)

    check = [
             "(1, [δ(ap), δ(bq), δ(re), δ(im), δ(sf), δ(jn)])",
             "(-1, [δ(ap), δ(bq), δ(re), δ(jm), δ(sf), δ(in)])",
             "(-1, [δ(ap), δ(bq), δ(se), δ(im), δ(rf), δ(jn)])",
             "(1, [δ(ap), δ(bq), δ(se), δ(jm), δ(rf), δ(in)])",
             "(-1, [δ(bp), δ(aq), δ(re), δ(im), δ(sf), δ(jn)])",
             "(1, [δ(bp), δ(aq), δ(re), δ(jm), δ(sf), δ(in)])",
             "(1, [δ(bp), δ(aq), δ(se), δ(im), δ(rf), δ(jn)])",
             "(-1, [δ(bp), δ(aq), δ(se), δ(jm), δ(rf), δ(in)])"
            ]

    for eq_c, eq in zip(check, full):
        assert eq_c == str(eq)

