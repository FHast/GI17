from typing import List, Set, Dict, FrozenSet

import os

from group17.sources.graph import Vertex, Graph
from group17.sources.graph_io import load_graph, write_dot

"""
A set containing all lists of graphs that will be tested when running this module
Comment out a line to exclude the graphs in the file from the test
"""
TEST_GRAPHS = set()

# TEST_GRAPHS.add("colorref_largeexample_4_1026.grl")
# TEST_GRAPHS.add("colorref_largeexample_6_960.grl")
# TEST_GRAPHS.add("colorref_smallexample_2_49.grl")
# TEST_GRAPHS.add("colorref_smallexample_4_7.grl")
# TEST_GRAPHS.add("colorref_smallexample_4_16.grl")
# TEST_GRAPHS.add("colorref_smallexample_6_15.grl")
TEST_GRAPHS.add("threepaths2560.gr")

TESTFILES_PATH = os.path.split(os.getcwd())[0] + "/testfiles/"
DOTFILES_PATH = os.path.split(os.getcwd())[0] + "/dotfiles/"


def color_refinement(graph: Graph, initial: Set[FrozenSet[Vertex]] = set()) -> Set[FrozenSet[Vertex]]:
    partition = initial
    result = set()
    done = False
    if not partition:
        partition = degree_partitioning(graph)

    while not done:
        result = set()
        done = True
        assign_colors(partition)
        neighbourhoods = map_neighbourhoods(graph)
        for cell in partition:
            refined = refine_cell(cell, neighbourhoods)
            if len(refined) == 1:
                result.add(cell)
            else:
                done = False
                for c in refined:
                    result.add(c)
        partition = result

    assign_colors(result)
    return result


def refine_cell(cell: FrozenSet[Vertex], neighbourhoods: Dict[Vertex, List[int]]) -> Set[FrozenSet[Vertex]]:
    result = set()
    if len(cell) == 0:
        return result
    elif len(cell) == 1:
        result.add(frozenset(cell))
        return result
    else:
        check = None
        checked_positive = set()
        checked_negative = set()
        for v in cell:
            if check is None:
                if not neighbourhoods[v]:
                    result.add(frozenset(cell))
                    return result
                check = neighbourhoods[v].pop()
                checked_positive.add(v)
            elif check in neighbourhoods[v]:
                checked_positive.add(v)
                neighbourhoods[v].remove(check)
            else:
                checked_negative.add(v)
        positive_refined = refine_cell(frozenset(checked_positive), neighbourhoods)
        for c in positive_refined:
            result.add(c)
        negative_refined = refine_cell(frozenset(checked_negative), neighbourhoods)
        for c in negative_refined:
            result.add(c)
        return result


def map_neighbourhoods(graph: Graph) -> Dict[Vertex, List[int]]:
    result = {}
    for v in graph:
        neighbourhood = []
        result[v] = neighbourhood
        for n in v.neighbours:
            neighbourhood.append(n.colornum)

    return result


def degree_partitioning(graph: Graph) -> Set[FrozenSet[Vertex]]:
    result = set()
    color_map = {}
    for v in graph.vertices:
        if v.degree not in color_map:
            color_map[v.degree] = set()
        color_map[v.degree].add(v)
    for c in color_map:
        result.add(frozenset(color_map[c]))
    return result


def assign_colors(partition: Set[FrozenSet[Vertex]]):
    colornum = 0
    for cell in partition:
        for v in cell:
            v.colornum = colornum
        colornum += 1


def count_isomorphisms(vertices_g, vertices_h, done, todo) -> int:
    return 0


if __name__ == "__main__":
    if not os.path.exists(DOTFILES_PATH):
        os.makedirs(DOTFILES_PATH)
    for file_name in TEST_GRAPHS:
        with open(TESTFILES_PATH + file_name) as f:
            L = load_graph(f)

        g = L
        color_refinement(g)
        dot_name = "Test.dot"
        with open(DOTFILES_PATH + dot_name, 'w') as f:
            write_dot(g, f)
