from .tools.tools import UsAirlines
import os


def main_airlines(limited):
    script_path = os.path.dirname(os.path.abspath(__file__))
    obj = UsAirlines(script_path, limited)
    obj.main()
