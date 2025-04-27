NETTSKJEMA_REPORT_CAPTION = """
\\textbf{Number of answers on the quantitative survey questions.}
"""

SHAPIRO_WILK_GENERIC_CAPTION = """
The \\textbf{W} is the Shapiro-Wilk test statistic, highlighted in \\textbf{bold} if it is greater than 0.9.
The p-value is highlighted in \\textbf{bold} if it is less than 0.05.
"""

SHAPIRO_WILK_MAIN_CAPTION = """
\\textbf{The group test data is \\textit{not} approximately normal.} For most groups, The Shapiro Wilk test show a low
\\textbf{W} (< 0.9), and the null hypothesis of normality is rejected (p-value < 0.05). The data is split based on
survey responses, and three different variables are investigated.
""" + SHAPIRO_WILK_GENERIC_CAPTION

SHAPIRO_WILK_EXTRA_ACCEPTS_CAPTION = """
\\textbf{Shapiro-Wilk normality statistics for the number of cookie banner accepts on different devices.}
The Shapiro-Wilk \\textbf{W} statistic is never above 0.9 when the data is grouped based on survey questions and the
number of acceptances on computer and phone,  indicating that the data is not approximately normal.
Additionally, the p-value is less than 0.05 for most groups, rejecting the null hypothesis of normality.
""" + SHAPIRO_WILK_GENERIC_CAPTION


SHAPIRO_WILK_EXTRA_TIME_CAPTION = """
\\textbf{Shapiro-Wilk normality statistics for time spent on cookie banners on different devices.} When considering the
average response time on computer, Shapiro-Wilk rejects normality for most groups. However, on phone, many groups
have high \\textbf{W} and p-values, suggesting that the data is approximately normal. Nevertheless, this is only for a
small number of groups overall.
""" + SHAPIRO_WILK_GENERIC_CAPTION

MEAN_AND_SD_MAIN_CAPTION = """
\\textbf{Means and standard deviations} for the subgroups investigated and variables investigated. The means and
standard deviations are calculated on the cookie question score, the total amount of cookie consent accepts and the
average time spent answering the cookie consent banners. The groups are made from the survey question responses.
"""

MEAN_AND_SD_EXTRA_ACCEPTS_CAPTION = """
\\textbf{Means and standard deviations of the number of accepts on different devices}.
"""

MEAN_AND_SD_EXTRA_TIME_CAPTION = """
\\textbf{Means and standard deviations of cookie banner response time on different devices}.
"""

BOOTSTRAP_MAIN_CAPTION = """
\\textbf{Bootstrap confidence intervals (CI) and statistics for the survey groups}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{bold}.
The bootstrap used 10000 iterations.
"""

BOOTSTRAP_EXTRA_ACCEPTS_CAPTION = """
\\textbf{Bootstrap confidence intervals (CI) for the number of cookie banner accepts on different devices}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{bold}.
The bootstrap used 10000 iterations.
"""

BOOTSTRAP_EXTRA_TIME_CAPTION = """
\\textbf{Bootstrap confidence intervals (CI) for cookie banner response time on different devices}.
The CI's not containing 0 rejects the null hypothesis, and are marked in \\textbf{bold}.
The bootstrap used 10000 iterations.
"""

FRIEDMAN_CAPTION = """
\\textbf{Friedman tests on consent accepts and banner answer time on the different websites are highly significant}.
All of the tests have very low p-values, indicating that the null hypothesis stating that the websites have the
same expected cookie consent acceptance rate and cookie banner answer time can safely be rejected.
"""
