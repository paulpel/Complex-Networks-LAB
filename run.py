import argparse
import os
import subprocess

parser = argparse.ArgumentParser("Complex Network Module")

parser.add_argument(
    "project",
    metavar="project_number",
    choices=('1','2', '3'),
    help="Choose which script to run",
)

args = parser.parse_args()

paths = {
    "1": os.path.join('labo_1_geralt', 'geralt.py'),
    "2": os.path.join('labo_2_actors', 'actors.py'),
    "3": os.path.join('labo_3_us_airlines', 'us_airlines.py')
}
script_path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_path, paths[args.project])
subprocess.run(['python', script_path])
