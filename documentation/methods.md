# Data collection and processing

## Related publication

These recordings are the vibration measurements analysed in:

Witulska, J., & Wyłomańska, A. (2022). Identification of the structure break point for data with changing variance. *Mathematica Applicanda*, 50(1), 65–106. https://doi.org/10.14708/ma.v50i1.7155

Cite both the article and this dataset (see `CITATION.cff` and the README).

## What was measured

Nine time series of oscillation / vibration recorded with a smartphone running **Physics Toolbox Sensor Suite** (Android). Each recording uses one or more of:

| Sensor | Range (paper) | Maximum sampling frequency (paper) | Original columns |
|---|---|---|---|
| G-Force Meter | ±4 g | 100 Hz | `gFx`, `gFy`, `gFz` (processed: `gforce_x/y/z`) |
| Linear Accelerometer | not stated | 100 Hz | `ax`, `ay`, `az` (processed: `lin_acc_x/y/z`) |
| Gyroscope | ±17.45 rad/s | 100 Hz | `wx`, `wy`, `wz` (processed: `ang_vel_x/y/z`) |

All channels are recorded separately on three device axes. Time is elapsed seconds from the start of the recording (`time` → `time_s`). There is **no calendar datetime** in the files.

The data are **not** medical records, survey responses, or identified personal profiles. They are anonymous motion-sensor streams. No participant names, IDs, GPS tracks, audio, or video are included.

## Experimental design

Two settings were used to induce a change in variance, following the paper.

### Person (measurements 01–04), 2021-09-03

A person changed the way of moving. Variance is expected to increase when motion becomes more dynamic (for example walking → running). Seasonality (gait periodicity) is visible.

Protocol recovered from original export comments / sheet names (comments themselves are not in the published files):

- **01** — person; G-Force Meter; one observer-declared break associated with a gait change (walking to running).
- **02** — rotation, then about 30 s walking, then about 30 s running; G-Force Meter and gyroscope.
- **03** — walking / running / walking (original Excel sheet name `chodzenie-bieganie-chodzenie`); G-Force Meter and gyroscope. Source file: `pomiar_nr3.xlsx`.
- **04** — rotation, then about 30 s walking, 30 s running, 30 s walking, 30 s jumping, 30 s walking; G-Force Meter and linear accelerometer.

### Vehicles (measurements 05–09)

A motorbike or car travelled on a route with **cobblestone (sett)** and **asphalt** segments. Oscillations are typically larger on stone / cobblestone than on asphalt.

Approximate speeds from observer notes (notes removed from files; place names not published):

- **05** motorbike — first half of the route ~50 km/h, second half ~80 km/h.
- **06** motorbike — ~60 km/h throughout.
- **07** motorbike — ~50 km/h throughout.
- **08** car — surface change; G-Force Meter only.
- **09** car — surface change; G-Force Meter and gyroscope.

Collection dates from original folder names: 2021-09-04 (05–08) and 2021-09-07 (09).

## Observer-declared structural breaks

During each recording an observer noted when the character of the vibrations changed. Those times are treated as **theoretical change points**, with a reaction-time error. The paper therefore reports an **interval** that contains the break. The theoretical point used in the article is the **median (midpoint) of the interval**.

Intervals are stored in `documentation/change_points.csv` and in `measurements_catalog.csv`. They come from Table 2 of the paper, not from an automatic detector.

Note on measurement 08: the paper table lists `regime number = 3` and **three** intervals `[103,104]`, `[197,199]`, `[279,281]`. This release keeps both the reported regime count and all three intervals so users can reproduce the table as printed.

## Sampling and duplicate timestamps

The app’s nominal maximum rate is 100 Hz per sensor. When two sensors are logged together, Physics Toolbox often **interleaves** samples. That produces:

- duplicate or tied `time_s` values,
- a higher *row* rate than 100 Hz (sometimes ~200–500 rows/s if `median(Δt)` is used naively).

This release **does not resample**. Duplicate timestamps are a property of the original export and are documented per file (`n_duplicate_times` in the catalog).

## Missing values

- No numeric field is missing in the processed sensor columns (`n_missing_cells = 0`).
- A missing sensor is represented by **omitted columns**, not by `NA`, `NaN`, `-999`, or `.`.
- If a future version introduced missing numbers, they would be empty CSV fields / JSON `null`.

## Personal data and redaction

Removed before publication:

- Free-text observer notes in trailing CSV columns (vehicle recordings 05–07), which mentioned incidental local landmarks and approximate speed.
- Comment header rows with protocol text (recordings 02 and 04); the protocol is summarized above without copying the raw comment string into the data files.
- Excel workbook metadata that stored a local Windows filesystem path (recording 03).

No names of people, contact details, or GPS coordinates are present. Approximate vehicle speeds are retained only in this documentation.

## Processing pipeline (raw → processed)

See also the generated `processing_log.md` (file-level checksums and row counts).

1. Read each source file (`pomiar_nr1.csv` … `pomiar_nr9.csv`, and `pomiar_nr3.xlsx`).
2. Detect encoding: UTF-8, UTF-8 BOM, or Windows-1250 (`cp1250`). Excel is read via `openpyxl`.
3. Drop comment headers and unnamed trailing comment columns.
4. Coerce remaining columns to numeric values. Fail if any cell is non-numeric.
5. Write `data/raw/` archives with **original Physics Toolbox names**, semicolon-separated CSV (or a cleaned XLSX sheet), **including `TgF` when it existed**. This is the archived source after redaction, not a bit-identical app dump.
6. Drop `TgF` if present.
7. Rename columns to the stable names in `column_mapping.csv`.
8. Write UTF-8 processed files: comma-separated CSV, TSV, JSON, and a combined XLSX workbook.
9. No interpolation, filtering, detrending, outlier removal, or unit conversion beyond renaming.

Reproduce:

```bash
python scripts/process_dataset.py --source /path/to/original_exports
```

## Units and formats

| quantity | format |
|---|---|
| time | floating-point seconds, decimal point `.` |
| g-force | multiples of standard gravity `g` |
| angular velocity | rad/s |
| linear acceleration | m/s² (Physics Toolbox linear accelerometer) |
| dates in catalogs | ISO 8601 `YYYY-MM-DD` |
| CSV | UTF-8, comma, Unix newlines, header row |
| TSV | UTF-8, tab, Unix newlines |
| JSON | UTF-8, wrapper object with `records` array |

## File inventory

| id | subject | sensors in processed file | paper total time (s) | declared intervals (s) |
|---:|---|---|---:|---|
| 01 | person | G-Force | 83.74 | [66, 68] |
| 02 | person | G-Force, gyroscope | 77.72 | [43, 44] |
| 03 | person | G-Force, gyroscope | 201.53 | [72, 74], [132, 134] |
| 04 | person | G-Force, linear accelerometer | 181.88 | [48, 50], [79, 81], [109, 111], [139, 141] |
| 05 | motorbike | G-Force, gyroscope | 265.49 | [85, 87], [214, 216] |
| 06 | motorbike | G-Force | 233.66 | [49, 51], [179, 181] |
| 07 | motorbike | G-Force, gyroscope | 274.62 | [56, 58], [211, 213] |
| 08 | car | G-Force | 344.88 | [103, 104], [197, 199], [279, 281] |
| 09 | car | G-Force, gyroscope | 176.55 | [91, 93], [149, 151] |
