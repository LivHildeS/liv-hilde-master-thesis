import yaml
from pathlib import Path


def read_yaml(file_path):
    """
    Read and returns the constants, saved as yaml.

    Args:
        file_path (Path or str): Yaml file to load.

    Raises:
        FileNotFoundError: If the file is not found.

    Returns:
        dict: Dictionary of the constants read from yaml.
    """
    constants_path = Path(file_path)
    if not constants_path.exists():
        raise FileNotFoundError(f"File {constants_path} not found. ")

    with open(constants_path, "r") as infile:
        constants = yaml.safe_load(infile)
    return constants


def get_constants():
    """
    Reads and returns the constants.yaml file.

    Returns:
        dict: Dictionary of the constants from `constants.yaml`.
    """
    return read_yaml("constants.yaml")
