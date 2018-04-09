import os

import time

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
TEST_GRAPHS.add("colorref_smallexample_4_16.grl")

TESTFILES_PATH = os.path.split(os.getcwd())[0] + "/testfiles/"
DOTFILES_PATH = os.path.split(os.getcwd())[0] + "/dotfiles/"


def color_graph(g):
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

    for v in g.vertices:
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
            in_queue.append(True)
            queue.append(free_color)
            free_color += 1

    while queue:

        l_set = set()
        a_map = {}
        popped = queue.pop(0)

        for v in color_classes[popped]:
            for n in v.neighbours:
                i = vertex_to_color[n]
                if i in l_set:
                    a_map[i] += 1
                else:
                    l_set.add(i)
                    a_map[i] = 1

        # Transities van kleurgroepen naar kleurgoepen tellen voldoet niet
        # Transities van vertices naar kleurgroepen tellen implementeren

        new_color = {}

        for i in l_set:
            if a_map[i] < len(color_classes[i]):
                new_color[i] = free_color
                color_classes.append(DoublyLinkedList())
                if in_queue[i]:
                    queue.append(free_color)
                    in_queue.append(True)
                else:
                    if a_map[i] < len(color_classes[i]) - a_map[i]:
                        queue.append(free_color)
                        in_queue.append(True)
                    else:
                        queue.append(i)
                        in_queue[i] = True
                free_color += 1

        for v in color_classes[popped]:
            for n in v.neighbours:
                i = vertex_to_color[n]
                if i in new_color:
                    j = new_color[i]
                    node = color_classes[j].append_right(n)
                    vertex_to_node[n].remove()
                    vertex_to_node[n] = node
                    vertex_to_color[n] = j

    for v in g.vertices:
        v.colornum = vertex_to_color[v]


if __name__ == "__main__":
    t = time.clock()
    if not os.path.exists(DOTFILES_PATH):
        os.makedirs(DOTFILES_PATH)
    for file_name in TEST_GRAPHS:
        with open(TESTFILES_PATH + file_name) as f:
            L = load_graph(f)

        g = L

        color_graph(g)

        dot_name = file_name.split(".")[0] + ".dot"
        with open(DOTFILES_PATH + dot_name, 'w') as f:
            write_dot(g, f)
    print(time.clock() - t)
