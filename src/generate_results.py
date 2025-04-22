from src.get_constants import get_constants
from src.process_data import _quantisize_answers
from src.hypothesis_tests import run_group_test


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

    print("-----------------------------------------")
    print(f"Test statistic: {result['test_statistic']}")
    print(f"Test type     : {result['test_type']}")
    print(f"Group 1       : {group1} (n={size1}, mean={mean1:.3f})")
    print(f"Group 2       : {group2} (n={size2}, mean={mean2:.3f})")

    if "normality" in result:
        print("\nNormality (Shapiro-Wilk):")
        for group in result["normality"]:
            W = result["normality"][group]["W"]
            p = result["normality"][group]["p"]
            print(f"  {group:<12}: W = {W:.3f}, p = {p:.4f}")

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


def make_nettskjema_report(df):
    columns = [
        "privacy_concern",
        "knows_cookies",
        "understand_cookie_consent",
        "cookie_sharing_feeling",
        "cookie_banner_response",
        "have_withdrawn_consent",
        "aware_withdrawal_ease",
        "age",
        "it_background",
        "cookie_questions_score",
    ]
    with open("data/nettskjema_report.txt", "w") as outfile:
        for column in columns:
            outfile.write(str(df[column].value_counts()) + "\n\n")


def print_all_group_test_results(df):
    """

    Args:
        df (pd.Dataframe): All the data.

    """
    cookie_questions = {
        "df1": df[df["cookie_questions_score"] == 4],
        "df2": df[df["cookie_questions_score"] < 4],
        "group_names": ["4/4 correct cookie questions", "<4 correct cookie questions"]
    }
    it_background = {
        "df1": df[df["it_background"] != "No"],
        "df2": df[df["it_background"] == "No"],
        "group_names": ["With IT background", "Without IT background"]
    }
    age = {
        "df1": df[df["age_int"] < 30],
        "df2": df[df["age_int"] > 30],
        "group_names": ["Under 30 years", "30 years or older"]
    }
    privacy_concern = {
        "df1": df[df["privacy_concern"] != "Slightly concerned"],
        "df2": df[df["privacy_concern"] == "Slightly concerned"],
        "group_names": ["Concerned", "Not concerned"]
    }
    understand_cookie_consent = {
        "df1": df[~df["understand_cookie_consent"].isin(["Not at all", "To a small extent", "Neither nor"])],
        "df2": df[~df["understand_cookie_consent"].isin(["To a great extent", "To some extent"])],
        "group_names": ["Understand a lot", "Do not understand so much"]
    }
    cookie_banner_response = {
        "df1": df[df["cookie_banner_response"] == "I actively take steps to withhold my consent."],
        "df2": df[df["cookie_banner_response"] != "I actively take steps to withhold my consent."],
        "group_names": ["Witholds consent", "Does always withhold consent"]
    }
    have_withdrawn_consent = {
        "df1": df[df["have_withdrawn_consent"] == "Yes"],
        "df2": df[df["have_withdrawn_consent"] == "No"],
        "group_names": ["Have withdrawn", "Have not withdrawn"]
    }
    aware_withdrawal_ease = {
        "df1": df[df["aware_withdrawal_ease"] == "Yes"],
        "df2": df[df["aware_withdrawal_ease"] == "No"],
        "group_names": ["Awere of withdrawal ease", "Not aware of withdrawal ease"]
    }

    groups = [
        cookie_questions,
        it_background,
        age,
        privacy_concern,
        understand_cookie_consent,
        cookie_banner_response,
        have_withdrawn_consent,
        aware_withdrawal_ease
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

    for test_variable in test_variables:
        for group in groups:
            result = run_group_test(
                group["df1"], group["df2"], value_column=test_variable, test_type="mannwhitney",
                group_names=group["group_names"])
            print_group_test_result(result)
