# Processed files

| pattern | format |
|---|---|
| `measurement_01.csv` … `measurement_09.csv` | UTF-8, comma-separated, header row, Unix newlines |
| `measurement_XX.tsv` | same content, tab-separated |
| `measurement_XX.json` | wrapper with `metadata`, `column_units`, and `records` |
| `measurements.xlsx` | one sheet per recording (`m01` … `m09`) plus an `index` sheet |
| `checksums.sha256` | SHA-256 of archived raw files and processed files |

Column names and units: `../../documentation/data_dictionary.csv` and `column_mapping.csv`.

Missing sensors are omitted columns, not sentinel values. There are no missing numeric cells in this release.
