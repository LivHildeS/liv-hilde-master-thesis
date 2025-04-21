import numpy as np
import pandas as pd
import yaml

from src.get_constants import get_constants
from src.paths import get_experiment_results_path

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


def _quantisize_answers(text):
    """
    Given an answer to a website (accept_all, reject_all, alternatives_reject_all, etc), returns 1
    if "accept" is included and 0 if "reject" is included in the answer. If neither are, return 0.

    Args:
        text (str): The text answer.

    Returns:
        int: 1 if accept is included, 0 if reject is included, else np.nan.
    """
    if pd.isna(text):
        return np.nan
    text = text.lower()
    if "accept" in text:
        return 1
    if "reject" in text:
        return 0
    return np.nan


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
    Processes the data that is collected from the observational study and writes to csv.

    This consists of reading all the yaml files with the participant data, and saving them as rows
    to a pandas dataframe.

    Then, the number of accepts per participant and website is quantified as an int (instead of string).

    Returns:
        pd.DataFrame: The dataframe with the participants data from the observational study.
    """
    # First, read the data from the yaml files into a pandas dataframe.
    n_participants = CONSTANTS["number_of_participants"]
    all_data = []

    for participant_number in range(1, n_participants + 1):
        data = _get_experiment_results(participant_number=participant_number)
        all_data.append(pd.json_normalize(data))
    df = pd.concat(all_data, ignore_index=True)

    # Now process the data further. Quantify the number of accepts per websites.
    df["computer_accepts"] = 0
    df["phone_accepts"] = 0

    for website in WEBSITES:
        df[f"{website}_accepts_int"] = 0

    for device in DEVICES:
        for website in WEBSITES:
            column_name = f"{device}.{website}.answer"
            df[f"{column_name}.int"] = df[column_name].apply(_quantisize_answers)
            df[f"{device}_accepts"] += df[f"{column_name}.int"]
            df[f"{website}_accepts_int"] += df[f"{column_name}.int"]

    df["total_accepts"] = df["computer_accepts"] + df["phone_accepts"]

    return df


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
