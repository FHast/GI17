import os

import time
from math import inf

from shutil import rmtree

from group17.sources.dll import DoublyLinkedList
from group17.sources.graph_io import load_graph, write_dot

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
# TEST_GRAPHS.add("cubes6.grl")
TEST_GRAPHS.add("torus144.grl")

READ_LIST = True

TESTFILES_PATH = os.path.split(os.getcwd())[0] + "/testfiles/"
DOTFILES_PATH = os.path.split(os.getcwd())[0] + "/dotfiles/"


def color_refinement(colored, uncolored):
    free_color = 0

    # Colors that need to be refined
    queue = []

    # List of color classes as DLL's containing all vertices in that color class
    color_classes = []

    # List of booleans to indicate if a color is in the queue
    in_queue = []

    # Maps vertices to dll nodes
    vertex_to_node = {}

    # Maps vertices to color classes
    vertex_to_color = {}

    # Maps vertex degree values to color values
    degree_to_color = {}

    for cell in colored:
        dll = DoublyLinkedList()
        for v in cell:
            vertex_to_color[v] = free_color
            node = dll.append_right(v)
            vertex_to_node[v] = node
        color_classes.append(dll)
        free_color += 1
        in_queue.append(False)

    for v in uncolored:
        d = v.degree
        if d in degree_to_color:
            color = degree_to_color[d]
            vertex_to_color[v] = color
            dll = color_classes[color]
            node = dll.append_right(v)
            vertex_to_node[v] = node
        else:
            degree_to_color[d] = free_color
            vertex_to_color[v] = free_color
            dll = DoublyLinkedList()
            color_classes.append(dll)
            node = dll.append_right(v)
            vertex_to_node[v] = node
            free_color += 1
            in_queue.append(False)

    x = 0
    size = len(color_classes[0])
    for y in range(1, len(color_classes)):
        k = len(color_classes[y])
        if k < size:
            queue.append(y)
            in_queue[y] = True
        else:
            queue.append(x)
            in_queue[x] = True
            x = y
            size = k

    while queue:

        popped = queue.pop(0)

        vertex_to_transitions = {}
        color_to_vertices = {}

        for v in color_classes[popped]:
            for n in v.neighbours:
                if n in vertex_to_transitions:
                    vertex_to_transitions[n] += 1
                else:
                    vertex_to_transitions[n] = 1

                i = vertex_to_color[n]
                if i in color_to_vertices:
                    color_to_vertices[i].add(n)
                else:
                    s = set()
                    s.add(n)
                    color_to_vertices[i] = s

        color_to_transitions_to_vertices = {}

        for i in color_to_vertices:
            m = {}
            for v in color_to_vertices[i]:
                c = vertex_to_transitions[v]
                if c in m:
                    m[c].add(v)
                else:
                    s = set()
                    s.add(v)
                    m[c] = s
            color_to_transitions_to_vertices[i] = m

        for i in color_to_transitions_to_vertices:
            m = color_to_transitions_to_vertices[i]
            biggest_class = None
            biggest_class_size = 0
            for c in m:
                s = m[c]
                if len(s) < len(color_classes[i]):
                    dll = DoublyLinkedList()
                    in_queue.append(False)

                    for v in s:
                        node = dll.append_right(v)
                        vertex_to_node[v].remove()
                        vertex_to_node[v] = node
                        vertex_to_color[v] = free_color
                    color_classes.append(dll)

                    if in_queue[i]:
                        queue.append(free_color)
                        in_queue[free_color] = True
                    elif biggest_class is None:
                        biggest_class = free_color
                        biggest_class_size = len(dll)
                    elif len(dll) > biggest_class_size:
                        queue.append(biggest_class)
                        in_queue[biggest_class] = True
                        biggest_class = free_color
                        biggest_class_size = len(dll)
                    else:
                        queue.append(free_color)
                        in_queue[free_color] = True

                    free_color += 1
            if biggest_class is not None:
                if biggest_class_size < len(color_classes[i]):
                    queue.append(biggest_class)
                    in_queue[biggest_class] = True
                else:
                    queue.append(i)
                    in_queue[i] = True

    return color_classes


def evaluate_coloring(coloring):
    smallest_class = None
    smallest_class_size = inf
    for cell in coloring:
        size = len(cell)
        if size % 2 == 0:
            if size == 2:
                if cell[0].id == cell[1].id:
                    return False, None, []
            else:
                check = 0
                for v in cell:
                    check += v.id
                if check != 0:
                    return False, None, []
                elif size < smallest_class_size:
                    smallest_class_size = size
                    smallest_class = cell
        else:
            return False, None, []

    if smallest_class is None:
        return True, None, []
    else:
        x = None
        y = set()
        for v in smallest_class:
            if v.id > 0:
                y.add(v)
            elif x is None:
                x = v
        return True, x, y


def count_aut(colored, uncolored):
    coloring = color_refinement(colored, uncolored)
    evaluation = evaluate_coloring(coloring)
    result = 0
    if not evaluation[0]:
        return 0
    x = evaluation[1]
    if x is None:
        return 1
    else:
        uncolored.remove(x)
        for y in evaluation[2]:
            pair = (x, y)
            colored.append(pair)
            uncolored.remove(y)
            result += count_aut(colored, uncolored)
            uncolored.append(y)
            colored.remove(pair)
        uncolored.append(x)
        return result


def is_isomorphic(colored, uncolored):
    coloring = color_refinement(colored, uncolored)
    evaluation = evaluate_coloring(coloring)
    if not evaluation[0]:
        return False
    x = evaluation[1]
    if x is None:
        return True
    else:
        uncolored.remove(x)
        for y in evaluation[2]:
            pair = (x, y)
            colored.append(pair)
            uncolored.remove(y)
            if is_isomorphic(colored, uncolored):
                return True
            uncolored.append(y)
            colored.remove(pair)
        uncolored.append(x)
        return False


def solve_aut_single(graph):
    u = graph + graph
    num_aut = count_aut([], u.vertices)
    print("\nNumber of automorphisms: " + str(num_aut))


def solve_aut_list(graphs):
    to_solve = list(range(len(graphs)))
    sets = []
    num_aut = []
    while to_solve:
        i = to_solve.pop(0)
        g = graphs[i]
        matches = [i]
        for j in to_solve:
            h = graphs[j]
            u = g + h
            if is_isomorphic([], u.vertices):
                matches.append(j)
        for x in matches:
            if x in to_solve:
                to_solve.remove(x)
        sets.append(matches)
        w = g + g
        num_aut.append(count_aut([], w.vertices))
    print("\n{0:30}  {1}".format("Sets of isomorphic graphs:", "Number of automorphisms:"))

    i = 0
    while i < len(sets):
        print("{0:30}  {1}".format(str(sets[i]), str(num_aut[i])))
        i += 1


def solve_gi(graphs):
    to_solve = list(range(len(graphs)))
    result = []
    while to_solve:
        i = to_solve.pop(0)
        g = graphs[i]
        matches = [i]
        for j in to_solve:
            h = graphs[j]
            u = g + h
            if is_isomorphic([], u.vertices):
                matches.append(j)
        for x in matches:
            if x in to_solve:
                to_solve.remove(x)
        result.append(matches)
    print("\nSets of isomorphic graphs:")
    for s in result:
        print(s)
