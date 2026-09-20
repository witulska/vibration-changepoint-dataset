# Processing log

Generated: 2026-09-19T15:22:01Z
Script: `scripts/process_dataset.py`

This file is produced by the processing script. It lists every operation
applied to each recording.

## Operations applied to every file

1. Detect encoding (UTF-8, UTF-8 BOM, or Windows-1250 / `cp1250`) or read Excel.
2. Convert remaining columns to numeric values (`pandas.to_numeric`).
3. Rename columns to stable names (`time` → `time_s`, `gFx` → `gforce_x`, …).
4. Write processed CSV (comma-separated) and JSON under `data/processed/`.
5. Do not interpolate, resample, detrend, or impute. Duplicate timestamps are kept.

## Per-file notes

### Measurement 01

- Source encoding / format: `utf-8-sig`
- Rows: 8157; unique timestamps: 8157; duplicate timestamps: 0.
- Time range: 0.008482 s to 83.748350 s (duration 83.739868 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z.
- SHA-256 (processed CSV): `68b1e1db063972e4be179144e94500c6295905e94047032b8e88a9bd71c01d0a`.

### Measurement 02

- Source encoding / format: `cp1250`
- Rows: 15496; unique timestamps: 15226; duplicate timestamps: 270.
- Time range: 0.003000 s to 77.720000 s (duration 77.717000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'ang_vel_x': 0, 'ang_vel_y': 0, 'ang_vel_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, ang_vel_x, ang_vel_y, ang_vel_z.
- SHA-256 (processed CSV): `a7adc729738db578380fa05ed2c3d64d97904043b7f11ae2f31d53a6ee650ab5`.

### Measurement 03

- Source encoding / format: `xlsx`
- Rows: 40202; unique timestamps: 39529; duplicate timestamps: 673.
- Time range: 0.003000 s to 201.530000 s (duration 201.527000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'ang_vel_x': 0, 'ang_vel_y': 0, 'ang_vel_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, ang_vel_x, ang_vel_y, ang_vel_z.
- SHA-256 (processed CSV): `6269270ee2dd4861757adc6750cf993c4355e36b6f53114f13db08ed3b6beaa3`.

### Measurement 04

- Source encoding / format: `utf-8-sig`
- Rows: 36146; unique timestamps: 32761; duplicate timestamps: 3385.
- Time range: 0.003000 s to 181.884000 s (duration 181.881000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'lin_acc_x': 0, 'lin_acc_y': 0, 'lin_acc_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, lin_acc_x, lin_acc_y, lin_acc_z.
- SHA-256 (processed CSV): `1e7aa69fc27e0e1e4118dddf4fbbcdc7b690e6af2bf2a28e24d7359d0696f56a`.

### Measurement 05

- Source encoding / format: `cp1250`
- Rows: 52918; unique timestamps: 52031; duplicate timestamps: 887.
- Time range: 0.004000 s to 265.489000 s (duration 265.485000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'ang_vel_x': 0, 'ang_vel_y': 0, 'ang_vel_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, ang_vel_x, ang_vel_y, ang_vel_z.
- SHA-256 (processed CSV): `60d626d9a042f0de818532e3d1e1554dc38567c83ed23e6f94037e0087b3ec06`.

### Measurement 06

- Source encoding / format: `cp1250`
- Rows: 23231; unique timestamps: 23231; duplicate timestamps: 0.
- Time range: 0.004524 s to 233.664644 s (duration 233.660120 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z.
- SHA-256 (processed CSV): `caa6cf934744a24efeb522438fb2ffdcd86eb884bb2f27d4aaee51b440df3991`.

### Measurement 07

- Source encoding / format: `cp1250`
- Rows: 54554; unique timestamps: 53696; duplicate timestamps: 858.
- Time range: 0.002000 s to 274.622000 s (duration 274.620000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'ang_vel_x': 0, 'ang_vel_y': 0, 'ang_vel_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, ang_vel_x, ang_vel_y, ang_vel_z.
- SHA-256 (processed CSV): `6fc5c54e82777bbd3c2303432fc12cb1445dbbb8e4297c456eee485db7ec9f04`.

### Measurement 08

- Source encoding / format: `utf-8-sig`
- Rows: 86024; unique timestamps: 86024; duplicate timestamps: 0.
- Time range: 0.009623 s to 344.883208 s (duration 344.873585 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z.
- SHA-256 (processed CSV): `26f9eaad6d5e49fd8418fda582cef895fa96bbc1342cfa069bac9f7a4ae14c34`.

### Measurement 09

- Source encoding / format: `utf-8-sig`
- Rows: 35172; unique timestamps: 34956; duplicate timestamps: 216.
- Time range: 0.003000 s to 176.556000 s (duration 176.553000 s).
- Missing numeric cells: 0 (by column: {'time_s': 0, 'gforce_x': 0, 'gforce_y': 0, 'gforce_z': 0, 'ang_vel_x': 0, 'ang_vel_y': 0, 'ang_vel_z': 0}).
- Processed columns: time_s, gforce_x, gforce_y, gforce_z, ang_vel_x, ang_vel_y, ang_vel_z.
- SHA-256 (processed CSV): `f6987e0c8316f5cfeb9f5963222504cd77186b5b7dec757f27e6bebb1fd85f74`.
