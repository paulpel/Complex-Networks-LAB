import os
import json
import shutil
import networkx as nx
import matplotlib.pyplot as plt
from .colors_terminal import bcolors


class UsAirlines:

    def __init__(
            self, script_path,
            limited, show_graph,
            show_labels, print_stats) -> None:

        self.script_path = script_path
        self.nodes_to_take = [
            311, 150, 248, 118, 293, 258, 69, 161, 263, 261, 297, 4, 1, 2, 8, 6
            ]
        self.highlitght = []
        self.limited = limited
        self.show_graph = show_graph
        self.show_labels = show_labels
        self.print_stats = print_stats
        self.airport_data = {
            "airports": {},
            "connections": []
        }
        self.connections = []

    def main(self):
        self.load_data()
        self.create_output_dir()
        self.export_json()
        self.limit_edges()
        self.print_graph()

    def load_data(self):
        file_path = os.path.join(self.script_path, 'data', 'USAir97.net')
        with open(file_path, 'r') as txt_file:
            vertices = False
            edges = False
            for line in txt_file:

                if "*Vertices" in line:
                    vertices = True
                    edges = False
                    continue
                elif "*Edges" in line:
                    vertices = False
                    edges = True
                    continue

                if vertices:
                    list_name = line.split()
                    vert = list_name[0]
                    name = ' '.join(list_name[1:-3])
                    x_y_z = [float(elem) for elem in line.split()[-3:]]
                    x_y_z[1] = 1 - x_y_z[1]

                    self.airport_data['airports'][vert] = {
                        'name': name[1:-1],
                        'x_y_z_cords': x_y_z
                    }

                if edges:
                    connection = [int(x) for x in line.split()[:-1]]
                    connection.append(float(line.split()[-1]))
                    self.airport_data['connections'].append(tuple(connection))

    def create_output_dir(self):
        ot_path = os.path.join(self.script_path, 'output')
        if os.path.exists(ot_path):
            shutil.rmtree(ot_path)
        os.mkdir(ot_path)

    def export_json(self):
        output_path = os.path.join(
            self.script_path, 'output', 'airport_data.json')
        with open(output_path, 'w') as jf:
            json.dump(self.airport_data, jf, indent=2)

    def prepare_for_networkx(self, limited=False):
        labels = {}
        pos = {}
        for airport in self.airport_data['airports']:
            if limited:
                if int(airport) in self.nodes_to_take:
                    labels[int(airport)] = (
                        self.airport_data['airports'][airport]['name'])
                    pos[int(airport)] = (
                        self.airport_data['airports']
                        [airport]
                        ['x_y_z_cords'][:-1])

            else:
                labels[int(airport)] = (
                    self.airport_data['airports'][airport]['name'])
                pos[int(airport)] = (
                    self.airport_data['airports'][airport]['x_y_z_cords'][:-1])

        return labels, pos

    def color_specific_nodes(self, G):
        color_map = []
        for node in G:
            if node in self.highlitght:
                color_map.append('#CEFF00')
            else:
                color_map.append('#FF8243')
        return color_map

    def print_graph(self):
        fig, ax = plt.subplots(figsize=(15, 8))
        G = nx.Graph()

        if self.limited:
            edges = self.limit_edges()
            labels, pos = self.prepare_for_networkx(True)
        else:
            edges = self.airport_data['connections']
            labels, pos = self.prepare_for_networkx()

        if not self.show_labels:
            labels = None

        G.add_weighted_edges_from(edges)

        degree = self.print_graph_character(G)
        color_map = self.color_specific_nodes(G)

        nx.draw(
            G, pos=pos, labels=labels, with_labels=True,
            font_size=8, edge_color='#C8A2C8', node_size=200,
            node_color=color_map, node_shape='h')

        fig.set_facecolor('#6D9BC3')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.node_degree_hist(list(degree))

        if self.show_graph:
            plt.show()

    def limit_edges(self):
        nodes_to_take = self.nodes_to_take
        filtered_connections = []
        for connection in self.airport_data['connections']:
            if (connection[0] in nodes_to_take and
                    connection[1] in nodes_to_take):
                filtered_connections.append(connection)
        return filtered_connections

    def print_graph_character(self, G):
        density = nx.density(G)
        degree = nx.degree(G)
        close = nx.closeness_centrality(G)
        between = nx.betweenness_centrality(G)
        diameter = nx.diameter(G)
        connected_c = nx.connected_components(G)
        n = 4
        connected_n = nx.is_k_edge_connected(G, n)
        connectivity_e = nx.edge_connectivity(G)
        connectivity_n = nx.node_connectivity(G)
        edges = nx.number_of_edges(G)
        nodes = nx.number_of_nodes(G)
        path_av = nx.average_shortest_path_length(G)
        cliques = [x for x in nx.find_cliques(G)]
        max_cliques = self.maximum_cliques(cliques)
        if self.limited:
            cliques_bigger_than_3 = len(
                [x for x in nx.enumerate_all_cliques(G) if len(x) >= 3])
        self.highlitght = self.color_max_cliques(max_cliques)
        adjacency_matrix = nx.adjacency_matrix(G, weight=None)
        incidence_matrix = nx.incidence_matrix(G, weight=None, oriented=False)

        if self.print_stats:
            print(f'{bcolors.OKCYAN}Gęstość: {bcolors.ENDC}{density}')
            print(f"{bcolors.OKCYAN}Średnica {bcolors.ENDC}{diameter}")
            print(
                f"{bcolors.OKCYAN}Czy jest k-spójny dla k={n}:"
                f"{bcolors.ENDC}{connected_n}")
            print(
                f"{bcolors.OKCYAN}Spójność krawędziowa: "
                f"{bcolors.ENDC}{connectivity_e}")
            print(
                f"{bcolors.OKCYAN}Spójność wierzchołkowa: "
                f"{bcolors.ENDC}{connectivity_n}")
            print(f"{bcolors.OKCYAN}Ilość krawędzi: {bcolors.ENDC}{edges}")
            print(f"{bcolors.OKCYAN}Ilość wierzchołków: {bcolors.ENDC}{nodes}")
            print(
                f"{bcolors.OKCYAN}Średnia długość ścieki: "
                f"{bcolors.ENDC}{path_av}")
            print(f"{bcolors.OKCYAN}Maksymalne kliki grafu: {bcolors.ENDC}")
            for x in max_cliques:
                print(x)
            if self.limited:
                print(f"{bcolors.OKCYAN}Stopnie: {bcolors.ENDC}{degree}")
                print(f"{bcolors.OKCYAN}Bliskość: {bcolors.ENDC}{close}")
                print(f"{bcolors.OKCYAN}Pośrednictwo: {bcolors.ENDC}{between}")
                for x in connected_c:
                    print(
                        f"{bcolors.OKCYAN}Składowa spójna: {bcolors.ENDC}", x)
                print(
                    f"{bcolors.OKCYAN}Liczba klik większych/równych 3: "
                    f"{bcolors.ENDC}{cliques_bigger_than_3}")
                print(
                    f"{bcolors.OKCYAN}Maksymalne kliki wierzchołków: "
                    f"{bcolors.ENDC}")
                for x in cliques:
                    print(x)
                print(
                    f"{bcolors.OKCYAN}Wierzchołki: {bcolors.ENDC}{G.nodes()}")
                print(f"{bcolors.OKCYAN}Macierz sąsiedctwa: {bcolors.ENDC}")
                print(adjacency_matrix.todense())
                print(f"{bcolors.OKCYAN}Macierz incydencji: {bcolors.ENDC}")
                print(incidence_matrix.todense())
        return degree

    def maximum_cliques(self, cliques):
        lenght = 0
        max_cliques = []

        for clique in cliques:
            if len(clique) > lenght:
                lenght = len(clique)

        for clique in cliques:
            if len(clique) == lenght:
                max_cliques.append(clique)

        return max_cliques

    def color_max_cliques(self, max_cliques):
        set_nodes = set()
        for clique in max_cliques:
            for node in clique:
                set_nodes.add(node)

        return list(set_nodes)

    def node_degree_hist(self, degree):
        degree.sort(key=lambda x: x[1], reverse=True)
        print(degree)
        x = []
        y = []
        for pair in degree:
            x.append(str(pair[0]))
            y.append(pair[1])

        print(x, y)
        fig, ax = plt.subplots(figsize=(15, 8))

        ax.scatter(x, y)
        plt.savefig("fig.png")
