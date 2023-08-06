import yaml
import requests
from diz.utils import validators


def load_yaml(path):
    if validators.is_valid_url(path):
        return load_yaml_with_url(path)
    with open(path, 'r') as (f):
        return yaml.safe_load(f)


def load_yaml_with_url(url):
    return yaml.safe_load(requests.get(url).text)