from fractions import Fraction
import itertools as it

import click

from wickedtree.bintree import (
        OCCS_FREE, UNOCCS_FREE,
        OCCS_FIXED, UNOCCS_FIXED,
        FULL_FREE
        )
from wickedtree.bintree import Operator, Node, wicks, collect_fully_contracted, collect_unique
from wickedtree.operators import gen_fermi_onebody, gen_fermi_twobody


def get_single_operator(label, rank, spin):
    """Get an operator in a 3 digit representation. This version is
    used in BCH"""

    if label == "P":
        inds = [f"{i} {a}"
                for i, a in zip(OCCS_FIXED, UNOCCS_FIXED)]
        inds = " ".join(reversed(inds[0:rank]))

        string = Operator(label+str(rank), inds)

    elif label == "H":
        #mid = rank
        #inds = [f"{i}d" for i in FULL_FREE[0:mid]]
        #inds += [i for i in reversed(FULL_FREE[mid:2*rank])]

        #inds = " ".join(inds)
        if rank == 1:
            string = gen_fermi_onebody("F")
        elif rank == 2:
            string = gen_fermi_twobody("V")
        else:
            raise NotImplementedError(
                    "rank > 3 Hamiltonians not implemented"
            )

        #string = Operator(label+str(rank), inds)

    elif label == "T":
        inds = [f"{a}d {i}d"
                for i, a in zip(OCCS_FREE, UNOCCS_FREE)]
        inds = " ".join(inds[0:rank])

        string = Operator(label+str(rank), inds,
                weight=Fraction(1,rank))



    return string


def get_rhs_operators(label, ranks, spins, rhs):
    """Get the RHS operators in a 3 digit representation"""

    h_indx = 3
    p_indx = 4

    string = []

    ket_indx = 1
    bra_indx = 1

    for i in rhs:

        # skip indentity
        if i == 0:
            continue

        t = []

        for r in range(ranks[i-1]):
            spin_idx = 2 if ranks[i-1] - (r + 1) < spins[i-1] else 1
            t.append(spin_idx * 100 + h_indx * 10 + ket_indx)
            ket_indx += 1

        for r in reversed(range(ranks[i-1])):
            spin_idx = 2 if (r + 1) <= spins[i-1] else 1
            t.append(spin_idx * 100 + p_indx * 10 + bra_indx)
            bra_indx += 1

        string.append(t)

    return string

def test_allowed_contraction(p_id, h_id, rhs, op_rank):

    # get number of lines
    p_lines = 2*(op_rank[p_id])
    h_lines = 2*(op_rank[h_id])
    rhs_lines = [2*(op_rank[x-1]) for x in rhs if x > 0]

    total_lines = p_lines + h_lines + sum(rhs_lines)

    if total_lines / 2 < p_lines:
        return True
    elif total_lines / 2 < h_lines:
        return True
    elif total_lines / 2 < sum(rhs_lines):
        return True
    elif total_lines / 2 == p_lines \
            and sum(rhs_lines) != 0:
        return True

    return False

def bch_loop(order):

    op_rank = []
    op_spin = []

    for i in range(order):
        op_rank.append(i+1)
        #for j in range(i + 2):
        #    op_rank.append(i+1)
        #    op_spin.append(j)

    n_ops = len(op_rank)

    # T operators including identity
    ts = list(range(n_ops + 1))

    # Hamiltonian
    h_rank = op_rank[:5]
    #h_spin = op_spin[:5]
    n_ham = len(h_rank)


    CC = {}

    for p_id in range(n_ops):

        #f_out = OutTex(p_id, op_rank[p_id], op_spin[p_id])

        for rhs in it.combinations_with_replacement(ts, 4):

            scalars = []
            terms = []
            many_bodys = []
            hams = []

            for h_id in range(n_ham):

                if test_allowed_contraction(
                        p_id, h_id, rhs, op_rank
                        ):
                    continue


                # generate operators
                P = get_single_operator("P",
                        op_rank[p_id],
                        0)
                        #op_spin[p_id])

                H = get_single_operator("H",
                        op_rank[h_id],
                        0)
                        #op_spin[h_id])

                Ts = [get_single_operator("T",
                    op_rank[i-1],
                    0) for i in rhs if i > 0]


                key = f"{P} {op_rank[h_id]} {Ts}"
                CC.setdefault(key,
                        {
                            "titles": [],
                            "eqs": []
                        })

                for h in H:
                    #print('----------------------------')
                    CC[key]["titles"].append(f"{P} {h} {Ts}")

                    #print('')

                    string = P * h
                    #print(P * H)
                    #sys.exit()
                    for T in Ts:
                        string = string * T

                    #print(string)

                    # Initialize tree
                    tree = Node(string)
                    wicks(tree)

                    full = collect_fully_contracted(tree)
                    #print(tree.print())
                    #print(full)
                    #print(tree.print())
                    for i, eq in enumerate(full):
                        evs = [kd.evaluate() for kd in eq.deltas]
                        #print(eq.deltas)

                        #print(eq[1])
                        if 0 in evs:
                            continue


                        #print(eq[1])
                        mv = h.eval_deltas(eq.deltas)
                        mts = []
                        for T in Ts:
                            mt = T.eval_deltas(eq.deltas)
                            mts.append(mt)

                        ##print(eq.sign * eq.weight, mv, mt)
                        #print(eq.sign * eq.weight, mv)

                        CC[key]["eqs"].append((eq, mv, mts))

                # uniques only
                #all_eqs = [x[0] for x in CC[key]["eqs"]]
                #CC[key]["new_eqs"], CC[key]["new_eqs_weights"] = \
                #        collect_unique(P, all_eqs)

                    #for key, eqs in CC[key]["new_eqs"].items():

                    #    eq = eqs[0]

                    #    evs = [kd.evaluate() for kd in eq.deltas]

                    #    #print(eq[1])
                    #    if 0 in evs:
                    #        continue

                    #    #print(eq[1])
                    #    mv = v.eval_deltas(eq.deltas)
                    #    mt = t.eval_deltas(eq.deltas)
                    #    equiv = new_eqs_weights[key]
                    #    print(equiv)
                    #    print(eq.sign * eq.weight * equiv, mv, mt)



                    #print('----------------------------')
                    #if op_rank[h_id] > 1:
                    #    pass
                        #sys.exit()

    for key, val in CC.items():
        if len(val["eqs"]) > 0:
            print("----------------------")
            print(key)
            #print(val["titles"])

            #print(val["new_eqs"])

            #print("weight -> ", val["new_eqs_weights"])
            #for i, j in it.combinations(val["eqs"], 2):

            #seen_sets = set()

            #for idx_i, i in enumerate(val["eqs"]):
            #    inds_per_oper = []

            #    inds_per_oper.append(("h", i[1].lower + i[1].upper))

            #    all_inds = i[1].lower + i[1].upper

            #    for t in i[2]:
            #        inds_per_oper.append((t.symbol, t.lower + t.upper))
            #        all_inds += t.lower + t.upper


            #    for j in OCCS_FIXED + UNOCCS_FIXED:
            #        if j in all_inds:
            #            all_inds.remove(j)

            #    all_inds = set(all_inds)

            #    #import pdb; pdb.set_trace()
            #    edges = {}
            #    for j in all_inds:
            #        for k, v in inds_per_oper:
            #            #print(k, v)
            #            if j in v:
            #                edges.setdefault(j, [])
            #                edges[j].append(k)


            #    #print(edges)
            #    top = set()
            #    for k, v in edges.items():
            #        #assert len(v) == 2, f"{k}: {v} larger than 2"
            #        top.add(f"{v[0]}{k}{v[1]}")

            #    #print(edges)
            #    #print(top)

            #    #i_set = frozenset(i[1].lower + i[1].upper)
            #    #if i_set in seen_sets:
            #    #    continue
            #    #else:
            #    #    seen_sets.add(i_set)
            #    #
            #    #    print(i_set)

            #    #for idx_j in range(idx_i+i, len(val["eqs"])):
            #    #    pass





            for term in val["eqs"]:
                #print(term[0])

                print(term[0].sign * term[0].weight, term[1], term[2])


            print("----------------------\n")


@click.command()
@click.argument('order', nargs=1, type=int)
def main(order):
    bch_loop(order)


if __name__ == "__main__":
    main()
