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

A person changed the way of moving. Variance is expected to increase when motion becomes more dynamic (for example walking → running). Seasonality (gait periodicity) is visible. These recordings were collected on a **straight road**.

Labeled activity intervals are in `documentation/events.csv`:

- **01** — person; G-Force Meter; one observer-declared break associated with a gait change (walking to running).
- **02** — rotation, then walking, then running; G-Force Meter and gyroscope.
- **03** — walking / running / walking; G-Force Meter and gyroscope. Imported from Excel.
- **04** — walking / running / walking / running / walking; G-Force Meter and linear accelerometer.

### Vehicles (measurements 05–09)

A motorbike or car travelled on a route with **cobblestone (sett)** and **asphalt** segments. Oscillations are typically larger on stone / cobblestone than on asphalt.

Motorbike recordings (05–07): the labeled states *driving along a stone route* and *driving along an asphalt route* include **straight segments**. *Exiting the car park*, *return to the car park*, and the *U-turn maneuver* are **not** straight.

Car recordings (08–09): the route was **irregular** (turns, roundabout driving, and similar manoeuvres). Those geometric features were **not logged** during the measurement. **Car speed was not recorded.**

Approximate motorbike speeds. The **first half of the route** is the first asphalt segment plus the first stone segment; the **second half** is the asphalt segment and the stone segment after the U-turn:

- **05** motorbike — first half 50 km/h, second half 80 km/h.
- **06** motorbike — first half 60 km/h, second half 60 km/h.
- **07** motorbike — first half 50 km/h, second half 50 km/h.
- **08** car — surface change; G-Force Meter only; speed not recorded.
- **09** car — surface change; G-Force Meter and gyroscope; speed not recorded.

Collection dates from original folder names: 2021-09-04 (05–08) and 2021-09-07 (09).

## Observer-declared structural breaks

During each recording an observer noted when the character of the vibrations changed. Those times are treated as **theoretical change points**, with a reaction-time error. The paper therefore reports an **interval** that contains the break. The theoretical point used in the article is the **median (midpoint) of the interval**.

The marked / observer-declared breaks concern **scale (variance) changes only**, not changes in the mean level of the signal.

Intervals are stored in `documentation/change_points.csv` and in `measurements_catalog.csv`. They come from Table 2 of the paper, not from an automatic detector.

Note on measurement 08: the paper table lists `regime number = 3` and **three** intervals `[103,104]`, `[197,199]`, `[279,281]`. This release keeps both the reported regime count and all three intervals so users can reproduce the table as printed.

## Labeled activity events

Each recording also has labeled activity intervals (`start`, `stop`, `name`) in elapsed seconds. They describe gait or road-surface states (and, for the motorbike, car-park and U-turn segments). The list is stored in `documentation/events.csv` and in `metadata.events` of each `measurement_XX.json`. Some event boundaries coincide with theoretical change points; the event catalog is not limited to Table 2.

## Sampling and duplicate timestamps

The app’s nominal maximum rate is 100 Hz per sensor. When two sensors are logged together, Physics Toolbox often **interleaves** samples. That produces:

- duplicate or tied `time_s` values,
- a higher *row* rate than 100 Hz (sometimes ~200–500 rows/s if `median(Δt)` is used naively).

This release **does not resample**. Duplicate timestamps are a property of the original export and are documented per file (`n_duplicate_times` in the catalog).

## Missing values

- No numeric field is missing in the processed sensor columns (`n_missing_cells = 0`).
- A missing sensor is represented by **omitted columns**, not by `NA`, `NaN`, `-999`, or `.`.
- If a future version introduced missing numbers, they would be empty CSV fields / JSON `null`.

## Personal data

No names of people, contact details, or GPS coordinates are present. Approximate motorbike speeds are retained in the README and in this documentation. Car speed was not recorded.

## Processing pipeline

See also the generated `processing_log.md` (file-level checksums and row counts).

1. Read each original Physics Toolbox export (CSV or Excel). Original filenames are not published.
2. Detect encoding: UTF-8, UTF-8 BOM, or Windows-1250 (`cp1250`). Excel is read via `openpyxl`.
3. Coerce remaining columns to numeric values. Fail if any cell is non-numeric.
4. Rename columns to the stable names in `column_mapping.csv`.
5. Write UTF-8 processed files: comma-separated CSV, JSON, and a combined XLSX workbook.
6. No interpolation, filtering, detrending, outlier removal, or unit conversion beyond renaming.

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
