from group17.sources.graph_io import load_graph

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


def partition_refinement(graph, initial=set()):
    if not initial:
        pass


if __name__ == "__main__":
    for file_name in TEST_GRAPHS:
        with open(file_name) as f:
            L = load_graph(f, read_list=True)
