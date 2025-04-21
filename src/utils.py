import pandas as pd
import numpy as np

from src.get_constants import get_constants
from src.paths import ALL_EXPERIMENTS_PATH, NETTSKJEMA_PATH, NETTSKJEMA_QUESTIONS_PATH
from src.process_data import process_nettskjema_data, process_participant_data

CONSTANTS = get_constants()


def write_nettskjema_questions_to_file():
    """
    Writes the original questions to file, which are the original columns names in the nettskjema file.
    """
    df = pd.read_excel(NETTSKJEMA_PATH)
    with open(NETTSKJEMA_QUESTIONS_PATH, "w") as outfile:
        for i, question in enumerate(df.columns):
            outfile.write(f"{i}: {question} \n")


def read_nettskjema_data():
    """
    Reads the nettskjema data and returns as a pandas dataframe.

    Returns:
        pd.DataFrame: The dataframe with the data.
    """
    df = pd.read_excel(NETTSKJEMA_PATH)
    column_names = CONSTANTS["nettskjema_column_names"]
    df.columns = column_names.values()
    df = process_nettskjema_data(df)

    return df


def read_participant_data():
    """
    Reads the experiment results and returns it as pandas DataFrame.

    Returns:
        pd: Dataframe with the experiment results.
    """
    return process_participant_data()


def get_all_data():
    """
    Reads and merges the nettskjema data and the participant data.

    Returns:
        pd: Dataframe with the nettskjema data and the experiment data.
    """
    nettskjema_df = read_nettskjema_data()
    participant_df = read_participant_data()
    df = pd.merge(nettskjema_df, participant_df, left_on="submission_id", right_on="nettskjema_id")
    return df
