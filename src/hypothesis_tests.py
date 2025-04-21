from itertools import combinations

import pandas as pd
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
from statsmodels.stats.contingency_tables import cochrans_q, mcnemar


def run_group_test(group_df1, group_df2, value_column, test_type, group_names=None):
    """
    Runs an independent samples test (t-test or Mann-Whitney U) on two groups.

    Args:
        group_df1 (pd.DataFrame): Dataframe with rows for the first group.
        group_df2 (pd.DataFrame): Dataframe with rows for the second group.
        value_column (str): Name of numeric column to compare between groups.
        test_type (str): In ["t-test", "mannwhitney", "u-test"].
        group_names (list of str or None): Optional list of names for the two groups.

    Returns:
        Dictionary with group labels, sizes, means, normality checks, test statistic, and p-value.
    """
    if test_type not in ["t-test", "mannwhitney", "u-test"]:
        raise ValueError(f"Unsupported test type. Use 't-test', 'mannwhitney' or 'u-test'. Got {test_type}")

    if group_names is None:
        group_names = ["group1", "group2"]

    values1 = group_df1[value_column]
    values2 = group_df2[value_column]

    result = {
        "test_type": test_type,
        "group_names": group_names,
        "group_sizes": [len(values1), len(values2)],
        "group_means": [values1.mean(), values2.mean()],
        "normality": {},
        "stat": None,
        "p_value": None
    }

    if len(values1) >= 3:
        W1, p1 = shapiro(values1)
        result["normality"][str(group_names[0])] = {"W": W1, "p": p1}
    if len(values2) >= 3:
        W2, p2 = shapiro(values2)
        result["normality"][str(group_names[1])] = {"W": W2, "p": p2}

    if test_type == "t-test":
        stat, p_value = ttest_ind(values1, values2, equal_var=False)
    else:
        stat, p_value = mannwhitneyu(values1, values2, alternative="two-sided", method="exact")

    result["stat"] = stat
    result["p_value"] = p_value

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

        test_result = mcnemar(table, exact=True)

        results.append({
            "test_type": "mcnemar",
            "device": device,
            "pair": (site1, site2),
            "table": table,
            "statistic": test_result.statistic,
            "p_value": test_result.pvalue
        })

    return results
