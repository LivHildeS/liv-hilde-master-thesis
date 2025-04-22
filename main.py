from src.generate_results import (get_website_averages, make_nettskjema_report, print_all_group_test_results,
                                  print_group_test_result, print_pairwise_mcnemar_results,
                                  print_pairwise_wilcoxon_results)
from src.hypothesis_tests import (run_cochrans_q_test, run_friedman_test, run_group_test, run_pairwise_mcnemar_tests,
                                  run_pairwise_wilcoxon_tests)
from src.utils import get_all_data, read_nettskjema_data, read_participant_data

if __name__ == "__main__":
    nettskjema_df = read_nettskjema_data()
    experiments_df = read_participant_data()
    df = get_all_data()
    print_all_group_test_results(df)
    # from IPython import embed
    # embed()
