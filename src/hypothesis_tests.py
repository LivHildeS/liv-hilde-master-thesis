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


def run_group_test(group_df1, group_df2, value_column, test_type, group_names=None, n_permutations=10000,
                   random_state=2025):
    """
    Runs an independent samples test (t-test, Mann-Whitney U, or permutation test) on two groups.
    Also tests for normality with Shapiro-Wilk.

    Args:
        group_df1 (pd.DataFrame): Dataframe with rows for the first group.
        group_df2 (pd.DataFrame): Dataframe with rows for the second group.
        value_column (str): Name of numeric column to compare between groups.
        test_type (str): In ["t-test", "mannwhitney", "u-test", "permutation"].
        group_names (list of str or None): Optional list of names for the two groups.
        n_permutations (int): Number of permutations for the permutation test.
        random_state (int or None): Random seed for reproducibility.

    Returns:
        Dictionary with group labels, sizes, means, normality checks, test statistic, and p-value.
    """
    if test_type not in ["t-test", "mannwhitney", "u-test", "permutation"]:
        raise ValueError(
            f"Unsupported test type. Use 't-test', 'mannwhitney', 'u-test', or 'permutation'. Got {test_type}")

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
    elif test_type == "permutation":
        rng = np.random.default_rng(seed=random_state)
        observed_diff = abs(values1.mean() - values2.mean())
        combined = np.concatenate([values1, values2])
        n1 = len(values1)
        count = 0
        for _ in range(n_permutations):
            rng.shuffle(combined)
            new_diff = abs(combined[:n1].mean() - combined[n1:].mean())
            if new_diff >= observed_diff:
                count += 1
        stat = observed_diff
        p_value = count / n_permutations

    result["stat"] = stat
    result["p_value"] = p_value

    return result


def run_bootstrap_test(group_df1, group_df2, value_column, group_names=None, n_bootstraps=100, random_state=2025):
    """
    Runs a bootstrap hypothesis test between two groups based on the mean difference.
    Also calculates group means, standard deviations, and Cohen's d.

    Args:
        group_df1 (pd.DataFrame): DataFrame for the first group.
        group_df2 (pd.DataFrame): DataFrame for the second group.
        value_column (str): Column name to compare.
        group_names (list of str or None): Optional list of names for the two groups.
        n_bootstraps (int): Number of bootstrap resamples.
        random_state (int): Random seed for reproducibility.

    Returns:
        dict: Results including group statistics, observed mean difference, bootstrap CI, and Cohen's d.
    """
    if group_names is None:
        group_names = ["group1", "group2"]

    rng = np.random.default_rng(seed=random_state)

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
    for _ in range(n_bootstraps):
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


def run_cochrans_q_test(df, device):
    """
    Runs Cochran's Q test for binary repeated measures data across multiple conditions.

    Args:
        df (pd.Dataframe): DataFrame with participants as rows, binary responses as columns.
        device (str): "phone" or "computer" — selects which device's data to test.

    Returns:
        Dictionary with test statistic and p-value.
    """
    # Extract the relevant columns
    websites = ["finn", "dnb", "facebook", "google", "dagens"]
    columns = [f"{device}.{site}.answer.int" for site in websites]
    data = df[columns]

    # Cochran's Q expects a 2D array of shape (n_subjects, k_conditions) with binary values
    result = cochrans_q(data)

    return {
        "test_type": "cochrans_q",
        "device": device,
        "websites": websites,
        "statistic": result.statistic,
        "df": result.df,
        "p_value": result.pvalue
    }


def run_pairwise_mcnemar_tests(df, device, exact=True):
    """
    Runs McNemar's test for all pairs of websites on a single device.

    Args:
        df (pd.DataFrame): DataFrame with participants as rows and binary responses as columns.
        device (str): 'phone' or 'computer'.
        exact (bool): Whether or not to run exact (binomial) McNeymar test or not (Chi-Square approximation).

    Returns:
        List of result dictionaries with test results per website pair.
    """
    websites = ["finn", "dnb", "facebook", "google", "dagens"]
    results = []

    for site1, site2 in combinations(websites, 2):
        col1 = f"{device}.{site1}.answer.int"
        col2 = f"{device}.{site2}.answer.int"

        # 2x2 contingency table
        table = pd.crosstab(df[col1], df[col2])

        # Normalize to ensure all 2x2 cells exist
        table = table.reindex(index=[0, 1], columns=[0, 1], fill_value=0)

        test_result = mcnemar(table, exact=exact)

        results.append({
            "test_type": "mcnemar",
            "device": device,
            "pair": (site1, site2),
            "table": table,
            "statistic": test_result.statistic,
            "p_value": test_result.pvalue
        })

    return results


def run_friedman_test(df):
    """
    Runs the Friedman test on repeated ordinal data across multiple websites.

    Args:
        df (pd.DataFrame): The data from the study.

    Returns:
        Dictionary with test type, websites, test statistic, degrees of freedom, and p-value.
    """
    columns = [f"{site}_accepts_int" for site in WEBSITES]
    data = df[columns]

    # Friedman expects each column to be a condition, and each row to be a subject
    stat, p_value = friedmanchisquare(*[data[col] for col in columns])

    return {
        "test_type": "friedman",
        "websites": WEBSITES,
        "statistic": stat,
        "df": len(WEBSITES) - 1,
        "p_value": p_value
    }


def run_pairwise_wilcoxon_tests(df):
    """
    Runs Wilcoxon signed-rank tests for all pairs of websites with ordinal response values (0-2).

    Args:
        df (pd.DataFrame): DataFrame of ordinal data per website per participant.

    Returns:
        List of dictionaries with test results for each pair of websites.
    """
    results = []

    for site1, site2 in combinations(WEBSITES, 2):
        col1 = f"{site1}_accepts_int"
        col2 = f"{site2}_accepts_int"

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
