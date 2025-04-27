from src.write_latex_tables import write_all_latex_tables
from src.utils import get_all_data, read_nettskjema_data, read_participant_data
from src.make_plots import plot_response_times_per_device

if __name__ == "__main__":
    nettskjema_df = read_nettskjema_data()
    experiments_df = read_participant_data()
    df = get_all_data()
    write_all_latex_tables(
        df,
        nettskjema_report=False,
        shapiro_wilk=False,
        mean_and_sd=False,
        bootstrap=False,
        website_statistics=True,
        friedman=False,
        wilcoxon=False,
        withdrawal=True,
    )
    # plot_response_times_per_device(df, "computer")
    # plot_response_times_per_device(df, "phone")
