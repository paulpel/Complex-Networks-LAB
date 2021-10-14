import os
import networkx as nx
import matplotlib.pyplot as plt
import random

def main():
    script_path = script_path = os.path.dirname(os.path.abspath(__file__))
    edges = get_actors(script_path)
    random_edges = random_connections(edges)
    print_graph(random_edges)

def get_actors(script_path):
    connections = []
    data_path  = os.path.join(script_path, 'data', 'movie_actors.txt')
    with open(data_path, 'r', encoding='latin-1') as textfile:
        for line in textfile:
            connection = tuple(line.strip().split(' '))
            connections.append(connection)
    return connections

def random_connections(connections):
    random_c = []
    for i in range(200):
        random_c.append(random.choice(connections))
    return random_c

def print_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    nx.draw_random(G, node_size=100)
    plt.show()

if __name__ == "__main__":
    main()