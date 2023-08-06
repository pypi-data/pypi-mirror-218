import yaml


def get_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        config_data: dict = yaml.safe_load(file)
    return config_data
