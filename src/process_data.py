import numpy as np
import pandas as pd
import yaml

from src.get_constants import get_constants
from src.paths import QUALITATIVE_ANSWERS_FILENAME, get_experiment_results_path

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

    # Now process the data further. Quantify the number of accepts per websites and the time spent answering banners.
    df["computer_accepts"] = 0
    df["phone_accepts"] = 0
    df["computer_average_time"] = 0
    df["phone_average_time"] = 0

    for website in WEBSITES:
        df[f"{website}_accepts_int"] = 0
        df[f"{website}_average_time"] = 0

    for device in DEVICES:
        for website in WEBSITES:
            df[f"{device}.{website}.answer.int"] = df[f"{device}.{website}.answer"].apply(_quantisize_answers)
            df[f"{device}_accepts"] += df[f"{device}.{website}.answer.int"]
            df[f"{website}_accepts_int"] += df[f"{device}.{website}.answer.int"]
            df[f"{device}_average_time"] += df[f"{device}.{website}.time"]
            df[f"{website}_average_time"] += df[f"{device}.{website}.time"]

    df["total_accepts"] = df["computer_accepts"] + df["phone_accepts"]

    df["computer_average_time"] = df["computer_average_time"] / len(WEBSITES)
    df["phone_average_time"] = df["phone_average_time"] / len(WEBSITES)
    df["total_average_time"] = (df["computer_average_time"] + df["phone_average_time"]) / 2

    # Make average withdrawal and consent column per participant
    withdrawal_column_names = []

    for device in DEVICES:
        for website in WEBSITES:
            # Check which withdrawal columns that exists, and save them for later with corresponding answer time.
            withdrawal_column_name = f"Withdraw.{device}.{website}.time"
            if withdrawal_column_name in df:
                withdrawal_column_names.append({
                    "withdraw": withdrawal_column_name,
                    "answer": f"{device}.{website}.time"
                })

    average_withdrawal_times = []
    average_consent_given_withdrawal_times = []

    for _, row in df.iterrows():
        withdrawal_times = []
        consent_times = []

        for column_name_dict in withdrawal_column_names:
            withdrawal_column_name = column_name_dict["withdraw"]
            consent_column_name = column_name_dict["answer"]

            if not pd.isna(row[withdrawal_column_name]):
                withdrawal_times.append(row[withdrawal_column_name])
                consent_times.append(row[consent_column_name])

        if withdrawal_times != []:
            average_withdrawal_times.append(np.mean(withdrawal_times))
            average_consent_given_withdrawal_times.append(np.mean(consent_times))
        else:
            average_withdrawal_times.append(np.nan)
            average_consent_given_withdrawal_times.append(np.nan)

    df["average_withdrawal_times"] = average_withdrawal_times
    df["average_consent_given_withdrawal_times"] = average_consent_given_withdrawal_times

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
    # Set new column names
    column_names = CONSTANTS["nettskjema_column_names"]
    df.columns = column_names.values()

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

    # Remove trailing whitespaces and wrongly encoded unicode characters (from UiO Nettskjema)
    for column in column_names.values():
        if column == "submission_id":
            continue
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.replace("&#43;", "+", regex=False)
            .str.replace("&#39;", "'", regex=False)
        )

    return df


def write_qualitative_answers_per_participant(df):
    """
    Writes the qualitative answers in the same folder as the experiment results.

    Args:
        df (pd.Dataframe): The dataframe of the data containing the qualitative answers.
    """
    qualitative_questions = [
        "Q5: How do you feel about cookie consent banners?",
        "Q10: During the task-solving earlier, you were presented with cookie consent banners from the various "
        "web-sites. Can you explain why you chose the responses you did to these banners?",
        "Q13: Do you have any other comments?"
    ]
    qualitative_questions_column_names = [
        "cookie_banner_feeling", "banner_response_reasoning", "freetext_additional_comments"
    ]

    for i, row in df.iterrows():
        experiments_path = get_experiment_results_path(i + 1)
        file_path = experiments_path.parent / QUALITATIVE_ANSWERS_FILENAME
        with open(file_path, "w") as outfile:
            for j in range(len(qualitative_questions)):
                outfile.write(qualitative_questions[j] + "\n\n")
                answer = row[qualitative_questions_column_names[j]]
                outfile.write(answer + "\n\n\n")
