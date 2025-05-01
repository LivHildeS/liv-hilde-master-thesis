from src.get_constants import get_constants

CONSTANTS = get_constants()


NETTSKJEMA_REPORT_CAPTION = """
\\textbf{Number of answers on the quantitative survey questions.}
"""

SHAPIRO_WILK_GENERIC_CAPTION = """
The  Shapiro-Wilk test statistic \\textbf{W}, highlighted in \\textbf{bold} if it is greater than 0.9.
The p-value is highlighted in \\textbf{bold} if it is less than 0.05.
"""

SHAPIRO_WILK_MAIN_CAPTION = """
\\textbf{The group test data is \\textit{not} approximately normal.} The table shows results from Shapiro-Wilk normality
tests for the subgroups and outcome variables inspected. The null hypothesis of normality is often clearly rejected.
""" + SHAPIRO_WILK_GENERIC_CAPTION

SHAPIRO_WILK_EXTRA_ACCEPTS_CAPTION = """
\\textbf{Shapiro-Wilk normality statistics for the number of cookie banner accepts on different devices.}
The Shapiro-Wilk \\textbf{W} statistic is never above 0.9 when the data is grouped based on survey questions and the
number of acceptances on computer and phone, indicating that the data is not approximately normal.
Additionally, the p-value is less than 0.05 for most groups, rejecting the null hypothesis of normality.
""" + SHAPIRO_WILK_GENERIC_CAPTION

SHAPIRO_WILK_EXTRA_TIME_CAPTION = """
\\textbf{Shapiro-Wilk normality statistics for time spent on cookie banners on different devices.} When considering the
average response time on computer, Shapiro-Wilk rejects normality for most groups. However, on phone, many groups
have high \\textbf{W} and p-values, suggesting that the data is approximately normal. Nevertheless, this is only for a
small number of groups overall.
""" + SHAPIRO_WILK_GENERIC_CAPTION

MEAN_AND_SD_MAIN_CAPTION = """
\\textbf{Means and standard deviations} for the subgroups and outcome variables investigated. The sub-headers marks
which outcome variable that the statistics are calculated with, and the values immediately following them on the right
corresponds to the full dataset.
"""

MEAN_AND_SD_EXTRA_ACCEPTS_CAPTION = """
\\textbf{Means and standard deviations of the number of accepts on different devices}. The numbers on the same
line as the subheaders with the outcome variables corresponds to the full dataset.
"""

MEAN_AND_SD_EXTRA_TIME_CAPTION = """
\\textbf{Means and standard deviations of cookie banner response time on different devices}. The numbers on the same
line as the subheaders with the outcome variables corresponds to the full dataset.
"""

BOOTSTRAP_MAIN_CAPTION = f"""
\\textbf{{Bootstrap confidence intervals (CI) and statistics for the survey groups}}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{{bold}}.
The amount of bootstrap samples used was {CONSTANTS['n_bootstraps']}.
"""

BOOTSTRAP_EXTRA_ACCEPTS_CAPTION = f"""
\\textbf{{Bootstrap confidence intervals (CI) for the number of cookie banner accepts on different devices}}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{{bold}}.
The amount of bootstrap samples used was {CONSTANTS['n_bootstraps']}.
"""

BOOTSTRAP_EXTRA_TIME_CAPTION = f"""
\\textbf{{Bootstrap confidence intervals (CI) for cookie banner response time on different devices}}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{{bold}}.
The amount of bootstrap samples used was {CONSTANTS['n_bootstraps']}.
"""

WEBSITE_STATISTICS_ACCEPTS_CAPTION = f"""
\\textbf{{Total amount of cookie consent accepts}} for the different websites on all devices. There were
{CONSTANTS['number_of_participants']} number of participants.
"""

WEBSITE_STATISTICS_TIME_CAPTION = """
\\textbf{Average time in seconds spent on cookie banners} for the different websites on all devices. The paranthesis
contains the standard deviations.
"""

FRIEDMAN_CAPTION = """
\\textbf{Friedman tests on consent accepts and banner answer time on the different websites are highly significant}.
All of the tests have very low p-values, indicating that the null hypothesis stating that the websites have the
same expected cookie consent acceptance rate and cookie banner answer time can safely be rejected.
"""

WILCOXON_GENERIC_CAPTION = """
The number \\textbf{n} marks the amount of observations with different responses for each pair of website, as the
Wilcoxon test only uses these. The statistic shows bigger difference the closer the number is to 0.
"""

WILCOXON_TOTAL_ACCEPTS_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the consent acceptances on both devices.} ``Dagens'' has significantly different
responses than the other websites.
""" + WILCOXON_GENERIC_CAPTION

WILCOXON_COMPUTER_ACCEPTS_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the consent acceptances on computer.}
""" + WILCOXON_GENERIC_CAPTION

WILCOXON_PHONE_ACCEPTS_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the consent acceptances on both phone.}
""" + WILCOXON_GENERIC_CAPTION

WILCOXON_TOTAL_TIME_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the banner response time on both devices.}
""" + WILCOXON_GENERIC_CAPTION

WILCOXON_COMPUTER_TIME_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the banner response time on computer.} ``Dagens'' has significantly different
responses than the other websites.
""" + WILCOXON_GENERIC_CAPTION

WILCOXON_PHONE_TIME_CAPTION = """
\\textbf{Pairwise Wilcoxon tests on the banner response time on phone.}
""" + WILCOXON_GENERIC_CAPTION

WITHDRAWAL_STATISTICS_CAPTION = """
\\textbf{Withdrawing consent takes over 20 times longer than giving it.} The table shows average time spent giving
consent and withdrawing it in seconds, and the number of participants that has given consent and withdrawn it.
Comparing the average withdrawal time and corresponding consent time per participant gave highly significant results
with a Wilcoxon test, with a test statistic of 0 and p-value of \\textbf{0.000061}, rejecting the null hypothesis
of equal consent and withdrawal times.
"""
