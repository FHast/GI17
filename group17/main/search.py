import sources.graph
from sources.graph_io import *


def find_degrees(g):
    degrees = []
    for v in g.vertices:
        degrees.append([])
    for v in g.vertices:
        degrees[len(v.incidence)].append(v)
    return degrees

        
def find_start(g, degrees):
    min = 999999
    minIndex = 0
    for a in degrees:
        if len(a) == 1:
            return a
        if len(a) != 0 and len(a) < min:
            min = len(a)
            minIndex = a
    return minIndex

        
def bsearch(g, start, degrees):
    result = []
    result.append([start])
    i = 0
    while len(result[i]) != 0 and sum(len(x) for x in degrees) <= len(g.vertices) and i <= len(g.vertices):
        result.append([])
        for v in result[i]:
            for n in v.neighbours:
                if n not in result[i+1]:
                    result[i + 1].append(n)
        i += 1
    return result

    
def is_present(elem, result):
    for a in result:
        if (elem in a):
            return True
    return False


def main(g):
    degrees = find_degrees(g)
    results = []
    start =  find_start(g, degrees)
    for v in start:
        results.append(bsearch(g, v, degrees))
    return results

    
def is_isomorphic(results1, results2):
    for x in results1:
        for y in results2:
            if is_length_equal(x, y):
                return True
    return False
    
def is_length_equal(l1,l2):
    if len(l1) != len(l2):
        return False
    flag = True
    for i in range(len(l1)):
        flag = flag and len(l1[i])==len(l2[i]) 
    return flag
    
def test():
    with open("colorref_largeexample_6_960.grl") as inFile:
        list = load_graph(inFile, read_list=True)
        
    print(is_isomorphic(main(list[0][0]), main(list[0][2])))
    
    with open("visualisation.dot", "w") as dotFile:
        write_dot(list[0][0], dotFile)
    with open("visualisation2.dot", "w") as dotFile:
        write_dot(list[0][1], dotFile)
        

test()
