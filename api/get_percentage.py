import sys
import re
import os
sys.path.append(os.path.join(os.getcwd(), '..', 'build_report', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), 'build_report', 'scripts'))
from genomics import get_config

def main(filename):
    path = os.path.join(get_config.main("flaskAPI", "log_dir"), filename)
    with open(path, 'r') as f:
        percentage = 0
        for line in f:
            line = line.rstrip()
            if line.find('steps (') != -1:
                pos1 = line.find('steps (') + len('steps (')
                pos2 = line.find('%', pos1)
                pct = int(line[pos1:pos2])
                if percentage < pct:
                    percentage = pct
    return percentage

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)