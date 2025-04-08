from pathlib import Path

from src.get_constants import get_constants


PATHS = get_constants()["paths"]

DATA_FOLDER = Path(PATHS["folders"]["data_folder"])
PARTICIPANTS_FOLDER_BASE = PATHS["folders"]["participant_folder_base"]

NETTSKJEMA_FILENAME = PATHS["filenames"]["nettskjema"]
EXPERIMENT_RESULTS_FILENAME = PATHS["filenames"]["experiment_results"]
ALL_EXPERIMENTS_FILENAME = PATHS["filenames"]["all_experiment_results"]
NETTSKJEMA_QUESTIONS_FILENAME = PATHS["filenames"]["nettskjema_questions"]

NETTSKJEMA_PATH = DATA_FOLDER / NETTSKJEMA_FILENAME
ALL_EXPERIMENTS_PATH = DATA_FOLDER / ALL_EXPERIMENTS_FILENAME
NETTSKJEMA_QUESTIONS_PATH = DATA_FOLDER / NETTSKJEMA_QUESTIONS_FILENAME


def get_experiment_results_path(participant_number):
    """
    Given an experiment number, returns the filepath to the corresponding experiment results file.

    Args:
        participant_number (int): The participant number.

    Returns:
        Path: The path to the experiment file.
    """
    folder_path = DATA_FOLDER / (PARTICIPANTS_FOLDER_BASE + str(participant_number))
    file_path = folder_path / EXPERIMENT_RESULTS_FILENAME
    return file_path
