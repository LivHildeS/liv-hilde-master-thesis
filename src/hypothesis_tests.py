from itertools import combinations

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, mannwhitneyu, shapiro, ttest_ind, wilcoxon
from statsmodels.stats.contingency_tables import cochrans_q, mcnemar

from src.get_constants import get_constants

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


def get_means_and_sd(group_df1, group_df2, value_column, group_names):
    """
    On the same format as the other tests, but do not perform a test. Only finds the means and sd's of the subgroups.

    Args:
        group_df1 (pd.DataFrame): Dataframe with rows for the first group.
        group_df2 (pd.DataFrame): Dataframe with rows for the second group.
        value_column (str): Name of numeric column to compare between groups.
        group_names (list of str or None): Optional list of names for the two groups.

    Returns:
        Dictionary with group labels and normality check.
    """
    if group_names is None:
        group_names = ["group1", "group2"]

    values1 = group_df1[value_column]
    values2 = group_df2[value_column]

    result = {
        "test_variable": value_column,
        "group_names": group_names,
        "group_sizes": [len(values1), len(values2)],
        "group_means": [values1.mean(), values2.mean()],
        "group_sds": [values1.std(), values2.std()],
    }

    return result


def run_shapriro_wilk_normality_test(values):
    """
    Performs a Shapiro-Wilk test on values, which tests if data is close to normally distributed.
    If W is high, data is close to normal, and if p is low, one can reject normality with high certainty.

    Args:
        values (pd.Series or list type): The data to test for normality

    Returns:
        dict: Dict with the W and p values.
    """
    if len(values) >= 3:
        W1, p1 = shapiro(values)
        return {"W": W1, "p": p1}
    return {"W": -1, "p": - 1}


def run_grouped_shapiro_wilk_normality_test(group_df1, group_df2, value_column, group_names):
    """
    Runs Shapiro-Wilk test on two groups and returns a dictionary of results.

    Args:
        group_df1 (pd.DataFrame): Dataframe with rows for the first group.
        group_df2 (pd.DataFrame): Dataframe with rows for the second group.
        value_column (str): Name of numeric column to compare between groups.
        group_names (list of str or None): Optional list of names for the two groups.

    Returns:
        Dictionary with group labels and normality check.
    """
    if group_names is None:
        group_names = ["group1", "group2"]

    values1 = group_df1[value_column]
    values2 = group_df2[value_column]

    result = {
        "test_variable": value_column,
        "group_names": group_names,
        "group_sizes": [len(values1), len(values2)],
        "normality": {},
    }

    result["normality"][str(group_names[0])] = run_shapriro_wilk_normality_test(values1)
    result["normality"][str(group_names[1])] = run_shapriro_wilk_normality_test(values2)

    return result


def run_group_test(group_df1, group_df2, value_column, test_type, group_names=None):
    """
    Runs an independent samples test (t-test or Mann-Whitney U) on two groups.
    Also tests for normality with Shapiro-Wilk.

    Args:
        group_df1 (pd.DataFrame): Dataframe with rows for the first group.
        group_df2 (pd.DataFrame): Dataframe with rows for the second group.
        value_column (str): Name of numeric column to compare between groups.
        test_type (str): In ["t-test", "mannwhitney", "u-test", "permutation"].
        group_names (list of str or None): Optional list of names for the two groups.
        random_state (int or None): Random seed for reproducibility.

    Returns:
        Dictionary with group labels, sizes, means, normality checks, test statistic, and p-value.
    """
    if test_type not in ["t-test", "mannwhitney", "u-test"]:
        raise ValueError(
            f"Unsupported test type. Use \"t-test\" or \"mannwhitney\". Got {test_type}")

    if group_names is None:
        group_names = ["group1", "group2"]

    values1 = group_df1[value_column]
    values2 = group_df2[value_column]

    result = {
        "test_variable": value_column,
        "test_type": test_type,
        "group_names": group_names,
        "group_sizes": [len(values1), len(values2)],
        "group_means": [values1.mean(), values2.mean()],
        "group_sds": [values1.std(), values2.std()],
        "normality": {},
        "stat": None,
        "p_value": None
    }

    result["normality"][str(group_names[0])] = run_shapriro_wilk_normality_test(values1)
    result["normality"][str(group_names[1])] = run_shapriro_wilk_normality_test(values2)

    if test_type == "t-test":
        stat, p_value = ttest_ind(values1, values2, equal_var=False)
    elif test_type in ["mannwhitney", "u-test"]:
        stat, p_value = mannwhitneyu(values1, values2, alternative="two-sided", method="exact")

    result["stat"] = stat
    result["p_value"] = p_value

    return result


def run_bootstrap_test(group_df1, group_df2, value_column, group_names=None):
    """
    Runs a bootstrap hypothesis test between two groups based on the mean difference.
    Also calculates group means, standard deviations, and Cohen's d.

    Args:
        group_df1 (pd.DataFrame): DataFrame for the first group.
        group_df2 (pd.DataFrame): DataFrame for the second group.
        value_column (str): Column name to compare.
        group_names (list of str or None): Optional list of names for the two groups.

    Returns:
        dict: Results including group statistics, observed mean difference, bootstrap CI, and Cohen's d.
    """
    if group_names is None:
        group_names = ["group1", "group2"]

    rng = np.random.default_rng(seed=CONSTANTS["random_state"])

    values1 = group_df1[value_column].dropna()
    values2 = group_df2[value_column].dropna()

    mean1 = values1.mean()
    mean2 = values2.mean()
    sd1 = values1.std()
    sd2 = values2.std()
    observed_diff = mean1 - mean2

    pooled_sd = np.sqrt(
        ((len(values1) - 1) * sd1**2 + (len(values2) - 1) * sd2**2) / (len(values1) + len(values2) - 2)
    )
    cohens_d = observed_diff / pooled_sd

    # Bootstrap
    bootstrap_diffs = []
    for _ in range(CONSTANTS["n_bootstraps"]):
        sample1 = rng.choice(values1, size=len(values1), replace=True)
        sample2 = rng.choice(values2, size=len(values2), replace=True)
        diff = sample1.mean() - sample2.mean()
        bootstrap_diffs.append(diff)

    bootstrap_diffs = np.array(bootstrap_diffs)
    ci_lower = np.percentile(bootstrap_diffs, 2.5)
    ci_upper = np.percentile(bootstrap_diffs, 97.5)

    result = {
        "test_variable": value_column,
        "test_type": "bootstrap",
        "group_names": group_names,
        "group_sizes": [len(values1), len(values2)],
        "group_means": [mean1, mean2],
        "group_sds": [sd1, sd2],
        "observed_mean_difference": observed_diff,
        "bootstrap_ci": [ci_lower, ci_upper],
        "cohens_d": cohens_d,
    }

    return result


def run_friedman_test(df, test_variable, device):
    """
    Runs the Friedman test on repeated ordinal data across multiple websites.

    Args:
        df (pd.DataFrame): The data from the study.
        test_variable (str): The variable to test, either "accepts" or "time".
        device (str): The device to test, either "computer", "phone" or "both".

    Returns:
        Dictionary with test type, websites, test statistic, degrees of freedom, and p-value.
    """
    test_variable_values = ["accepts", "time"]
    if test_variable not in test_variable_values:
        raise ValueError(f"Argument `test_variable` must be in {test_variable_values}. Was {test_variable}. ")

    device_values = ["computer", "phone", "both"]
    if device not in device_values:
        raise ValueError(f"Argument `device` must be in {device_values}. Was {device}.")

    if device == "both":
        if test_variable == "accepts":
            column_ending = "_accepts_int"
        if test_variable == "time":
            column_ending = "_average_time"
        columns = [f"{website}{column_ending}" for website in WEBSITES]
    else:
        if test_variable == "accepts":
            column_ending = ".answer.int"
        if test_variable == "time":
            column_ending = ".time"
        columns = [f"{device}.{website}{column_ending}" for website in WEBSITES]

    data = df[columns]

    # Friedman expects each column to be a condition, and each row to be a subject
    statistic, p_value = friedmanchisquare(*[data[col] for col in columns])

    return {
        "test_type": "friedman",
        "websites": WEBSITES,
        "statistic": statistic,
        "df": len(WEBSITES) - 1,
        "p_value": p_value
    }


def run_device_wilcoxon_tests(df, column_name1, column_name2, min_group_size=3):
    """
    Run a Wilcoxon signed rank test based on the columns `column_name1` and `column_name2` in the dataframe `df`.

    Args:
        df (pd.DataFrame): DataFrame of with the columns
        column_name1 (str): Name of the first column to test.
        column_name2 (str): name of the second column to test
        min_group_size (int, optional): The minimum amount of instances that must be included to run the test.
            Defaults to 3.

    Returns:
        dict: Dictionary of the test statistic and the corresponding p-value.
    """
    # Wilcoxon test can only use values were the participants have answered differently for the two options
    accept_mask = df[[column_name1, column_name2]].notna().all(axis=1)
    if accept_mask.sum() >= min_group_size:
        stat, p_value = wilcoxon(
            df.loc[accept_mask, column_name1],
            df.loc[accept_mask, column_name2]
        )
    else:
        stat = None
        p_value = None
    return {"stat": stat, "p_value": p_value}


def run_pairwise_wilcoxon_tests(df, test_variable, device):
    """
    Runs Wilcoxon signed-rank tests for all pairs of websites with ordinal response values (0-2).

    Args:
        df (pd.DataFrame): DataFrame of ordinal data per website per participant.
        test_variable (str): The variable to test, either "accepts" or "time".
        device (str): The device to test, either "computer", "phone" or "both".

    Returns:
        List of dictionaries with test results for each pair of websites.
    """
    test_variable_values = ["accepts", "time"]
    if test_variable not in test_variable_values:
        raise ValueError(f"Argument `test_variable` must be in {test_variable_values}. Was {test_variable}. ")

    device_values = ["computer", "phone", "both"]
    if device not in device_values:
        raise ValueError(f"Argument `device` must be in {device_values}. Was {device}.")

    if device == "both":
        if test_variable == "accepts":
            column_ending = "_accepts_int"
        if test_variable == "time":
            column_ending = "_average_time"
        website_to_column_mapping = {website: f"{website}{column_ending}" for website in WEBSITES}
    else:
        if test_variable == "accepts":
            column_ending = ".answer.int"
        if test_variable == "time":
            column_ending = ".time"
        website_to_column_mapping = {website: f"{device}.{website}{column_ending}" for website in WEBSITES}

    results = []

    for site1, site2 in combinations(WEBSITES, 2):
        col1 = website_to_column_mapping[site1]
        col2 = website_to_column_mapping[site2]

        # Drop rows with equal values — wilcoxon test requires non-zero differences
        mask = df[col1] != df[col2]
        data1 = df.loc[mask, col1]
        data2 = df.loc[mask, col2]

        if len(data1) >= 3:
            stat, p_value = wilcoxon(data1, data2, zero_method="wilcox", alternative="two-sided", method="auto")
        else:
            stat, p_value = None, None

        results.append({
            "test_type": "wilcoxon",
            "pair": (site1, site2),
            "n": len(data1),
            "statistic": stat,
            "p_value": p_value
        })

    return results


def run_withdrawal_wilcoxon_test(df):
    """
    Runs Wilcoxon signed-rank test on avg consent vs withdrawal times.

    Args:
        df (pd.DataFrame): Dataframe with the results

    Returns:
        dict: {"stat": test statistic, "p_value": p-value}
    """
    valid = df.dropna(subset=["average_consent_given_withdrawal_times", "average_withdrawal_times"])
    stat, p_value = wilcoxon(valid["average_consent_given_withdrawal_times"], valid["average_withdrawal_times"])
    return {"stat": stat, "p_value": p_value}
