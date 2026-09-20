# Data dictionary

This dictionary describes processed files in `data/processed/measurement_XX.csv` (and the matching JSON/XLSX sheets). Source Physics Toolbox names are in `column_mapping.csv`.

Missing numeric values do not occur in this release. If a sensor was not recorded for a measurement, **the corresponding columns are omitted** rather than filled with a sentinel. Empty fields would be the missing-value code if they appeared.

Time is elapsed seconds from the start of each recording. It is **not** a calendar timestamp.

## Columns that may appear in a measurement file

| column_name | data_type | unit | allowed_values | sensor | description |
|---|---|---|---|---|---|
| time_s | float64 | s | ≥ 0, increasing except for duplicate timestamps from interleaved sensors | — | Time from the start of the recording. Physics Toolbox original name: `time`. |
| gforce_x | float64 | g (standard gravity, 9.81 m/s²) | typically within about ±4 g (device range in the paper) | G-Force Meter | Acceleration including gravity, device X axis. Original name: `gFx`. |
| gforce_y | float64 | g | typically within about ±4 g | G-Force Meter | Acceleration including gravity, device Y axis. Original name: `gFy`. |
| gforce_z | float64 | g | typically within about ±4 g | G-Force Meter | Acceleration including gravity, device Z axis. Original name: `gFz`. |
| ang_vel_x | float64 | rad/s | typically within ±17.45 rad/s (device range in the paper) | Gyroscope | Angular velocity, device X axis. Original name: `wx`. |
| ang_vel_y | float64 | rad/s | typically within ±17.45 rad/s | Gyroscope | Angular velocity, device Y axis. Original name: `wy`. |
| ang_vel_z | float64 | rad/s | typically within ±17.45 rad/s | Gyroscope | Angular velocity, device Z axis. Original name: `wz`. |
| lin_acc_x | float64 | m/s² | unconstrained beyond device limits | Linear Accelerometer | Linear acceleration with gravity removed, device X axis. Original name: `ax`. Present only in measurement 04. |
| lin_acc_y | float64 | m/s² | unconstrained beyond device limits | Linear Accelerometer | Linear acceleration with gravity removed, device Y axis. Original name: `ay`. Present only in measurement 04. |
| lin_acc_z | float64 | m/s² | unconstrained beyond device limits | Linear Accelerometer | Linear acceleration with gravity removed, device Z axis. Original name: `az`. Present only in measurement 04. |

## Catalog files

### `measurements_catalog.csv`

One row per recording.

| column_name | data_type | description |
|---|---|---|
| measurement_id | integer | Identifier 1–9, matching Table 2 in Witulska & Wyłomańska (2022). |
| processed_csv | string | Processed CSV filename. |
| subject | string | `person`, `motorbike`, or `car`. |
| collection_date | date (YYYY-MM-DD) | Calendar date of the experiment, from original folder names. |
| variance_change_factor | string | `dynamic_of_motion_change` or `surface_change`. |
| n_regimes_reported | integer | Number of regimes reported in the paper table. |
| n_declared_breaks | integer | Number of observer intervals listed in the paper table. |
| declared_break_intervals_s | string | Observer intervals in seconds, semicolon-separated, e.g. `[72,74];[132,134]`. |
| theoretical_change_points_s | string | Interval midpoints (medians) in seconds, used in the paper as theoretical change points. |
| sensors_reported_in_paper | string | Sensors listed for that row of Table 2. |
| sensors_present | string | Sensors actually present in the processed file. |
| n_rows | integer | Number of samples. |
| n_unique_times | integer | Number of distinct `time_s` values. |
| n_duplicate_times | integer | Extra rows sharing a timestamp (interleaved multi-sensor logging). |
| time_start_s | float | First timestamp (s). |
| time_end_s | float | Last timestamp (s); matches the paper “total time of measurement” to two decimals. |
| duration_s | float | `time_end_s - time_start_s`. |
| paper_total_time_s | float | Total time as printed in the paper. |
| n_missing_cells | integer | Count of NA cells; 0 in this release. |
| columns | string | Ordered processed column names. |
| sha256_csv | string | SHA-256 of the processed CSV. |

### `events.csv`

One row per labeled activity interval. Times are elapsed seconds from the start of the recording. These labels describe what was happening on the route; they are not the same object as the observer-declared variance-change intervals.

| column_name | data_type | unit | description |
|---|---|---|---|
| measurement_id | integer | — | Recording identifier. |
| event_index | integer | — | Order of the event in that recording (1-based). |
| start_s | float | s | Inclusive start of the labeled interval. |
| stop_s | float | s | End of the labeled interval. |
| name | string | — | Activity or road-state label (for example `walking`, `driving along a stone route`). |

### `change_points.csv`

One row per observer-declared structural break. The breaks concern scale (variance) changes only.

| column_name | data_type | unit | description |
|---|---|---|---|
| measurement_id | integer | — | Recording identifier. |
| break_index | integer | — | Order of the break in that recording (1-based). |
| interval_start_s | float | s | Left endpoint of the observer interval. |
| interval_end_s | float | s | Right endpoint of the observer interval. |
| theoretical_change_point_s | float | s | Midpoint `(start+end)/2`, following the paper. |
| source | string | — | Provenance of the interval. |

## JSON record files

Each `measurement_XX.json` object contains:

| field | type | description |
|---|---|---|
| measurement_id | integer | Recording identifier. |
| metadata | object | Catalog fields plus sampling summary and labeled `events` (`start`, `stop`, `name` in seconds). |
| column_units | object | Map of column name → unit string. |
| missing_value_code | string | How missing values would be coded. |
| n_rows | integer | Number of records. |
| records | array of objects | One object per sample, same columns as the CSV. |
