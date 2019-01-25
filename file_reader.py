from ruamel.yaml import YAML
from pathlib import Path


def read_actions(filename='setupsetup.yml'):
    yaml = YAML(typ='safe')
    data = yaml.load(Path(filename))
    return data


if __name__ == "__main__":
    print(read_actions())
