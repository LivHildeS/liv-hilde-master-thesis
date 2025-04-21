from src.generate_results import get_website_averages, print_pairwise_mcnemar_results
from src.hypothesis_tests import run_cochrans_q_test, run_pairwise_mcnemar_tests
from src.utils import get_all_data, read_nettskjema_data, read_participant_data

if __name__ == "__main__":
    nettskjema_df = read_nettskjema_data()
    experiments_df = read_participant_data()
    df = get_all_data()
    get_website_averages(df)
    from IPython import embed
    embed()
