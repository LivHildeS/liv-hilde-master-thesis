import numpy as np

from src.get_constants import get_constants
from src.hypothesis_tests import (get_means_and_sd, run_bootstrap_test, run_group_test,
                                  run_grouped_shapiro_wilk_normality_test)
from src.process_data import _quantisize_answers

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


def print_group_test_result(result):
    """
    Prints the result dictionary returned by run_group_test in a readable format.

    Args:
        result (dict): Output dictionary from run_group_test.
    """
    group1, group2 = result["group_names"]
    size1, size2 = result["group_sizes"]
    mean1, mean2 = result["group_means"]
    sd1, sd2 = result["group_sds"]
    print("-----------------------------------------")
    print(f"Test variable : {result['test_variable']}")
    print(f"Test type     : {result['test_type']}")
    print(f"Group 1       : {group1} (n={size1}, mean={mean1:.3f}, sd={sd1:.3f})")
    print(f"Group 2       : {group2} (n={size2}, mean={mean2:.3f}, sd={sd2:.3f})")

    if "normality" in result:
        print("\nNormality (Shapiro-Wilk):")
        for group in result["normality"]:
            W = result["normality"][group]["W"]
            p = result["normality"][group]["p"]
            print(f"  {group:<12}: W = {W:.3f}, p = {p:.4f}")

    if "bootstrap_ci" in result:
        significant = np.sign(result['bootstrap_ci'][0]) == np.sign(result['bootstrap_ci'][1])
        print(f"Observed mean difference : {result['observed_mean_difference']:.3f}")
        print(f"Cohen's d                : {result['cohens_d']:.3f}")
        print(f"Bootstrap lower CI       : {result['bootstrap_ci'][0]:.3f}")
        print(f"Bootstrap upper CI       : {result['bootstrap_ci'][1]:.3f}")
        print(f"Significant              : {significant}")

    print("\nTest statistic:")
    print(f"  stat = {result['stat']:.4f}")
    print(f"  p     = {result['p_value']:.4f}")
    print("-----------------------------------------\n")


def print_pairwise_mcnemar_results(results):
    """
    Prints McNemar pairwise test results in a formatted table.

    Args:
        results (list): Output from run_pairwise_mcnemar_tests.
    """
    print("Pairwise McNemar Test Results:")
    print(f"{'Site 1':<12} {'Site 2':<12} {'Stat':>6} {'p-value':>10}")
    print("-" * 42)
    for r in results:
        site1, site2 = r['pair']
        stat = f"{r['statistic']:.2f}" if r['statistic'] is not None else "-"
        pval = f"{r['p_value']:.4f}"
        print(f"{site1:<12} {site2:<12} {stat:>6} {pval:>10}")


def print_pairwise_wilcoxon_results(results):
    """
    Prints Wilcoxon pairwise test results in a formatted table.

    Args:
        results (list): Output from run_pairwise_wilcoxon_tests.
    """
    print("Pairwise Wilcoxon Test Results:")
    print(f"{'Site 1':<12} {'Site 2':<12} {'N':>3} {'Stat':>8} {'p-value':>10}")
    print("-" * 48)
    for r in results:
        site1, site2 = r['pair']
        stat = f"{r['statistic']:.2f}" if r['statistic'] is not None else "-"
        pval = f"{r['p_value']:.4f}" if r['p_value'] is not None else "-"
        print(f"{site1:<12} {site2:<12} {r['n']:>3} {stat:>8} {pval:>10}")


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


def get_all_group_test_results(df, test_type="mannwhitney", print_values=False):
    """
    Run grouped tests for all the groups and test statistics of interest.

    Args:
        df (pd.Dataframe): All the data.
        test_type (str): In ["mean-sd", "shapiro-wilk", "t-test", "mannwhitney", "permutation", "bootstrap"].
        print_values (bool): Whether to print results or not.

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
        "group_names": ["Q1. Quite or very concerned about privacy", "Q1. Slightly concered about privacy"],
        "grouping_name": "privacy concern",
    }
    understand_cookie_consent = {
        "df1": df[~df["understand_cookie_consent"].isin(["To a great extent", "To some extent"])],
        "df2": df[~df["understand_cookie_consent"].isin(["Not at all", "To a small extent", "Neither nor"])],
        "group_names": [
            "Q4. Understand cookie consent to some or more extent", "Q4. Do not understand cookie consent well"
        ],
        "grouping_name": "understands cookie concent",
    }
    cookie_banner_response = {
        "df1": df[df["cookie_banner_response"] == "I actively take steps to withhold my consent."],
        "df2": df[df["cookie_banner_response"] != "I actively take steps to withhold my consent."],
        "group_names": ["Q7. Activly withholds consent", "Q7. Does not activly withhold consent"],
        "grouping_name": "witholds consent",
    }
    have_withdrawn_consent = {
        "df1": df[df["have_withdrawn_consent"] == "Yes"],
        "df2": df[df["have_withdrawn_consent"] == "No"],
        "group_names": ["Q8. Have withdrawn consent", "Q8. Have not withdrawn consent"],
        "grouping_name": "withdrawn consent",
    }
    aware_withdrawal_ease = {
        "df1": df[df["aware_withdrawal_ease"] == "Yes"],
        "df2": df[df["aware_withdrawal_ease"] == "No"],
        "group_names": ["Q9. Aware of withdrawal ease", "Q9. Not aware of withdrawal ease"],
        "grouping_name": "aware withdrawal ease",
    }
    age = {
        "df1": df[df["age_int"] < 30],
        "df2": df[df["age_int"] > 30],
        "group_names": ["Q11. Under 30 years", "Q11. 30 years or older"],
        "grouping_name": "age",
    }
    it_background = {
        "df1": df[df["it_background"] != "No"],
        "df2": df[df["it_background"] == "No"],
        "group_names": ["Q12. With IT background", "Q12. Without IT background"],
        "grouping_name": "it background",
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

    all_results = {}
    for test_variable in test_variables:
        test_variable_results = {}

        for group in groups:
            if test_type == "mean-sd":
                result = get_means_and_sd(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"]
                )
            elif test_type == "shapiro-wilk":
                result = run_grouped_shapiro_wilk_normality_test(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"]
                )
            elif test_type == "bootstrap":
                result = run_bootstrap_test(
                    group["df1"], group["df2"], value_column=test_variable, group_names=group["group_names"]
                )
            else:
                result = run_group_test(
                    group["df1"], group["df2"], value_column=test_variable, test_type=test_type,
                    group_names=group["group_names"]
                )
            test_variable_results[group["grouping_name"]] = result
            if print_values:
                print_group_test_result(result)

        all_results[test_variable] = test_variable_results

    return all_results


def test_time_given_accept(df):
    for device in DEVICES:
        for website in WEBSITES:
            df1 = df[df[f"{device}.{website}.answer.int"] == 0]
            df2 = df[df[f"{device}.{website}.answer.int"] == 1]
            group_names = [f"Accept {device} {website}", f"Reject {device} {website}"]
            test_variable = f"{device}.{website}.time"
            result = run_group_test(
                df1, df2, value_column=test_variable, test_type="permutation", group_names=group_names
            )
            print_group_test_result(result)
