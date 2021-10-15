import os
import json
import shutil
import networkx as nx
import matplotlib.pyplot as plt

class UsAirlines:

    def __init__(self, script_path) -> None:
        self.script_path = script_path
        self.nodes_to_take = [311, 150, 248, 118, 293, 258, 69, 161, 263]
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
                        'x_y_z_cords' : x_y_z
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
        output_path = os.path.join(self.script_path, 'output', 'airport_data.json')
        with open(output_path, 'w') as jf:
            json.dump(self.airport_data, jf, indent=2)

    def prepare_for_networkx(self, limited=False):
        labels = {}
        pos = {}
        for airport in self.airport_data['airports']:
            if limited:
                if int(airport) in self.nodes_to_take:
                    labels[int(airport)] = self.airport_data['airports'][airport]['name']
                    pos[int(airport)] = self.airport_data['airports']\
                        [airport]['x_y_z_cords'][:-1]

            else:
                labels[int(airport)] = self.airport_data['airports'][airport]['name']
                pos[int(airport)] = self.airport_data['airports']\
                    [airport]['x_y_z_cords'][:-1]

        return labels, pos

    def color_specific_nodes(self, G):
        color_map = []
        highlight_nodes = [150, 23]
        for node in G:
            if node in highlight_nodes:
                color_map.append('#CEFF00')
            else:
                color_map.append('#FF8243')
        return color_map

    def print_graph(self):
        fig, ax = plt.subplots(figsize=(15,8))
        G = nx.Graph()
        if self.nodes_to_take:
            edges = self.limit_edges()
            labels, pos = self.prepare_for_networkx(True)
        else:
            edges = self.airport_data['connections']
            labels, pos = self.prepare_for_networkx()

        G.add_weighted_edges_from(edges)

        
        color_map = self.color_specific_nodes(G)

        nx.draw(G, pos=pos, labels=labels, with_labels=True, font_size=6,
            edge_color='#C8A2C8', node_size=200, node_color=color_map,
            node_shape='h')

        fig.set_facecolor('#6D9BC3')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.show()

    def limit_edges(self):
        nodes_to_take = self.nodes_to_take
        filtered_connections = []
        for connection in self.airport_data['connections']:
            if connection[0] in nodes_to_take and connection[1] in nodes_to_take:
                filtered_connections.append(connection)
        return filtered_connections