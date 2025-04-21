from src.get_constants import get_constants
from src.process_data import _quantisize_answers


CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


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
