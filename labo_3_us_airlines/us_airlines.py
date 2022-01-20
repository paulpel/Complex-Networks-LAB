from .tools.tools import UsAirlines
import os


def main_airlines(limited, show_graph, show_labels, edge_labels, calc_stats):
    script_path = os.path.dirname(os.path.abspath(__file__))

    obj = UsAirlines(
        script_path, limited,
        show_graph, show_labels,
        edge_labels, calc_stats)

    obj.main()
