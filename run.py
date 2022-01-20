import argparse
import os
import subprocess
import time
from labo_3_us_airlines.us_airlines import main_airlines
from labo_3_us_airlines.tools.colors_terminal import bcolors

parser = argparse.ArgumentParser("Complex Network Module")

parser.add_argument(
    "project",
    metavar="project_number",
    choices=('1', '2', '3'),
    help="choose which script to run",
)
parser.add_argument(
    '-l',
    '--limited',
    help='set limited node mode',
    action='store_true',
    default=False,
    dest='limited',
)
parser.add_argument(
    '-sg',
    '--show_graph',
    help='Plot graph.',
    action='store_true',
    default=False,
    dest='show_graph',
)
parser.add_argument(
    '-sl',
    '--show_labels',
    help='Show node labels',
    action='store_true',
    default=False,
    dest='show_labels',
)
parser.add_argument(
    '-ps',
    '--print_stats',
    help='Print graph statistics',
    action='store_true',
    default=False,
    dest='print_stats',
)
parser.add_argument(
    '-dl',
    '--draw_edge',
    help='Draw edge labels',
    action='store_true',
    default=False,
    dest='draw_edge',
)

args = parser.parse_args()
paths = {
    "1": os.path.join('labo_1_geralt', 'geralt.py'),
    "2": os.path.join('labo_2_actors', 'actors.py'),
    "3": os.path.join('labo_3_us_airlines', 'us_airlines.py')
}

if args.project in ['1', '2']:
    script_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_path, paths[args.project])
    subprocess.run(['python', script_path])
elif args.project == '3':
    start_time = time.time()

    main_airlines(
        args.limited,
        args.show_graph,
        args.show_labels,
        args.print_stats,
        args.draw_edge)

    end_time = time.time()
    print(
        f"{bcolors.FAIL}Run time:"
        f" {bcolors.ENDC} --- {end_time-start_time} --- seconds")
