import os

class UsAirlines:

    def __init__(self, script_path) -> None:
        self.script_path = script_path

    def main(self):
        file_path = os.path.join(self.script_path, 'data', 'USAir97.net')
        with open(file_path, 'r') as txt_file:
            for line in txt_file:
                print(line)