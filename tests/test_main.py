from wickedtree.bintree import Operator, OperatorString, Node, wicks, collect_fully_contracted


def vt2_2p():
    """Create V T_2 projected on 2 particles string"""

    p = Operator("p", "j b i a")
    v = Operator("v", "pd qd s r")
    t = Operator("t", "ed md fd nd")

    # set Fermi vacuum reference
    v.string[0].above = True
    v.string[1].above = True
    v.string[2].above = True
    v.string[3].above = True

    full_string = OperatorString(p.string + v.string + t.string)

    return p, full_string


def test_vt2_2p():
    """Test V T_2 projected on 2 particles"""

    p, full_string = vt2_2p()

    tree = Node(full_string)
    wicks(tree)

    terms = collect_fully_contracted(tree)

    terms_reference = [
             "[δ(ap), δ(bq), δ(re), δ(im), δ(sf), δ(jn)]",
             "[δ(ap), δ(bq), δ(re), δ(jm), δ(sf), δ(in)]",
             "[δ(ap), δ(bq), δ(se), δ(im), δ(rf), δ(jn)]",
             "[δ(ap), δ(bq), δ(se), δ(jm), δ(rf), δ(in)]",
             "[δ(bp), δ(aq), δ(re), δ(im), δ(sf), δ(jn)]",
             "[δ(bp), δ(aq), δ(re), δ(jm), δ(sf), δ(in)]",
             "[δ(bp), δ(aq), δ(se), δ(im), δ(rf), δ(jn)]",
             "[δ(bp), δ(aq), δ(se), δ(jm), δ(rf), δ(in)]"
            ]
    signs_reference = [1, -1, -1, 1, -1, 1, 1, -1]

    assert len(terms_reference) == len(terms), "Number of terms doesn't matchNot the same length"

    for term_ref, term in zip(terms_reference, terms):
        assert term_ref == str(term.deltas), "Terms don't match: " + str(term.detas)

    for sign_ref, term in zip(signs_reference, terms):
        assert sign_ref == term.sign, "Signs don't match: " + str(term.sign)
