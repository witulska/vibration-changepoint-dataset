# Smartphone vibration measurements with observer-declared variance change points

**Version 1.0.0** · **2026-09-19** · **License: [CC BY 4.0](LICENSE)**

Nine motion-sensor time series recorded with a smartphone, intended for methods that detect **structural breaks in variance**. A person, a motorbike, and a car were measured with a G-Force Meter, a gyroscope, and/or a linear accelerometer. An observer marked the times when the character of the vibrations changed; those intervals (and their midpoints) are published with the data.

These are the vibration recordings analysed in:

> Witulska, J., & Wyłomańska, A. (2022). Identification of the structure break point for data with changing variance. *Mathematica Applicanda*, 50(1), 65–106. https://doi.org/10.14708/ma.v50i1.7155

Polish summary: dziewięć pomiarów drgań ze smartfona (osoba / motocykl / samochód). W plikach usunięto komentarze i kolumnę `TgF`. Pomiar nr 3 pochodzi z `pomiar_nr3.xlsx`. Słownik kolumn, metoda zbierania i log czyszczenia są w `documentation/`.

## Metadata

| Field | Value |
|---|---|
| Title | Smartphone vibration measurements with observer-declared variance change points |
| Authors | Justyna Witulska; Agnieszka Wyłomańska |
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
│   ├── raw/                 # archived exports (original column names; comments removed)
│   └── processed/           # CSV, TSV, JSON, XLSX with stable column names
├── scripts/
│   └── process_dataset.py   # raw → processed (re-runnable)
├── documentation/
│   ├── data_dictionary.csv  # every column: type, unit, allowed values
│   ├── data_dictionary.md
│   ├── methods.md           # collection + processing
│   ├── processing_log.md    # per-file operations and checksums
│   ├── measurements_catalog.csv
│   ├── change_points.csv
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

- Person recordings: walking / running / jumping. Variance is typically larger when motion is more dynamic. Gait periodicity is visible.
- Vehicle recordings: cobblestone (sett) versus asphalt. Oscillations are typically larger on stone than on asphalt.
- Measurement **03** was archived from Excel (`pomiar_nr3.xlsx`, sheet `chodzenie-bieganie-chodzenie`).
- Measurement **08**: the paper table reports 3 regimes and lists three intervals; both facts are kept as printed.

Observer intervals account for reaction time. The paper takes the **midpoint of each interval** as the theoretical change point (`documentation/change_points.csv`).

There is **no unnecessary personal data**: no names, IDs, GPS, audio, or video. Trailing CSV comments that named incidental landmarks were deleted; approximate speeds are described only in `documentation/methods.md`.

## Column names and units

Processed files use stable names. Physics Toolbox names remain in `data/raw/` and in `documentation/column_mapping.csv`.

| processed | original | unit |
|---|---|---|
| `time_s` | `time` | seconds from recording start |
| `gforce_x`, `gforce_y`, `gforce_z` | `gFx`, `gFy`, `gFz` | g (standard gravity) |
| `ang_vel_x`, `ang_vel_y`, `ang_vel_z` | `wx`, `wy`, `wz` | rad/s |
| `lin_acc_x`, `lin_acc_y`, `lin_acc_z` | `ax`, `ay`, `az` | m/s² (measurement 04 only) |

`TgF` (total g-force) was **dropped** from processed files when present (measurements 01, 06, 08). It is still in the matching archived raw CSVs.

If a sensor was not recorded, its columns are **absent**, not filled with a code. There are **no missing numeric cells** in this release. Empty CSV fields / JSON `null` would be the missing-value code if they appeared later.

Duplicate timestamps occur when two sensors are interleaved by the app. They are kept. Do not treat `1 / median(Δt)` as the physical sampling rate of a single sensor (nominal maximum 100 Hz per sensor).

Full dictionary: [`documentation/data_dictionary.csv`](documentation/data_dictionary.csv). Methods: [`documentation/methods.md`](documentation/methods.md). Operations actually applied: [`documentation/processing_log.md`](documentation/processing_log.md).

## How to load a recording

```python
import pandas as pd

df = pd.read_csv("data/processed/measurement_03.csv")
breaks = pd.read_csv("documentation/change_points.csv")
breaks_03 = breaks.query("measurement_id == 3")
print(df.columns.tolist(), df["time_s"].iloc[[0, -1]].tolist())
print(breaks_03[["interval_start_s", "interval_end_s", "theoretical_change_point_s"]])
```

CSV is the canonical processed format. TSV, JSON, and `data/processed/measurements.xlsx` contain the same samples.

To regenerate processed files from the archived sources:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/process_dataset.py --source data/raw
```

SHA-256 checksums: `data/processed/checksums.sha256`.

## How to cite

**Dataset** (after the Zenodo DOI exists — replace the placeholder):

Witulska, J., & Wyłomańska, A. (2026). *Smartphone vibration measurements with observer-declared variance change points* (Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

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
  title        = {Smartphone vibration measurements with observer-declared variance change points},
  author       = {Witulska, Justyna and Wy{\l}oma{\'n}ska, Agnieszka},
  year         = {2026},
  note         = {Version 1.0.0 [Data set]},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX}
}
```

In the article, cite the dataset like any other scholarly source (dataset → repository → DOI → version → documentation → paper), not as an informal spreadsheet link.

## DOI via Zenodo (versioned)

A GitHub URL is not a DOI. Zenodo issues a **DOI for a specific version** (a GitHub release). Later substantial changes should be a new version; previous versions remain citable.

1. Push this repository to GitHub (public).
2. Sign in at [https://zenodo.org](https://zenodo.org) with the same GitHub account (or enable GitHub in Zenodo settings).
3. In Zenodo: *GitHub* → enable this repository.
4. On GitHub: *Releases* → create tag **`v1.0.0`** (matches `CITATION.cff`).
5. Zenodo archives that release and shows a DOI such as `10.5281/zenodo.1234567`.
6. Put that DOI into `CITATION.cff` (`identifiers`) and into the citation block above, then tag **`v1.0.1`** only if you need the metadata files themselves to contain the DOI.

`.zenodo.json` supplies title, authors, license, keywords, and the related-article DOI `10.14708/ma.v50i1.7155`.
