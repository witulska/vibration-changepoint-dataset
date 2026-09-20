#!/usr/bin/env python3
"""Plot each processed measurement as a stack of time-series subplots.

Observer-declared break intervals are shaded; theoretical change points
(interval midpoints from Witulska & Wyłomańska, 2022) are dashed lines.

Example:
    python scripts/plot_measurements.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
DOC_DIR = ROOT / "documentation"
FIGURES_DIR = ROOT / "figures"

COLUMN_ORDER = [
    "gforce_x",
    "gforce_y",
    "gforce_z",
    "ang_vel_x",
    "ang_vel_y",
    "ang_vel_z",
    "lin_acc_x",
    "lin_acc_y",
    "lin_acc_z",
]

COLUMN_LABELS = {
    "gforce_x": "G-force, X axis (g)",
    "gforce_y": "G-force, Y axis (g)",
    "gforce_z": "G-force, Z axis (g)",
    "ang_vel_x": "Angular velocity, X axis (rad/s)",
    "ang_vel_y": "Angular velocity, Y axis (rad/s)",
    "ang_vel_z": "Angular velocity, Z axis (rad/s)",
    "lin_acc_x": "Linear acceleration, X axis (m/s²)",
    "lin_acc_y": "Linear acceleration, Y axis (m/s²)",
    "lin_acc_z": "Linear acceleration, Z axis (m/s²)",
}

SUBJECT_LABELS = {
    "person": "person",
    "motorbike": "motorbike",
    "car": "car",
}

FACTOR_LABELS = {
    "dynamic_of_motion_change": "change in motion dynamics",
    "surface_change": "road-surface change",
}

LINE_COLOR = "#1f4e79"
INTERVAL_COLOR = "#f4c430"
CHANGEPOINT_COLOR = "#c0392b"


def load_catalog() -> pd.DataFrame:
    return pd.read_csv(DOC_DIR / "measurements_catalog.csv")


def load_change_points() -> pd.DataFrame:
    return pd.read_csv(DOC_DIR / "change_points.csv")


def plot_measurement(row: pd.Series, breaks: pd.DataFrame, out_dir: Path) -> Path:
    measurement_id = int(row["measurement_id"])
    csv_path = PROCESSED_DIR / row["processed_csv"]
    data = pd.read_csv(csv_path)
    signal_cols = [c for c in COLUMN_ORDER if c in data.columns]
    n = len(signal_cols)
    fig_h = max(2.2 * n, 6.0)
    fig, axes = plt.subplots(
        n,
        1,
        sharex=True,
        figsize=(11.5, fig_h),
        constrained_layout=True,
    )
    if n == 1:
        axes = [axes]

    subject = SUBJECT_LABELS.get(row["subject"], row["subject"])
    factor = FACTOR_LABELS.get(row["variance_change_factor"], row["variance_change_factor"])
    fig.suptitle(
        f"Measurement {measurement_id:02d}: {subject}, {factor}",
        fontsize=13,
        fontweight="bold",
    )

    time = data["time_s"]
    first_ax = axes[0]
    for ax, col in zip(axes, signal_cols):
        ax.plot(time, data[col], color=LINE_COLOR, linewidth=0.45, rasterized=True)
        ax.set_ylabel(COLUMN_LABELS[col], fontsize=9)
        ax.grid(True, alpha=0.35, linewidth=0.6)
        ax.tick_params(labelsize=8)

        for i, br in enumerate(breaks.itertuples(index=False)):
            interval_label = "Observer-declared interval" if i == 0 else None
            point_label = "Theoretical change point" if i == 0 else None
            ax.axvspan(
                br.interval_start_s,
                br.interval_end_s,
                color=INTERVAL_COLOR,
                alpha=0.35,
                zorder=0,
                label=interval_label,
            )
            ax.axvline(
                br.theoretical_change_point_s,
                color=CHANGEPOINT_COLOR,
                linestyle="--",
                linewidth=1.1,
                zorder=3,
                label=point_label,
            )

    axes[-1].set_xlabel("Time (s)", fontsize=10)
    handles, labels = first_ax.get_legend_handles_labels()
    if handles:
        first_ax.legend(handles, labels, loc="upper right", fontsize=8, framealpha=0.92)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"measurement_{measurement_id:02d}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=FIGURES_DIR,
        help="Directory for PNG figures (default: figures/)",
    )
    args = parser.parse_args()

    catalog = load_catalog()
    change_points = load_change_points()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )

    written = []
    for _, row in catalog.iterrows():
        breaks = change_points[change_points["measurement_id"] == int(row["measurement_id"])]
        path = plot_measurement(row, breaks, args.output_dir)
        written.append(path)
        print(path.relative_to(ROOT))

    print(f"Wrote {len(written)} figures to {args.output_dir}")


if __name__ == "__main__":
    main()
