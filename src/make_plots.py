import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from src.get_constants import get_constants

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]


def plot_response_times_per_device(df, device, max_time=31, time_scale_factor=1.0, show=False):
    """
    Plot response times per website and device, colored by response type.

    Args:
        df (pd.DataFrame): DataFrame containing the time and response data.
        device (str): "computer" or "phone".
        max_time (int): The highest amount of response time that will be shown in the plot.
        time_scale_factor (float): Optional scaling of x-axis (default 1.0 = seconds).
        show (bool): Whether or not to show the plot.
    """
    if device not in ["computer", "phone"]:
        raise ValueError("Device must be 'computer' or 'phone'.")

    # Prepare column names based on device
    time_columns = {website: f"{device}.{website}.time" for website in WEBSITES}
    accept_columns = {website: f"{device}.{website}.answer.int" for website in WEBSITES}

    _, ax = plt.subplots(figsize=(12, 6))
    y_positions = {site: idx for idx, site in enumerate(WEBSITES)}
    colors = {1: "tab:blue", 0: "tab:red"}  # 1 = Accept, 0 = Reject

    # Add the average markers
    for idx, website in enumerate(WEBSITES):
        for response, color in zip([0, 1], ["red", "blue"]):  # 0 = reject, 1 = accept
            subset = df[df[f"{device}.{website}.answer.int"] == response]
            mean_time = subset[f"{device}.{website}.time"].mean()
            if not np.isnan(mean_time):
                ax.scatter(mean_time, idx, color=color, marker="*", s=200, edgecolor="black", zorder=3)

    # Add the individual times
    for site in WEBSITES:
        y = y_positions[site]

        times = df[time_columns[site]]
        accepts = df[accept_columns[site]]

        # Draw the website line
        ax.hlines(y, xmin=0, xmax=max_time * 1.05, color="gray", alpha=0.5, linestyle="--")

        for t, a in zip(times, accepts):
            t = np.min([t, max_time])
            color = colors.get(int(a), "gray")
            ax.plot(t * time_scale_factor, y + np.random.normal(0, 0.08), 'o', color=color, markersize=6, alpha=0.8)

    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(WEBSITES)
    ax.set_xlabel("Response Time (seconds)" if time_scale_factor == 1.0 else "Response Time (scaled)")
    ax.set_ylabel("Website")
    ax.set_title(f"Response Times by Website and Response Type ({device.capitalize()})")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)

    # Manual legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label="accept", markerfacecolor='tab:blue', markersize=8),
        Line2D([0], [0], marker='o', color='w', label="reject", markerfacecolor='tab:red', markersize=8),
    ]
    ax.legend(handles=legend_elements, title="Response Type", loc="lower right")

    plt.tight_layout()

    # Save the plot to file
    plots_folder_path = Path(CONSTANTS["paths"]["folders"]["plots_folder"])
    file_path = plots_folder_path / CONSTANTS["paths"]["filenames"][f"answer_times_line_plot_{device}"]
    if not os.path.exists(plots_folder_path):
        os.makedirs(plots_folder_path)
    plt.savefig(file_path)

    if show:
        plt.show()
