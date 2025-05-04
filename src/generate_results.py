import numpy as np
import pandas as pd

from src.get_constants import get_constants
from src.hypothesis_tests import (get_means_and_sd, run_bootstrap_test, run_device_wilcoxon_tests, run_friedman_test,
                                  run_group_test, run_grouped_shapiro_wilk_normality_test, run_pairwise_wilcoxon_tests)
from src.process_data import _quantisize_answers

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


def get_website_averages(df):
    """
    Calculates the average number of accepts per website and per device.

    Args:
        df (pd.DataFrame): The dataframe with the data `src.utils.get_all_data()`.
    """
    results = {}
    times = {}
    for device in DEVICES:
        results[device] = {}
        times[device] = {}
        for website in WEBSITES:
            answer_column_name = f"{device}.{website}.answer"
            time_column_name = f"{device}.{website}.time"
            answers = df[answer_column_name].apply(_quantisize_answers)
            results[device][website] = int(answers.sum())
            times[device][website] = round(float(df[time_column_name].mean()), 3)
    print(f"{results=}")
    print(f"{times=}")
    average_computer_clicks = 100 * sum(list(results["computer"].values())) / (len(WEBSITES) * len(df))
    average_phone_clicks = 100 * sum(list(results["phone"].values())) / (len(WEBSITES) * len(df))
    average_clicks = (average_computer_clicks + average_phone_clicks) / 2
    print(f"{average_computer_clicks=}")
    print(f"{average_phone_clicks=}")
    print(f"{average_clicks=}")
    print(f"{len(df)=}")


def get_all_group_test_results(df, test_type="mannwhitney"):
    """
    Run grouped tests for all the groups and test statistics of interest.

    Args:
        df (pd.Dataframe): All the data.
        test_type (str): In ["mean-sd", "shapiro-wilk", "t-test", "mannwhitney", "bootstrap"].

    Returns:
        dict: Dict of all the results.
    """
    test_type = test_type.lower().strip()
    test_types = ["mean-sd", "shapiro-wilk", "t-test", "mannwhitney", "permutation", "bootstrap"]
    if test_type not in test_types:
        raise ValueError(f"Test type must be in {test_types}. Was {test_type}. ")

    # Group the data based on all the groups we want to use
    privacy_concern = {
        "df1": df[df["privacy_concern"] != "Slightly concerned"],
        "df2": df[df["privacy_concern"] == "Slightly concerned"],
        "group_names": ["Q1. Quite or very concerned about privacy", "Q1. Slightly concerned about privacy"],
        "grouping_name": "Quite or very concerned about privacy",
    }
    understand_cookie_consent = {
        "df1": df[~df["understand_cookie_consent"].isin(["To a great extent", "To some extent"])],
        "df2": df[~df["understand_cookie_consent"].isin(["Not at all", "To a small extent", "Neither nor"])],
        "group_names": [
            "Q4. Understand cookie consent to some or more extent", "Q4. Do not understand cookie consent well"
        ],
        "grouping_name": "Understands cookie consent",
    }
    cookie_banner_response = {
        "df1": df[df["cookie_banner_response"] == "I actively take steps to withhold my consent."],
        "df2": df[df["cookie_banner_response"] != "I akictively take steps to withhold my consent."],
        "group_names": ["Q7. Actively withholds consent", "Q7. Does not actively withhold consent"],
        "grouping_name": "Actively withholds consent",
    }
    have_withdrawn_consent = {
        "df1": df[df["have_withdrawn_consent"] == "Yes"],
        "df2": df[df["have_withdrawn_consent"] == "No"],
        "group_names": ["Q8. Have withdrawn consent", "Q8. Have not withdrawn consent"],
        "grouping_name": "Have withdrawn consent",
    }
    aware_withdrawal_ease = {
        "df1": df[df["aware_withdrawal_ease"] == "Yes"],
        "df2": df[df["aware_withdrawal_ease"] == "No"],
        "group_names": ["Q9. Aware of withdrawal ease", "Q9. Not aware of withdrawal ease"],
        "grouping_name": "Aware of withdrawal ease",
    }
    age = {
        "df1": df[df["age_int"] < 30],
        "df2": df[df["age_int"] > 30],
        "group_names": ["Q11. Under 30 years", "Q11. 30 years or older"],
        "grouping_name": "Age",
    }
    it_background = {
        "df1": df[df["it_background"] != "No"],
        "df2": df[df["it_background"] == "No"],
        "group_names": ["Q12. With IT background", "Q12. Without IT background"],
        "grouping_name": "IT background",
    }

    groups = [
        privacy_concern,
        understand_cookie_consent,
        cookie_banner_response,
        have_withdrawn_consent,
        aware_withdrawal_ease,
        age,
        it_background,
    ]

    test_variables = [
        "cookie_questions_score",
        "computer_accepts",
        "phone_accepts",
        "total_accepts",
        "computer_average_time",
        "phone_average_time",
        "total_average_time",
    ]

    if test_type == "mean-sd":
        full_group = {
            "df": df,
            "group_names": ["\\qquad Full dataset"],
            "grouping_name": "Full Dataset",
        }
        groups.insert(0, full_group)

    all_results = {}
    for test_variable in test_variables:
        test_variable_results = {}

        for group in groups:
            if group["grouping_name"] == "Full Dataset":  # Special case for full dataset
                result = {
                    "test_variable": test_variable,
                    "group_names": group["group_names"],
                    "group_sizes": [len(group["df"])],
                    "group_means": [group["df"][test_variable].mean()],
                    "group_sds": [group["df"][test_variable].std()],
                }
            elif test_type == "mean-sd":
                result = get_means_and_sd(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"]
                )
            elif test_type == "shapiro-wilk":
                result = run_grouped_shapiro_wilk_normality_test(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"]
                )
            elif test_type == "bootstrap":
                result = run_bootstrap_test(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"],
                )
            else:
                result = run_group_test(
                    group["df1"], group["df2"], value_column=test_variable, test_type=test_type,
                    group_names=group["group_names"]
                )
            result["grouping_name"] = group["grouping_name"]
            test_variable_results[group["grouping_name"]] = result

        all_results[test_variable] = test_variable_results

    return all_results


def get_website_statistics(df, perform_wilcoxon_test=False):
    """
    Collects high level website data from the dataframe and returns as a dictionary.
    This data is the total amount of accepts and average time spent on the cookie banner for each of the websites,
    both means and standard deviations.

    Args:
        df (pd.Dataframe): All the data.
        perform_wilcoxon_test (bool): If True, will perform wilcoxon signed ranked test on each website. The outcome
            variable will be the amount of accepts and the time spent on each website, and it will test computer
            against phone.

    Returns:
        dict: Dict of all the results.
    """
    results = {}

    # Calculate stats for all individual websites
    for website in WEBSITES:
        results[website] = {}
        for device in DEVICES:
            results[website][f"{device}_accepts"] = df[f"{device}.{website}.answer.int"].sum()
            results[website][f"{device}_accepts_std"] = df[f"{device}.{website}.answer.int"].std()
            results[website][f"{device}_time"] = df[f"{device}.{website}.time"].mean()
            results[website][f"{device}_time_std"] = df[f"{device}.{website}.time"].std()

        # Add results for both devices
        results[website]["total_accepts"] = df[f"{website}_accepts_int"].sum()
        results[website]["total_accepts_std"] = df[f"{website}_accepts_int"].std()
        results[website]["total_time"] = df[f"{website}_average_time"].mean()
        results[website]["total_time_std"] = df[f"{website}_average_time"].std()

    all_stats = {}  # Aggregates all websites
    all_df = {}  # For Wilcoxon tests

    for device in DEVICES:
        all_accepts = pd.concat([df[f"{device}.{website}.answer.int"] for website in WEBSITES])
        all_times = pd.concat([df[f"{device}.{website}.time"] for website in WEBSITES])
        all_df[f"{device}_accepts"] = all_accepts
        all_df[f"{device}_time"] = all_times

        all_stats[f"{device}_accepts"] = all_accepts.sum()
        all_stats[f"{device}_accepts_std"] = all_accepts.std()
        all_stats[f"{device}_time"] = all_times.mean()
        all_stats[f"{device}_time_std"] = all_times.std()

    all_df = pd.DataFrame(all_df)

    # Calculate both devices for all websites aggregated
    all_accepts = pd.concat([df[f"{website}_accepts_int"] for website in WEBSITES])
    all_times = pd.concat([df[f"{website}_average_time"] for website in WEBSITES])

    all_stats["total_accepts"] = all_accepts.sum()
    all_stats["total_accepts_std"] = all_accepts.std()
    all_stats["total_time"] = all_times.mean()
    all_stats["total_time_std"] = all_times.std()

    results["all"] = all_stats

    if perform_wilcoxon_test:  # Run Wilcoxon signed ranked test on accepts and time given different devices.
        for website in WEBSITES:
            test_results_accepts = run_device_wilcoxon_tests(
                df, column_name1=f"computer.{website}.answer.int", column_name2=f"phone.{website}.answer.int"
            )
            results[website]["test_statistics_accepts"] = test_results_accepts

            test_results_time = run_device_wilcoxon_tests(
                df, column_name1=f"computer.{website}.time", column_name2=f"phone.{website}.time"
            )
            results[website]["test_statistics_time"] = test_results_time

        # Also run tests for the all website aggregation
        test_results_accepts = run_device_wilcoxon_tests(
            all_df, column_name1="computer_accepts", column_name2="phone_accepts"
        )
        results["all"]["test_statistics_accepts"] = test_results_accepts

        test_results_time = run_device_wilcoxon_tests(
            all_df, column_name1="computer_time", column_name2="phone_time"
        )
        results["all"]["test_statistics_time"] = test_results_time

    return results


def get_all_friedman_test_results(df):
    """
    Runs Friedman test with all testing configurations, meaning both the accepts and time as test variables,
    and computer, phone and both as device.

    Args:
        df (pd.Dataframe): All the data.

    Returns:
        dict: Dict of all the results.
    """
    all_results = {"accepts": {}, "time": {}}
    for test_variable in ["accepts", "time"]:
        for device in ["computer", "phone", "both"]:
            results = run_friedman_test(df, test_variable=test_variable, device=device)
            all_results[test_variable][device] = results

    return all_results


def get_all_wilcoxon_test_results(df):
    """
    Runs Wilcoxon test with all testing configurations, meaning both the accepts and time as test variables,
    and computer, phone and both as device.
    Each Wilcoxon test runs all pairs of websites.

    Args:
        df (pd.Dataframe): All the data.

    Returns:
        dict: Dict of all the results.
    """
    all_results = {"accepts": {}, "time": {}}
    for test_variable in ["accepts", "time"]:
        for device in ["computer", "phone", "both"]:
            results = run_pairwise_wilcoxon_tests(df, test_variable=test_variable, device=device)
            all_results[test_variable][device] = results

    return all_results


def get_withdrawal_and_answer_times(df):
    """
    Computes average cookie banner response times, withdrawal times, and group sizes for all devices and websites,
    including both devices and all websites aggregated.

    Args:
        df (pd.DataFrame): DataFrame containing response and withdrawal times.

    Returns:
        dict: Nested dictionary with statistics for each website and device, plus 'all'.
    """
    result = {}
    all_websites = {}

    for device in DEVICES:
        result[device] = {}
        all_websites[device] = {
            "avg_answer_all": 0,
            "avg_answer_no_withdraw": 0,
            "avg_withdraw": 0,
            "n_withdraw": 0,
            "n_answers": 0,
        }

        for website in WEBSITES:
            withdraw_column = f"Withdraw.{device}.{website}.time"

            answer_times = df[df[f"{device}.{website}.answer.int"] == 1][f"{device}.{website}.time"]
            if withdraw_column in df.columns:
                withdraw_times = df[withdraw_column]
            else:
                withdraw_times = pd.Series(dtype=float)  # No withdraws for this device and website

            withdraw_times = withdraw_times.reindex(answer_times.index)

            avg_answer_all = answer_times.mean()
            avg_withdraw = withdraw_times.mean()
            n_withdraw = withdraw_times.notna().sum()
            n_answer_all = len(answer_times)

            result[device][website] = {
                "avg_answer_all": avg_answer_all,
                "avg_withdraw": avg_withdraw,
                "n_withdraw": n_withdraw,
                "n_answers": n_answer_all,
            }

            # Aggregate websites
            all_websites[device]["avg_answer_all"] += avg_answer_all / len(WEBSITES)
            if n_withdraw > 0:
                all_websites[device]["avg_withdraw"] += avg_withdraw / len(WEBSITES)
            all_websites[device]["n_withdraw"] += n_withdraw
            all_websites[device]["n_answers"] += n_answer_all

        result[device]["all"] = all_websites[device]

    # Combine devices "computer" and "phone" to get "both"
    result["both"] = {}
    for website in WEBSITES + ["all"]:
        result_phone = result["phone"][website]
        result_computer = result["computer"][website]
        result["both"][website] = {
            "avg_answer_all": (result_computer["avg_answer_all"] + result_phone["avg_answer_all"]) / 2,
            "avg_withdraw": 0,
            "n_withdraw": result_computer["n_withdraw"] + result_phone["n_withdraw"],
            "n_answers": result_computer["n_answers"] + result_phone["n_answers"],
        }
        # avg_withdraw is nan if there are no withdraws, and x + nan = nan, so remove adding those.
        if result["computer"][website]["n_withdraw"] > 0:
            result["both"][website]["avg_withdraw"] += result["computer"][website]["avg_withdraw"] / 2
        if result["phone"][website]["n_withdraw"] > 0:
            result["both"][website]["avg_withdraw"] += result["phone"][website]["avg_withdraw"] / 2

    return result
