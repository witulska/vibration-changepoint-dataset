# Vibration measurements with observer-declared variance change points

**Version 1.0.0** · **2026-09-19** · **License: [CC BY 4.0](LICENSE)**

Nine motion-sensor time series recorded with a smartphone, intended for methods that detect **structural breaks in variance**. A person, a motorbike, and a car were measured with a G-Force Meter, a gyroscope, and/or a linear accelerometer. An observer marked the times when the character of the vibrations changed; those intervals (and their midpoints) are published with the data.

These are the vibration recordings analysed in:

> Witulska, J., & Wyłomańska, A. (2022). Identification of the structure break point for data with changing variance. *Mathematica Applicanda*, 50(1), 65–106. https://doi.org/10.14708/ma.v50i1.7155

## Metadata

| Field | Value |
|---|---|
| Title | Vibration measurements with observer-declared variance change points |
| Author | Justyna Witulska |
| Affiliation | Faculty of Pure and Applied Mathematics, Hugo Steinhaus Center, Wrocław University of Science and Technology, Wybrzeże Wyspiańskiego 27, 50-370 Wrocław, Poland |
| Contact | justyna.witulska@pwr.edu.pl |
| Description | Vibration time series with observer-declared variance-change intervals, from smartphone inertial sensors |
| Keywords | change-point detection; variance change; structural break; vibration; smartphone sensors; accelerometer; gyroscope; G-Force Meter; Physics Toolbox Sensor Suite |
| Publication date | 2026-09-19 |
| Version | 1.0.0 |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Acquisition | Physics Toolbox Sensor Suite on Android; three-axis G-Force Meter (±4 g, ≤100 Hz), linear accelerometer (≤100 Hz), gyroscope (±17.45 rad/s, ≤100 Hz) |
| Temporal coverage | Experiments on 2021-09-03, 2021-09-04, and 2021-09-07. The `time_s` column is elapsed seconds from the start of each recording, not calendar time. |
| Sources | Original Physics Toolbox CSV/XLSX exports; Table 2 of Witulska & Wyłomańska (2022) for observer intervals |
| DOI | Version-specific DOI is minted by depositing a GitHub **release** on [Zenodo](https://zenodo.org) (see below). Do not cite a floating repository URL as if it were a versioned dataset. |

Machine-readable copies: `CITATION.cff`, `.zenodo.json`, `metadata/metadata.json`.

## Repository layout

```
dataset/
├── data/
│   └── processed/           # CSV, JSON, XLSX with stable column names
├── figures/                 # one PNG per measurement (subplots of all channels)
├── scripts/
│   ├── process_dataset.py   # original exports → processed (re-runnable)
│   └── plot_measurements.py # time-series figures with observer change points
├── documentation/
│   ├── data_dictionary.csv  # every column: type, unit, allowed values
│   ├── data_dictionary.md
│   ├── methods.md           # collection + processing
│   ├── processing_log.md    # per-file operations and checksums
│   ├── measurements_catalog.csv
│   ├── change_points.csv
│   ├── events.csv
│   └── column_mapping.csv
├── metadata/
├── README.md
├── LICENSE
└── CITATION.cff
```

## What is in the data

| id | subject | factor | sensors (processed file) | duration in paper (s) | observer intervals (s) | theoretical points (s) | rows |
|---:|---|---|---|---:|---|---|---:|
| 01 | person | gait / motion change | G-Force | 83.74 | [66, 68] | 67.0 | 8157 |
| 02 | person | gait / motion change | G-Force, gyroscope | 77.72 | [43, 44] | 43.5 | 15496 |
| 03 | person | gait / motion change | G-Force, gyroscope | 201.53 | [72, 74], [132, 134] | 73.0; 133.0 | 40202 |
| 04 | person | gait / motion change | G-Force, linear accelerometer | 181.88 | [48, 50], [79, 81], [109, 111], [139, 141] | 49; 80; 110; 140 | 36146 |
| 05 | motorbike | surface change | G-Force, gyroscope | 265.49 | [85, 87], [214, 216] | 86.0; 215.0 | 52918 |
| 06 | motorbike | surface change | G-Force | 233.66 | [49, 51], [179, 181] | 50.0; 180.0 | 23231 |
| 07 | motorbike | surface change | G-Force, gyroscope | 274.62 | [56, 58], [211, 213] | 57.0; 212.0 | 54554 |
| 08 | car | surface change | G-Force | 344.88 | [103, 104], [197, 199], [279, 281] | 103.5; 198.0; 280.0 | 86024 |
| 09 | car | surface change | G-Force, gyroscope | 176.55 | [91, 93], [149, 151] | 92.0; 150.0 | 35172 |

Total processed samples: **351 900**.

- Person recordings: walking / running. Variance is typically larger when motion is more dynamic. Gait periodicity is visible.
- Vehicle recordings: cobblestone (sett) versus asphalt. Oscillations are typically larger on stone than on asphalt.
- Measurement **03** was imported from Excel (walking / running / walking).
- Measurement **08**: the paper table reports 3 regimes and lists three intervals; both facts are kept as printed.

Observer intervals account for reaction time. The paper takes the **midpoint of each interval** as the theoretical change point (`documentation/change_points.csv`). The marked / observer-declared breaks concern **scale (variance) changes only**, not changes in the mean level of the signal.

Labeled activity intervals (`start`, `stop`, `name`, elapsed seconds) are stored in each processed JSON file under `metadata.events` and in `documentation/events.csv`. Some event boundaries coincide with theoretical change points; the event list is a richer description of the route and is not limited to the paper’s Table 2 breaks.

### Route geometry and speed

- Person recordings (01–04) were collected on a **straight road**.
- Motorbike recordings (05–07): the states *driving along a stone route* and *driving along an asphalt route* include **straight segments**. *Exiting the car park*, *return to the car park*, and the *U-turn maneuver* are **not** straight.
- Car recordings (08–09): the route was **irregular** (turns, roundabout driving, and similar manoeuvres). Those geometric features were **not logged** during the measurement. **Car speed was not recorded.**

Approximate motorbike speeds. The **first half of the route** is the first asphalt segment plus the first stone segment; the **second half** is the asphalt segment and the stone segment after the U-turn:

| id | first half of the route | second half of the route |
|---:|---|---|
| 05 | 50 km/h | 80 km/h |
| 06 | 60 km/h | 60 km/h |
| 07 | 50 km/h | 50 km/h |

There is **no unnecessary personal data**: no names, IDs, GPS, audio, or video.

## Column names and units

Processed files use stable names. Original Physics Toolbox names are listed in `documentation/column_mapping.csv`.

| processed | original | unit |
|---|---|---|
| `time_s` | `time` | seconds from recording start |
| `gforce_x`, `gforce_y`, `gforce_z` | `gFx`, `gFy`, `gFz` | g (standard gravity) |
| `ang_vel_x`, `ang_vel_y`, `ang_vel_z` | `wx`, `wy`, `wz` | rad/s |
| `lin_acc_x`, `lin_acc_y`, `lin_acc_z` | `ax`, `ay`, `az` | m/s² (measurement 04 only) |

If a sensor was not recorded, its columns are **absent**, not filled with a code. There are **no missing numeric cells** in this release. Empty CSV fields / JSON `null` would be the missing-value code if they appeared later.

Duplicate timestamps occur when two sensors are interleaved by the app. They are kept. Do not treat `1 / median(Δt)` as the physical sampling rate of a single sensor (nominal maximum 100 Hz per sensor).

Full dictionary: [`documentation/data_dictionary.csv`](documentation/data_dictionary.csv). Methods: [`documentation/methods.md`](documentation/methods.md). Operations actually applied: [`documentation/processing_log.md`](documentation/processing_log.md).

## How to load a recording

```python
import pandas as pd

df = pd.read_csv("data/processed/measurement_03.csv")
breaks = pd.read_csv("documentation/change_points.csv")
events = pd.read_csv("documentation/events.csv")
breaks_03 = breaks.query("measurement_id == 3")
events_03 = events.query("measurement_id == 3")
print(df.columns.tolist(), df["time_s"].iloc[[0, -1]].tolist())
print(breaks_03[["interval_start_s", "interval_end_s", "theoretical_change_point_s"]])
print(events_03[["start_s", "stop_s", "name"]])
```

CSV is the canonical format. JSON and `data/processed/measurements.xlsx` contain the same samples.

## Figures

Each recording has a PNG in `figures/` with one subplot per channel (shared time axis). Yellow bands are observer-declared break intervals; dashed red lines are the theoretical change points (interval midpoints).

```bash
python scripts/plot_measurements.py
```

## How to cite

**Dataset** (after the Zenodo DOI exists — replace the placeholder):

Witulska, J., & Wyłomańska, A. (2026). *Vibration measurements with observer-declared variance change points* (Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

**Related article** (always cite with the dataset):

Witulska, J., & Wyłomańska, A. (2022). Identification of the structure break point for data with changing variance. *Mathematica Applicanda*, 50(1), 65–106. https://doi.org/10.14708/ma.v50i1.7155

BibTeX for the article:

```bibtex
@article{witulska2022identification,
  title   = {Identification of the structure break point for data with changing variance},
  author  = {Witulska, Justyna and Wy{\l}oma{\'n}ska, Agnieszka},
  journal = {Mathematica Applicanda},
  volume  = {50},
  number  = {1},
  pages   = {65--106},
  year    = {2022},
  doi     = {10.14708/ma.v50i1.7155}
}
```

BibTeX for the dataset (fill in the Zenodo DOI after the first release):

```bibtex
@misc{witulska2026vibration,
  title        = {Vibration measurements with observer-declared variance change points},
  author       = {Witulska, Justyna},
  year         = {2026},
  note         = {Version 1.0.0 [Data set]},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX}
}
```

In the article, cite the dataset like any other scholarly source (dataset → repository → DOI → version → documentation → paper), not as an informal spreadsheet link.
