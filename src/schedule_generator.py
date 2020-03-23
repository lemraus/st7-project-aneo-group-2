import os
import networkx as nx
import json
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

#graphs = ["exampleGraph", "graph", "MediumComplex", "mediumRandom", "smallComplex", "smallRandom"]

def jsonDataFile(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def makeGraph(name):
    G = nx.DiGraph()
    with open(jsonDataFile(name)) as jsonFile:
        dataDict = json.load(jsonFile)
        for key, value in dataDict["nodes"].items():
            G.add_node(key, data=value["Data"])
            for otherKey in value["Dependencies"]:
                G.add_edge(str(otherKey), key)

    return G

def scheduler(nb_machines, name):
    G = makeGraph(name)
    bfs = nx.bfs_edges(G, "1")
    schedule = [("1", "0")]
    i = 1
    for (parent, child) in bfs:
        schedule.append((child, str(i % nb_machines)))
        i += 1

    return schedule

# The bfs algorithm is bfs_edges(G, source)

# nx.draw_kamada_kawai(G, with_labels = True)
# plt.draw()
# plt.show()

# Pour tester:
if __name__ == "__main__":
    print(scheduler(5, "mediumRandom"))
