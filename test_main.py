from bintree import Operator, OperatorString, \
        Node, wicks, collect_fully_contracted

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
    tree = Node(full_string)

    # Contract string
    wicks(tree)

    #
    terms = collect_fully_contracted(tree)

    terms_master = [
             "[δ(ap), δ(bq), δ(re), δ(im), δ(sf), δ(jn)]",
             "[δ(ap), δ(bq), δ(re), δ(jm), δ(sf), δ(in)]",
             "[δ(ap), δ(bq), δ(se), δ(im), δ(rf), δ(jn)]",
             "[δ(ap), δ(bq), δ(se), δ(jm), δ(rf), δ(in)]",
             "[δ(bp), δ(aq), δ(re), δ(im), δ(sf), δ(jn)]",
             "[δ(bp), δ(aq), δ(re), δ(jm), δ(sf), δ(in)]",
             "[δ(bp), δ(aq), δ(se), δ(im), δ(rf), δ(jn)]",
             "[δ(bp), δ(aq), δ(se), δ(jm), δ(rf), δ(in)]"
            ]

    signs_master = [1, -1, -1, 1, -1, 1, 1, -1]


    assert len(terms_master) == len(terms), "Not the same length"

    for term_master, term in zip(terms_master, terms):
        assert term_master == str(term.deltas), \
                "Terms don't match" + str(term.detas)

    for sign_master, term in zip(signs_master, terms):
        assert sign_master == term.sign, \
                "Signs don't match" + str(term.sign)
