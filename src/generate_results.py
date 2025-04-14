from scipy.stats import friedmanchisquare, mannwhitneyu, shapiro, ttest_ind


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
        stat, p_value = mannwhitneyu(values1, values2, alternative="two-sided")

    result["stat"] = stat
    result["p_value"] = p_value

    return result
