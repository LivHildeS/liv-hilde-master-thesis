from pathlib import Path

from src.generate_results import get_all_group_test_results
from src.get_constants import get_constants
from src.latex_table_captions import (BOOTSTRAP_EXTRA_ACCEPTS_CAPTION, BOOTSTRAP_EXTRA_TIME_CAPTION,
                                      BOOTSTRAP_MAIN_CAPTION, MEAN_AND_SD_EXTRA_ACCEPTS_CAPTION,
                                      MEAN_AND_SD_EXTRA_TIME_CAPTION, MEAN_AND_SD_MAIN_CAPTION,
                                      NETTSKJEMA_REPORT_CAPTION, SHAPIRO_WILK_EXTRA_ACCEPTS_CAPTION,
                                      SHAPIRO_WILK_EXTRA_TIME_CAPTION, SHAPIRO_WILK_MAIN_CAPTION)
from src.make_latex_tables import (make_bootstrap_latex_table, make_mean_sd_latex_table, make_nettskjema_report_latex,
                                   make_shapiro_latex_table)

CONSTANTS = get_constants()


def _write_latex_table_to_file(text, filename):
    """
    Writes a LaTeX table string to file.

    Args:
        text (str): The string of the LaTeX table.
        filename (str): The filename.
    """
    # We have most paths handled in `src.paths.py`, but it is simpler to handle these here.
    file_path = Path(CONSTANTS["paths"]["folders"]["latex_tables_folder"]) / filename
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
    nettskjema_table = make_nettskjema_report_latex(df, caption=caption, label=label)
    _write_latex_table_to_file(text=nettskjema_table, filename=filename)


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
    _write_latex_table_to_file(text=shapiro_wilk_table, filename=filename)


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
    _write_latex_table_to_file(text=shapiro_wilk_table, filename=filename)


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
    _write_latex_table_to_file(text=shaprio_wilk_table, filename=filename)


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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


def write_mean_sd_extra_time(df):
    """
    Writes table with means and standard deviations for all subgroups for computer and phone for the answer time.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = MEAN_AND_SD_EXTRA_TIME_CAPTION.replace("\n", " ")
    label = "tab:mean_and_sd_extra_time"
    filename = "mean_and_sd_extra_time.txt"
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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


def write_bootstrap_main(df):
    """
    Writes table with bootstrap confidence intervals metrics.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_MAIN_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_main"
    filename = "bootstrap_main.txt"
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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


def write_bootstrap_extra_accepts(df):
    """
    Writes table with bootstrap confidence intervals metrics for number of accepts on computer and phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_EXTRA_ACCEPTS_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_extra_accepts"
    filename = "bootstrap_extra_accepts.txt"
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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


def write_bootstrap_extra_time(df):
    """
    Writes table with bootstrap confidence intervals metrics for time spent on cookie banner for computer and phone.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    caption = BOOTSTRAP_EXTRA_TIME_CAPTION.replace("\n", " ")
    label = "tab:bootstrap_extra_time"
    filename = "bootstrap_extra_time.txt"
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
    _write_latex_table_to_file(text=mean_and_sd_table, filename=filename)


def write_all_latex_tables(df):
    """
    Writes all of the LaTeX tables. Calls all of the other functions to do so.

    Args:
        df (pd.DataFrame): The dataframe with the results. Get with `src.utils.get_all_data()`
    """
    write_nettskjema_report(df)
    write_shapiro_wilk_main(df)
    write_shapiro_wilk_extra_accepts(df)
    write_shapiro_wilk_extra_time(df)
    write_mean_sd_main(df)
    write_mean_sd_extra_accepts(df)
    write_mean_sd_extra_time(df)
    write_bootstrap_main(df)
    write_bootstrap_extra_accepts(df)
    write_bootstrap_extra_time(df)
