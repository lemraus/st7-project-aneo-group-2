import os
import networkx as nx
import json
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

def jsonDataFile(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def makeGraph():
    G = nx.DiGraph()
    with open(jsonDataFile("smallRandom")) as jsonFile:
        dataDict = json.load(jsonFile)
        for key, value in dataDict["nodes"].items():
            G.add_node(key, data=value["Data"])
            for otherKey in value["Dependencies"]:
                G.add_edge(str(otherKey), key)

    return G

def scheduler():
    # We start with a bfs search
    G = makeGraph()
    bfs = nx.bfs_edges(G, "1")
    schedule = [("1", "1")]
    buff =  0
    for (parent, child) in bfs:
        schedule.append(("1", child))

    return schedule
# The bfs algorithm is bfs_edges(G, source)

# nx.draw_kamada_kawai(G, with_labels = True)
plt.draw()
plt.show()

if __name__ == "__main__":
    print(scheduler())