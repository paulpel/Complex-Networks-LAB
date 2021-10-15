import argparse
import os
import subprocess
from labo_3_us_airlines.us_airlines import main_airlines

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
    main_airlines(args.limited)
