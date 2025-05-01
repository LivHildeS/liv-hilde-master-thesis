from src.write_latex_tables import write_all_latex_tables
from src.utils import get_all_data, read_nettskjema_data, read_participant_data
from src.make_plots import plot_response_times_per_device
from src.hypothesis_tests import run_withdrawal_wilcoxon_test


if __name__ == "__main__":
    run_plots = False
    nettskjema_df = read_nettskjema_data()
    experiments_df = read_participant_data()
    df = get_all_data()
    write_all_latex_tables(
        df,
        nettskjema_report=True,
        shapiro_wilk=True,
        mean_and_sd=True,
        bootstrap=False,
        website_statistics=True,
        friedman=True,
        wilcoxon=True,
        withdrawal=True,
    )

    if run_plots:
        plot_response_times_per_device(df, "computer")
        plot_response_times_per_device(df, "phone")

    withdrawal_test_result = run_withdrawal_wilcoxon_test(df)
    print(f"The results from the Wilcoxon withdrawal test was stat: {withdrawal_test_result['stat']:.8f}")
    print(f"With p-value {withdrawal_test_result['p_value']:.8f}.")
