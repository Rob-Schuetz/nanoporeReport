import sys
import os
import yaml


def main(section, element):
    cwd = os.getcwd()
    if cwd.find('workflow') != -1:
        project_path = cwd[:cwd.find('workflow') + len('workflow')]
        config_path = os.path.join(project_path, 'config', 'config.yaml')
    else:
        project_path = cwd[:cwd.find('nanoporeReport') + len('nanoporeReport')]
        config_path = os.path.join(project_path, 'workflow', 'config', 'config.yaml')

    with open(config_path, 'r') as conf:
        cfg = yaml.safe_load(conf)

    return cfg[section][element]


if __name__ == "__main__":

    if len(sys.argv[1:]) != 2:
        print("Usage get_config.py section element")
        sys.exit(1)

    else:
        section = sys.argv[1]
        element = sys.argv[2]

    main(section, element)
