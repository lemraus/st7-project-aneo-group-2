import json
import math
import os

import matplotlib.pyplot as plt
import networkx as nx

from construct_graph import construct_graph

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")


# graphs = ["exampleGraph", "graph", "MediumComplex", "mediumRandom", "smallComplex", "smallRandom"]

# def jsonDataFile(name):
#     return os.path.join(DATA_DIR, f"{name}.json")

# def parse_time(string):
#     temp = string.split(':')
#     return 3600*int(temp[0]) + 60*int(temp[1]) + math.ceil(float(temp[2]))

# def makeGraph(name):
#     graph = nx.DiGraph()
#     with open(jsonDataFile(name)) as jsonFile:
#         dataDict = json.load(jsonFile)
#         first_node = int(list(dataDict["nodes"].keys())[0])
#         for key, value in dataDict["nodes"].items():
#             graph.add_node(str(int(key)-first_node), data=parse_time(value["Data"]))
#             for otherKey in value["Dependencies"]:
#                 graph.add_edge(str(int(otherKey)-first_node), str(int(key)-first_node))

#     return graph


def scheduler(nb_machines, graph):
    bfs = nx.bfs_edges(graph, "0")
    schedule = [["0", 0]]
    i = 1
    for (parent, child) in bfs:
        schedule.append([child, i % nb_machines])
        i += 1

    return schedule



def init_generation(nb_chrm, max_machine, graph):
    generation = []
    for i in range(nb_chrm):
        generation.append(scheduler(i % max_machine + 1, graph))
    return generation


# The bfs algorithm is bfs_edges(G, source)


if __name__ == "__main__":
    G = construct_graph("smallRandom")
    nx.draw_kamada_kawai(G, with_labels=True)
    plt.draw()
    plt.show()
    # print(scheduler("mediumRandom", 5))
    gen = init_generation(100, 10, G)
    for chr in gen:
        print(chr)
