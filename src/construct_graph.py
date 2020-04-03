import os
import networkx as nx
import json
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

def parse_time(string):
    temp = string.split(':')
    return 3600*int(temp[0]) + 60*int(temp[1]) + int(temp[2])

def json_data_file(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def main():
    G = nx.DiGraph()
    current_index = 0
    keys_indexes = {}
    with open(json_data_file("smallComplex")) as json_file:
        data_dict = json.load(json_file)
        for key, value in data_dict["nodes"].items():
            keys_indexes[key] = current_index
            G.add_node(current_index, data=parse_time(value["Data"]))
            for other_key in value["Dependencies"]:
                G.add_edge(keys_indexes[str(other_key)], current_index)
            current_index += 1

    print(f"Longest path: {nx.algorithms.dag.dag_longest_path(G)}")
    print(f"Length of the longest path: {nx.algorithms.dag.dag_longest_path_length(G)}")

if __name__ == "__main__":
    main()
