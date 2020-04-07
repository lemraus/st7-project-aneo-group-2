import os
import networkx as nx
import json
import matplotlib.pyplot as plt
import math

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")

def parse_time(string):
    temp = string.split(':')
    return 3600*int(temp[0]) + 60*int(temp[1]) + math.ceil(float(temp[2]))

def json_data_file(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def construct_graph(filename):
    G = nx.DiGraph()
    current_index = 1
    keys_indexes = {}
    maximum_duration = 0

    # Initial node so all tasks have at least one dependency
    G.add_node('0', data=0)
    with open(json_data_file(filename)) as json_file:
        data_dict = json.load(json_file)
        for key, value in data_dict["nodes"].items():
            try: # if an index has already been attributed to the task
                G.add_node(keys_indexes[key], data=parse_time(value["Data"]))
            except KeyError: # else we attribute the task a new index to the task
                keys_indexes[key] = str(current_index)
                G.add_node(str(current_index), data=parse_time(value["Data"]))
                keys_indexes[key] = str(current_index)
                current_index += 1
                maximum_duration += parse_time(value["Data"])
            if value["Dependencies"]:
                for other_key in value["Dependencies"]:
                    try: # if an index has already been attributed to the task
                        G.add_edge(keys_indexes[str(other_key)], keys_indexes[key])
                    except KeyError: # else we attribute a new index to the task
                        G.add_edge(str(current_index), keys_indexes[key])
                        keys_indexes[str(other_key)] = str(current_index)
                        current_index += 1
                        maximum_duration += parse_time(value["Data"])
            else: # The task has no dependency
                G.add_edge('0', keys_indexes[key])

    return G, maximum_duration / 30

if __name__ == "__main__":
    G, _ = construct_graph("MediumComplex")
    nx.draw_kamada_kawai(G, with_labels=True)
    plt.draw()
    plt.show()
