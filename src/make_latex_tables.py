import re

import numpy as np
import pandas as pd


def _get_nettskjema_answer_options():
    """
    Returns the answers options for the nettskjema questions, as values in a dict where the
    keys are the columns for the respective questions.

    Returns:
        dict: The answer options.
    """
    all_nettskjema_answer_options = {
        "privacy_concern": [
            "Very concerned",
            "Quite concerned",
            "Slightly concerned",
            "Don't know",
        ],
        "knows_cookies": [
            "Yes",
            "No",
        ],
        "understand_cookie_consent": [
            "To a great extent",
            "To some extent",
            "Neither nor",
            "To a small extent",
            "Not at all",
            "Don't know",
        ],
        "cookie_sharing_feeling": [
            "I want as little information as possible about me and my online activity to be saved and shared.",
            "I want information about me and my online activity to be saved and shared, "
            "since it improves my user experience.",
            "I am indifferent to my information and online activity being saved and shared.",
            "Don't know",
        ],
        "cookie_banner_response": [
            "I ignore them and leave them open.",
            "I choose the easiest option, whether it's accept or decline.",
            "I try to decline when possible, but accept if rejecting is too much effort.",
            "I actively take steps to withhold my consent.",
            "I consent because it improves my user experience.",
            "Don't know",
        ],
        "have_withdrawn_consent": ["Yes", "No", "Don't know"],
        "aware_withdrawal_ease": ["Yes", "No", "Don't know"],
        "age": [
            "15 - 19 years",
            "20 - 29 years",
            "30 - 39 years",
            "40 - 49 years",
            "50 - 59 years",
            "60+ years",
        ],
        "it_background": [
            "Yes, programming and/or design related",
            "Yes, other",
            "No",
        ],
    }
    return all_nettskjema_answer_options


def _get_nettskjema_question_mapping():
    """
    Maps the column names for the questions to the actual questions with numbers.

    Returns:
        dict: The question mapping.
    """
    question_mapping = {
        "privacy_concern": "Q1. Privacy is about your right, as far as possible, to decide for yourself over "
        "your own personal data. To what extent are you concerned about privacy?",
        "knows_cookies": "Q2. Do you know what cookies are?",
        "understand_cookie_consent": "Q4. Most websites ask for consent to collect information about you through "
        "cookies. To what extent would you say you understand what kind of information "
        "different websites request permission to collect?",
        "cookie_sharing_feeling": "Q6. Which statement best describes how you feel about sharing your information "
        "through cookies?",
        "cookie_banner_response": "Q7. How do you usually respond to cookie consent banners?",
        "have_withdrawn_consent": "Q8. Have you ever withdrawn your consent to cookies, after first having given it?",
        "aware_withdrawal_ease": "Q9. Were you aware that legally, withdrawing consent must be as easy as giving it?",
        "age": "Q11. How old are you?",
        "it_background": "Q12. Do you have an IT-related background?",
    }
    return question_mapping


def _get_test_varible_mapping():
    """
    Returns a mapping from the column names of metrics to a description of them.

    Returns:
        dict: The test variable (column name) to description mapping.
    """
    test_variable_mapping = {
        "cookie_questions_score": "Cookie questions score",
        "computer_accepts": "Total accepts on computer",
        "phone_accepts": "Total accepts on phone",
        "total_accepts": "Total accepts on both devices",
        "computer_average_time": "Average computer banner answer time",
        "phone_average_time": "Average phone banner answer time",
        "total_average_time": "Average banner answer time on both devices",
    }
    return test_variable_mapping


def make_nettskjema_report_latex(df, caption="", label=""):
    """
    Make a LaTeX table for the answers to the quantitative nettskjema questions.

    Args:
        df (pd.DataFrame): The dataframe with the results.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: The LaTeX table as a string.
    """
    all_nettskjema_answer_options = _get_nettskjema_answer_options()
    nettskjema_question_mapping = _get_nettskjema_question_mapping()
    columns = list(all_nettskjema_answer_options.keys())

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\footnotesize")
    lines.append("    \\begin{tabular}{|p{12.5cm}|r|}")
    lines.append("        \\hline")
    lines.append("        \\textbf{Response} & \\textbf{Count} \\\\")
    lines.append("        \\hline")

    for column in columns:
        # Add a bold row with the question name above the responses
        question = nettskjema_question_mapping[column]
        question_formatted = re.sub(r"(Q\d{1,2}\.)", r"\\textbf{\1}", question)
        lines.append(f"        {question_formatted} & ~ \\\\[0.2em]")

        counts = df[column].value_counts().reindex(all_nettskjema_answer_options[column], fill_value=0)
        for response, count in counts.items():
            response = str(response).replace("_", " ")
            lines.append(f"        {response} & {count} \\\\")
        lines.append("        \\hline")

    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_shapiro_latex_table(results_dict, test_variables=None, groups=None, caption="", label=""):
    """
    Generate a LaTeX table for Shapiro-Wilk normality test results from a nested result dict.

    Args:
        results_dict (dict): The nested dictionary returned by run_group_test results.
        test_variables (list of str or None): Which test variables to include.
        groups (list of str or None): Which groupings to include.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    test_varible_mapping = _get_test_varible_mapping()

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\begin{tabular}{|l|r|r|r|}")
    lines.append("        \\hline")
    lines.append("        \\textbf{Group} & \\textbf{n} & \\textbf{W} & \\textbf{p-value} \\\\")
    lines.append("        \\hline")

    for test_variable, group_dict in results_dict.items():
        if test_variables and test_variable not in test_variables:
            continue

        # Add a header row to separate this test variable
        test_variable_description = test_varible_mapping[test_variable]
        lines.append(f"        \\multicolumn{{4}}{{|l|}}{{\\textbf{{{test_variable_description}}}}} \\\\")
        lines.append("        \\hline")

        for group_name, result in group_dict.items():
            if groups and group_name not in groups:
                continue

            group_sizes = result.get("group_sizes", [None, None])

            for idx, (subgroup, normality) in enumerate(result["normality"].items()):
                W = normality["W"]
                p = normality["p"]
                n = group_sizes[idx] if idx < len(group_sizes) else "?"

                if p < 0.05:
                    p_fmt = f"\\textbf{{{p:.4f}}}"
                else:
                    p_fmt = f"{p:.4f}"
                if W > 0.9 and p > 0.05:
                    w_fmt = f"\\textbf{{{W:.4f}}}"
                else:
                    w_fmt = f"{W:.3f}"

                subgroup_formatted = re.sub(r"(Q\d{1,2}\.)", r"\\textbf{\1}", subgroup)
                lines.append(f"        {subgroup_formatted} & {n} & {w_fmt} & {p_fmt} \\\\")

        lines.append("        \\hline")

    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_mean_sd_latex_table(results_dict, test_variables=None, groups=None, caption="", label=""):
    """
    Generate a LaTeX table for group means and standard deviations from a nested result dict.

    Args:
        results_dict (dict): The nested dictionary returned by run_group_test results.
        test_variables (list of str or None): Which test variables to include.
        groups (list of str or None): Which groupings to include.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    test_variable_mapping = _get_test_varible_mapping()

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\begin{tabular}{|l|r|r|r|}")
    lines.append("        \\hline")
    lines.append("        \\textbf{Group} & \\textbf{n} & \\textbf{Mean} & \\textbf{SD} \\\\")
    lines.append("        \\hline")

    for test_variable, group_dict in results_dict.items():
        if test_variables and test_variable not in test_variables:
            continue

        test_variable_description = test_variable_mapping[test_variable]
        full_dataset_results = results_dict[test_variable]["Full Dataset"]
        line = f"\\textbf{{{test_variable_description}}} &"
        line += f"{full_dataset_results.get('group_sizes', [0])[0]} & "
        line += f"{full_dataset_results.get('group_means', [0])[0]:.2f} & "
        line += f"{full_dataset_results.get('group_sds', [0])[0]:.2f} \\\\"
        lines.append(line)
        lines.append("        \\hline")

        for group_name, result in group_dict.items():
            if (groups and group_name not in groups) or group_name == "Full Dataset":
                continue

            group_sizes = result.get("group_sizes", [None, None])
            group_means = result.get("group_means", [None, None])
            group_sds = result.get("group_sds", [None, None])

            for idx, subgroup in enumerate(result["group_names"]):
                n = group_sizes[idx] if idx < len(group_sizes) else "?"
                mean = group_means[idx] if idx < len(group_means) else "?"
                sd = group_sds[idx] if idx < len(group_sds) else "?"

                subgroup_formatted = re.sub(r"(Q\d{1,2}\.)", r"\\textbf{\1}", subgroup)
                lines.append(f"        {subgroup_formatted} & {n} & {mean:.2f} & {sd:.2f} \\\\")

        lines.append("        \\hline")

    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_bootstrap_latex_table(results_dict, test_variables=None, groups=None, caption="", label=""):
    """
    Generate a LaTeX table for bootstrap confidence interval results from a nested result dict.

    Args:
        results_dict (dict): The nested dictionary returned by run_bootstrap_group_test results.
        test_variables (list of str or None): Which test variables to include.
        groups (list of str or None): Which groupings to include.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    test_variable_mapping = _get_test_varible_mapping()

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\begin{tabular}{|l|r|r|r|}")
    lines.append("        \\hline")
    header = "        \\textbf{Group comparison} & \\textbf{Mean difference} & \\textbf{Cohen's d} "
    header += "& \\textbf{95\\% Bootstrap CI} \\\\"
    lines.append(header)
    lines.append("        \\hline")

    for test_variable, group_dict in results_dict.items():
        if test_variables and test_variable not in test_variables:
            continue

        test_variable_description = test_variable_mapping[test_variable]
        lines.append(f"        \\multicolumn{{4}}{{|l|}}{{\\textbf{{{test_variable_description}}}}} \\\\")
        lines.append("        \\hline")

        for group_name, result in group_dict.items():
            if groups and group_name not in groups:
                continue

            grouping_name = result.get("grouping_name", "group")
            mean_diff = result.get("observed_mean_difference", "?")
            cohens_d = result.get("cohens_d", "?")
            ci_low, ci_high = result.get("bootstrap_ci", ["?", "?"])
            if np.sign(ci_low) == np.sign(ci_high):
                confidence_intervals = f"\\textbf{{[{ci_low:.2f}, {ci_high:.2f}]}}"
            else:
                confidence_intervals = f"[{ci_low:.2f}, {ci_high:.2f}]"

            lines.append(
                f"        {grouping_name} & {mean_diff:.2f} & {cohens_d:.2f} & {confidence_intervals} \\\\"
            )

        lines.append("        \\hline")

    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_website_statistics_latex_table(website_stats, test_variable="accepts", caption="", label=""):
    """
    Generate a LaTeX table summarizing either accepts or time spent per website and device.

    Args:
        website_stats (dict): Output dictionary from get_website_statistics.
        test_variable (str): "accepts" or "time" — determines which set of stats to show.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    if test_variable not in ["accepts", "time"]:
        raise ValueError(f"Invalid test_variable '{test_variable}'. Must be 'accepts' or 'time'.")

    stat_suffix = "accepts" if test_variable == "accepts" else "time"

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\footnotesize")
    lines.append("    \\begin{tabular}{|l|r|r|r|}")
    lines.append("        \\hline")
    if test_variable == "accepts":
        header = "        \\textbf{Website} & \\textbf{Computer} & \\textbf{Phone} & \\textbf{Total} \\\\"
    else:
        header = "        \\textbf{Website} & \\textbf{Computer} (Mean (SD)) & \\textbf{Phone} (Mean (SD)) "
        header += "& \\textbf{Total} (Mean (SD))\\\\"
    lines.append(header)
    lines.append("        \\hline")

    for site, stats in website_stats.items():
        computer = f"{stats[f'computer_{stat_suffix}']}"
        phone = f"{stats[f'phone_{stat_suffix}']}"
        total = f"{stats[f'total_{stat_suffix}']}"
        if test_variable == "time":  # Add standard deviations
            computer += f" ({stats[f'computer_{stat_suffix}_std']:.2f})"
            phone += f" ({stats[f'phone_{stat_suffix}_std']:.2f})"
            total += f" ({stats[f'total_{stat_suffix}_std']:.2f})"
        line = f"        {site.capitalize()} & {computer} & {phone} & {total} \\\\"
        lines.append(line)

    lines.append("        \\hline")
    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_friedman_latex_table(results_dict, caption="", label=""):
    """
    Generate a LaTeX table for Friedman test results for accepts and time.

    Args:
        results_dict (dict): Dictionary with results for "accepts" and "time".
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\begin{tabular}{|l|l|r|r|}")
    lines.append("        \\hline")
    lines.append(
        "        \\textbf{Test variable} & \\textbf{Device} & \\textbf{Test statistic} & \\textbf{p-value} \\\\"
    )
    lines.append("        \\hline")

    device_mapping = {
        "computer": "Computer",
        "phone": "Phone",
        "both": "Both devices"
    }

    test_variable_mapping = {
        "accepts": "Consent accepts",
        "time": "Banner answer time"
    }

    for test_variable in ["accepts", "time"]:
        readable_test_variable = test_variable_mapping[test_variable]
        for device in ["computer", "phone", "both"]:
            device_results = results_dict.get(test_variable, {}).get(device, {})
            stat = device_results.get("statistic", "?")
            p = device_results.get("p_value", "?")

            if isinstance(stat, float):
                stat_fmt = f"{stat:.3f}"
            else:
                stat_fmt = str(stat)

            if isinstance(p, float):
                p_fmt = f"\\textbf{{{p:.8f}}}" if p < 0.05 else f"{p:.8f}"
            else:
                p_fmt = str(p)

            lines.append(f"        {readable_test_variable} & {device_mapping[device]} & {stat_fmt} & {p_fmt} \\\\")

    lines.append("        \\hline")
    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_wilcoxon_latex_table(wilcoxon_results, caption="", label=""):
    """
    Generate a LaTeX table for Wilcoxon pairwise test results.

    Args:
        wilcoxon_results (list of dicts): Each dict contains 'pair', 'n', 'statistic', 'p_value'.
        caption (str): Caption text for the LaTeX table.
        label (str): Label for the LaTeX table.

    Returns:
        str: A LaTeX-formatted table string.
    """
    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\footnotesize")  # TODO: Is this needed here?
    lines.append("    \\begin{tabular}{|l|l|r|r|r|}")
    lines.append("        \\hline")
    lines.append(
        "        \\textbf{Website 1} & \\textbf{Website 2} & \\textbf{n} & \\textbf{Statistic} & \\textbf{p-value} \\\\"
    )
    lines.append("        \\hline")

    for res in wilcoxon_results:
        site1, site2 = res["pair"]
        n = res["n"]
        stat = res["statistic"]
        p = res["p_value"]

        if isinstance(p, float):
            p_fmt = f"\\textbf{{{p:.6f}}}" if p < 0.05 else f"{p:.6f}"
        else:
            p_fmt = str(p)

        stat_fmt = f"{stat:.1f}" if isinstance(stat, float) else str(stat)

        lines.append(f"        {site1.capitalize()} & {site2.capitalize()} & {n} & {stat_fmt} & {p_fmt} \\\\")

    lines.append("        \\hline")
    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def make_withdrawal_statistics_latex_table(results_dict, caption="", label=""):
    """
    Generate a LaTeX table summarizing answer times, withdrawal times,
    and Mann-Whitney U test results per website and device.

    Args:
        results_dict (dict): Nested dictionary with websites -> devices -> stats.
        caption (str): Caption for the table.
        label (str): Label for the table.

    Returns:
        str: LaTeX table string.
    """
    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("    \\centering")
    lines.append("    \\footnotesize")
    lines.append("    \\begin{tabular}{|l|l|r|r|r|r|r|r|}")
    lines.append("        \\hline")
    header = "\\textbf{Website} & \\textbf{Device} & \\makecell{\\textbf{Answer} \\\\ (mean)} & "
    header += "\\makecell{\\textbf{Answer} \\\\ (no withdraws)} & \\makecell{\\textbf{Withdraw} \\\\ (mean)} & "
    header += "\\textbf{ n} & \\textbf{U-value} & \\textbf{p-value}\\\\"
    lines.append(header)
    lines.append("        \\hline")

    device_mapping = {
        "computer": "Computer",
        "phone": "Phone",
        "both": "Both"
    }

    for website, device_dict in results_dict.items():
        for device in ["computer", "phone", "both"]:
            data = device_dict.get(device, {})

            avg_answer_all = data.get("avg_answer_all", "-")
            avg_answer_no_withdraw = data.get("avg_answer_no_withdraw", "-")
            avg_withdraw = data.get("avg_withdraw", "-")
            n_withdraw = data.get("n_withdraw", "-")

            stat = data.get("stat", "-")
            p_value = data.get("p_value", "-")

            def fmt(x):
                if isinstance(x, (float, int)):
                    if pd.isna(x):
                        return "-"
                    return f"{x:.2f}"
                if x is None:
                    return "-"
                return str(x)

            def fmt_p(x):
                if isinstance(x, (float, int)):
                    return f"\\textbf{{{x:.4f}}}" if x < 0.05 else f"{x:.4f}"
                if x is None:
                    return "-"
                return str(x)

            line = (
                f"        {website.capitalize()} & {device_mapping[device]} & {fmt(avg_answer_all)} & "
                f"{fmt(avg_answer_no_withdraw)} & {fmt(avg_withdraw)} & {n_withdraw} & "
                f"{fmt(stat)} & {fmt_p(p_value)} \\\\"
            )
            lines.append(line)

        lines.append("        \\hline")

    lines.append("    \\end{tabular}")
    if caption:
        lines.append(f"    \\caption{{{caption}}}")
    if label:
        lines.append(f"    \\label{{{label}}}")
    lines.append("\\end{table}")

    return "\n".join(lines)
