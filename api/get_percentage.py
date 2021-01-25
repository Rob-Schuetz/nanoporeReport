import sys
import re
import os
import yaml

# Import config files
config_file_paths = [os.path.join(os.path.realpath('..'),'config', 'config.yml')]
config = {}
for cf in config_file_paths:
    f = open(cf,'r')
    conf = yaml.load(f, Loader=yaml.FullLoader)
    config.update(conf)
    f.close()


def main(filename):
    path = os.path.join(config["flaskAPI"]["log_dir"], filename)
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