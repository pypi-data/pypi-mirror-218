import yaml


def get_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        config_data: dict = yaml.safe_load(file)
    return config_data


def return_appmode_dict(app_mode: str) -> dict:
    set_mode = get_yaml("config.yaml").get(app_mode, {})
    print(f"MODE: {app_mode}")
    return set_mode
