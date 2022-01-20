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
    help='limit nodes',
    action='store_true',
    default=False,
    dest='limited',
)
parser.add_argument(
    '-p',
    '--plot',
    help='Plot graph.',
    action='store_true',
    default=False,
    dest='plot',
)
parser.add_argument(
    '-n',
    '--node_labels',
    help='Show node labels',
    action='store_true',
    default=False,
    dest='node_labels',
)
parser.add_argument(
    '-e',
    '--edge_labels',
    help='Draw edge labels',
    action='store_true',
    default=False,
    dest='edge_labels',
)
parser.add_argument(
    '-s',
    '--calc_stats',
    help='Draw edge labels',
    action='store_true',
    default=False,
    dest='calc_stats',
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
        args.plot,
        args.node_labels,
        args.edge_labels,
        args.calc_stats)

    end_time = time.time()
    print(
        f"{bcolors.FAIL}Run time:"
        f" {bcolors.ENDC} --- {end_time-start_time} --- seconds")
