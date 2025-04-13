import os

import pandas as pd
import yaml

from src.get_constants import get_constants
from src.paths import ALL_EXPERIMENTS_PATH, NETTSKJEMA_PATH, NETTSKJEMA_QUESTIONS_PATH, get_experiment_results_path

CONSTANTS = get_constants()


def process_nettskjema_data(df):
    """
    Processes the nettskjema data.
    Calculates a score based on the cookie answers.
    Makes a quantitative version of the Likert answers.
    Make int version of the ages.

    Args:
        df (pd.DataFrame): Pandas dataframe with the nettskjema data.

    Returns:
        pd.DataFrame: The dataframe processed.
    """
    # Calculate amount of correctly answered cookie questions
    correct_cookie_answers = CONSTANTS["correct_cookie_answers"]
    wrong_cookie_answers = CONSTANTS["wrong_cookie_answers"]

    df["cookie_questions_correct"] = 0
    df["cookie_questions_wrong"] = 0

    for correct_cookie_answer in correct_cookie_answers:
        not_checked = df[correct_cookie_answer].isna()
        for i in range(len(df)):
            if not not_checked[i]:
                df.loc[i, "cookie_questions_correct"] += 1
    for wrong_cookie_answer in wrong_cookie_answers:
        not_checked = df[wrong_cookie_answer].isna()
        for i in range(len(df)):
            if not not_checked[i]:
                df.loc[i, "cookie_questions_wrong"] += 1

    df["cookie_questions_score"] = df["cookie_questions_correct"] - df["cookie_questions_wrong"]

    # Make an int version of the Likert answer
    cookie_consent_likert_mapping = CONSTANTS["cookie_consent_likert_mapping"]
    df["understand_cookie_consent"] = df["understand_cookie_consent"].str.strip()  # Remove trailing whitespace
    df["understand_cookie_consent_int"] = df["understand_cookie_consent"].map(cookie_consent_likert_mapping)

    # Make age into int in order to compare ages easier. 35 will represent 30-39 group and similar.
    age_mapping = CONSTANTS["age_mapping"]
    df["age"] = df["age"].str.strip()  # Remove trailing whitespace
    df["age_int"] = df["age"].map(age_mapping)

    return df


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
