import os
from sources.graph_io import load_graph
from sources.iso import solve_aut_single, solve_gi, solve_aut_list

# The name of the directory that contains the graph files
GRAPH_DIRECTORY = "testfiles"


def iso_solver():
    """
    Handles user interaction and chooses algorithms to use accordingly
    """
    top_path = os.path.dirname(os.getcwd())
    graph_path = os.path.join(top_path, GRAPH_DIRECTORY)
    if os.path.exists(graph_path):
        keep_reading = True
        while keep_reading:
            file_name = input("Provide filename containing graphs (including extension): ")
            file_path = os.path.join(graph_path, file_name)
            if os.path.exists(file_path):
                if file_path.endswith(".gr"):
                    with open(file_path) as f:
                        graph = load_graph(f)
                    print("Single graph detected -> Solving #Aut problem")
                    solve_aut_single(graph)
                else:
                    with open(file_path) as f:
                        graphs = load_graph(f, read_list=True)[0]
                    done = False
                    while not done:
                        decision_str = input("Solve GI or #Aut problem? (gi/aut): ")
                        if decision_str == "gi":
                            solve_gi(graphs)
                            done = True
                        elif decision_str == "aut":
                            solve_aut_list(graphs)
                            done = True
                        else:
                            print("Input should be either 'gi' or 'aut'")
                keep_reading = None
                while keep_reading is None:
                    again_str = input("\nSolve another problem? (y/n): ")
                    if again_str == "y":
                        keep_reading = True
                    elif again_str == "n":
                        keep_reading = False
                    else:
                        print("Input should be either 'y' or 'n'")
            else:
                print("Could not find graph file '" + file_name + "' in path '" + graph_path + "'")
    else:
        print("Could not find graph directory '" + GRAPH_DIRECTORY + "' in path '" + top_path + "'")


if __name__ == "__main__":
    iso_solver()
