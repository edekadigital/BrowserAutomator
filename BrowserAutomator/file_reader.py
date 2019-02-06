from ruamel.yaml import YAML
from pathlib import Path


def read_actions(filename):
    """given the filename of a yml file, reads and parses the yml"""
    path = filename
    yaml = YAML(typ='safe')
    data = yaml.load(Path(path))
    return data
