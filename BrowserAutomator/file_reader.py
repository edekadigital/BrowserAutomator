from ruamel.yaml import YAML
from pathlib import Path
import os


def read_actions(filename):
    """given the filename of a yml file, reads and parses the yml"""
    # path = get_absolute_path(filename)
    path = filename
    yaml = YAML(typ='safe')
    data = yaml.load(Path(path))
    return data


# def get_absolute_path(filename):
#    """given the filename of a file in the project's config directory, returns the absolute path of that file"""
#    full_path = os.path.realpath(__file__)
#    directory = os.path.split(full_path)[0].split("/")
#    directory = "/".join(directory[:-1])
#    absolute_path = directory + "/config/" + filename
#    return absolute_path


if __name__ == "__main__":
    # print(get_absolute_path("test"))
    pass
