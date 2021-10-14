from tools.tools import UsAirlines
import os

if __name__ == "__main__":
    script_path = os.path.dirname(os.path.abspath(__file__))
    obj = UsAirlines(script_path)
    obj.main()