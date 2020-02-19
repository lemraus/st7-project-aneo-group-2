import json

class Graph:
    def __init__(self, absJsonFilePath):
        with open(absJsonFilePath) as jsonFile:
            self.object = json.load(jsonFile)
            self.nodes = {}
            self.parents = {}
            for nodeId, value in self.object["nodes"].items():
                self.nodes[nodeId] = {
                    "duration": value["data"]
                }
                self.parents[nodeId] = [str(childId) for childId in value["dependencies"]]
            print("\n===== Graph data based on the input JSON file =====")
            print(f"\nNodes: {self.nodes}")
            print(f"\nParents: {self.parents}")
            

if __name__ == "__main__":
    import os
    SRC_DIR = os.path.abspath(os.path.curdir)
    ROOT_DIR = os.path.join(SRC_DIR, "..")
    graphJsonFilePath = os.path.join(ROOT_DIR, "graph.json")
    graph = Graph(graphJsonFilePath)