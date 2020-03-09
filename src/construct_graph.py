import os
import networkx as nx
import json
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

def jsonDataFile(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def main():
    G = nx.DiGraph()
    with open(jsonDataFile("smallComplex")) as jsonFile:
        dataDict = json.load(jsonFile)
        for key, value in dataDict["nodes"].items():
            G.add_node(key, data=value["Data"])
            for otherKey in value["Dependencies"]:
                G.add_edge(str(otherKey), key)

    print(f"Longest path: {nx.algorithms.dag.dag_longest_path(G)}")
    print(f"Length of the longest path: {nx.algorithms.dag.dag_longest_path_length(G)}")

if __name__ == "__main__":
    main()