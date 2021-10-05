import os
import yaml

def get_env_var(name, config_):
    """Get value from environment variable.
       Raises informative message if not set.

    Args:
        name (str): the name of the environment variable

    Returns:
        str: The value of the environment variable

    """
    var = None
    try:
        var = os.environ[name]
    except KeyError:
        print(f"Environment variable '{name}' is not defined. Loading in the local yml file.")
        try:
            var = config_[name]
        except Exception:
            print(f"Environment variable '{name}' is not defined in local yml file.")
    if var is None:
        print(f"Some error happens while loading variable {name}")
    return var

def read_config_file(config_file_path):
    """Read configuration file in YAML

    Args:
        config_file_path (str): the path to the configuration file

    Returns:
        dict: The dictionary with file contents

    """
    with open(config_file_path, 'r') as config_file:
        config = yaml.full_load(config_file)
    return config['variables']
