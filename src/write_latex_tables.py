import os
from pathlib import Path

from src.generate_results import get_all_friedman_test_results, get_all_group_test_results, get_website_statistics
from src.get_constants import get_constants
from src.hypothesis_tests import run_pairwise_wilcoxon_tests
from src.latex_table_captions import (BOOTSTRAP_EXTRA_ACCEPTS_CAPTION, BOOTSTRAP_EXTRA_TIME_CAPTION,
                                      BOOTSTRAP_MAIN_CAPTION, FRIEDMAN_CAPTION, MEAN_AND_SD_EXTRA_ACCEPTS_CAPTION,
                                      MEAN_AND_SD_EXTRA_TIME_CAPTION, MEAN_AND_SD_MAIN_CAPTION,
                                      NETTSKJEMA_REPORT_CAPTION, SHAPIRO_WILK_EXTRA_ACCEPTS_CAPTION,
                                      SHAPIRO_WILK_EXTRA_TIME_CAPTION, SHAPIRO_WILK_MAIN_CAPTION,
                                      WEBSITE_STATISTICS_ACCEPTS_CAPTION, WEBSITE_STATISTICS_TIME_CAPTION,
                                      WILCOXON_COMPUTER_ACCEPTS_CAPTION, WILCOXON_COMPUTER_TIME_CAPTION,
                                      WILCOXON_PHONE_ACCEPTS_CAPTION, WILCOXON_PHONE_TIME_CAPTION,
                                      WILCOXON_TOTAL_ACCEPTS_CAPTION, WILCOXON_TOTAL_TIME_CAPTION)
from src.make_latex_tables import (make_bootstrap_latex_table, make_friedman_latex_table, make_mean_sd_latex_table,
                                   make_nettskjema_report_latex, make_shapiro_latex_table,
                                   make_website_statistics_latex_table, make_wilcoxon_latex_table)

CONSTANTS = get_constants()
GROUP_TESTS_FOLDER = CONSTANTS["paths"]["folders"]["group_tests_folder"]
WEBISTE_TESTS_FOLDER = CONSTANTS["paths"]["folders"]["website_tests_folder"]
OVERVIEW_TABLES_FOLDER = CONSTANTS["paths"]["folders"]["overview_tables_folder"]


def _write_latex_table_to_file(text, filename, folder):
    """
    Writes a LaTeX table string to file.

    Args:
        text (str): The string of the LaTeX table.
        filename (str): The filename.
        folder (str): The subfolder to store the latex table in.
    """
    # We have most paths handled in `src.paths.py`, but it is simpler to handle these here.
    folder_path = Path(CONSTANTS["paths"]["folders"]["latex_tables_folder"]) / folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = folder_path / filename
    with open(file_path, "w") as outfile:
        outfile.write(text)


def write_nettskjema_report(df):
    """
    Writes the nettskjema report to file.
    This contains information about the number of answers on each of the quantitative questions from the nettskjema
    survey.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = NETTSKJEMA_REPORT_CAPTION.replace("\n", " ")
    label = "tab:nettskjema_report"
    filename = "nettskjema_report.txt"
    folder = OVERVIEW_TABLES_FOLDER
    nettskjema_table = make_nettskjema_report_latex(df, caption=caption, label=label)
    _write_latex_table_to_file(text=nettskjema_table, filename=filename, folder=folder)


def write_shapiro_wilk_main(df):
    """
    Generates the main Shapiro Wilk table. This one contains the test variables for the cookie question score, total
    accepts and total average time spent.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = SHAPIRO_WILK_MAIN_CAPTION.replace("\n", " ")
    label = "tab:shapiro_wilk_main"
    filename = "shapiro_wilk_main.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="shapiro-wilk", print_values=False)
    shapiro_wilk_table = make_shapiro_latex_table(
        results,
        test_variables=[
            "cookie_questions_score",
            "total_accepts",
            "total_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=shapiro_wilk_table, filename=filename, folder=folder)


def write_shapiro_wilk_extra_accepts(df):
    """
    Generates the main Shapiro Wilk table. This one contains the test variables for the number of accepts, both on
    computer on phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = SHAPIRO_WILK_EXTRA_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:shapiro_wilk_extra_accepts"
    filename = "shapiro_wilk_extra_accepts.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="shapiro-wilk", print_values=False)
    shapiro_wilk_table = make_shapiro_latex_table(
        results,
        test_variables=[
            "computer_accepts",
            "phone_accepts",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=shapiro_wilk_table, filename=filename, folder=folder)


def write_shapiro_wilk_extra_time(df):
    """
    Generates the main Shapiro Wilk table. This one contains the test variables for the average time spent, both on
    computer and phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = SHAPIRO_WILK_EXTRA_TIME_CAPTION.replace("\n", " ")
    label = "tab:shapiro_wilk_extra_time"
    filename = "shapiro_wilk_extra_time.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="shapiro-wilk", print_values=False)
    shaprio_wilk_table = make_shapiro_latex_table(
        results,
        test_variables=[
            "computer_average_time",
            "phone_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=shaprio_wilk_table, filename=filename, folder=folder)


def write_mean_sd_main(df):
    """
    Writes table with means and standard deviations for all subgroups, given the cookie answers, total accepts and
    total average time spent on cookie banners.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = MEAN_AND_SD_MAIN_CAPTION.replace("\n", " ")
    label = "tab:mean_and_sd_main"
    filename = "mean_and_sd_main.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="mean-sd", print_values=False)
    mean_and_sd_table = make_mean_sd_latex_table(
        results_dict=results,
        test_variables=[
            "cookie_questions_score",
            "total_accepts",
            "total_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_mean_sd_extra_accepts(df):
    """
    Writes table with means and standard deviations for all subgroups for computer and phone for the total amount of
    accepts.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = MEAN_AND_SD_EXTRA_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:mean_and_sd_extra_accepts"
    filename = "mean_and_sd_extra_accepts.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="mean-sd", print_values=False)
    mean_and_sd_table = make_mean_sd_latex_table(
        results_dict=results,
        test_variables=[
            "computer_accepts",
            "phone_accepts",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_mean_sd_extra_time(df):
    """
    Writes table with means and standard deviations for all subgroups for computer and phone for the answer time.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = MEAN_AND_SD_EXTRA_TIME_CAPTION.replace("\n", " ")
    label = "tab:mean_and_sd_extra_time"
    filename = "mean_and_sd_extra_time.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="mean-sd", print_values=False)
    mean_and_sd_table = make_mean_sd_latex_table(
        results_dict=results,
        test_variables=[
            "computer_average_time",
            "phone_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_bootstrap_main(df):
    """
    Writes table with bootstrap confidence intervals metrics.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_MAIN_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_main"
    filename = "bootstrap_main.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="bootstrap", print_values=False)
    mean_and_sd_table = make_bootstrap_latex_table(
        results_dict=results,
        test_variables=[
            "cookie_questions_score",
            "total_accepts",
            "total_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_bootstrap_extra_accepts(df):
    """
    Writes table with bootstrap confidence intervals metrics for number of accepts on computer and phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_EXTRA_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_extra_accepts"
    filename = "bootstrap_extra_accepts.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="bootstrap", print_values=False)
    mean_and_sd_table = make_bootstrap_latex_table(
        results_dict=results,
        test_variables=[
            "computer_accepts",
            "phone_accepts",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_bootstrap_extra_time(df):
    """
    Writes table with bootstrap confidence intervals metrics for time spent on cookie banner for computer and phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_EXTRA_TIME_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_extra_time"
    filename = "bootstrap_extra_time.txt"
    folder = GROUP_TESTS_FOLDER
    results = get_all_group_test_results(df, test_type="bootstrap", print_values=False)
    mean_and_sd_table = make_bootstrap_latex_table(
        results_dict=results,
        test_variables=[
            "computer_average_time",
            "phone_average_time",
        ],
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename, folder=folder)


def write_website_statistics_accepts(df):
    """
    Writes table with accepts for each website and every device.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = WEBSITE_STATISTICS_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:website_statistics_accepts"
    filename = "website_statistics_accepts.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = get_website_statistics(df)
    website_statistics_table = make_website_statistics_latex_table(
        results,
        test_variable="accepts",
        caption=caption,
        label=label
    )
    _write_latex_table_to_file(website_statistics_table, filename=filename, folder=folder)


def write_website_statistics_time(df):
    """
    Writes the time spent on the different website for all devices, including standard deviations.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = WEBSITE_STATISTICS_TIME_CAPTION.replace("\n", " ")
    label = "tab:website_statistics_time"
    filename = "website_statistics_time.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = get_website_statistics(df)
    website_statistics_table = make_website_statistics_latex_table(
        results,
        test_variable="time",
        caption=caption,
        label=label
    )
    _write_latex_table_to_file(website_statistics_table, filename=filename, folder=folder)


def write_friedman(df):
    """
    Writes table with Friedman test for the different websites with one row for each device (including "both"),
    looking at the number of accepts given.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = FRIEDMAN_CAPTION.replace("\n", " ")
    label = "tab:friedman"
    filename = "friedman.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = get_all_friedman_test_results(df)
    friedman_table = make_friedman_latex_table(
        results_dict=results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=friedman_table, filename=filename, folder=folder)


def write_wilcoxon_total_accepts(df):
    """
    Writes a Wilcoxon table for each pair of website looking at number of accepts on both devices.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_TOTAL_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_total_accepts"
    filename = "wilcoxon_total_accepts.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="accepts",
        device="both"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_wilcoxon_computer_accepts(df):
    """
    Writes a Wilcoxon table for each pair of website looking at number of accepts on computer.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_COMPUTER_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_computer_accepts"
    filename = "wilcoxon_computer_accepts.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="accepts",
        device="computer"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_wilcoxon_phone_accepts(df):
    """
    Writes a Wilcoxon table for each pair of website looking at number of accepts on phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_PHONE_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_phone_accepts"
    filename = "wilcoxon_phone_accepts.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="accepts",
        device="phone"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_wilcoxon_total_time(df):
    """
    Writes a Wilcoxon table for each pair of website looking at the time spent on both devices.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_TOTAL_TIME_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_total_times"
    filename = "wilcoxon_total_time.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="time",
        device="both"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_wilcoxon_computer_time(df):
    """
    Writes a Wilcoxon table for each pair of website looking at the time spent on computer.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_COMPUTER_TIME_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_computer_times"
    filename = "wilcoxon_computer_time.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="time",
        device="computer"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_wilcoxon_phone_time(df):
    """
    Writes a Wilcoxon table for each pair of website looking at the time spent on phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    make_wilcoxon_latex_table
    caption = WILCOXON_PHONE_TIME_CAPTION.replace("\n", " ")
    label = "tab:wilcoxon_phone_times"
    filename = "wilcoxon_phone_time.txt"
    folder = WEBISTE_TESTS_FOLDER
    results = run_pairwise_wilcoxon_tests(
        df,
        test_variable="time",
        device="phone"
    )
    wilcoxon_table = make_wilcoxon_latex_table(
        results,
        caption=caption,
        label=label,
    )
    _write_latex_table_to_file(text=wilcoxon_table, filename=filename, folder=folder)


def write_all_latex_tables(df, nettskjema_report=False, shapiro_wilk=False, mean_and_sd=False, bootstrap=False,
                           website_statistics=False, friedman=False, wilcoxon=False):
    """
    Writes the LaTeX tables, depending on the arguments passed. Calls all of the other functions to do so.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
        nettskjema_report (bool): Whether or not to write the nettskjema report.
        shapiro_wilk (bool): Whether or not to write the three Shapiro-Wilk normality tables.
        mean_and_sd (bool): Whether or not to write the three mean and standard deviation tables.
        bootstrap (bool): Whether or not to print the three bootstrap tables.
        website_statistics (bool): Whether or not to print the two website statistic tables.
        friedman (bool): Whether or not to print the friedman table.
        wilcoxon (bool): Whether or not to print the six Wilcoxon tables.
    """
    if nettskjema_report:
        write_nettskjema_report(df)
    if shapiro_wilk:
        write_shapiro_wilk_main(df)
        write_shapiro_wilk_extra_accepts(df)
        write_shapiro_wilk_extra_time(df)
    if mean_and_sd:
        write_mean_sd_main(df)
        write_mean_sd_extra_accepts(df)
        write_mean_sd_extra_time(df)
    if bootstrap:
        write_bootstrap_main(df)
        write_bootstrap_extra_accepts(df)
        write_bootstrap_extra_time(df)
    if website_statistics:
        write_website_statistics_accepts(df)
        write_website_statistics_time(df)
    if friedman:
        write_friedman(df)
    if wilcoxon:
        write_wilcoxon_total_accepts(df)
        write_wilcoxon_computer_accepts(df)
        write_wilcoxon_phone_accepts(df)
        write_wilcoxon_total_time(df)
        write_wilcoxon_computer_time(df)
        write_wilcoxon_phone_time(df)
