# Archived source files

These files keep **original Physics Toolbox column names** (`time`, `gFx`, `gFy`, `gFz`, `wx`, `wy`, `wz`, `ax`, `ay`, `az`, and `TgF` when it existed). CSV uses a semicolon delimiter, as in the app export.

They are **not** bit-identical copies of the phone dumps:

- comment headers and trailing free-text observer notes were removed;
- encoding was normalized to UTF-8;
- Excel metadata that stored a local Windows path was not copied (`pomiar_nr3.xlsx`).

Numeric sensor samples were not resampled or interpolated. Processed FAIR files (renamed columns, `TgF` dropped, comma-separated CSV / TSV / JSON / XLSX) are in `../processed/`.
