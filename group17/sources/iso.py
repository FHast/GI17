from math import inf
from group17.sources.dll import DoublyLinkedList


def solve_gi(graphs):
    """
    Solves the graph isomorphism problem given a list of graphs
    Prints lists of graphs that are isomorphic
    :param graphs: The graphs to check for being isomorphic or not
    """
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


def solve_aut_single(graph):
    """
    Solves the automorphism counting problem for a single graph
    Prints the number of automorphisms of the graph
    :param graph: The graph to solve
    """
    u = graph + graph
    num_aut = count_aut([], u.vertices)
    print("\nNumber of automorphisms: " + str(num_aut))


def solve_aut_list(graphs):
    """
    Solves the automorphism counting problem for a list of graphs
    First finds a list of isomorphic graphs and then counts the automorphisms of one of these graphs
    Prints lists of isomorphic graphs with their respective automorphism count
    :param graphs: The graphs to solve
    """
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


def is_isomorphic(colored, uncolored):
    """
    Determines whether an isomorphism exists between two graphs by looking at their vertices
    These vertices are split up into those with an initial coloring and those without
    Any vertex of either of the graphs should be in one of the two lists at any time
    :param colored: A list of lists of vertices with the same initial color
    :param uncolored: A list of all vertices that have no initial color
    :return: Whether there is an isomorphism between the graphs or not
    """
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


def count_aut(colored, uncolored):
    """
    Counts the number of automorphisms of a graph
    The parameters should contain vertices of the disjoint union of this graph and a copy
    These vertices are split up into those with an initial coloring and those without
    Any vertex of either of the graphs should be in one of the two lists at any time
    :param colored: A list of lists of vertices with the same initial color
    :param uncolored: A list of all vertices that have no initial color
    :return: The amount of automorphisms of a given graph
    """
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


def color_refinement(colored, uncolored):
    """
    Determines the coarsest stable coloring that refines the coloring provided
    This provided coloring is split up in vertices with an initial coloring and those without
    Any vertex of either of the graphs should be in one of the two lists at any time
    :param colored: A list of lists of vertices with the same initial color
    :param uncolored: A list of all vertices without an initial color
    :return: The coarsest stable coloring
    """
    next_free_color = 0

    # List of colors that still need to be compared to for refinement
    queue = []

    # List of booleans to indicate if a color is or has been in the queue by index
    in_queue = []

    # List of DoublyLinkedLists of vertices representing the coloring
    coloring = []

    # Dictionary that maps each vertex to the node in the coloring representing that vertex
    vertex_to_node = {}

    # Dictionary that maps each vertex to its current color
    vertex_to_color = {}

    # Dictionary that maps every observed degree to a color
    degree_to_color = {}

    # Initialises local variables with the initially colored vertices
    for cell in colored:
        dll = DoublyLinkedList()
        for v in cell:
            vertex_to_color[v] = next_free_color
            node = dll.append_right(v)
            vertex_to_node[v] = node
        coloring.append(dll)
        next_free_color += 1
        in_queue.append(False)

    # Initialises local variables with the vertices without initial color
    # These vertices are grouped and given the same color according to their degree
    for v in uncolored:
        d = v.degree
        if d in degree_to_color:
            color = degree_to_color[d]
            vertex_to_color[v] = color
            dll = coloring[color]
            node = dll.append_right(v)
            vertex_to_node[v] = node
        else:
            degree_to_color[d] = next_free_color
            vertex_to_color[v] = next_free_color
            dll = DoublyLinkedList()
            coloring.append(dll)
            node = dll.append_right(v)
            vertex_to_node[v] = node
            next_free_color += 1
            in_queue.append(False)

    # Initialises the queue with all colors in the current coloring, except for the color of the largest color class
    x = 0
    size = len(coloring[0])
    for y in range(1, len(coloring)):
        k = len(coloring[y])
        if k < size:
            queue.append(y)
            in_queue[y] = True
        else:
            queue.append(x)
            in_queue[x] = True
            x = y
            size = k

    while queue:
        current_color = queue.pop(0)

        # Dictionary that maps all neighbours of the vertices inside the current color class
        # to the amount of transitions it has to vertices inside the current color class
        vertex_to_transitions = {}

        # Dictionary that maps the colors of all neighbours of the vertices inside the current color class
        # to a set of the neighbours with that color
        color_to_vertices = {}

        # Fill the two new dictionaries accordingly
        for v in coloring[current_color]:
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

        # Dictionary that maps the colors of all neighbours of the vertices inside the current color class
        # to dictionaries that maps the amount of transitions to vertices inside the current color class
        # to a set of the neighbours that of that color and transition count
        color_to_transitions_to_vertices = {}

        # Fill the new dictionary accordingly
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

        # Checks for all colors encountered if each vertex of this color has the same number of transitions
        # to vertices inside the current color class
        # Color classes are split up if this is not the case, creating a new color class for each transition count
        # If a color class is split up and the current color is in the queue, then all newly created color classes
        # are added to the queue.
        # If a color class is split up and the current color is not in the queue, then all color classes except the
        # biggest out of the newly created classes and the remaining current color class are added
        for i in color_to_transitions_to_vertices:
            m = color_to_transitions_to_vertices[i]
            biggest_class = None
            biggest_class_size = 0
            for c in m:
                s = m[c]
                if len(s) < len(coloring[i]):
                    dll = DoublyLinkedList()
                    in_queue.append(False)

                    for v in s:
                        node = dll.append_right(v)
                        vertex_to_node[v].remove()
                        vertex_to_node[v] = node
                        vertex_to_color[v] = next_free_color
                    coloring.append(dll)

                    if in_queue[i]:
                        queue.append(next_free_color)
                        in_queue[next_free_color] = True
                    elif biggest_class is None:
                        biggest_class = next_free_color
                        biggest_class_size = len(dll)
                    elif len(dll) > biggest_class_size:
                        queue.append(biggest_class)
                        in_queue[biggest_class] = True
                        biggest_class = next_free_color
                        biggest_class_size = len(dll)
                    else:
                        queue.append(next_free_color)
                        in_queue[next_free_color] = True

                        next_free_color += 1
            if biggest_class is not None:
                if biggest_class_size < len(coloring[i]):
                    queue.append(biggest_class)
                    in_queue[biggest_class] = True
                else:
                    queue.append(i)
                    in_queue[i] = True

    return coloring


def evaluate_coloring(coloring):
    """
    Evaluates a given coloring
    Determines whether this coloring is balanced or not
    If the coloring is balanced it determines whether it defines a bijection
    When there is no bijection defined, ideal vertices are determined for branching
    :param coloring: The coloring to evaluate
    :return: If the coloring is unbalanced, the first value is False and the other values are irrelevant
             If the coloring defines a bijection, the first value is True,
             the second is None and the third is irrelevant
             If the coloring is balanced but does not define a bijection, the first value is True,
             the second value is a vertex from the first graph and
             the third value a list of all vertices of the second graph in the same color class
    """
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
