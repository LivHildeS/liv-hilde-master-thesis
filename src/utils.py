import os

import pandas as pd
import yaml

from src.get_constants import get_constants
from src.paths import ALL_EXPERIMENTS_PATH, NETTSKJEMA_PATH, NETTSKJEMA_QUESTIONS_PATH, get_experiment_results_path

CONSTANTS = get_constants()


def read_nettskjema_data():
    """
    Reads the nettskjema data and returns as a pandas dataframe.

    Returns:
        pd.DataFrame: The dataframe with the data.
    """
    df = pd.read_excel(NETTSKJEMA_PATH)
    column_names = CONSTANTS["nettskjema_column_names"]
    df.columns = column_names.values()
    return df


def write_nettskjema_questions_to_file():
    """
    Writes the original questions to file, which are the original columns names in the nettskjema file.
    """
    df = pd.read_excel(NETTSKJEMA_PATH)
    with open(NETTSKJEMA_QUESTIONS_PATH, "w") as outfile:
        for i, question in enumerate(df.columns):
            outfile.write(f"{i}: {question} \n")


def _get_experiment_results(participant_number):
    """
    Given a participant, retun a dictionary with the corresponding experiment results.

    Args:
        participant_number (int): The participant number.

    Raises:
        FileNotFoundError: If there are no data for the participant number.

    Returns:
        dict: Dictionary with the experiment results.
    """
    file_path = get_experiment_results_path(participant_number=participant_number)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found. ")

    with open(file_path, "r") as infile:
        results = yaml.safe_load(infile)
    return results


def process_participant_data():
    """
    Processes the data that is qualitivly assigned and then quantized into yaml files.
    Writes result to csv.
    """
    n_participants = CONSTANTS["number_of_participants"]
    all_data = []

    for participant_number in range(1, n_participants + 1):
        data = _get_experiment_results(participant_number=participant_number)
        all_data.append(pd.json_normalize(data))
    df = pd.concat(all_data, ignore_index=True)

    df.to_csv(ALL_EXPERIMENTS_PATH)


def read_participant_data(process_data=False):
    """
    Reads the experiment results and returns it as pandas DataFrame. If the data is not yet processed, or if
    `process_data` is `True`, will call process_participant_data to write data to csv first.

    Args:
        process_data (bool, optional): If True, will always call `process_participant_data()`.

    Returns:
        pd: Dataframe with the experiment results.
    """
    if process_data or not os.path.isfile(ALL_EXPERIMENTS_PATH):
        process_participant_data()
    return pd.read_csv(ALL_EXPERIMENTS_PATH)


def get_all_data(process_data=False):
    """
    Reads and merges the nettskjema data and the participant data.

    Args:
        process_data (bool, optional): If True, will always call `process_participant_data()`, which processes the
            participant data.

    Returns:
        pd: Dataframe with the nettskjema data and the experiment data.
    """
    nettskjema_df = read_nettskjema_data()
    participant_df = read_participant_data(process_data=process_data)
    df = pd.merge(nettskjema_df, participant_df, left_on="submission_id", right_on="nettskjema_id")
    return df
