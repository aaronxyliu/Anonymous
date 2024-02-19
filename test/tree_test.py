# Test suite for the labeled tree algorithm

import ultraimport
tree = ultraimport('__dir__/../utils/tree.py')
Vertex = tree.Vertex
Gamma = tree.Gamma
LabeledTree = tree.LabeledTree


def create_vertices(n):
    v = []
    for i in range(n):
        v.append(Vertex(i))
    return v

def create_test_trees():
    G = Gamma()

    v = create_vertices(10)
    v[1].addc(v[2])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T0'))

    v = create_vertices(10)
    v[1].addc(v[2])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T1'))

    v = create_vertices(10)
    v[1].addc(v[2])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T2'))

    v = create_vertices(10)
    v[1].addc(v[2])
    v[1].addc(v[6])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T3'))

    v = create_vertices(10)
    v[1].addc(v[2])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T4'))

    v = create_vertices(10)
    v[1].addc(v[2])
    v[2].addc(v[3])
    v[2].addc(v[4])
    G.addt(LabeledTree(v[1], 'T5'))

    v = create_vertices(10)
    v[0].addc(v[1])
    v[1].addc(v[2])
    v[2].addc(v[5])
    v[1].addc(v[6])
    G.addt(LabeledTree(v[1], 'T6'))

    v = create_vertices(10)
    v[0].addc(v[1])
    v[1].addc(v[2])
    v[1].addc(v[6])
    v[2].addc(v[3])
    v[2].addc(v[4])
    v[2].addc(v[5])
    G.addt(LabeledTree(v[1], 'T7'))

    return G

def print_fpath(trees): 
    print("\n===== Full Path Display =====\n")
    for i in range(len(trees)):
        print(trees[i].name + ':')
        for p in trees[i].fpaths:
            print("    " + str(p.vn))

def print_rpath(trees):
    print("\n===== Root Path Display =====\n")
    for i in range(len(trees)):
        print(trees[i].name + ':')
        for p in trees[i].rpaths:
            print("    " + str(p.vn))

def print_Omega(G):
    assert(isinstance(G, Gamma))
    print("\n===== Omega  Display =====\n")
    for i in range(len(G.trees)):
        print(G.trees[i].name + ':')
        print("    " + str(G.trees[i].Omega))

def print_S(G):
    assert(isinstance(G, Gamma))
    print("\n== Supertree Set Display ==\n")
    for i in range(len(G.trees)):
        print(G.trees[i].name + ':')
        print("    " + str(G.trees[i].S))

def print_Sm(G):
    assert(isinstance(G, Gamma))
    print("\n== Minified Strict Supertree Set Display ==\n")
    for i in range(len(G.trees)):
        print(G.trees[i].name + ':')
        print("    " + str(G.trees[i].Sm))



def test_suite1():
    G = create_test_trees()
    G.get_equivalence()
    G.get_trees_metas()
    print_fpath(G.trees)

    G.tree_size_reduction()
    G.get_mtrees_metas()
    print_fpath(G.mtrees)

    G.strict_supertree_set_minify()
    print_Sm(G)

def test_suite2():
    G = create_test_trees()
    print(G)

    G2 = G.freq_subtree_mining(4)
    print(G2)

    

if __name__ == '__main__':
    test_suite2()




