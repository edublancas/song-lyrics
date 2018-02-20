import os
import yaml
from pkg_resources import resource_filename


def load_yaml_asset(path):
    """
    Load a yaml located in the assets folder
    by specifying a relative path to the assets/ folder
    """
    relative_path = os.path.join('assets', path)
    absolute_path = resource_filename('song_lyrics', relative_path)

    with open(absolute_path) as f:
        asset = yaml.load(f)

    return asset


def load_logging_config_file():
    content = load_yaml_asset('logging.yaml')
    return content
