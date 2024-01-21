import yaml


def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.load(f, yaml.Loader)
