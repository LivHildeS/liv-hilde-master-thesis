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
