import json
import os
import networkx as nx
import matplotlib.pyplot as plt

def read_json():
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_path, 'witcher_connections.json')
    with open(data_path, 'r') as jf:
        data = json.load(jf)
    return data

def create_connections(data):
    connections = set()
    for key in data:
        for relation in data[key]:
            connections.add((key, relation))
    return list(connections)

if __name__ == "__main__":
    data = read_json()
    connections = create_connections(data)

    G = nx.Graph()
    G.add_edges_from(connections)

    nx.draw_spring(G, with_labels=True)
    plt.show()
