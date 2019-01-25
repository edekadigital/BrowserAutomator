from ruamel.yaml import YAML
from pathlib import Path
import os


def read_actions(filename='setup.yml'):
    path = get_absolute_path(filename)
    yaml = YAML(typ='safe')
    data = yaml.load(Path(path))
    return data


def get_absolute_path(filename):
    full_path = os.path.realpath(__file__)
    directory = os.path.split(full_path)[0]
    absolute_path = directory + "/" + filename
    return absolute_path


if __name__ == "__main__":
    print(get_absolute_path("test"))
