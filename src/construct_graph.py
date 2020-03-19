import os
import networkx as nx
import json
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

def json_data_file(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def main():
    G = nx.DiGraph()
    with open(json_data_file("smallComplex")) as json_file:
        data_dict = json.load(json_file)
        for key, value in data_dict["nodes"].items():
            G.add_node(key, data=value["Data"])
            for other_key in value["Dependencies"]:
                G.add_edge(str(other_key), key)

    print(f"Longest path: {nx.algorithms.dag.dag_longest_path(G)}")
    print(f"Length of the longest path: {nx.algorithms.dag.dag_longest_path_length(G)}")

if __name__ == "__main__":
    main()
