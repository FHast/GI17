'''
Created on 9 Apr 2018

@author: gereon
'''

from sources.iso import color_refinement, evaluate_coloring
from sources.permv2 import permutation
from sources.basicpermutationgroup import FindNonTrivialOrbit, Orbit, Stabilizer
import os
import time
from shutil import rmtree
from sources.graph_io import load_graph, write_dot

TEST_GRAPHS = set()

# TEST_GRAPHS.add("threepaths5.gr")
# TEST_GRAPHS.add("threepaths10.gr")
# TEST_GRAPHS.add("threepaths20.gr")
# TEST_GRAPHS.add("threepaths40.gr")
# TEST_GRAPHS.add("threepaths80.gr")
# TEST_GRAPHS.add("threepaths160.gr")
# TEST_GRAPHS.add("threepaths320.gr")
# TEST_GRAPHS.add("threepaths640.gr")
# TEST_GRAPHS.add("threepaths1280.gr")
# TEST_GRAPHS.add("threepaths2560.gr")
# TEST_GRAPHS.add("threepaths5120.gr")
# TEST_GRAPHS.add("threepaths10240.gr")
# TEST_GRAPHS.add("colorref_smallexample_4_7.grl")
# TEST_GRAPHS.add("colorref_smallexample_4_16.grl")
# TEST_GRAPHS.add("colorref_smallexample_6_15.grl")
# TEST_GRAPHS.add("torus24.grl")
# TEST_GRAPHS.add("colorref_smallexample_2_49.grl")
# TEST_GRAPHS.add("trees36.grl")
TEST_GRAPHS.add("cubes3.grl")
# TEST_GRAPHS.add("torus144.grl")

READ_LIST = True

TESTFILES_PATH = os.path.split(os.getcwd())[0] + "/testfiles/"
DOTFILES_PATH = os.path.split(os.getcwd())[0] + "/dotfiles/"

global generators

# this function collects all generators
def get_generators(colored, uncolored, trivial=False):
    coloring = color_refinement(colored, uncolored)
    evaluation = evaluate_coloring(coloring)
    if not evaluation[0]:
        return False  # 0

    x = evaluation[1]
    if x is None:
        cur_mapping = get_mapping(coloring)
        print(len(cur_mapping), cur_mapping)
        perm = permutation(len(cur_mapping), mapping=cur_mapping)
        if len(generators) == 0 or not membership(generators, perm):
            generators.append(perm)
        return True  # 
    else:
        # first recursion for trivial pairs
        uncolored.remove(x)
        for y in evaluation[2]:
            if y.number == x.number:
                pair = (x, y)
                colored.append(pair)
                uncolored.remove(y)
                get_generators(colored, uncolored, trivial)
                uncolored.append(y)
                colored.remove(pair)
        uncolored.append(x)
        # Now for all the other possibilities
        flag = False
        uncolored.remove(x)
        for y in evaluation[2]:
            if y.number != x.number:
                pair = (x, y)
                colored.append(pair)
                uncolored.remove(y)
                flag = get_generators(colored, uncolored)
                uncolored.append(y)
                colored.remove(pair)
            if flag and not trivial:
                break
        uncolored.append(x)
        return True  # after branching

def get_mapping(coloring):
    mapping = [0 for _ in range(len(coloring))]
    for cell in coloring:
        n0 = cell[0].number
        n1 = cell[1].number
        print(n0, n1)
        mapping[n0]=n1
        mapping[n1]=n0
    return mapping
    

def membership(generators, perm):
    # print(perm, generators)
    if perm in generators:
        return True
    non_trivial = FindNonTrivialOrbit(generators)
    if non_trivial == None:
        return False  # ???
    orbit, transversals = Orbit(generators, non_trivial, returntransversal=True)
    non_trivial_image = perm[non_trivial]
    
    # print(orbit, transversals, non_trivial, "->", non_trivial_image)
    stabilizer = Stabilizer(generators, non_trivial)
    # get the correct transversal u(a)=b
    i = 0
    try:
        while transversals[i][non_trivial] != non_trivial_image:
            i += 1
    except IndexError:
        return False
    computation_result = transversals[i] ** -1 * perm
    return membership(stabilizer, computation_result)


def automorphisms(graph):
    global generators
    i = 0
    for v in graph.vertices:
        v.number = i
        i += 1

    combined = graph + graph
    generators = []
    get_generators([], combined.vertices, generators)
    # print(generators)
    # order computation
    non_trivial = FindNonTrivialOrbit(generators)
    orbit = Orbit(generators, non_trivial)
    stabilizer = Stabilizer(generators, non_trivial)
    
    return len(orbit) * len(stabilizer)


def test_membership():
    g1 = permutation(7, cycles=[[0, 1, 2], [4, 5]])
    g2 = permutation(7, cycles=[[2, 3]])
    perm = permutation(7, cycles=[[0, 2]])
    
    return membership([g2, g1], perm)


def test_automorphism():
    t = time.clock()
    if os.path.exists(DOTFILES_PATH):
        rmtree(DOTFILES_PATH)
    os.makedirs(DOTFILES_PATH)
    for file_name in TEST_GRAPHS:
        if READ_LIST:
            with open(TESTFILES_PATH + file_name) as f:
                L = load_graph(f, read_list=True)[0]

            for i in range(len(L)):
                aut = automorphisms(L[i])
                print(i, "#aut:", aut)
    print(time.clock() - t)

    
test_automorphism()
# print(test_membership())

