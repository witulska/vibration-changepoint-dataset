# Processed files

| pattern | format |
|---|---|
| `measurement_01.csv` … `measurement_09.csv` | UTF-8, comma-separated, header row, Unix newlines |
| `measurement_XX.json` | wrapper with `metadata` (including labeled `events`), `column_units`, and `records` |
| `measurements.xlsx` | one sheet per recording (`m01` … `m09`) plus an `index` sheet |

Column names and units: `../../documentation/data_dictionary.csv` and `column_mapping.csv`.

Missing sensors are omitted columns, not sentinel values. There are no missing numeric cells in this release.
